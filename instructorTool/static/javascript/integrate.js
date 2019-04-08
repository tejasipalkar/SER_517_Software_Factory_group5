$(document).ready(function() {
    $("#btn-cal").click(function() {
      // disable button
      $(this).prop("disabled", true);
    // add spinner to button
      $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Loading`
      );
    });
    $("#btn-grp").click(function() {
      // disable button
      $(this).prop("disabled", true);
      // add spinner to button
      $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Loading..`
      );
    });

    $(document).on('click', '.row_data', function(event) 
  {
    event.preventDefault(); 
 
    if($(this).attr('edit_type') == 'button')
    {
      return false; 
    }

    //make div editable
    $(this).closest('div').attr('contenteditable', 'true');
    //add bg css
    $(this).addClass('bg-warning').css('padding','5px');

    $(this).focus();

  }) ;
  $(document).on('focusout', '.row_data', function(event) 
  {
    event.preventDefault();

    if($(this).attr('edit_type') == 'button')
    {
      return false; 
    }

    var row_id = $(this).closest('tr').attr('row_id'); 
    
    var row_div = $(this)       
    .removeClass('bg-warning') //add bg css
    .css('padding','')

    var col_name = row_div.attr('col_name'); 
    var col_val = row_div.html(); 

    var arr = {};
    arr[col_name] = col_val;

    $.extend(arr, {row_id:row_id});
    
  });
  $(document).on('click', '.btn_edit', function(event) 
  {
    event.preventDefault();
    var tbl_row = $(this).closest('tr');

    var row_id = tbl_row.attr('row_id');

    tbl_row.find('.btn_save').show();
    tbl_row.find('.btn_cancel').show();


    tbl_row.find('.btn_edit').hide(); 

    tbl_row.find('.row_data')
    .attr('contenteditable', 'true')
    .attr('edit_type', 'button')
    .addClass('bg-warning')
    .css('padding','3px')

    tbl_row.find('.row_data').each(function(index, val) 
    {  
      $(this).attr('original_entry', $(this).html());
    });     
    

  });
    $(document).on('click', '.btn_cancel', function(event) 
  {
    event.preventDefault();

    var tbl_row = $(this).closest('tr');

    var row_id = tbl_row.attr('row_id');

    tbl_row.find('.btn_save').hide();
    tbl_row.find('.btn_cancel').hide();
<<<<<<< HEAD

    //show edit button
    tbl_row.find('.btn_edit').show();

    //make the whole row editable
=======
    tbl_row.find('.btn_edit').show();

    
>>>>>>> dd8dcba6bd2d7bdcd2190be3522303ce1fb8db82
    tbl_row.find('.row_data')
    .attr('edit_type', 'click')
    .removeClass('bg-warning')
    .css('padding','') 

    tbl_row.find('.row_data').each(function(index, val) 
    {   
      $(this).html( $(this).attr('original_entry') ); 
    });  
  });
  //--->button > cancel > end

  
  //--->save whole row entery > start 
  $(document).on('click', '.btn_save', function(event) 
  {
    event.preventDefault();
    var tbl_row = $(this).closest('tr');

    var row_id = tbl_row.attr('row_id');

    
    //hide save and cacel buttons
    tbl_row.find('.btn_save').hide();
    tbl_row.find('.btn_cancel').hide();

    //show edit button
    tbl_row.find('.btn_edit').show();


    //make the whole row editable
    tbl_row.find('.row_data')
    .attr('edit_type', 'click')
    .removeClass('bg-warning')
    .css('padding','') 

    //--->get row data > start
    var arr = {}; 
    tbl_row.find('.row_data').each(function(index, val) 
    {   
      var col_name = $(this).attr('col_name');  
      var col_val  =  $(this).html();
      arr[col_name] = col_val;
    });
<<<<<<< HEAD
    //--->get row data > end

    //use the "arr" object for your ajax call
=======
  
>>>>>>> dd8dcba6bd2d7bdcd2190be3522303ce1fb8db82
    $.extend(arr, {row_id:row_id});
     

  });
<<<<<<< HEAD
  //--->save whole row entery > end
=======
  
>>>>>>> dd8dcba6bd2d7bdcd2190be3522303ce1fb8db82

}); 


