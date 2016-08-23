var HUB = (function(HUB, $, undefined) {
    HUB.numofrequests = 0;
    HUB.polling = false;
    HUB.numofpolls = HUB.numoffails = 0;
    HUB.blocknumber = HUB.peercount = 0;
	HUB.balance = HUB.latest = HUB.pending = HUB.earliest = 0;
	 
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
	
    HUB.logout = function(page){
		var error,
			data = [{'result':false}];
			
		if (HUB.activeAccount != '') {
			data = HUB.startRequest("lock_account",'["'+HUB.activeAccount+'"]',1);
		}

		if (data.result == true) {
			window.Site.writeStorage('{ "activeAccount" : "" }'); // Clear
			window.Site.cmd("wrapperNotification", ["done", "Logged out", 5000])
		}

		$('body').fadeOut('slow', function() {
			window.location.href = page != 'undefined' ? page : '/'; 
		});

		return true;
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

//	  Current blockheight	  
/*	  Site.cmd("blockHeight", {}, function(result) {
		console.log("blockheight = "+ HUB.blocknumber + "/" + result.blockheight);
		HUB.blocknumber = result.blockheight;	  

		if (HUB.blocknumber == false) HUB.numoffails++;
		else $("#current_blocknumber").text(HUB.blocknumber);
	  });

	  HUB.blocknumber = HUB.getBlocknumber(); 
	  if (HUB.blocknumber == false) HUB.numoffails++;
	  else $("#current_blocknumber").text(HUB.blocknumber);
*/	  Site.loadMessages('blockHeight');

	  // Call every x time we get here  
	  var modulo = HUB.numofpolls > 5 ? 10 : 2;
	  if (HUB.numofpolls == 1 || HUB.numofpolls % modulo == 1) {
		console.log('Polling called, nr: '+HUB.numofpolls);
		
		// Number of peers
/*		data = HUB.startRequest("net_peercount",'[]'); 
		if (typeof data.result == 'string' || data.result instanceof String) HUB.peercount = data.result;
		else HUB.numoffails++;
		$("#net_peercount").text(HUB.peercount);  
*/		Site.loadMessages('peerCount');

		// Detect balance changes
		Site.loadMessages('getBalance', {'address': HUB.activeAccount}, function(){ 
			if (typeof HUB.show_balances != 'undefined') {
				HUB.show_balances(HUB.activeAccount, false);
			}
			return; 
		});

		if (HUB.balance != last_balance) { 
		  last_balance = HUB.balance;
//		  console.log('Last known balance:' +last_balance);
		  
		  if (false) HUB.show_txs(HUB.activeAccount); // Disabled for now: db syncing not yet implemented in gshift
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