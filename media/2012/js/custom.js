$(document).ready(function(){
            
    $('#target').parallax(
        {triggerExposesEdges: true}, 
        {xtravel:0.2, ytravel:0.2}, 
        {xtravel:0.6, ytravel:0.6}
    );
 
    $('a[href="#one"]').click(function() {
        var ref=$(this).attr("href");
        
        $('#target').trigger("parallax", [ref]);
        return false;
    });
    
    $('.quarter').mouseover(function() {
        $(this).children(".content").show();
    });
    
    $('.quarter').mouseout(function() {
        $(this).children(".content").hide();
    });
    
    logo_horizontal = $(window).width()/2-100;
    logo_vertical = $(window).height()/2-100; 
    
    //$('#logo').css({
    //  left: logo_horizontal + "px",
    //  right: logo_horizontal + "px",
    //  top: logo_vertical - 60 + "px",
    //  bottom: logo_vertical + "px",
    //})
});