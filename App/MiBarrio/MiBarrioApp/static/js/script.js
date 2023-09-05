// jQuery code
$(document).ready(function() {
  $("#toggleSidebar").click(function(e) {
    e.preventDefault();
    $("#sidebar").toggleClass("collapsed");

    // Used Bootstrap 5 utility classes for toggling visibility
    if ($("#sidebar").hasClass("collapsed")) {
      $(".nav-text").addClass("d-none");
    } else {
      $(".nav-text").removeClass("d-none");
    }
  });

  console.log("jQuery part of the script loaded!"); // a check if script has loaded correctly!
});

// JavaScript Code
document.addEventListener('DOMContentLoaded', function() {

  console.log("JS part of the script loaded!"); // a check if script has loaded correctly!

  //code for editSaveBtn
  const editSaveBtn = document.getElementById('editSaveBtn');
  if (editSaveBtn) {
    editSaveBtn.addEventListener('click', function() {
      if (this.innerText === 'Edit') {
        this.innerText = 'Save';
        document.getElementById('cancelBtn').classList.remove('disabled');
        document.querySelectorAll('#accountDetailsForm input:not(#username):not(#password)').forEach(input => {
          input.disabled = false;
        });
      } else {
        document.getElementById('hiddenSubmitBtn').click();
      }
    });
  } else {
    console.error("Element with id='editSaveBtn' not found.");
  }

  // code for cancelBtn
  const cancelBtn = document.getElementById('cancelBtn');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', function() {
      document.getElementById('editSaveBtn').innerText = 'Edit';
      this.classList.add('disabled');
      document.querySelectorAll('#accountDetailsForm input:not(#username):not(#password)').forEach(input => {
          input.disabled = true;
      });
    });
  }

  // code for saveProfileBtn
  const saveProfileBtn = document.getElementById('saveProfileBtn');
  if (saveProfileBtn) {
    saveProfileBtn.addEventListener('click', function(event) {

      console.log("Save button clicked"); // Debugging line

      let spName = document.getElementById('sp_name').value;
      let age = document.getElementById('age').value;

      let socialCulturalLevel = document.querySelector('input[name="socialLikert"]:checked');
      let healthWellnessLevel = document.querySelector('input[name="healthLikert"]:checked');
      let leisureRecreationLevel = document.querySelector('input[name="leisureLikert"]:checked');
      let communityServicesLevel = document.querySelector('input[name="communityLikert"]:checked');

      let socialCulturalTags = document.querySelectorAll('input[name="social_cultural[]"]:checked');
      let healthWellnessTags = document.querySelectorAll('input[name="health_wellness[]"]:checked');
      let leisureRecreationTags = document.querySelectorAll('input[name="leisure_recreation[]"]:checked');
      let communityServicesTags = document.querySelectorAll('input[name="community_services[]"]:checked');

      let missingFields = [];

      if (!spName) missingFields.push("Profile Name");
      if (!age) missingFields.push("Age");

      if (!socialCulturalLevel) missingFields.push("Social & Cultural Level");
      if (!healthWellnessLevel) missingFields.push("Health & Wellness Level");
      if (!leisureRecreationLevel) missingFields.push("Leisure & Recreation Level");
      if (!communityServicesLevel) missingFields.push("Community & Services Level");

      if (socialCulturalTags.length === 0) missingFields.push("Social & Cultural Tags");
      if (healthWellnessTags.length === 0) missingFields.push("Health & Wellness Tags");
      if (leisureRecreationTags.length === 0) missingFields.push("Leisure & Recreation Tags");
      if (communityServicesTags.length === 0) missingFields.push("Community & Services Tags");

      if (missingFields.length > 0) {
          alert('Please complete the following mandatory fields: ' + missingFields.join(", "));
          event.preventDefault();
      } else {
        document.getElementById('hiddenSearchProfileSubmitBtn').click();
      }
    });
  }

});
