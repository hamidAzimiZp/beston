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
