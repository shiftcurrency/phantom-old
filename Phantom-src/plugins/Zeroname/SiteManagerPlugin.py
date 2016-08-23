import logging
import re

from Config import config
from Plugin import PluginManager
from Phantom import Phantom_Ui
from Phantom import Phantom_Db
allow_reload = False  # No reload supported

log = logging.getLogger("ZeronamePlugin")


@PluginManager.registerTo("SiteManager")
class SiteManagerPlugin(object):
    site_zeroname = None

    def load(self):
        super(SiteManagerPlugin, self).load()
        if not self.get(config.bit_resolver):
            self.need(config.bit_resolver)  # Need ZeroName site

    # Checks if its a valid address
    def isAddress(self, address):
        if self.isDomain(address):
            return True
        else:
            return super(SiteManagerPlugin, self).isAddress(address)

    # Return: True if the address is domain
    def isDomain(self, address):
        return re.match("(.*?)([A-Za-z0-9_-]+\.[A-Za-z0-9]+)$", address)

    # Resolve domain
    # Return: The address or None

    def resolveDomain(self, domain):
        domain = domain.lower()
        self.phantomdb = Phantom_Db.PhantomDb()
        res = self.phantomdb.check_dns_cache(domain)
        if res == None or res == "":
            self.phantom_ui = Phantom_Ui.Phantom_Ui()
            self.params = { "params":[{"domain":str(domain)}]}
            res = self.phantom_ui.resolve_phantom_domain(self.params)
            if 'result' in res and res['result'][0] != "false":
                insert = self.phantomdb.insert_dns_cache(domain, res['result'][0])
                return  res['result'][0]
        elif res != None or res != "":
            return res
        return None

    # Return or create site and start download site files
    # Return: Site or None if dns resolve failed
    def need(self, address, all_file=True):
        if self.isDomain(address):  # Its looks like a domain
            address_resolved = self.resolveDomain(address)
            print address_resolved
            if address_resolved:
                address = address_resolved
            else:
                return None

        return super(SiteManagerPlugin, self).need(address, all_file)

    # Return: Site object or None if not found
    def get(self, address):
        if self.sites is None:  # Not loaded yet
            self.load()
        if self.isDomain(address):  # Its looks like a domain
            address_resolved = self.resolveDomain(address)
            if address_resolved:  # Domain found
                site = self.sites.get(address_resolved)
                if site:
                    site_domain = site.settings.get("domain")
                    if site_domain != address:
                        site.settings["domain"] = address
            else:  # Domain not found
                site = self.sites.get(address)

        else:  # Access by site address
            site = self.sites.get(address)
        return site
