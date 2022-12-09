$(document).ready(function() {
    $("#gototop").hide()
    $(window).scroll(function() {
      if ($(this).scrollTop() >= 500)
        $("#gototop").slideDown("3000")
      else
        $("#gototop").slideUp("3000")
    })
    $("#gototop").click(function() {
        $("html, body").animate({
          scrollTop: 0
        },1000);
    })
  })