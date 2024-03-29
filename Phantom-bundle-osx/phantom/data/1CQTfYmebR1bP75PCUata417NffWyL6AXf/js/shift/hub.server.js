var HUB = (function(HUB, $, undefined) {
    HUB.numofrequests = 0;
    HUB.polling = false;
    HUB.numofpolls = 0;
    HUB.numoffails = 0;
    HUB.blocknumber = 0
    HUB.peercount = 0
	HUB.balance = 0;
	 
    HUB.startRequest = function(method, params){
        HUB.numofrequests++;
        
        if(typeof params === 'undefined') {
            params = '[]';
        }
        
        var result = {};
        $.ajax({
            url: HUB.server,
            type: "POST", // OPTIONS
//			cors: true,
//			crossDomain: true,
//			useDefaultXhrHeader : false, 	
//			dataType: "jsonp",
//			data: JSON.stringify('{"jsonrpc":"2.0","method":"'+method+'","params":'+params+',"id":'+HUB.numofrequests+'}'),
			xhrFields: {
//				withCredentials: true
			},
			dataType: "json",
			data: '{"jsonrpc":"2.0","method":"'+method+'","params":'+params+',"id":'+HUB.numofrequests+'}',
//			headers: { 'Access-Control-Allow-Origin': 'localhost' },
            async: false,
			beforeSend: function(xhr) {
//				xhr.withCredentials = true;
//				xhr.setRequestHeader('Origin', 'http://127.0.0.1:53903');
//				xhr.setRequestHeader('Access-Control-Request-Headers', 'x-requested-with');
//				xhr.setRequestHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:53903');
			}
        }).done(function(data){
            result = data;
            $("#connectionerror").hide();
        }).fail(function(){
            $("#connectionerror").show();
        });
        
        return result;
    }
	
    HUB.getBlocknumber = function(){
		var error,
			result = 0, 
			data = HUB.startRequest("get_blocknumber",'[]');

		if (typeof data.error != 'undefined') {
			error = data.error.message;
		} else if (typeof data.result != 'undefined' && data.result[1].length > 0) {
			error = data.result[1];
		}

        if (typeof data.result == 'string' || data.result instanceof String) {
			result = data.result;
		} else {
			result = false;
			console.log(error);
		}
        
        return result;
    }	
	
	var last_balance = HUB.balance;
	HUB.callPolling = function() {
	  HUB.numofpolls++;
	  
	  HUB.blocknumber = HUB.getBlocknumber(); 
	  if (HUB.blocknumber == false) HUB.numoffails++;
	  else $("#current_blocknumber").text(HUB.blocknumber);
	  
	  // Call every x time we get here  
	  var modulo = HUB.numofpolls > 5 ? 10 : 2;
	  if (HUB.numofpolls % modulo == 1) {
		console.log('Polling called, nr: '+HUB.numofpolls);
		
		// Number of peers
		data = HUB.startRequest("net_peercount",'[]'); 
		if (typeof data.result == 'string' || data.result instanceof String) HUB.peercount = data.result;
		else HUB.numoffails++;
		$("#net_peercount").text(HUB.peercount);  
		
		// Detect balance changes
		HUB.show_balances(HUB.activeAccount);
		if (false && HUB.balance != last_balance) { // Disabled for now: syncing not yet implemented in gshift
		  HUB.show_txs(HUB.activeAccount);
		  last_balance = HUB.balance;
		  console.log('Last known balance:' +last_balance);
		} 
	  }
	   
	  // Don't keep trying forever
	  if (HUB.numoffails > 10) {
		HUB.stopPolling();
		return false;
	  }
	  
	}
	
	HUB.startPolling = function() {
	  if (window.pollinterval) return;
	  
	  HUB.numofpolls = 1;
	  HUB.callPolling();
	  window.pollinterval = window.setInterval(HUB.callPolling, 15000);	
	  
	  console.log('Polling started, id:' +window.pollinterval);
	}
	
	HUB.stopPolling = function() {
	  clearInterval(window.pollinterval);
	  HUB.polling = false;
	  
	  console.log('Polling stopped, id:' +window.pollinterval);
	}

    return HUB;
}(HUB || {}, jQuery));