// for alert boxes
$(".close").on("click", function(){
    $(this).parent().fadeOut(1000)
})

// open and close navigation menu for small devices

$(".navButton").on("click", ()=>{
    $(".my_nav2").toggleClass("show_nav")
})

// close when click on body
$(".wrapper").on("click", function(){
    $(".my_nav2").removeClass("show_nav")
})

// run slider
$('#slider1').zpSlider({
    speed : "2000"
});

//add active class to newsSlider
if (!$(".for_get_first").hasClass("active")){
    $(".for_get_first:first").addClass("active")
}

// add active class to newsSlider for small client
if (!$(".for_get_first_small").hasClass("active")){
    $(".for_get_first_small:first").addClass("active")
}

// smoth scroll to

$(document).ready(function(){
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();

        $('a').each(function () {
            $(this).removeClass('active');
        })
        $(this).addClass('active');

        var target = this.hash;
        $target = $(target);
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top + 2
        }, 1000, 'swing', function () {
            window.location.hash = target;
        });
    });
})