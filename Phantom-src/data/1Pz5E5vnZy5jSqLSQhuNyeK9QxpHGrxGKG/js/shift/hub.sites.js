var HUB = (function(HUB, $, undefined) {
    "use strict";
	
    HUB.loadSites = function(){
//	  var site_rows = Site.siteListing();
	  Site.loadMessages('siteList', {}, function(site_rows){
		$.each(site_rows, function( k, v ) {
//		  console.log( v.settings.domain+'/'+v.address ); 
		  if (v.settings.own == true) {
			HUB.generate(v.address, v.settings.domain, false); // v.content.description
		  }
		});	
	  });	
    }
	
	HUB.generate = function(address, domain, edit){
		var site = edit ? $("#"+address) : $("#site-dummy").clone();
		
		$(site).attr("id",address);
		$(site).find('h4.brief input').val(address);
		$(site).find('h2 span.domain').html(domain != null ? domain : 'Unknown');
		$(site).find("a.site-visit").prop('href', '/'+(domain != null ? domain : address));
		$(site).find("button.site-edit").hide().click(function() {
//			HUB.switchForm(address, domain, true);
		});
		$(site).find("button.site-publish").click(function() {
			Site.cmd("wrapperPrompt", ["Please supply your private key"], function(private_key){
				HUB.publish_site(address, private_key);
			});
		});
		if (!edit) $(site).appendTo($("#site-dummy").parent()).show();
		
		$('#ContactReset').click();
	}	
	
    HUB.create_site = function(domain, wallet, password){
		var error, result, 
			address, private_key, 
			data = HUB.startRequest("create_site",'[]');

		if (typeof data.error != 'undefined') {
			error = data.error.message;
		} else if (typeof data.result != 'undefined' && data.result[0] !== 'true') {
			error = data.result[1];
		}  
		if (typeof data.result != 'undefined' && data.result.length >= 3) {
			address = data.result[1];
			private_key = data.result[2];
								
			$('#step-3').find('.label-default').toggleClass('label-default, label-success');
			$('#step-3').find('tr.hidden').removeClass('hidden');			

			$('#r-address, #r-folder').text(function(i, v) { return v.replace("auto generate",address) });
			$('#r-private_key').text(private_key);			

			$('#site_open').attr("href",'../'+address).attr("target",'_blank').removeClass('hidden').click(function(){
				$('#site_publish').removeClass('hidden');
			});
			$('#site_publish').click(function(){
				HUB.publish_site(address, private_key);
			});
			
			if (wallet != '' && domain != '' && password != '') {
				domain = domain+'.shift';
				result = this.create_domain(wallet, domain, address, password);
				if (result) {
					$('#r-address').text(function(i, v) { return v.replace(address, domain) });
					$('#site_open').attr('href', function(i, v) { return v.replace(address, domain) });
				}
			}
								
			$("#NewSiteSubmit, #agreeToTheTerms, #termsLabel").hide();

			window.Site.cmd("wrapperNotification", ["done", "Site succesfully created", 5000]);
			
			return true;
		} else {
			Site.cmd("wrapperNotification", ["error", error, 5000]);
		} 
		
		return false;
    }
	
    HUB.publish_site = function(address, private_key){
		var error, data;	
		
		if (address.length <= 25 || private_key.length <= 50) {
			error = "You need to provide correct keys";
			Site.cmd("wrapperNotification", ["error", error, 5000])
        } else {
			data = HUB.startRequest("sign_and_publish",'["'+address+'", "'+private_key+'"]');
		
			if (typeof data.error != 'undefined') {
				error = data.error.message;
			} else if (typeof data.result != 'undefined' && data.result[0] !== 'true') {
				error = data.result[1];
			}  
			
			if (data.result.length > 1 && address == data.result[1]) {
				window.Site.cmd("wrapperNotification", ["done", "Site succesfully signed and published", 5000]);
				return true;
			} else {
				Site.cmd("wrapperNotification", ["error", error, 5000]);
			}
		}
		
		return false;
    }	
	
    HUB.create_domain = function(wallet, domain, domain_address, password){
		var error, data, 
			from = this.format_address(wallet, true), 
			contract_address = '0xa69818b38011e84dbc98bd0f180e6084855eae2e';
			
		if (false) {
			error = "Incomplete domain details";
			Site.cmd("wrapperNotification", ["error", error, 5000])
		} else {
			data = HUB.startRequest("create_phantom_domain",'[{"from":"'+from+'", "domain":"'+domain+'", "domain_address":"'+domain_address+'", "password":"'+password+'"}]');

			if (typeof data.error != 'undefined') {
				error = data.error.message;
				Site.cmd("wrapperNotification", ["error", error, 5000]);				
			} else if (typeof data.result != 'undefined' && data.result[0] == 'false') {
				error = data.result[1];
			}
			return true;
		}
		
		return false;
	}

    return HUB;
}(HUB || {}, jQuery));