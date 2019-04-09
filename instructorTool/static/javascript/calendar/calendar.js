
const DATE_REGEX = /^\d{4}-(0[1-9]|1[12])-(0[1-9]|[12][0-9]|3[01])$/;
const TIME_REGEX = /^(?:2[0-3]|[01][0-9]):[0-5][0-9]$/;

var selectedEvent = null;
var newEvents = [];
var editEvents = [];
var deleteEvents = [];
var editAssign = [];
var editQuiz = [];
var colorTagMap = {Project:"#bd85a8",Deadline:"#bd403a",Assign:"#006666",Quiz:"#009999"}

$(document).ready(function() {
  $('#calendar').fullCalendar({
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'month,agendaWeek,agendaDay,listWeek'
    },
    navLinks: true, // can click day/week names to navigate views
    editable: true,
    eventLimit: true, // allow "more" link when too many events
    selectable: true,
    selectHelper: true,
    droppable: true,
    eventTextColor: '#ffffff',
    timezone: "local",
    select: function(start, end) {
      console.log("Select date",end)
      openModelForNewEvent(end._d);
    },
    events: [],
    
    eventClick: function(event, element) {
      console.log("eventclicked ",event)
      //if end and start are same, end is set to null by default
      if(event.end == null){
        event.end = event.start;
      }
      selectedEvent = event;
      openModelForUpdateEvent(event);
    },
    eventDrop: function(event, delta, revertFunc) {
      if (!confirm("Are you sure about this change?")) {
        revertFunc();
      }
      var eventType = event.eventType
      if(eventType){
        if(eventType == 'Event'){
          editEvents.push(event._id);
        }else if(eventType == 'Assign'){
          editAssign.push(event._id);
        }
      }
    }
  });
  fetchEvents();
});

function openModelForNewEvent(Date){
  selectedEvent = null;
  clearModel()
  if(Date){
    $('#start_date').val(formatDate(Date));
  }
  $('#event_details_model').modal('show');
}

