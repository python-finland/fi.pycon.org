$(document).ready(function(){

    // navigation
    $('a[href^="#"]').click(function(e) {
        var ref = this.hash;
            target = $(ref);

        // We hit modal dialog trigger
        if($(this).attr("data-toggle") == "modal") {
            // Let bootstrap take over
            return true;
        }

        // track with Google Analytics
        if (typeof(_gaq) !== "undefined") {
            _gaq.push(['_trackEvent', 'Navigation', ref.slice(1)]);
        }

        $('.quarter').attr('style', '');
        $('.content').attr('style', '');
        $('.content').fadeOut();
        $('body > header a.active').removeClass('active');
        $('body > header a[href="'+ref+'"]').addClass('active');

        if (ref !== '#sponsors') {
            // calculate height and render css accordingly
            if (target.height() > (($(window).height()-120)/2)) {
                target.css({'overflow-y':'scroll', 'height':'100%'});
            } else {
                target.css('height', '100%');
            }
            // fade content in
            target.fadeIn();
        } else {
            $('html,body').animate({scrollTop: target.offset().top}, 500);
        }

        try {
            // http://stackoverflow.com/questions/4715073/window-location-hash-prevent-scrolling-to-the-top
            e.preventDefault();
            window.location.hash = ref;
            $(window).scrollTop(0);
        } catch(e) {
        }

        e.stopPropagation();
        return false;
    });

    // hide content if click outside
    $(document).click(function(e) {
        var clickTarget = $(e.target);

        if (!clickTarget.closest('.content').get(0)) {
            $('.quarter').attr('style', '');
            $('.content').attr('style', '');
            $('.content').fadeOut();
            $('body > header a.active').removeClass('active');
            window.location.hash = '';
        }
    });

    var update_price = function() {
        var prices = {
            'corporate': 125,
            'normal': 50,
            'student': 10
        };
        var price = prices[$('#id_ticket_type').val()] +
            ($('#id_snailmail_bill').is(':checked') ? 5 : 0);

        $('#registration form span.price').html(price + ' &euro;');
    };

    $('#id_ticket_type').change(function() {
        var val = $(this).val(),
            is_corporate = (val == 'corporate'),
            is_normal = (val == 'normal');
        $('#dinner-disclaimer').toggle(is_corporate || is_normal);
        $('#id_dinner').attr('checked', is_corporate || is_normal);
        $('#companywrapper').toggle(is_corporate);
        update_price();
    });

    $('#id_snailmail_bill').change(function() {
        $('#billing-details').toggle($(this).is(':checked'));
        update_price();
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

    // Handle modals
    $

    // See if we have a fragment and scroll there
    function init() {
        var frag = window.location.hash;
        if(frag) {
            $("a[href=" + frag + "]").first().click();
        }
    }

    init();
});