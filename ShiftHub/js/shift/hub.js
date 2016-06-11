var HUB = (function(HUB, $, undefined) {
    "use strict";

    HUB.server = "http://127.0.0.1:53903"; // http://localhost:53901/
    HUB.updateInterval = 30;
    
    HUB.activeAccount = '';
    HUB.password = '';
    HUB.keepUnlocked = false;

    HUB.init = function(){
        console.log('Hub initialised');
    }
    
    return HUB;
}(HUB || {}, jQuery));