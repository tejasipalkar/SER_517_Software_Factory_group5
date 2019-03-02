const DATE_REGEX = /^\d{4}-(0[1-9]|1[12])-(0[1-9]|[12][0-9]|3[01])$/;
const TIME_REGEX = /^(?:2[0-3]|[01][0-9]):[0-5][0-9]$/;

var selectedEvent = null;
const DEFAULT_EVENT_COLOR = ""

$(document).ready(function() {

  $('#external-events .fc-event').each(function() {
    // store data so the calendar knows to render an event upon drop
    $(this).data('event', {
      title: $.trim($(this).text()), // use the element's text as the event title
      stick: true // maintain when user navigates (see docs on the renderEvent method)
    });
    // make the event draggable using jQuery UI
    $(this).draggable({
      zIndex: 999,
      revert: true,      // will cause the event to go back to its
      revertDuration: 0  //  original position after the drag
    });
  });

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
      console.log("eventclicked ",event,event.start.format())
      selectedEvent = event;
      openModelForUpdateEvent(event);
    }
  });
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
  var title = "";
  var startDate = "";
  var endDate = "";
  var startTime = "";
  var endTime = "";
  var color = DEFAULT_EVENT_COLOR;

  if(event){
    if(event.title){
      title = event.title;
    }if(event.start){
        startDate = event.start.format().substring(0,10)
        startTime = event.start.format().substring(11,16)
    }if(event.end){
        endDate = event.end.format().substring(0,10)
        endTime = event.end.format().substring(11,16)
    }
    if(event.color){
      color = event.color;
    }
  }
  clearModel();
  setModelValue(title, startDate, endDate, startTime, endTime, color);
  $('#delete_button').show();
  $('#event_details_model').modal('show');
  console.log("start", startDate, "end", endDate,
  "start", startTime, "end", endTime)
}

  //get all event and put them on the calendar
  function fetchEvents() {
    var source = [
      {
        title: 'All Day Event',
        start: '2019-02-01',
        end: '2019-02-01'
      },
      {
        title: 'Long Event',
        start: '2019-01-07T00:00',
        end: '2019-02-10T23:59'
      },
      {
        id: 999,
        title: 'Repeating Event',
        start: '2019-02-09T16:00:00'
      },
      {
        title: 'Meeting',
        start: '2019-02-12T10:30:00',
        end: '2019-02-12T12:30:00'
      }
    ]
    $('#calendar').fullCalendar('removeEvents');
    $('#calendar').fullCalendar('addEventSource', source);
  }

  function createEvents() {
    var title = $('#event_title').val();
    var startDate = $('#start_date').val();
    var endDate = $('#end_date').val();
    var startTime = $('#start_time').val();
    var endTime = $('#end_time').val();
    var color = $('#color_input').val();
    var isSameDay = $('#same_day_checkbox').is(":checked")
    var isAllDay = $('#all_day_checkbox').is(":checked")

    var errorMessage = "Invalid parameter(s): ";
    if(title == null || title.length < 1){
      $('#title_error').text("Invalid Title");
      errorMessage += "Title, "
    }if(startDate == null || !DATE_REGEX.test(startDate)){
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
        startDate = startDate + 'T' + '00:00';
      }
      console.log(title,startDate,endDate)
      var eventData;
      if(selectedEvent){
        //update event
        eventData = selectedEvent;
        eventData.title = title;
        eventData.start = startDate;
        eventData.end = endDate;
        eventData.color = color;
        eventData.allDay = false;
        $('#calendar').fullCalendar('removeEvents',eventData._id);
      }else{
        eventData = {
          title: title,
          start: startDate,
          end: endDate,
          color: color,
          allDay: false
        };
      }
      $('#calendar').fullCalendar('renderEvent', eventData, true);
      $('#calendar').fullCalendar('unselect');
      $('#event_details_model').modal('hide');
    }
  }

  function deleteEvent(){
    if(selectedEvent){
      $('#calendar').fullCalendar( 'removeEvents', selectedEvent._id)
      $('#delete_confirm_model').modal('hide');
      $('#event_details_model').modal('hide');
    }else{
      console.log('event deletion failed')
    }
  }

  function getAllEvents() {
      var events = $('#calendar').fullCalendar('clientEvents');
      console.log("events",events);
    }

  function setModelValue(title, startDate, endDate, startTime, endTime, color){
    $('#event_title').val(title);
    $('#start_date').val(startDate);
    $('#end_date').val(endDate);
    $('#start_time').val(startTime);
    $('#end_time').val(endTime);
    $('#color_input').val(color);
    if(endDate != ""){
      if(endDate == startDate){
        endDate = ""
        $('#end_date').val(endDate);
      }else{
        $('#same_day_checkbox').prop('checked', false);
        $('#end_date_div').show()
      }
    }
    if((startTime == "00:00" && endTime == "23:59")|| (startTime == "" && endTime == "")){
      //isAllDay event
    }else{
      $('#all_day_checkbox').prop('checked', false);
      $('#all_date_div').show()
    }
  }

  function clearModel() {
    $('#title_error').text("");
    $('#start_date_error').text("");
    $('#end_date_error').text("");
    $('#start_time_error').text("");
    $('#end_time_error').text("");
    $('#color_input').val(DEFAULT_EVENT_COLOR);

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

  function setColorField(color){
    $('#color_input').val(color);
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

  //TODO:
  //drag and drop events
  //clean error message
  //event color
  //2 day event