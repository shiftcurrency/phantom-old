var HUB = (function(HUB, $, undefined) {
    HUB.numofrequests = 0;
    
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

    return HUB;
}(HUB || {}, jQuery));