function openModelForUpdateEvent(event){
  var tag = "";
  var title = "";
  var startDate = "";
  var endDate = "";
  var startTime = "";
  var endTime = "";
  var eventType = "";

  if(event){
    if(event.eventType){
      eventType = event.eventType;
    }
    if(event.tag){
      tag = event.tag;
    }
    if(event.title){
      title = event.title;
    }if(event.start){
        startDate = event.start.format().substring(0,10)
        startTime = event.start.format().substring(11,16)
    }if(event.end){
        endDate = event.end.format().substring(0,10)
        endTime = event.end.format().substring(11,16)
    }
  }
  
  if(eventType == 'Event'){
    clearModel();
    setModelValue(tag,title, startDate, endDate, startTime, endTime);
    $('#delete_button').show();
    $('#event_details_model').modal('show');
  }else if(eventType == 'Assign' || eventType == 'Quiz'){
    clearAssignModel();
    setAssignModelValue(tag,title, startDate, startTime);
    $('#assign_details_model').modal('show');
  }
  
  console.log("start", startDate, "end", endDate,
  "start", startTime, "end", endTime)
}

  //get all event and put them on the calendar
  function fetchEvents() {
    var source = []
    var events = canvasEventsToFullCalendar();
    var assign = canvasAssignmentToFullCalendar()
    source = events.concat(assign)
    $('#calendar').fullCalendar('removeEvents');
    $('#calendar').fullCalendar('addEventSource', source);
  }

  function createEvents() {
    var tag = $('#tag_input').val().trim();
    var title = $('#event_title').val();
    var startDate = $('#start_date').val();
    var endDate = $('#end_date').val();
    var startTime = $('#start_time').val();
    var endTime = $('#end_time').val();
    var isSameDay = $('#same_day_checkbox').is(":checked")
    var isAllDay = $('#all_day_checkbox').is(":checked")

    var errorMessage = "Invalid parameter(s): ";
    if(title == null || title.length < 1){
      $('#title_error').text("Invalid Title");
      errorMessage += "Title, "
    }if(title != null && title.includes(':')){
      $('#title_error').text("Char not allowed: ':'");
      errorMessage += "Title, "
    }
    if(startDate == null || !DATE_REGEX.test(startDate)){
      $('#start_date_error').text("Invalid Date");
      errorMessage += "StartDate, "
    }if(!isSameDay && (endDate == null || !DATE_REGEX.test(endDate))){
      $('#end_date_error').text("Invalid Date");
      errorMessage += "EndDate, "
    }else if(!isSameDay && (endDate == null || startDate == null || !compareDates(startDate, endDate))){
      $('#end_date_error').text("End Date should be after start date");
      errorMessage += "EndDate < StartDate, "
    }if(!isAllDay && (startTime == null || !TIME_REGEX.test(startTime))){
      $('#start_time_error').text("Invalid Time");
      errorMessage += "StartTime, "
    }if(!isAllDay && (endTime == null || !TIME_REGEX.test(endTime))){
      $('#end_time_error').text("Invalid Time");
      errorMessage += "EndTime "
    }else if(!isAllDay && (endTime == null || startTime == null || !compareTime(startTime, endTime, startDate, endDate))){
      $('#end_time_error').text("End Time should be after start time");
      errorMessage += "EndTime < StartTime"
    }

    if(errorMessage != "Invalid parameter(s): "){
      console.log(errorMessage,)
    }else{
      if(isSameDay){
        endDate = startDate;
      }
      if(!isAllDay){
        endDate = endDate + 'T' + endTime;
        startDate = startDate + 'T' + startTime;
      }else{
        endDate = endDate + 'T' + '23:59';
        startDate = startDate + 'T' + '00:01';
      }
      console.log(title,startDate,endDate)
      var eventData;
      if(selectedEvent){
        //update event
        eventData = selectedEvent;
        eventData.title = title;
        eventData.start = startDate;
        eventData.end = endDate;
        eventData.color = colorTagMap[tag];
        eventData.allDay = false;
        eventData.tag = tag;
        editEvents.push(eventData._id)
        $('#calendar').fullCalendar('removeEvents',eventData._id);
      }else{
        var id = Math.random();
        newEvents.push(id.toString());
        eventData = {
          _id: id,
          title: title,
          start: startDate,
          end: endDate,
          color: colorTagMap[tag],
          allDay: false,
          tag: tag
        };
      }
      $('#calendar').fullCalendar('renderEvent', eventData, true);
      $('#calendar').fullCalendar('unselect');
      $('#event_details_model').modal('hide');
    }
  }

  function editAssignment() {
    var title = $('#assign_title').val();
    var startDate = $('#assign_start_date').val();
    var startTime = $('#assign_start_time').val();

    var errorMessage = "Invalid parameter(s): ";
    if(title == null || title.length < 1){
      $('#assign_title_error').text("Invalid Title");
      errorMessage += "Title, "
    }if(title != null && title.includes(':')){
      $('#assign_title_error').text("Char not allowed: ':'");
      errorMessage += "Title, "
    }
    if(startDate == null || !DATE_REGEX.test(startDate)){
      $('#assign_start_date_error').text("Invalid Date");
      errorMessage += "StartDate, "
    }if(startTime == null || !TIME_REGEX.test(startTime)){
      $('#assign_start_time_error').text("Invalid Time");
      errorMessage += "StartTime, "
    }

    if(errorMessage != "Invalid parameter(s): "){
      console.log(errorMessage,)
    }else{
      startDate = startDate + 'T' + startTime;
      console.log(title,startDate)
      var eventData;
      if(selectedEvent){
        eventData = selectedEvent;
        eventData.title = title;
        eventData.start = startDate;
        eventData.end = startDate;
        eventData.allDay = false;
        editAssign.push(eventData._id)
        $('#calendar').fullCalendar('removeEvents',eventData._id);
      }
      $('#calendar').fullCalendar('renderEvent', eventData, true);
      $('#calendar').fullCalendar('unselect');
      $('#assign_details_model').modal('hide');
    }
  }

  function deleteEvent(){
    if(selectedEvent){
      if(!newEvents.includes(selectedEvent._id)){
        deleteEvents.push(selectedEvent.id)
      }
      $('#calendar').fullCalendar( 'removeEvents', selectedEvent._id)
      $('#delete_confirm_model').modal('hide');
      $('#event_details_model').modal('hide');
    }else{
      console.log('event deletion failed')
    }
  }

  function pushDeleteEvents(){
    if(deleteEvents.length>0){
      console.log("events to be deleted",deleteEvents);
      $.ajax({
        url: '/deleteevent',
        data: JSON.stringify(deleteEvents),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            console.log("deleteEvents",response);
            $("#success-alert").show().delay(2000).fadeOut();
            $('#hyperlink-button')[0].click();
        },
        error: function(error) {
            console.log("deleteEvents",error);
            $("#failure-alert").show().delay(2000).fadeOut();
        }
      });
    }else{
      $("#success-alert").show().delay(2000).fadeOut();
      $('#hyperlink-button')[0].click();
    }
  }

  function pushNewEvents() {
    $('#push-spinner').show();
    var events = []
    console.log("newEvents",newEvents)
    for(var i = 0; i < newEvents.length; i++){
      var completeEvent = $('#calendar').fullCalendar('clientEvents', newEvents[i])[0];
      if(completeEvent != null){
        var event = {
          context_code: null,
          title: null,
          start_at: null,
          end_at: null,
          time_zone_edited: "America/Phoenix"
        };
        var title = completeEvent.title;
        if(completeEvent.tag.trim().length != 0){
          title = completeEvent.tag.trim() + ":" + title
        }
        event.context_code = course;
        event.title = title;
        event.start_at = FullCalendarToCanvasDate(completeEvent.start.format().substring(0,10),completeEvent.start.format().substring(11,16));
        event.end_at = FullCalendarToCanvasDate(completeEvent.end.format().substring(0,10),completeEvent.end.format().substring(11,16));
        events.push(event);
      }
    }
    
    if(events.length>0){
      console.log("new events to push",events);
      $.ajax({
        url: '/newevent',
        data: JSON.stringify(events),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            pushEditEvents();
        },
        error: function(error) {
            console.log("newEvents",error);
            $("#failure-alert").show().delay(2000).fadeOut();
        }
      });
    }else{
      pushEditEvents();
    }
  }

  function pushEditEvents(){
    console.log("editEvents",editEvents)
    var events = []
    for(var i = 0; i < editEvents.length; i++){
      var completeEvent = $('#calendar').fullCalendar('clientEvents', editEvents[i])[0];
        if(completeEvent != null && completeEvent.id != null){
        var event = {
          id: null,
          title: null,
          start_at: null,
          end_at: null
        };
        var title = completeEvent.title;
        if(completeEvent.tag.trim().length != 0){
          title = completeEvent.tag.trim() + ":" + title
        }
        event.id = completeEvent.id;
        event.title = title;
        event.start_at = FullCalendarToCanvasDate(completeEvent.start.format().substring(0,10),completeEvent.start.format().substring(11,16));
        if(completeEvent.end == null){
          event.end_at = event.start_at;
        }else{
          event.end_at = FullCalendarToCanvasDate(completeEvent.end.format().substring(0,10),completeEvent.end.format().substring(11,16));
        }
        events.push(event);
      }
    }
    if(events.length>0){
      console.log("edit events to push",events);
      $.ajax({
        url: '/editevent',
        data: JSON.stringify(events),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
          pushEditAssign();
        },
        error: function(error) {
          console.log("editEvents",error);
          $("#failure-alert").show().delay(2000).fadeOut();
        }
      });
    }else{
      pushEditAssign();
    }
  }

  function pushEditAssign(){
    console.log("editAssign",editAssign)
    var events = []
    for(var i = 0; i < editAssign.length; i++){
      var completeEvent = $('#calendar').fullCalendar('clientEvents', editAssign[i])[0];
        if(completeEvent != null && completeEvent.id != null){
        var event = {
          id: null,
          name: null,
          due_at: null
        };
        event.id = completeEvent.id;
        event.name = completeEvent.title;
        event.due_at = FullCalendarToCanvasDate(completeEvent.start.format().substring(0,10),completeEvent.start.format().substring(11,16));
        events.push(event);
      }
    }
    if(events.length>0){
      var data = {}
      data.event = events;
      data.course = course;
      console.log("edit assign to push",events);
      $.ajax({
        url: '/editassign',
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
          pushDeleteEvents();
        },
        error: function(error) {
          console.log("editAssign",error);
          $("#failure-alert").show().delay(2000).fadeOut();
        }
      });
    }else{
      pushDeleteEvents();
    }
  }

  function pushEditQuiz(){
    console.log("editquiz",editQuiz)
    var events = []
    for(var i = 0; i < editQuiz.length; i++){
      var completeEvent = $('#calendar').fullCalendar('clientEvents', editQuiz[i])[0];
        if(completeEvent != null && completeEvent.id != null){
        var event = {
          id: null,
          title: null,
          due_at: null
        };
        event.id = completeEvent.id;
        event.title = completeEvent.title;
        event.due_at = FullCalendarToCanvasDate(completeEvent.start.format().substring(0,10),completeEvent.start.format().substring(11,16));
        events.push(event);
      }
    }
    if(events.length>0){
      console.log("edit quiz to push",events);
      $.ajax({
        url: '/editquiz',
        data: JSON.stringify(events),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
          pushDeleteEvents();
        },
        error: function(error) {
          console.log("editQuiz",error);
          $("#failure-alert").show().delay(2000).fadeOut();
        }
      });
    }else{
      pushDeleteEvents();
    }
  }

  function setModelValue(tag, title, startDate, endDate, startTime, endTime){
    $('#tag_input').val(tag);
    $('#event_title').val(title);
    $('#start_date').val(startDate);
    $('#end_date').val(endDate);
    $('#start_time').val(startTime);
    $('#end_time').val(endTime);
    if(endDate != ""){
      if(endDate == startDate){
        endDate = ""
        $('#end_date').val(endDate);
      }else{
        $('#same_day_checkbox').prop('checked', false);
        $('#end_date_div').show()
      }
    }
    if((startTime == "00:01" && endTime == "23:59")|| (startTime == "" && endTime == "")){
      //isAllDay event
    }else{
      $('#all_day_checkbox').prop('checked', false);
      $('#all_date_div').show()
    }
  }

  function setAssignModelValue(tag, title, startDate, startTime){
    $('#assign_tag').val(tag);
    $('#assign_title').val(title);
    $('#assign_start_date').val(startDate);
    $('#assign_start_time').val(startTime);
  }

  function clearModel() {
    $('#title_error').text("");
    $('#start_date_error').text("");
    $('#end_date_error').text("");
    $('#start_time_error').text("");
    $('#end_time_error').text("");

    $('#event_title').val("");
    $('#start_date').val("");
    $('#end_date').val("");
    $('#start_time').val("");
    $('#end_time').val("");
    $('#same_day_checkbox').prop('checked', true);
    $('#all_day_checkbox').prop('checked', true);
    $('#end_date_div').hide()
    $('#all_date_div').hide()
    $('#delete_button').hide()
  }

  function clearAssignModel() {
    $('#assign_title_error').text("");
    $('#assign_start_date_error').text("");
    $('#assign_start_time_error').text("");

    $('#assign_title').val("");
    $('#assign_start_date').val("");
    $('#assign_start_time').val("");
  }

  function setTagField(tag){
    $('#tag_input').val(tag);
  }

  function formatDate(Date){
    var month = String((Date.getMonth()+1))
    var date = String(Date.getDate())
    if(month.length < 2){
      month = "0"+month;
    }
    if(date.length < 2){
      date = "0"+date;
    }
    var date = Date.getFullYear() + "-" + month + "-" + date;
    return date;
  }

  function formatTime(Date){
    var hours = String((Date.getHours()))
    var mins = String(Date.getMinutes())
    if(hours.length < 2){
      hours = "0"+hours;
    }
    if(mins.length < 2){
      mins = "0"+mins;
    }
    var time = hours + ":" + mins;
    return time;
  }

  //true if date1 is less than date2
  function compareDates(date1,date2){
    var date1complete = date1.split('-');
    var date2complete = date2.split('-');
    if(date1complete.length == 3 && date2complete.length == 3){
      if(date1complete[0] <=  date2complete[0]){  //year
        if(date1complete[1] <= date2complete[1] ||
          (date1complete[1] > date2complete[1] && date1complete[0] <  date2complete[0])){ //month
          if(date1complete[2] < date2complete[2] ||
            (date1complete[2] > date2complete[2] && date1complete[1] < date2complete[1])){ //date
              return true;
          }
        }    
      }
    }
    return false;
  }

  function compareTime(time1,time2, startDate, endDate){
    var time1complete = time1.split(':');
    var time2complete = time2.split(':');

    if(time1complete.length == 2 && time2complete.length == 2){
      if(time1complete[0] <=  time2complete[0]){  //hours
        if(time1complete[1] <= time2complete[1] || 
          (time1complete[1] > time2complete[1] && time1complete[0] < time2complete[0])){  //mins
            return true;
        }
      }
      if(endDate != null && startDate != null && endDate != "" && startDate != "" && 
        compareDates(startDate,endDate)){ //different days
          return true;
      }
    }
    return false;
  }

  function canvasEventsToFullCalendar(){
    var events = JSON.parse(eventsJSON);
    for(var i=0 ;i <events.length ;i++ ){
      events[i].eventType = "Event";
      events[i].start = events[i].start_at;
      events[i].end = events[i].end_at;
      events[i].tag = "";
      var fullTitle = events[i].title.split(':');
      if(fullTitle.length == 2){
        events[i].tag = fullTitle[0];
        events[i].title = fullTitle[1];
        events[i].color = colorTagMap[fullTitle[0]];
      }
      delete events[i].start_at;
      delete events[i].end_at;
      delete events[i].url;
      events[i].start = formatDateCanvasToFullCalendar(events[i].start)
      events[i].end = formatDateCanvasToFullCalendar(events[i].end)
    }
    console.log(events);
    return events;
  }

  function canvasAssignmentToFullCalendar(){
    var events = JSON.parse(assignmentsJSON);
    for(var i=0 ;i <events.length ;i++ ){
      if(events[i].due_at != null){
        events[i].eventType = "Assign";
        events[i].title = events[i].name;
        events[i].start = events[i].due_at;
        events[i].tag = "Assign";
        var fullTitle = events[i].name.split(':');
        if(fullTitle.length == 2){
          events[i].title = fullTitle[1];
        }
        events[i].color = colorTagMap[events[i].tag];
        delete events[i].due_at;
        delete events[i].url;
        events[i].start = formatDateCanvasToFullCalendar(events[i].start)
      }
    }
    return events;
  }

  function canvasQuizToFullCalendar(){
    var events = JSON.parse(quizJSON);
    for(var i=0 ;i <events.length ;i++ ){
      events[i].eventType = "Quiz";
      events[i].title = events[i].title;
      events[i].start = events[i].due_at;
      events[i].tag = "Quiz";
      var fullTitle = events[i].name.split(':');
      if(fullTitle.length == 2){
        events[i].title = fullTitle[1];
      }
      events[i].color = colorTagMap[events[i].tag];
      delete events[i].due_at;
      delete events[i].url;
      events[i].start = formatDateCanvasToFullCalendar(events[i].start)
    }
    return events;
  }

  function formatDateCanvasToFullCalendar(canvasDate){
    var fullDate = new Date(Date.parse(canvasDate))
    var month = fullDate.getMonth()+1
    var date = fullDate.getFullYear() + "-" + pad(month) + "-" + pad(fullDate.getDate())
    var time = pad(fullDate.getHours()) + ":" + pad(fullDate.getMinutes())
    return date + 'T' + time;
  }

  function pad(d) {
    return (d < 10) ? '0' + d.toString() : d.toString();
}

  //2019-03-20T05:59:00Z  TO
  //2019-02-10T23:59
  function canvasToFullCalendarDate(canvasTime){
    var fullDate = canvasTime.split('T');
    var date = fullDate[0];
    var fullTime = fullDate[1];
    if(fullTime[fullTime.length -1] == 'Z'){
      return date + 'T' + fullTime.slice(0, -1);
    }else{
      var time = fullTime.split('-')[1];
      return date + 'T' + time;
    }
  }

  //2019-02-10T23:59  to
  //2019-03-20T05:59:00Z 
  function FullCalendarToCanvasDate(localDate, localTime){
    return localDate + 'T' + localTime + ':00-07:00'
  }

  function imageDownload(){
    html2canvas(document.querySelector("#calendar")).then(canvas => {
      image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
      var link = document.createElement('a');
      link.download = "calendar.png";
      link.href = image;
      link.click();
  });
  }
  //TODO:
  //clean error message