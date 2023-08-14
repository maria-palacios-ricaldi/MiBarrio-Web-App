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
  console.log("Script loaded!");  // This should appear in your browser's console
  // ... rest of the code ...
});


document.getElementById('editSaveBtn').addEventListener('click', function() {
  if (this.innerText === 'Edit') {
      this.innerText = 'Save';
      document.getElementById('cancelBtn').classList.remove('disabled');
      document.querySelectorAll('#accountDetailsForm input:not(#username)').forEach(input => {
          input.disabled = false;
      });
      document.getElementById('repasswordDiv').style.display = 'block';
  } else {
      this.innerText = 'Edit';
      document.getElementById('cancelBtn').classList.add('disabled');
      document.querySelectorAll('#accountDetailsForm input:not(#username)').forEach(input => {
          input.disabled = true;
      });
      document.getElementById('repasswordDiv').style.display = 'none';
  }
});

document.getElementById('cancelBtn').addEventListener('click', function() {
  document.getElementById('editSaveBtn').innerText = 'Edit';
  this.classList.add('disabled');
  document.querySelectorAll('#accountDetailsForm input:not(#username)').forEach(input => {
      input.disabled = true;
  });
  document.getElementById('repasswordDiv').style.display = 'none';
});
