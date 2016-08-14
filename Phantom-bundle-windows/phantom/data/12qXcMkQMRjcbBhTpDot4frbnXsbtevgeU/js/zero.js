/* ---- ZeroFrame ---- */


(function() {
  var ZeroFrame,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __slice = [].slice;

  ZeroFrame = (function() {
    function ZeroFrame(url) {
      this.onCloseWebsocket = __bind(this.onCloseWebsocket, this);
      this.onOpenWebsocket = __bind(this.onOpenWebsocket, this);
      this.route = __bind(this.route, this);
      this.onMessage = __bind(this.onMessage, this);
      this.url = url;
      this.waiting_cb = {};
      this.connect();
      this.next_message_id = 1;
      this.init();
    }

    ZeroFrame.prototype.init = function() {
      return this;
    };

    ZeroFrame.prototype.connect = function() {
      this.target = window.parent;
      window.addEventListener("message", this.onMessage, false);
      return this.cmd("innerReady");
    };

    ZeroFrame.prototype.onMessage = function(e) {
      var cmd, message;
      message = e.data;
      cmd = message.cmd;
      if (cmd === "response") {
        if (this.waiting_cb[message.to] != null) {
          return this.waiting_cb[message.to](message.result);
        } else {
          return this.log("Websocket callback not found:", message);
        }
      } else if (cmd === "wrapperReady") {
        return this.cmd("innerReady");
      } else if (cmd === "ping") {
        return this.response(message.id, "pong");
      } else if (cmd === "wrapperOpenedWebsocket") {
        return this.onOpenWebsocket();
      } else if (cmd === "wrapperClosedWebsocket") {
        return this.onCloseWebsocket();
      } else {
        return this.route(cmd, message);
      }
    };

    ZeroFrame.prototype.route = function(cmd, message) {
	  return this.log("Unknown command", message);
    };

    ZeroFrame.prototype.response = function(to, result) {
      return this.send({
        "cmd": "response",
        "to": to,
        "result": result
      });
    };

    ZeroFrame.prototype.cmd = function(cmd, params, cb) {
      if (params == null) {
        params = {};
      }
      if (cb == null) {
        cb = null;
      }
      return this.send({
        "cmd": cmd,
        "params": params
      }, cb);
    };

    ZeroFrame.prototype.send = function(message, cb) {
      if (cb == null) {
        cb = null;
      }
      message.id = this.next_message_id;
      this.next_message_id += 1;
      this.target.postMessage(message, "*");
      if (cb) {
        return this.waiting_cb[message.id] = cb;
      }
    };

    ZeroFrame.prototype.log = function() {
      var args;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return console.log.apply(console, ["[ZeroFrame]"].concat(__slice.call(args)));
    };

    ZeroFrame.prototype.onOpenWebsocket = function() {
      return this.log("Websocket open");
    };

    ZeroFrame.prototype.onCloseWebsocket = function() {
      return this.log("Websocket close");
    };

    return ZeroFrame;

  })();

  window.ZeroFrame = ZeroFrame;

}).call(this);


/* ---- ZeroShift ---- */


(function() {
  var ZeroShift,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __hasProp = {}.hasOwnProperty;

  ZeroShift = (function(_super) {
    __extends(ZeroShift, _super);

    function ZeroShift() {
      this.reloadServerInfo = __bind(this.reloadServerInfo, this);
      this.reloadSiteInfo = __bind(this.reloadSiteInfo, this);
      this.onOpenWebsocket = __bind(this.onOpenWebsocket, this);
      return ZeroShift.__super__.constructor.apply(this, arguments);
    }

    ZeroShift.prototype.init = function() {
      this.server_info = null;
      this.site_info = null;
      return this.log("inited!");
    };	
	
    ZeroShift.prototype.loadMessages = function(call, params, callback=function(){}) {
		if (call == null) {
			call = 'netListening';
		}
		this.cmd('ShiftIPC', {
		  'call': call, 
		  'params': params
		}, (function(_this) {
          return function(result) {			
//			_this.log("socket call response", result);
			if (call == 'netListening'){
			} else if (call == 'blockHeight'){
				HUB.blocknumber = result;
				$("#current_blocknumber").text(HUB.blocknumber);
			} else if (call == 'peerCount'){
				HUB.peercount = result;
				$("#net_peercount").text(HUB.peercount); 
			} else if (call == 'getBalance'){
				HUB.latest = result.latest;
				HUB.pending = result.pending;
				HUB.balance = HUB.latest + HUB.pending;
			}
			return callback();
          };
		})(this));
		return false;
	};	
	
    ZeroShift.prototype.onOpenWebsocket = function(e) {
      this.reloadSiteInfo();
      return this.reloadServerInfo();
    };
	
    ZeroShift.prototype.reloadSiteInfo = function() {
      return this.cmd("siteInfo", {}, (function(_this) {
        return function(site_info) {
          return _this.setSiteInfo(site_info);
        };
      })(this));
    };

    ZeroShift.prototype.reloadServerInfo = function() {
      return this.cmd("serverInfo", {}, (function(_this) {
        return function(server_info) {
          return _this.setServerInfo(server_info);
        };
      })(this));
    };

    ZeroShift.prototype.setSiteInfo = function(site_info) {
	  this.site_info = site_info;
	  this.site_info.content.title = 'Yeah!';

	  if (site_info.settings.domain != '') this.site_info.content.title = site_info.settings.domain;
	  else if (site_info.content.description != '') this.site_info.content.title = site_info.content.description;
//	  console.log('Setting title to: '+this.site_info.content.title);

      return this.site_info = site_info;
    };

    ZeroShift.prototype.setServerInfo = function(server_info) {
      return this.server_info = server_info;
    };
	
	ZeroShift.prototype.loadData = function(inner_path) {
	  return this.cmd("fileGet", {
		"inner_path": inner_path,
		"required": true
	  }, (function(_this) {
		return function(html) {
			document.open();
			document.write(html);
			document.close();			
		};
	  })(this));	
    };

	ZeroShift.prototype.writeStorage = function(str) {
		Site.local_storage = str;
		Site.cmd("wrapperSetLocalStorage", Site.local_storage);	

		return true;
    }; 

	ZeroShift.prototype.readStorage = function() {	  
		this.cmd("wrapperGetLocalStorage", [], function(json) {
			return $.parseJSON(json);
		});	
    }; 
	
    return ZeroShift;

  })(ZeroFrame);

  window.Site = new ZeroShift();
  

}).call(this);