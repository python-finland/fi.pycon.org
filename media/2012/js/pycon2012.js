$(document).ready(function(){
    // init parallax        
    $('#target').parallax(
        {triggerExposesEdges: true}, 
        {xtravel:0.2, ytravel:0.2}, 
        {xtravel:0.6, ytravel:0.6}
    );

    // navigation
    $('a[href^="#"]').click(function(e) {
        var ref = this.hash;
            target = $(ref);

        // track with Google Analytics
        if (typeof(_gaq) !== "undefined") {
            _gaq.push(['_trackEvent', 'Navigation', ref.slice(1)]);
        }

        $('.content').fadeOut();
        $('body > header a.active').removeClass('active');
        $('body > header a[href="'+ref+'"]').addClass('active');

        if (ref !== '#sponsors') {
            target.fadeIn();    
        } else {
            $('html,body').animate({scrollTop: target.offset().top}, 500);
        }
        
        e.stopPropagation();
        return false;
    });

    // hide content if click outside
    $(document).click(function(e) {
        var clickTarget = $(e.target);
        
        if (!clickTarget.closest('.content').get(0)) {
            $('.content').fadeOut();
            $('body > header a.active').removeClass('active');
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
                    .attr('disabled', true)
                    .removeClass('error');
                $('#errorcontainer').hide();
            },
            success: function(data, textStatus, xhr) {
                if(data.ok) {
                    // Reset the form
                    self.reset();
                    $('.input-wrapper input').keyup();

                    // Show a thankyou message and bring it to view
                    $('#thankyou').show();
                    $('html, body').animate({
                        scrollTop: $('#thankyou').offset().top - 115
                    }, 500);
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
                }
            },
            error: function() {
                alert("Something went wrong! Try again!");
            },
            always: function() {
                $(self).find('input, select').attr('disabled', false);
            }
        });
    });

});