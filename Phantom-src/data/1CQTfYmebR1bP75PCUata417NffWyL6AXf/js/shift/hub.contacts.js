var HUB = (function(HUB, $, undefined) {
    "use strict";
	    
    HUB.loadContacts = function(){
		var error,
			alias = '',
			prefix = '0x',
			aliasses = [];
			
		aliasses = HUB.startRequest("get_address_book");
		if (typeof aliasses.result != 'undefined' && aliasses.result[0] != 'false') {
			aliasses = aliasses.result;
		} else {
			error = aliasses.result[1]+".\n"+HUB.runError;
			Site.cmd("wrapperNotification", ["error", error, 10000])
			$("#PasswordError > span").text(error).parent().show();

			return false;
		}
		
		aliasses.forEach(function(contact){	
			HUB.generate(contact[0], contact[1], false);
		});
    }
	
	HUB.generate = function(address, alias, edit){
		var contact = edit ? $("#"+address) : $("#contact-dummy").clone();
		
		$(contact).attr("id",address);
		$(contact).find('h4.brief').html('<i>'+address+'</i>');
		$(contact).find('h2 span.alias').html(alias);
		$(contact).find("button.contact-view").click(function() {
			HUB.switchForm(address, alias, true);
		});
		$(contact).find("button.contact-tx").click(function() {
			window.location.href = "home.html?recipient="+address;
		});
		if (!edit) $(contact).appendTo($("#contact-dummy").parent()).show();
		
		$('#ContactReset').click();
	} 
	
	HUB.switchForm = function(address, alias, edit) {
		var section = $('#contact-edit');
		section.find('.x_title > h2').html(edit ? 'Edit Contact <small>Modify an existing contact</small>' : 'New Contact <small>Add a new contact</small>');
		$('#ContactSubmit').text(edit ? 'Edit' : 'Add');
		$('#ContactReset').text(edit ? 'New' : 'Clear');
		$('#ContactDelete').toggle(edit);
		
		$('#contact-alias').val(edit ? alias : '');
		$('#wallet-address').val(edit ? address : '').prop('readonly',edit);
	}
	
	HUB.remove = function(address) {
		var data = HUB.startRequest("del_address_book",'["'+address+'"]');
		if (typeof data.error == 'undefined' && data.result[0] != 'false') {
			$('#'+address).fadeOut('slow', function() { 
				$(this).remove(); 
				$('#ContactReset').click();
			});
			
			return true;
		} else {
			error = data.result[1]+".\n"+HUB.runError;
			Site.cmd("wrapperNotification", ["error", error, 10000])
			$("#PasswordError > span").text(error).parent().show();

			return false;
		}
	}
	
    HUB.create = function(address, alias){
		var prefix = '0x',
			error = '';
		
 		$("#ContactRequiredError").hide();
		
		if (address === '' || alias === '') {
			error = "You need to provide a wallet address and an alias";
		} else if (address != '') {
			if (address.indexOf(prefix)==0) address = address.substr(prefix.length, address.length-prefix.length);
			if (address.length != 40) error = "Invalid wallet adress provided";
			else {
				var data = HUB.startRequest("store_address_book",'["'+address+'","'+alias+'"]');

				if (typeof data.error != 'undefined') {
					error = data.error.message;
				} else if (typeof data.result != 'undefined' && data.result[0] != 'true') {
					error = data.result[1]+".\n"+HUB.runError;
				} else {
					HUB.generate(address, alias, $('#'+address).length > 0);
				} 
			}
		}
		
		if (error != '') {
			Site.cmd("wrapperNotification", ["error", error, 5000])
			$("#ContactRequiredError > span").text(error).parent().show();
		}
		
 		$("#ContactSubmit").removeAttr("disabled readonly");	
    }
       
    $("#ContactSubmit").on("click", function(e){
        e.preventDefault();	
		if (!$(this).attr('readonly') && !$(this).attr('disabled')) $('form[name="contacts"]').submit();
	});
	
	$('form[name="contacts"]').on("submit", function(e) {
		$("#ContactSubmit").prop('readonly',true).prop('disabled',true);

		HUB.create($("#wallet-address").val(),$("#contact-alias").val());	
		return false;
    });
	
	$('#ContactReset').on("click", function(e){
		HUB.switchForm('', '', false);
	});
   
    $("#ContactDelete").hide().click(function(){
		window.Site.cmd("wrapperConfirm", ["Are you sure you want to delete this contact?"], function (res) { 
			if (res) HUB.remove($('#wallet-address').val());
		});	
	});

    $("#ContactRequiredError").hide();
    
    return HUB;
}(HUB || {}, jQuery));