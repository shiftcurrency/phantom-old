var HUB = (function(HUB, $, undefined) {
    "use strict";

    HUB.server = "http://127.0.0.1:53903"; // http://localhost:53901/
    HUB.updateInterval = 30;
    
    HUB.prefix = '0x';
    HUB.activeAccount = '';
    HUB.password = '';
    HUB.keepUnlocked = false;
	HUB.runError = "Is gshift running?"

    HUB.init = function(){
        console.log('Hub initialised');
    }
 	
    HUB.format_address = function(address, prepend){
		address = address.trim();
		if (address.indexOf(HUB.prefix)==0) address = address.substr(HUB.prefix.length, address.length-HUB.prefix.length);	
		if (prepend) address = HUB.prefix + address;
		
		return address;
	}
   
    return HUB;
}(HUB || {}, jQuery));