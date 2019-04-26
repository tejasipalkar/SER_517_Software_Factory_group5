
  $(function() {
    $('#submit_slack').bind('click', function(){
      document.getElementById("submit_slack").innerHTML="Loading";
        $.ajax({
            url: '/slack',
            data: $('form').serialize(),
            type: 'POST'
        })
        .done(function(response) {
          if(response == "invalid token")
            {alert("Invalid Token");
            document.getElementById("submit_slack").innerHTML="Submit";}
          else
            {document.getElementById("submit_slack").innerHTML="Submit";
              $("#slackModal").modal('hide');
            alert("Slack Groups Created");
            document.getElementById("slack-btn").disabled=true;}
        });
    });
});

  $(function() {
    $('#submit_taiga').bind('click', function(){
      document.getElementById("submit_taiga").innerHTML="Loading";
        $.ajax({
            url: '/taiga',
            data: $('form').serialize(),
            type: 'POST'
        })
        .done(function(response) {
          if(response == "invalid auth")
            {alert("Invalid Username/Password");
            document.getElementById("submit_taiga").innerHTML="Submit";}
          else
            { document.getElementById("submit_taiga").innerHTML="Submit";
              $("#taigaModal").modal('hide');
            alert("Taiga Channels Created");
            document.getElementById("taiga-btn").disabled=true;}
        });
    });
});

$(function() {
    $('#submit_github').bind('click', function(){
      document.getElementById("submit_github").innerHTML="Loading";
        $.ajax({
            url: '/github',
            data: $('form').serialize(),
            type: 'POST'
        })
        .done(function(response) {
          if(response == "invalid token")
            {alert("Invalid Token");
            document.getElementById("submit_github").innerHTML="Submit";}
          else
            {document.getElementById("submit_github").innerHTML="Submit";
              $("#githubModal").modal('hide');
            alert("Github Repositories Created");
            document.getElementById("github-btn").disabled=true;}
        });
    });
});

$(function() {
    $('#submitgroups').bind('click', function(){
      document.getElementById("submitgroups").innerHTML="Loading";
          var actuallist = new Array();
          var grouplist = new Array();
          var actualTable = new Array();
          $("#table2 tr:not(:first)").each(function () {
              var tds = $(this).find("td");
              var SStudent = { Group: $(this).find('td:eq(11)').text(), EmailID: $(this).find('td:eq(0)').text()};
              var tableData = { FullName: $(this).find('td:eq(1)').text(), ASURITE: $(this).find('td:eq(2)').text(), Github: $(this).find('td:eq(3)').text(), EmailID: $(this).find('td:eq(0)').text(), Preferences: $(this).find('td:eq(4)').text(), Avoidance: $(this).find('td:eq(5)').text(), TimeZone: $(this).find('td:eq(6)').text(), TimePreference: $(this).find('td:eq(7)').text(), GithubKnowledge: $(this).find('td:eq(8)').text(), ScrumKnowledge: $(this).find('td:eq(9)').text(), Comments: $(this).find('td:eq(10)').text(), GroupName: $(this).find('td:eq(11)').text()};
              actualTable.push(tableData);
              actuallist.push(SStudent);
          });
          $("#table1 tr:not(:first)").each(function () {
              var tds = $(this).find("td");
              var SStudent1 = { GroupNumber: $(this).find('td:eq(0)').text(), GroupName: $(this).find('td:eq(1) input').val() };
              grouplist.push(SStudent1);
          });
          var valuetosend = {'items':actuallist, 'new':grouplist, "actualTable": actualTable};
        $.ajax({
            url: '/submitgroups',
            data: JSON.stringify(valuetosend),
            type: 'POST',
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',
        })
        .done(function(response) {
          if(response == 'Groups Pushed to Canvas')
            { alert(response);
              document.getElementById("submitgroups").innerHTML="Submit Groups";
              document.getElementById("submitgroups").disabled=true;
              document.getElementById("slack-btn").style.display="block";
              document.getElementById("taiga-btn").style.display="block";
              document.getElementById("github-btn").style.display="block";
            }
          else
            {alert(response);
              document.getElementById("submitgroups").innerHTML="Submit Groups";}
        });
    });
});

