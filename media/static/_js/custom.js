$(document).ready(function(){
    // gallery grid
    $('.gallery-gird').masonry();

    // for navigation menu
    $(".navigation-btn").on("click", function(){
        if($(".navWraper").css("display") == "none"){
            $(".navWraper").show(450);
            $(".navigation-btn span").attr("class", "icon-close2");
            $(".wrapper").css("display", "none");
            $(".navigation ul li").addClass("active");
        }else{
            $(".navWraper").css("display", "none");
            $(".navigation-btn span").attr("class", "icon-menu");
            $(".wrapper").css("display", "block");
            $(".navigation ul li").removeClass("active");            
        }
    })

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

$(window).on("scroll", function(){
    $(".navigation-btn").css("position", "fixed")
})

// smoth scroll
function smothScroll(Ypos){
    let step = 20

    if(Ypos < scrollY){
        step *= -1
    }
    if(Math.abs(Ypos - scrollY) <= step){
        return;
    }
    window.scrollBy(0, step)
    setTimeout(function(){
        smothScroll(Ypos)
    }, 18)
}

// manage routes

let route = {
    _routes : {},

    add : function(URL, action){
        this._routes[URL] = action
    },

    run : function(){
        jQuery.each(this._routes, function(pattern){
            if(location.href.match(pattern)){
                this()
            }
        })
    }
}

// for fix par
route.add("gallery.html", function(){
    $(document).ready(function(){
        $("#par").css({top:'-251px',position: 'absolute',left: '199px',transform: 'rotate(24deg)'})
    })
})

route.run()