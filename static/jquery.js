$(document).ready(function(){
	$("#grp").click(function(){
		$("#content1").hide()
		$("#content2").show();
	})
	$("#home").click(function(){
		$("#content2").hide()
		$("#content1").show();
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

function uploadFile(){
	var x = document.getElementsById("file");
	x.disabled = true;
}
$(document).ready(
    function(){
        $('input:file').change(
            function(){
                if ($(this).val()) {
                    $('input:submit').attr('disabled',false); 
                    $('#remove-file').attr('disabled',false);
                } 
            }
            );
    });
$('#remove-file').on('click',function(e){
	var $el = $('#file');
	$el.wrap('<form>').closest('form').get(0).reset();
	$el.unwrap();
});
	