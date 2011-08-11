$(function() {
    $('body > header a').click(function(e) {
        var target = $(this.hash);
        $('body > header a.focus').removeClass('focus');
        if (target.length) {
            var offset = target.offset().top;
            $('html,body').animate({scrollTop: offset}, 1000);
            $(this).addClass('focus');
        }
        e.stopPropagation();
    });
});
