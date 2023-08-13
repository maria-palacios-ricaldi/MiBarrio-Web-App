//script.js//
$(document).ready(function() {
  $("#toggleSidebar").click(function(e) {
    e.preventDefault();
    $("#sidebar").toggleClass("collapsed");

    // Use Bootstrap 5 utility classes for toggling visibility
    if ($("#sidebar").hasClass("collapsed")) {
      $(".nav-text").addClass("d-none");
    } else {
      $(".nav-text").removeClass("d-none");
    }
  });
});


//toggle navbar - collapse
