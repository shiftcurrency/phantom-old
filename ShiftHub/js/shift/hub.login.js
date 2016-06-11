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
        if(typeof password !== 'undefined') {
			// Let's comment the unlocking for now
/*			var data =  HUB.startRequest("unlock_account",'["'+account+'","'+password+'"]',1);
            if (data.result != true) {
                $("#PasswordError").show();
                return;
            }
*/
        }
		
 		// Submit
		var form = $('form[name="login"]')[0];
		form.action+= 'address='+$('#LoginAccount').val();
//		form.submit();
		window.location.href = form.action;
		
        if(keepUnlocked === true) {
            HUB.keepUnlocked = true;
            HUB.password = password;
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
    
    $("#LoginSubmit").on("click", function(e){
        e.preventDefault();
        HUB.login($("#LoginAccount").val(),$("#LoginPassword").val(),$("#LoginKeepAccountUnlocked").is(":checked"));
    });
    
    $("#PasswordError").hide();
    $("#PasswordRequiredError").hide();
    
    return HUB;
}(HUB || {}, jQuery));