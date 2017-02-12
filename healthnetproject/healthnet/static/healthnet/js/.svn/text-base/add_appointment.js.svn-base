$( document ).ready( function() {
    var passedTime = localStorage.getItem("dateTime");
    if (passedTime != "no_date") {
        //fill in passed time - either current time or hour clicked
        //offset is already done when sending events so no offset needed
        var defaultDateTime = moment(passedTime)
            .utcOffset('0000').format('MMM DD YYYY, h:mm a');
        document.getElementById('date_time').value = defaultDateTime;
    } else { //new appointments without set time will need the offset
        document.getElementById('date_time').value = moment(new Date())
            .utcOffset('-0400').format('MMM DD YYYY, h:mm a');
    }
});