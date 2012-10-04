var App = {

    initialize: function() {

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
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
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });


        //If Backbone sync gets an unauthorized header, it means the user's
        //session has expired, so send them back to the homepage
        var sync = Backbone.sync;
        Backbone.sync = function(method, model, options) {
            options.error = function(xhr, ajaxOptions, thrownError) {
                if (xhr.status == 401) {
                    window.location = '/';
                }
            };
            sync(method, model, options);
        };

        this.router = new BookmarklyRouter();
        Backbone.history.start({pushState: true});

        var self = this;
        $(window).resize(function() {
            self.resizeHeader();
        });
        this.resizeHeader();

    },

    resizeHeader: function() {
        setTimeout(function() {
            var el = $('#app div:first');
            if (el && el.offset()) {
                var left = el.offset().left;
                if (left > 132) left = 132;
                if (left < 20) left = 20;
                $('#redbar .wrap').css('margin-left', left + 'px');
                $('#redbar .wrap').css('margin-right', (left + 20) + 'px');
            }
        }, 1000);
    }

};
