//some magic to take care of the csrf stuff - don't touch if unsure
$(function() {

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

function create_post() {
     $.ajax({
        url : "", // the endpoint
        type : "POST", // http method
        data : {
            role: function(){
                var buttons=$('input[name=role]');
                for(var i=0; i<buttons.length; i++){
                    if(buttons[i].checked){
                        return $(buttons[i]).val()
                    }
                }
                return null;
            },
            first_name: $('#first_name').val(),
            last_name: $('#last_name').val(),
            email: $('#email').val(),
            password: $('#password').val(),
            password_confirm: $('#password_confirm').val(),
            phone: $('#phone').val(),
            hospital: $('#hospital').val()

        }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            if(json.valid){
                window.location='/users/staff_confirmed/';
            }
            else{
                var form_errors=json.form_errors;
                var html_string="";
                for(var a in form_errors){
                    html_string=html_string+"<div class='alert alert-danger'>" +
                        "<div class='margin-left'><p class='error-message'>Error: "+ a+
                        ": "+form_errors[a]+"</p></div></div>"
                }
                $('#error_messages').html(html_string)

            }

        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //will never happen
        }
    });
}