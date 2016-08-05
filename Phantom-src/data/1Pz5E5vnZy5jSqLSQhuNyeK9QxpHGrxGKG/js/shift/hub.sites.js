var HUB = (function(HUB, $, undefined) {
    "use strict";
	
    HUB.create_site = function(){
		var error,
			data = HUB.startRequest("create_site",'[]');
				
		if (typeof data.error != 'undefined') {
			error = data.error.message;
		} else if (typeof data.result != 'undefined' && data.result[0] !== 'true') {
			error = data.result[1];
		}  
		if (typeof data.result != 'undefined' && data.result.length >= 3) {
			$('#r-address, #r-folder').text(function(i, v) { return v.replace("auto generate",data.result[1]) });
			$('#r-private_key').text(data.result[2]);
					
			$('#step-3').find('tr.hidden, .btn.hidden').removeClass('hidden');		
			$('#step-3').find('.label-default').toggleClass('label-default, label-success');
	
			$('#site_open').attr("href",'../'+data.result[1]).attr("target",'_blank');
			$('#site_publish').click(function(){
				HUB.publish_site(data.result[1], data.result[2]);
			});
	
			$("#NewSiteSubmit").text('Done')/*.removeAttr("disabled readonly")*/;
			$("#agreeToTheTerms, #termsLabel").hide();

			window.Site.cmd("wrapperNotification", ["done", "Site succesfully created", 5000]);
			
			return true;
		} else {
			Site.cmd("wrapperNotification", ["error", error, 5000]);
		} 
		
		return false;
    }
	
    HUB.publish_site = function(public_key, private_key){
		var error, data;	
		
		if (public_key.length <= 25 || private_key.length <= 50) {
			error = "You need to provide correct keys";
			Site.cmd("wrapperNotification", ["error", error, 5000])
			return false;
        } else {
			data = HUB.startRequest("sign_and_publish",'["'+public_key+'", "'+private_key+'"]');
		
			if (typeof data.error != 'undefined') {
				error = data.error.message;
			} else if (typeof data.result != 'undefined' && data.result[0] !== 'true') {
				error = data.result[1];
			}  
			
			if (data.result.length > 1 && public_key == data.result[1]) {
				window.Site.cmd("wrapperNotification", ["done", "Site succesfully signed and published", 5000]);
			} else {
				Site.cmd("wrapperNotification", ["error", error, 5000]);	
			}
		}
		
		return false;
    }	

    return HUB;
}(HUB || {}, jQuery));