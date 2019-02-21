const DATE_REGEX = /^\d{4}-(0[1-9]|1[12])-(0[1-9]|[12][0-9]|3[01])$/;
const TIME_REGEX = /^(?:2[0-3]|[01]?[0-9]):[0-5][0-9]$/;

var selected_event ;

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

    select: function(start, end) {
      console.log("Select date",end)
      openModel(end._d);
    },
    events: [],

    eventClick: function(event, element) {
      console.log("in eventclick ",event)
    }
  });
});

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
        start: '2019-01-07',
        end: '2019-02-10'
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
    }else if(!isAllDay && (endTime == null || startTime == null || !compareTime(startTime, endTime))){
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
      }
      console.log(title,startDate,endDate)
      var eventData;
      if (title) {
        eventData = {
          title: title,
          start: startDate,
          end: endDate
        };
        $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
      }
      $('#calendar').fullCalendar('unselect');
      $('#event_details_model').modal('hide');
    }
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
    $('#end_date_div').collapse('hide')
    $('#all_date_div').collapse('hide')
  }

  function setModelValues(Date){
    console.log("in setModelValues")
    var month = String((Date.getMonth()+1))
    var date = String(Date.getDate())
    if(month.length < 2){
      month = "0"+month;
    }
    if(date.length < 2){
      date = "0"+date;
    }
    var date = Date.getFullYear() + "-" + month + "-" + date;
    $('#start_date').val(date);
  }

  function openModel(Date){
    console.log("in openModel")
    clearModel()
    if(Date){
      setModelValues(Date);
    }
    $('#event_details_model').modal('show');
  }

  function compareDates(date1,date2){
    var date1complete = date1.split('-');
    var date2complete = date2.split('-');

    if(date1complete.length == 3 && date2complete.length == 3){
      if(date1complete[0] <=  date2complete[0] && date1complete[1] <= date2complete[1]
        && date1complete[2] <= date2complete[2]){
          return true;
        }
    }
    return false;
  }

  function compareTime(time1,time2){
    var time1complete = time1.split(':');
    var time2complete = time2.split(':');

    if(time1complete.length == 2 && time2complete.length == 2){
      if(time1complete[0] <=  time2complete[0] && time1complete[1] <= time2complete[1]){
          return true;
        }
    }
    return false;

  }

  //TODO: update event - delete
  //theme
  //drag and drop events
  //clear error on type
  //event color