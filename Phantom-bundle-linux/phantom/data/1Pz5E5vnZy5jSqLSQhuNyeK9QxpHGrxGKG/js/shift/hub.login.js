var HUB = (function(HUB, $, undefined) {
    "use strict";
	    
    HUB.loadLogin = function(){
		var error,
			counter = 0,
			alias = '',
			balances = [],
			accounts = [],
			aliasses = [],
			bigfloat = new BigNumber(0);
		
		accounts = HUB.startRequest("get_accounts");
		if (accounts.result[0] != 'false') {
			if (typeof accounts.result != 'undefined') accounts = accounts.result;
		} else {
			error = accounts.result[1]+".\n"+HUB.runError;
			Site.cmd("wrapperNotification", ["error", error, 10000])
			$("#PasswordError > span").text(error).parent().show();

			return false;
		}

 		if (accounts.length == 0) {
            window.location.href = "#toregister";
        } else {
			BigNumber.config({ DECIMAL_PLACES: 8, ERRORS: false });
			
			aliasses = HUB.startRequest("get_address_book",'[]');	
            accounts.forEach(function(account){
				counter++;
				alias = false;	
				if (typeof aliasses.result != 'undefined' && aliasses.result.length > 0) {
					aliasses.result.forEach(function(contact){
						if (HUB.prefix+''+contact[0] == account) alias = contact[1];
					});
				}

				$("#LoginAccount").hide().append('<option value="'+account+'">'+account+'</option>'); 
				$("#LoginAccounts").append('<li role="presentation"'+(false && counter == 1 ? ' class="active"' : '')+'><a href="#" id="a-'+counter+'">'+(alias ? '<strong>- '+alias+' -</strong> ' : '')+account+' <span class="badge"></span></a></li>'); 

				if (counter <= 3) { // Limit API calls for optimal performance
					balances = HUB.startRequest("get_balance",'["'+account+'", "latest"]');
					if (typeof balances.result != 'undefined' && balances.result[0] != 'false' && !isNaN(balances.result)) {
						bigfloat = BigNumber(balances.result);
						$('#a-'+counter).find(".badge").text(bigfloat.toFixed() / 1000000000000000000);
					}
				}
				
            });
			
			var selectAccount = function(elem, account) {
				$(elem).each(function(){
					var address = $(this).contents().filter(function(){
						return this.nodeType !== 1;
					}).text().trim();
					
					if (account == false || account == address) $(this).parent('li').addClass('active').siblings().removeClass('active');					
					$('#LoginAccount').val(address).change();
				});		
			}
			
			$("#LoginAccounts li a").click(function(){			
				selectAccount(this, false);	 
			});	
			
		    Site.cmd("wrapperGetLocalStorage", [], function(json) {
				var local_storage = $.parseJSON(json),
					address = local_storage != null ? local_storage.activeAccount : '';
				
				selectAccount("#LoginAccounts li a", address);
			});
        }
    }

    HUB.create = function(password,keepUnlocked){
		var error,
			password = $("#NewAccountPassword").val();

 		$("#PasswordRequiredError").hide();
		if (password === '') {
			error = "You need to provide a password";
			Site.cmd("wrapperNotification", ["error", error, 5000])
			$("#PasswordRequiredError > span").text(error).parent().show();
			return false;
        } else {
			var data = HUB.startRequest("create_account",'["'+password+'"]');
				
			if (typeof data.error != 'undefined') {
				error = data.error.message;
			} else if (typeof data.result != 'undefined' && data.result.length > 0) {
				error = data.result[1]+".\n"+HUB.runError;
			}
			
            if (typeof data.result == 'string' || data.result instanceof String) {
                HUB.login(data.result,password,$("#RegisterKeepAccountUnlocked").is(":checked"));
				return true;
			} else {
				Site.cmd("wrapperNotification", ["error", error, 5000]);
				$("#PasswordRequiredError > span").text(error).parent().show();
            } 
        }
 		$("#NewAccountSubmit").removeAttr("disabled readonly");	
    }
    
    HUB.login = function(account,password,keepUnlocked){
        HUB.activeAccount = account;

		var error,
			data = [{'result':false}];
			
        $("#PasswordError").hide();
		
        if (typeof password !== 'undefined') {
			if (account != '') {
				data = HUB.startRequest("unlock_account",'["'+account+'","'+password+'"]',1);
				if (typeof data.error != 'undefined') {
					error = data.error.message;
				} else if (typeof data.result != 'undefined' && data.result.length > 0) {
					error = data.result[1];
				}	
			} else {
				error = "Please select an account first";
			}
			
            if (data.result != true) {
				Site.cmd("wrapperNotification", ["error", error, 5000])
				$("#PasswordError > span").text(error).parent().show();
				
				return false; // Halt
           } else {
				if (keepUnlocked === true) {
					HUB.keepUnlocked = true;
					HUB.password = password;
				}
				
				// Submit (load html page with ZeroFrame)
				var form = $('form[name="login"]'),
					action = form.attr('action').split("?")[0];
					
				window.Site.cmd("wrapperNotification", ["done", "Login successful", 5000])
				$('#login').fadeOut('slow', function() {
					window.Site.writeStorage('{ "activeAccount" : "'+HUB.activeAccount+'" }');	
					
					window.location.href = action; 
					
//					window.Site.loadData(target); 
/*					window.Site.cmd("fileGet", { "inner_path": "home.html", "required": true }, function (html) { 
						document.open();
						document.write(html);
						document.close();
						
						$('.body').hide().fadeIn('slow', function(){
							$(this).show();
						});
					});
*/				});	
				return false; // Submit causes displayOpenerDialog (Linux)
			}
        }
		$("#LoginSubmit").removeAttr("disabled readonly");	
    }
    
    $("#NewAccountSubmit").on("click", function(e){
        e.preventDefault();	
		if (!$(this).attr('readonly') && !$(this).attr('disabled')) $('form[name="create"]').submit();
	});
	
	$('form[name="create"]').on("submit", function(e) {
		$("#NewAccountSubmit").prop('readonly',true).prop('disabled',true);

		HUB.create($("#NewAccountPassword").val(),$("#LoginKeepAccountUnlocked").is(":checked"));	
		return false;
    });

    $("#LoginSubmit").on("click", function(e){
		e.preventDefault();
		if (!$(this).attr('readonly') && !$(this).attr('disabled')) $('form[name="login"]').submit();
    });
	
	$('form[name="login"]').on("submit", function(e) {
		$("#LoginSubmit").prop('readonly',true).prop('disabled',true);

		return HUB.login($("#LoginAccount").val(),$("#LoginPassword").val(),$("#LoginKeepAccountUnlocked").is(":checked"));
	});	
   
    $("#PasswordError").hide();
    $("#PasswordRequiredError").hide();
    
    return HUB;
}(HUB || {}, jQuery));
