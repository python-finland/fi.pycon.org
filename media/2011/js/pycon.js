(function() {
    var canvas, context,
        stars = [],
        prevScroll = 0,
        justClicked = false;

    var starOpts = {
        // width, height, lineWidth, scrollRatio
        tiny: [2, 2, 4, 0.1],
        small: [10, 10, 2, 0.2],
        medium: [20, 20, 3, 0.4],
        large: [30, 30, 4, 0.7]
    };

    var randInt = function(a, b) {
        return Math.floor(a + Math.random() * (b - a + 1));
    };

    var choose = function(seq) {
        return seq[randInt(0, seq.length - 1)];
    };

    var init = function() {
        // XXX: All stars, especially those with smaller scroll
        // ratios, will never be visible
        var width = $(document).width(),
            height = $(document).height(),
            starCount = randInt(60, 90),
            sizes = [
                // Skewed to get more small stars
                'tiny', 'tiny', 'tiny', 'tiny',
                'small', 'small',
                'medium', 'medium',
                'large'
            ],
            colors = ['#5ff', '#5f5', '#ff5', '#f5f'];

        for(var i = 0; i < starCount; i++) {
            stars.push({
                size: choose(sizes),
                color: choose(colors),
                x: randInt(0, width),
                y: randInt(400, height)
            });
        }

        // Sot to draw from small to big (back to front)
        var order = ['tiny', 'small', 'medium', 'large'];
        stars.sort(function(a, b) {
            var ai = order.indexOf(a.size),
                bi = order.indexOf(b.size);

            return ai < bi ? -1 : ai == bi ? 0 : 1;
        });
    };

    var setup = function() {
        // XXX: If the page is loaded in a small browser window which
        // is then grown, there will be a starless area in the right
        // edge
        canvas.width = $(window).width();
        canvas.height = $(window).height();
        draw();
    };

    var drawStar = function(star) {
        var opts = starOpts[star.size],
            width = opts[0],
            height = opts[1],
            lineWidth = opts[2];

        if(star.x < -30 || star.x > canvas.width + 30 ||
           star.y < -30 || star.y > canvas.height + 30) {
            // Not visible
            return;
        }

        context.strokeStyle = star.color;
        context.lineWidth = lineWidth;

        context.beginPath();
        context.moveTo(star.x - width/2, star.y - height/2);
        context.lineTo(star.x + width/2, star.y + width/2);
        context.stroke();

        context.beginPath();
        context.moveTo(star.x + width/2, star.y - height/2);
        context.lineTo(star.x - width/2, star.y + height/2);
        context.stroke();
    };

    var draw = function() {
        // Clear canvas
        canvas.width = canvas.width;

        for(var i = 0; i < stars.length; i++)
            drawStar(stars[i]);
    };

    var scroll = function() {
        var current = $(window).scrollTop(),
            diff = current - prevScroll;

        if(justClicked && Math.abs(diff) > 30) {
            // Prevent star flickering when a link is clicked by
            // ignoring the first (bogus) scroll events
            return;
        }

        justClicked = false;
        prevScroll = current;

        for(var i = 0; i < stars.length; i++) {
            var star = stars[i];
            var scrollRatio = starOpts[star.size][3];

            star.y -= diff * scrollRatio;
        }

        draw();
    };

    $(function() {
        canvas = document.createElement('canvas');
        if(canvas.getContext) {
            $(canvas)
                .css('position', 'fixed')
                .css('left', 0)
                .css('top', 0)
                .css('z-index', -1);

            context = canvas.getContext('2d');
            $('body').append(canvas);

            init();
            setup();
            $(window).resize(setup).scroll(scroll);
        }

        $('body > header a').click(function(e) {
            var target = $(this.hash);
            _gaq.push(['_trackEvent', 'Navigation', this.hash.slice(1)]);
            $('body > header a.focus').removeClass('focus');
            if (target.length) {
                var offset = target.offset().top;
                $('html,body').animate({scrollTop: offset}, 1000);
                $(this).addClass('focus');
            }
            e.stopPropagation();
            justClicked = true;
        });
    });
})();
