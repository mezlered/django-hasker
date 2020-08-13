$(document).ready(function() {
    // CSRF code
       function getCookie(name) {
           var cookieValue = null;
           var i = 0;
           if (document.cookie && document.cookie !== '') {
               var cookies = document.cookie.split(';');
               for (i; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) === (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       var csrftoken = getCookie('csrftoken');
   
       function csrfSafeMethod(method) {
           // these HTTP methods do not require CSRF protection
           return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
       }
       $.ajaxSetup({
           crossDomain: false, // obviates need for sameOrigin test
           beforeSend: function(xhr, settings) {
               if (!csrfSafeMethod(settings.type)) {
                   xhr.setRequestHeader("X-CSRFToken", csrftoken);
               }
           }
       });

    $(".approve-answ").click(function (){
        var url = $(this).data("url"),
        container = $(this);

        $.ajax({
            type: "POST",
            url: url,
            data: {},
            dataType: "json",
            cache: false,

            success: function(data){
                if (data["is_accepted"]){
                    $(".approve-answ").removeClass("is_accepted-mark");
                    container.addClass("is_accepted-mark");
                } else {
                    $(".approve-answ").removeClass("is_accepted-mark");
                }
            }
        });
    });

    $(".rating--UP-DOWN").click(function (){
        var value = $(this).data("value"),
        container = $(this).parents(".votes"),
        target_id = $(this).parents(".votes").data("target"),
        url = $(this).parents(".votes").data("url");
        console.log(value, target_id);

        $.ajax({
            type: "POST",
            url: url,
            data: {
                value: value,
                target_id: target_id,
            },
            dataType: "json",
            cache: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function(data){
                console.log(data);
                container.find("span").html(data["rating"]);
            },
            error: function(xhr, status) {
                console.log(status, xhr["status"])
                if (status == "error" && xhr["status"] == 403) {
                    console.log("You don't have appropriate permissions!");
                } else {
                    console.log("Sorry, something went wrong!");
                }
            }
        });
    });
});

//Show photo file name
$('input[type="file"]').change(function(e){
    var fileName = e.target.files[0].name;
    $('.custom-file-label').html(fileName);
});
