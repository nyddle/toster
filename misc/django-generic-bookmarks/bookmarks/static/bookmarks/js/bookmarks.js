(function($) {
    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
    $(document).ready(function() {
        $('.bookmarks_form').live('submit', function() {
            var form = $(this);
            // toggle labels
            form.find('.bookmarks_toggle').toggle();
            var values = {};
            form.find(':input').each(function() {
                values[this.name] = $(this).val();
            });
            // submitting form using ajax
            $.ajax({  
                type: 'POST',  
                url: form.attr('action'),  
                data: values,  
                error: function() {
                    form.find('.error').show();
                },
                success: function(data) {
                    form.trigger('bookmarked', data);    
                }
            });
            return false;
        });
    });
})(jQuery);