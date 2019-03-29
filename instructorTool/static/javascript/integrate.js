
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

$(document).ready(function() {
    $("#btn-cal").click(function() {
      // disable button
      $(this).prop("disabled", true);
      // add spinner to button
      $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Loading...`
      );
    });
    $("#btn-grp").click(function() {
      // disable button
      $(this).prop("disabled", true);
      // add spinner to button
      $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Loading...`
      );
    });

});


