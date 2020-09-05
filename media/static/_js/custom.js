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