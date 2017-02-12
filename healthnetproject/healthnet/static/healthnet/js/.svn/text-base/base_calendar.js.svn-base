var pk;
var events_url;
var viewType = 'agendaDay';

//saves the pk for use later
function setPK(key) {
    pk = key;
    events_url = '/get_events/' + pk + '/';
}

//switches to add appointment page
function addAppointment(key, dateTime) {
    if (dateTime === undefined) {
        localStorage.setItem("dateTime", "no_date");
    } else {
        localStorage.setItem("dateTime", dateTime);
    }

    window.location.href = '/add_appointment/' + key + '/'
}

//set default calendar view style
function setDefaultView(user) {
    if (user == 'patient') {
        viewType = 'month';
    } else if (user == 'nurse') {
        viewType = 'basicWeek';
    }

    readyCalendar();
}

//calculates the desired calendar height
function get_calendar_height() {
      return $(window).height() - 200;
}

//sets up the calendar
function readyCalendar() {

    var calendar = $('#calendar');

    calendar.fullCalendar({
        height: get_calendar_height,
        customButtons: {
            addAppointment: {
                text: 'Add Appointment',
                click: function() {
                    addAppointment(pk);
                }
            }
        },
        header: {
            left: 'today addAppointment',
            center: 'prev, title, next',
            right: 'month,basicWeek,agendaDay'
        },

        defaultView: viewType,

        buttonText: {
            today: 'Today',
            month: 'Month',
            basicWeek: 'Week',
            agendaDay: 'Day'
        },

        events: events_url,

        dayClick: function(date, jsEvent, view) {
            if (calendar.fullCalendar( 'getView').name == 'agendaDay') { //if its a day view, then they clicked an hour
                addAppointment(pk, date.toDate());
            } else { //if not day view, switch to dayview
                viewType = 'agendaDay';
                calendar.fullCalendar( 'gotoDate', date );
                calendar.fullCalendar( 'changeView', 'agendaDay' );
            }
        },

        eventClick: function(calEvent, jsEvent, view) {
            // change the border color to show selected
            $(this).css('border', 'solid 3px #1976D2');

            window.location.href = '/edit_appointment/' + calEvent.id;
        }
    });
}

//resizes calendar when window resizes
$(document).ready(function() {
    //set calendar height to window height
    $(window).resize(function() {
        $('#calendar').fullCalendar('option', 'height', get_calendar_height());
    });

    //center calendar title
    var fc_center = $('.fc-center');
    fc_center.css({'marginLeft' : -(fc_center.width()/2)});
});