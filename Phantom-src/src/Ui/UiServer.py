import logging
import time
import cgi
import socket
import sys
import json

from gevent.pywsgi import WSGIServer
from gevent.pywsgi import WSGIHandler
from lib.geventwebsocket.handler import WebSocketHandler

from UiRequest import UiRequest
from Site import SiteManager
from Config import config
from Debug import Debug
from Phantom import Phantom_Ui
from Phantom import Phantom_Db


# Skip websocket handler if not necessary
class UiWSGIHandler(WSGIHandler):

    def __init__(self, *args, **kwargs):
        self.server = args[2]
        super(UiWSGIHandler, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def run_application(self):
        if "HTTP_UPGRADE" in self.environ:  # Websocket request
            try:
                ws_handler = WebSocketHandler(*self.args, **self.kwargs)
                ws_handler.__dict__ = self.__dict__  # Match class variables
                ws_handler.run_application()
            except Exception, err:
                logging.error("UiWSGIHandler websocket error: %s" % Debug.formatException(err))
                if config.debug:  # Allow websocket errors to appear on /Debug
                    import sys
                    sys.modules["main"].DebugHook.handleError()
        else:  # Standard HTTP request
            try:
                super(UiWSGIHandler, self).run_application()
            except Exception, err:
                logging.error("UiWSGIHandler error: %s" % Debug.formatException(err))
                if config.debug:  # Allow websocket errors to appear on /Debug
                    import sys
                    sys.modules["main"].DebugHook.handleError()

    def handle(self):
        # Save socket to be able to close them properly on exit
        self.server.sockets[self.client_address] = self.socket
        super(UiWSGIHandler, self).handle()
        del self.server.sockets[self.client_address]


class UiServer:

    def __init__(self):
        
        from Phantom import Run_Gshift

        self.ip = config.ui_ip
        self.port = config.ui_port
        if self.ip == "*":
            self.ip = ""  # Bind all
        self.wrapper_nonces = []
        self.sites = SiteManager.site_manager.list()
        self.log = logging.getLogger(__name__)
        self.rate_counter = 0
        self.gshift = Run_Gshift.Run_Gshift()
        self.gshift_process = self.gshift.start()


    def stopGshift_Windows(self):

        """ Stop Gshift process on windows by sending a kill signal. """
        from subprocess import Popen
        from sys import platform

        if platform == 'win32':
            self.gshift.stop()

    # After WebUI started
    def afterStarted(self):
        from util import Platform

# Handle WSGI request
    def handleRequest(self, env, start_response):
       
        path = env["PATH_INFO"]

        if env["REQUEST_METHOD"] == "POST":

            ''' Only import AsyncResult if we get an actual POST '''
            from gevent.event import AsyncResult

            ''' Create an instance of async '''
            async = AsyncResult()

            self.phantom_ui = Phantom_Ui.Phantom_Ui()

            ''' Wait for the IPC call to finish without blocking further processing. '''
            async.set(self.phantom_ui.run(env['wsgi.input'].read()))
            ipc_response = async.get()
            response_string = json.dumps(ipc_response)

            response_headers = [('Content-Type', 'application/json'),
                    ('Access-Control-Allow-Origin', '*'),
                    ('Content-Length', str(len(response_string)))]

            start_response("200", response_headers)
            return [response_string]



        if env.get("QUERY_STRING"):
            get = dict(cgi.parse_qsl(env['QUERY_STRING']))
        else:
            get = {}
        ui_request = UiRequest(self, get, env, start_response)
        if config.debug:  # Let the exception catched by werkezung
            return ui_request.route(path)
        else:  # Catch and display the error
            try:
                return ui_request.route(path)
            except Exception, err:
                logging.debug("UiRequest error: %s" % Debug.formatException(err))
                return ui_request.error500("Err: %s" % Debug.formatException(err))

    # Reload the UiRequest class to prevent restarts in debug mode
    def reload(self):
        global UiRequest
        import imp
        import sys
        reload(sys.modules["User.UserManager"])
        reload(sys.modules["Ui.UiWebsocket"])
        UiRequest = imp.load_source("UiRequest", "src/Ui/UiRequest.py").UiRequest
        # UiRequest.reload()

    # Bind and run the server
    def start(self):


        handler = self.handleRequest

        """ Start gshift. When phantom recieves ctrl+c gshift will also recieve this signal."""
        if not self.gshift_process:
            print "- Could not start gshift. Try to start it manually."

        print "- Checking if gshift is running...",
        self.running = self.gshift.check_running_proc("gshift")
        if self.running:
            print "found a running gshift process with process id: %i." % int(self.running[0])
            print "- Verifying IPC connection...",
            self.ipc_conn = self.gshift.verify_ipc_connection()
            if not self.ipc_conn: 
                print "could not establish an IPC connection with gshift."
                config.open_browser = False
            else:
                print "successfully established an IPC connection to gshift. Creating static node file."
                config.open_browser = "default_browser"
        else:
            print "could not find a running gshift process. Start gshift manually."
            config.open_browser = False

        self.phantom_ui = Phantom_Ui.Phantom_Ui()
        res = self.phantom_ui.create_static_nodefile()

        try:
            init_db = Phantom_Db.PhantomDb()
            if init_db.init_database() and init_db.clear_database():
                print "- Initialized Phantom database."
        except Exception as e:
            print "- Could not initalize phantom database, exiting..."
            sys.exit(0)

        if config.debug:
            # Auto reload UiRequest on change
            from Debug import DebugReloader
            DebugReloader(self.reload)

            # Werkzeug Debugger
            try:
                from werkzeug.debug import DebuggedApplication
                handler = DebuggedApplication(self.handleRequest, evalex=True)
            except Exception, err:
                self.log.info("%s: For debugging please download Werkzeug (http://werkzeug.pocoo.org/)" % err)
                from Debug import DebugReloader
        self.log.write = lambda msg: self.log.debug(msg.strip())  # For Wsgi access.log
        self.log.info("--------------------------------------")
        self.log.info("Web interface: http://%s:%s/" % (config.ui_ip, config.ui_port))
        self.log.info("--------------------------------------")

        self.server = WSGIServer((self.ip.replace("*", ""), self.port), handler, handler_class=UiWSGIHandler, log=self.log)
        self.server.sockets = {}
        print "- Notice: for full mesh syncronization(in alpha) the shift_txs.db in your gshift user directory must be fully synced."
        print "- Checking Phantom Network sites for which to enable full mesh syncronization...",
        try:
            found_domains = self.phantom_ui.check_index()
            print "found %i site(s)."% (len(found_domains))
        except Exception as e:
            print "could not fetch wallet addresses. Will not be able to sync sites. Reason(%s)." % str(e)
            pass
        print "- Starting syncronization...",
        res = self.full_mesh(found_domains)
        print "synced %i domains." % int(res)

        if config.open_browser:
            logging.info("Opening browser: %s...", config.open_browser)
            import webbrowser
            if config.open_browser == "default_browser":
                browser = webbrowser.get()
            else:
                browser = webbrowser.get(config.open_browser)
            browser.open("http://%s:%s/%s" % (config.ui_ip if config.ui_ip != "*" else "127.0.0.1", config.ui_port, config.homepage), new=2)

        self.afterStarted()
        try:
            self.server.serve_forever()
        except Exception, err:
            self.log.error("Web interface bind error, must be running already, exiting.... %s" % err)
            sys.modules["main"].file_server.stop()
        self.log.debug("Stopped.")

    def full_mesh(self, domains):

        self.phantom_ui = Phantom_Ui.Phantom_Ui()
        resolved_addresses = []
        for domain in domains:
            res = self.phantom_ui.resolve_phantom_domain({"params":[{"domain" : str(domain)}]})
            if 'result' in res and 'shift' in res['result']:
                resolved_addresses.append(str(res['result']))

        for address in resolved_addresses:
            try:
                self.sites.need(address)
            except Exception as e:
                print e
                pass
        return len(resolved_addresses)


    def stop(self):
        self.log.debug("Stopping...")
        self.gshift_process = self.gshift.stop()
        # Close WS sockets
        if "clients" in dir(self.server):
            for client in self.server.clients.values():
                client.ws.close()
        # Close http sockets
        sock_closed = 0
        for sock in self.server.sockets.values():
            try:
                sock.send("bye")
                sock.shutdown(socket.SHUT_RDWR)
                # sock._sock.close()
                # sock.close()
                sock_closed += 1
            except Exception, err:
                self.log.debug("Http connection close error: %s" % err)
        self.log.debug("Socket closed: %s" % sock_closed)
        time.sleep(0.1)

        """ Clear the database from unused filters for shh messaging """
        phantom_db = Phantom_Db.PhantomDb()
        try:
            if phantom_db.clear_database():
                print "- Removed filter id(s) from Phantom database."
        except:
            pass



        self.server.socket.close()
        self.server.stop()
        time.sleep(1)