$(function() {
    $('#exportgroups').bind('click', function(){
          var grouplist = new Array();
          var actualTable = new Array();
          $("#table2 tr:not(:first)").each(function () {
              var tds = $(this).find("td");
              var tableData = { FullName: $(this).find('td:eq(1)').text(), ASURITE: $(this).find('td:eq(2)').text(), Github: $(this).find('td:eq(3)').text(), EmailID: $(this).find('td:eq(0)').text(), Preferences: $(this).find('td:eq(4)').text(), Avoidance: $(this).find('td:eq(5)').text(), TimeZone: $(this).find('td:eq(6)').text(), TimePreference: $(this).find('td:eq(7)').text(), GithubKnowledge: $(this).find('td:eq(8)').text(), ScrumKnowledge: $(this).find('td:eq(9)').text(), Comments: $(this).find('td:eq(10)').text(), GroupName: $(this).find('td:eq(11)').text()};
              actualTable.push(tableData);
          });
          $("#table1 tr:not(:first)").each(function () {
              var tds = $(this).find("td");
              var SStudent1 = { GroupNumber: $(this).find('td:eq(0)').text(), GroupName: $(this).find('td:eq(1) input').val() };
              grouplist.push(SStudent1);
          });
          for(var table in actualTable){
            for(var value in grouplist){
              if(actualTable[table]['GroupName'] == grouplist[value]['GroupNumber']){
                actualTable[table]['GroupName'] = grouplist[value]['GroupName'];
              }
            }
          }
          var csv = '';
          var keysAmount = Object.keys(actualTable[0]).length
          var keysCounter = 0
          for(let key in actualTable[0]){
                    csv += key + (keysCounter+1 < keysAmount ? ',' : '\r\n' )
                    keysCounter++
            }
          for(var row = 0; row < actualTable.length; row++){
              keysAmount = Object.keys(actualTable[row]).length
              keysCounter = 0
              for(let key in actualTable[row]){
                if(actualTable[row][key].includes(',')){
                  csv += "\"" + actualTable[row][key] + "\"" + (keysCounter+1 < keysAmount ? ',' : '\r\n' )
                  }
                else{
                  csv += actualTable[row][key] + (keysCounter+1 < keysAmount ? ',' : '\r\n' )
                  }
                keysCounter++
              }

            keysCounter = 0
          }

        var link = document.createElement('a')
        link.id = 'download-csv'
        link.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(csv));
        link.setAttribute('download', 'GroupData.csv');
        document.body.appendChild(link)
        document.querySelector('#download-csv').click()
        var element = document.getElementById('download-csv');
        element.parentNode.removeChild(element);
      });
});

var col_names =[]
var rows =[]
function postgrouppref(){

  var pref = document.getElementById("sel1").value;
  var avoid = document.getElementById("sel2").value;
  var group_size = document.getElementById("size").value;
  var input_select = document.getElementById("sel4").value;
  var file = document.getElementById("file").value;
  url ="/group?"+"pref="+pref+"&avoid="+avoid+"&group="+group_size+"&input_select="+input_select+"&file="+file;
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
  tbl_1+='<th bgcolor="#D1B894">Group Name</th>';
  tbl_1+='<th bgcolor="#D1B894">New Group Name</th>';
  tbl_1+='</tr>';
  for(x in team_name){
    tbl_1+='<tr row_id="'+x+'">';
    tbl_1+='<td>'+x+'</td>';
    tbl_1+='<td><input type="text" value="'+team_map[x]+'" style="background-color: #F0EAD6"></td>';
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
    tbl+='<th bgcolor="#D1B894">'+col_names[head_cell]+'</th>';
  }
  tbl+='<th bgcolor="#D1B894">Move to Group</th>';
  tbl+='</tr>';
  for( var row=0;row<rows.length;row++){
    var row_id =randomid();
    /*console.log(row)*/
    if(rows[row][2] === ""){
      tbl +='<tr row_id="'+row_id+'" style="color:red;">';
    }
    else{
      tbl +='<tr row_id="'+row_id+'">';
    }
    /*tbl +='<tr row_id="'+row_id+'">';*/
    for(var col =0;col<col_names.length-1;col++){
        tbl +='<td ><div class="row_data" col_name="'+col_names[col]+'">'+rows[row][col]+'</div></td>';
      }
      tbl +='<td ><div class="row_data" col_name="'+col_names[col_names.length-1]+'">'+rows[row][col_names.length-1]+'</div></td>';

      tbl += '<td class="dropdown"><form action="" name="FILTER"> <select name="filter_for" id = "select' + row + '" style="background-color: #F0EAD6">';
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
    document.getElementById("new1").style.display="block";
    document.getElementById("new2").style.display="block";
    createtable_map_id(team_map,team_name);
    createtable(rows,col_names, team_name);
    document.getElementById("submitgroups").style.display="block";
    document.getElementById("exportgroups").style.display="block";
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
