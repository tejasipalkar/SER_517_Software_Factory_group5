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
        console.log("in select")
        console.log(start,end);
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

  //TODO: start date, end date
  //TODO: create event : whole day check box, if unchecked show start end end time
  //TODO: update event - delete
  //theme
  //drag and drop events
  //validate entries
  //auto load start date based on date clciked