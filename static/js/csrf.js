//$(document).ready(function () {
//    function getCookie(name) {
//        var cookieVal = null
//        if (document.cookie && document.cookie !== '') {
//            var cookies = document.cookie.split(';')
//            for (var i=0; i<cookies.length; i++) {
//                if (cookie.substring(0, name.length+1) === (name + '=')) {
//                    cookieVal = decodeURIComponent(cookie.substring(name.length + 1))
//                    break;
//                }
//            }
//        }
//        return cookieVal
//    }
//
//    var csrfToken = getCookie('csrftoken')
//
//    function csrfSafeMethod(method) {
//        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
//    }
//
//    $.ajaxSetup({
//        beforeSend: function (xhr, settings) {
//            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                xhr.setRequestHeader('X-CSRFToken', csrfToken)
//            }
//        }
//    })
//})

$(document).ready(function() {
    function getCookie(c_name) {
        if(document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if(c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if(c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }

    $(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        });
    });
});