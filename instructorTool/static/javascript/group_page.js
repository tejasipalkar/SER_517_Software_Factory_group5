
  $(function() {
    $('#submit_slack').bind('click', function(){
        $.ajax({
            url: '/slack',
            data: $('form').serialize(),
            type: 'POST'
        })
        .done(function(response) {
          if(response == "invalid token")
            alert("Invalid Token");
          else
            {$("#slackModal").modal('hide');
            alert("Slack Groups Created");}
        });
    });
});

  $(function() {
    $('#submit_taiga').bind('click', function(){
        $.ajax({
            url: '/taiga',
            data: $('form').serialize(),
            type: 'POST'
        })
        .done(function(response) {
          if(response == "invalid auth")
            alert("Invalid Username/Password");
          else
            {$("#taigaModal").modal('hide');
            alert("Taiga Channels Created");}
        });
    });
});

var col_names =[]
var rows =[]
function postgrouppref(){
  var pref = document.getElementById("sel1").value;
  var avoid = document.getElementById("sel2").value;
  var group_size = document.getElementById("size").value;
  var file = document.getElementById("file").value;
  url ="/group?"+"pref="+pref+"&avoid="+avoid+"&group="+group_size+"&file="+file;
  sendRequestWithCallback(url, null, true, callbackfn);
  //document.getElementById("content").value="";
}


function randomid(){
   return '_' + Math.random().toString(36).substr(2, 9);
}
function createtable_map_id(team_name,team_map){
  var tbl_1 ='';
  tbl_1 +='<table class="table table-bordered">';
  tbl_1+='<thead>';
  tbl_1+='<tr>';
  tbl_1+='<th>Group Name</th>';
  tbl_1+='<th>Group Members</th>';
  tbl_1+='</tr>';
  for(x in team_name){
    tbl_1+='<tr row_id="'+x+'">';
    tbl_1+='<td>'+x+'</td>';
    tbl_1+='<td><input type="text" value="'+team_map[x]+'"></td>';
    tbl_1+='</tr>';

  }
  tbl_1+='</thead>';
  tbl_1 +='</table>';




  var table = document.getElementById("table1");
  table.innerHTML="";
  table.innerHTML+=tbl_1;

}

function createtable(rows,col_names, team_name){

  var tbl ='';
  tbl +='<table class="table table-bordered">';
  tbl+='<thead>';
  tbl+='<tr>';
  for(var head_cell=0;head_cell<col_names.length;head_cell++){
    tbl+='<th>'+col_names[head_cell]+'</th>';
  }
  tbl+='<th>Change Group Name</th>';
  tbl+='</tr>';
  for( var row=0;row<rows.length;row++){
    var row_id =randomid();
    tbl +='<tr row_id="'+row_id+'">';
    for(var col =0;col<col_names.length-1;col++){
        tbl +='<td ><div class="row_data" col_name="'+col_names[col]+'">'+rows[row][col]+'</div></td>';
      }
      tbl +='<td ><div class="row_data" col_name="'+col_names[col_names.length-1]+'">'+rows[row][col_names.length-1]+'</div></td>';

      tbl += '<td class="dropdown"><form action="" name="FILTER"> <select name="filter_for" id = "select' + row + '" >';
      for(var number in team_name){
        if(number == rows[row][col_names.length-1])
        {
          tbl += '<option value="'+ row +'" selected="selected">' + number + '</option>' ;
        }
        else{
          tbl += '<option value="'+ row +'">' + number + '</option>' ;
        }
      }
      tbl += '</select> </form> </td>';
    tbl +='</tr>';
  }

  tbl +='</table>'
  var table = document.getElementById("table2");
  table.innerHTML="";
  table.innerHTML+=tbl;

  for( var row=0;row<rows.length;row++){
    var select = document.getElementById('select' + row);
    select.onchange = function () {
    var value = this.value;
    var text = this.options[this.selectedIndex].text;
    rows[value][col_names.length-1] = text;
    createtable(rows,col_names, team_name);
    }
  }
}

  function callbackfn(response){
    var team_map= new Object();
    var team_name= new Object();
    var res = JSON.parse(response);
    const value_1 =res.columns;
    const value_2=res.data;
    for(x in value_1){
        col_names[x] =value_1[x];
    }
    for(x in value_2){
        rows[x] =value_2[x];
      if(rows[x][11] in team_map){
          team_map[rows[x][11]].push(rows[x][1]);
      }else
      {
        team_map[rows[x][11]] = [rows[x][1]];

      }
      if(!(rows[x][11] in team_name)){
          team_name[rows[x][11]]= rows[x][11];
      }
    }
    createtable_map_id(team_map,team_name);
    createtable(rows,col_names, team_name);
    document.getElementById("submit-groups").disabled =false;
    document.getElementById("slack-btn").disabled=false;
    document.getElementById("taiga-btn").disabled=false;
}

function sendRequestWithCallback(action, params, async, callback) {
    var objHTTP = xhr();
    objHTTP.open('GET', action, async);
    objHTTP.setRequestHeader('Content-Type','application/x-www-form-urlencoded;charset=UTF-8');
    if(async){
  objHTTP.onreadystatechange=function() {
      if(objHTTP.readyState==4) {
    if(callback) {
        callback(objHTTP.responseText);
    }
      }
  };
    }
    objHTTP.send(params);
    if(!async) {
  if(callback) {
            callback(objHTTP.responseText);
        }
    }
}
function xhr() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
  xmlhttp=new XMLHttpRequest();
    }
    else if(window.ActiveXObject) {
  try {
      xmlhttp=new ActiveXObject("Msxml2.XMLHTTP");
  }
  catch(e) {
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
    }
    return xmlhttp;
}
