var mobilize = {

    // https://github.com/miohtama/plomobile
    isMobile : function() {

        // Query thru jQuery for maximum compatibility
        var color = $(document.body).css("backgroundColor");

        if(!color) {
            // The document body is missing explicit background color used to identify when mobile.css
            // kicks in
            return;
        }

        // Magic bg color set in mobile.css
        return (color.toLowerCase() == "rgb(255, 255, 254)");
    }
};


$(document).ready(function() {

    if (mobilize.isMobile()) {
        $('#content > .page').each(function() {
            var thisName = $(this).attr('id'),
                thisSubTemplate = '../2013/_' + thisName + '.html';
            $(this).load(thisSubTemplate, function() {
                if (thisName === 'registration') {
                    initialize_registration();
                }
            });
        });
    }

    function mangleHash(hash) {
        return hash.replace(/[#]/g, "");
    }

    function navigateTo(divId) {
        var target = $("#" + divId);
        
        if (typeof(_gaq) !== "undefined") { // track with Google Analytics
            _gaq.push(['_trackEvent', 'Navigation', divId]);
        }

        $('ul#menu li a.active').removeClass('active');
        $('ul#menu a[href^=#' + divId + ']').addClass('active');

        if (divId == 'sponsors') { // scroll down!
            $('html,body').animate({scrollTop: target.offset().top}, 500);
            $('ul#menu a[href$=#' + divId + ']').addClass('active');
        } else {
            // if is talk
            if (divId.indexOf('talks') === 0 && divId.length > 5) {
                var thisDiv = $('a[href=#'+divId+']');

                $('ul#menu a[href^=#talks]').addClass('active');

                if (location.hash.indexOf('talks') === 1 && thisDiv.length > 0) {
                    $(window).scrollTop(thisDiv.position().top + 120);
                } else {
                    // fade out current page
                    $('.page:visible').fadeOut();
                    $('#talks').load('../2013/_talks.html', function() {
                        $(this).fadeIn();
                        $("#content").animate({height: $(this).height() + 60}, function() {
                            $(window).scrollTop($('a[href=#'+divId+']').offset().top - 30);
                        });
                    });
                }
            } else {
                // fade out current page
                $('.page:visible').fadeOut();
                // load content from sub template
                target.load('../2013/_' + divId + '.html', function() {
                    $("#content").animate({height: target.height() + 60});
                    target.fadeIn();
                    if (divId === 'registration') {
                        initialize_registration();
                    }
                });
            }   
        }
        //location.hash = "#" + divId;
    }

    // navigation
    $('#wrapper').on('click', '#navigation a[href^="#"], a.pagelink', function(e) {

        if(mobilize.isMobile()) {
            return true;
        }

        var thisHash = mangleHash(this.hash);
        var locationHash = mangleHash(location.hash);

        if (thisHash === locationHash) {
            // if current page is same as link, do nothing.
        } else {
            try {
                // http://stackoverflow.com/questions/4715073/window-location-hash-prevent-scrolling-to-the-top
                e.preventDefault();
                location.hash = "#" + thisHash;
                $(window).scrollTop(0);
            } catch(e) {}
            // navigate to different page
            navigateTo(thisHash);
        }
        e.preventDefault();
        return false;
    });

    $('a#coc').click(function(e){
        // We hit modal dialog trigger
        if($(this).attr("data-toggle") == "modal" || $(this).attr("data-dismiss") == "modal") {
            // Let bootstrap take over
            return true;
        }
    });


    var update_price = function() {
        var prices = {
            'corporate': 125,
            'normal': 50,
            'student': 10,
            'sponsor': 0,
            'speaker': 0,
            'organizer': 0
        };
        var price = prices[$('#id_ticket_type').val()] +
            ($('#id_snailmail_bill').is(':checked') ? 5 : 0);

        $('#registration form span.price').html(price + ' &euro;');
    };

    var initialize_registration = function() {
        $('input#id_snailmail_bill').click(function(){
            if(!mobilize.isMobile()) {
                $("#content").animate({height: $('div#registration').height() + 60});
            }
        });

        $('#id_ticket_type').change(function() {
            var val = $(this).val(),
                is_corporate = (val == 'corporate'),
                is_normal = (val == 'normal')
                is_special = (val=='sponsor' || val=='speaker' || val=='organizer');
            $('#dinner-disclaimer').toggle(is_corporate || is_normal || is_special);
            $('#id_dinner').attr('checked', is_corporate || is_normal || is_special);
            $('#companywrapper').toggle(is_corporate || val=='sponsor');
            $('#papermail-disclaimer').toggle(!is_special);
            if(!mobilize.isMobile()) {
                $("#content").animate({height: $('div#registration').height() + 60});
            }
            update_price();
        });

        $('#id_snailmail_bill').change(function() {
            $('#billing-details').toggle($(this).is(':checked'));
            update_price();
        });

        $('#id_country').typeahead({
            minLength: 1,
            items: 10,
            source: function (query, process) {
                return $.get('/api/2012/country', { query: query }, function (data) {
                    return process(data);
                }, 'json');
            }
        });

        $('#registration-form').submit(function(e) {
            e.preventDefault();
            var self = this;

            $.ajax({
                url: '/api/2012/register/',
                type: 'POST',
                dataType: 'json',
                data: $(this).serialize(),
                beforeSend: function(xhr, settings) {
                    $('#thankyou').hide();
                    $(self).find('input, select')
                        .prop('disabled', true)
                        .removeClass('error');
                    $('#errorcontainer').hide();
                },
                success: function(data, textStatus, xhr) {
                    if(data.ok) {
                        // Reset the form
                        self.reset();
                        $('.input-wrapper input').keyup();
                        // Show a thankyou message
                        $('#thankyou').show();
                        $(self).hide();
                    } else {
                        var ul = $('#errorcontainer ul');
                        ul.empty();
                        $.each(data.errors, function(key, value) {
                            $('[name=' + key + ']')
                                .addClass('error');
                            $.each(value, function(index, error) {
                                var pretty = key.split('_').join(' ');
                                ul.append($('<li>').text(pretty + ': ' + error));
                            });
                        });
                        $('#errorcontainer').show();
                        if(!mobilize.isMobile()) {
                            $("#content").animate({height: $('div#registration').height() + 60});
                        }
                        $(self).find('input, select').prop('disabled', false);
                    }
                },
                error: function() {
                    alert("Something went wrong! Try again!");
                },
                always: function() {
                    $(self).find('input, select').prop('disabled', false);
                }
            });
        });
    };

    // See if we have a fragment and scroll there
    function init() {
        var frag = mangleHash(location.hash);
        //var showIndex = false;
        if(!frag) { frag = 'about'; }
        if(frag == "sponsors"){
            $("#about").fadeIn();
        }

        if(frag && !mobilize.isMobile()) {
            navigateTo(frag);
        }
    }

    init();
});