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

$(document).ready(function() {
  console.log("Script loaded!");  // a check if script has loaded correctly!
});


document.getElementById('editSaveBtn').addEventListener('click', function() {
  if (this.innerText === 'Edit') {
    this.innerText = 'Save';
    document.getElementById('cancelBtn').classList.remove('disabled');
    document.querySelectorAll('#accountDetailsForm input:not(#username):not(#password)').forEach(input => {
        input.disabled = false;
    });
} else {
  // Programmatically "click" the hidden submit button
  document.getElementById('hiddenSubmitBtn').click();
}
});

document.getElementById('cancelBtn').addEventListener('click', function() {
  document.getElementById('editSaveBtn').innerText = 'Edit';
  this.classList.add('disabled');
  document.querySelectorAll('#accountDetailsForm input:not(#username):not(#password)').forEach(input => {
      input.disabled = true;
  });
});


//mobiscroll.select('#multiple-select', {
  //inputElement: document.getElementById('my-input'),
 //touchUi: false
//});
