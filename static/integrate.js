
$(document).ready(function(){
	$("#grp").click(function(){
		$("#content1").hide()
		$("#content2").show();
	})
	$("#home").click(function(){
		$("#content2").hide()
		$("#content1").show();
	})
	
	$("#trigger-grouping").click(function(){

	})

	var acc = document.getElementsByClassName("accordion");

	for (var i = 0; i < acc.length; i++) {
	  	acc[i].addEventListener("click", function() {
	    this.classList.toggle("active");
	    var panel = this.nextElementSibling;
	    if (panel.style.maxHeight){
	      panel.style.maxHeight = null;
	    } else {
	      panel.style.maxHeight = panel.scrollHeight + "px";
	    } 
	  });
	}

});
var preferences = $("#preference-dropdown :selected").val();

$(document).ready(function(){
	$('#parse-input').on('click',function(e){
		//Ganesh's code
		$('#trigger-grouping').attr('disabled',false);
		$('#cancel-grouping').attr('disabled',false);
	});
});



$('#remove-file').on('click',function(e){
	var $el = $('#file');
	$el.wrap('<form>').closest('form').get(0).reset();
	$el.unwrap();
});
	