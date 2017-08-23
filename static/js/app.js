function hideFlash(){
	$('#flash').find("span").html("");
	$('#flash').hide();
}		
		
function flash(msg,_class, _autoHide){
	var f = $('#flash')
	$(f).removeClass().addClass('alert alert-' + _class).show();
	$(f).find("span").html( msg );
	if(_autoHide==true) {
		if(_class=="success"){	window.setTimeout(hideFlash,5000)}
	}	
}

function contactus_save(){
	var data = $('#frm_contactus').serialize();
	$.post("/contactus/save", data, function(response){
		if(response=='ok'){
			alert("Thank you for contacting us");
			$('#modal_contact').modal('hide');
		} else {
			alert(response);
		}	
	});
}

	
function logo_frame_loaded(){
	//var retval = $('#popup #logo_frame').contents().find("html").text();
	//alert(retval);
	//if (retval=='') return;
	//if(retval != 'Image Uploaded Sucessfully' && retval !='' ) {
	//	alert("Error Uploading Logo\r\n" + retval);
	//} else {
		//alert("Settings Updated sucessfully");
		//$('#popup').dialog('close').dialog('destroy');
	//}
}