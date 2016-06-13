var HUB = (function(HUB, $, undefined) {
    "use strict";
    
    HUB.loadLogin = function(){
		var accounts = []
		
		accounts = HUB.startRequest("get_accounts");
		if (accounts.result[0] != 'false') {
			if (typeof accounts.result != 'undefined') accounts = accounts.result;
		} else {
			alert(accounts.result[1]);
			return false;
		}

 		if (accounts.length == 0) {
            window.location.href = "#toregister";
        } else {
            accounts.forEach(function(account){
				$("#LoginAccount").append('<option value="'+account+'">'+account+'</option>'); 
            });
        }
    }
    
    HUB.login = function(account,password,keepUnlocked){
        HUB.activeAccount = account;
		
        if (typeof password !== 'undefined') {
			var error, 
				data = HUB.startRequest("unlock_account",'["'+account+'","'+password+'"]',1);
				
			if (typeof data.error != 'undefined') {
				error = data.error.message;
			} else if (typeof data.result[1] != 'undefined' && data.result[1].length > 0) {
				error = data.result[1];
			}
			
            if (data.result != true) {
				Site.cmd("wrapperNotification", ["error", error, 5000])
				$("#PasswordError").text(error).show();
                return;
            } else {
				if (keepUnlocked === true) {
					HUB.keepUnlocked = true;
					HUB.password = password;
				}
				
				// Submit (load html page with ZeroFrame)
				var form = $('form[name="login"]');
//				form.action += 'address='+$('#LoginAccount').val();
//				form.submit();
//				window.location.href = form.action;
				
				window.Site.cmd("wrapperNotification", ["done", "Login Succesful", 5000])
				window.Site.writeStorage('{ "activeAccount" : "'+HUB.activeAccount+'" }');
				$('#login').fadeOut('slow', function() {
					window.Site.loadData(form.attr('action').split("?")[0]); 
					window.Site.cmd("fileGet", { "inner_path": "html/home.html", "required": true }, function (html) { 
						document.open();
						document.write(html);
						document.close();
						
						$('.body').hide().fadeIn('slow', function(){
							$(this).show();
						});
					});
				});
			}
        }
    }
    
    $("#NewAccountSubmit").one("click", function(e){
        e.preventDefault();
        var password = $("#NewAccountPassword").val();
        if(password === '') {
            $("#PasswordRequiredError").show();
        } else {
            $("#PasswordRequiredError").hide();
            var data = HUB.startRequest("personal_newAccount",'["'+password+'"]');
            if(typeof data.result.length > 0){
                HUB.login(data.result,password,$("#RegisterKeepAccountUnlocked").is(":checked"));
            }
            
        }
    });
	
	$('form[name="login"]').on("submit", function(e) {
		HUB.login($("#LoginAccount").val(),$("#LoginPassword").val(),$("#LoginKeepAccountUnlocked").is(":checked"));	
		return false;
	});	
    
    $("#LoginSubmit").on("click", function(e){
		e.preventDefault();
		$('form[name="login"]').submit();
    });
    
    $("#PasswordError").hide();
    $("#PasswordRequiredError").hide();
    
    return HUB;
}(HUB || {}, jQuery));