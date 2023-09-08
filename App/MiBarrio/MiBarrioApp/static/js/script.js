// jQuery code
$(document).ready(function () {
  $("#toggleSidebar").click(function (e) {
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
document.addEventListener('DOMContentLoaded', function () {

  console.log("JS part of the script loaded!"); // a check if script has loaded correctly!

  //code for editSaveBtn
  const editSaveBtn = document.getElementById('editSaveBtn');
  if (editSaveBtn) {
    editSaveBtn.addEventListener('click', function () {
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
  }

  // code for cancelBtn
  const cancelBtn = document.getElementById('cancelBtn');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', function () {
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
    saveProfileBtn.addEventListener('click', function (event) {

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

        // Update the hidden input value if editing
        const editingSpId = document.getElementById('editingSpId').value;
        if (editingSpId) {
          // Perform any additional actions for editing

        }
        document.getElementById('hiddenSearchProfileSubmitBtn').click();
      }
    });
  }

  //handles the population of the form for search profile for the user to edit
  document.querySelectorAll('.edit-btn').forEach((button) => {
    button.addEventListener('click', function () {
      const spId = this.getAttribute('data-id');
      const spName = this.getAttribute('data-sp_name');
      const age = this.getAttribute('data-age');
      const social_cultural_tags = this.getAttribute('data-social_cultural_tags');
      const health_wellness_tags = this.getAttribute('data-health_wellness_tags');
      const leisure_recreation_tags = this.getAttribute('data-leisure_recreation_tags');
      const community_services_tags = this.getAttribute('data-community_services_tags');
      const social_cultural_levels = this.getAttribute('data-social_cultural_levels');
      const health_wellness_levels = this.getAttribute('data-health_wellness_levels');
      const leisure_recreation_levels = this.getAttribute('data-leisure_recreation_levels');
      const community_services_levels = this.getAttribute('data-community_services_levels');
      const transportation_active = this.getAttribute('data-transportation_active');
      const transportation_public = this.getAttribute('data-transportation_public');
      const backup_power_supply = this.getAttribute('data-backup_power_supply');
      const backup_water_supply = this.getAttribute('data-backup_water_supply');

      // Populate the form fields
      document.getElementById('sp_name').value = spName;
      document.getElementById('age').value = age;

      // Populate checkboxes for Social & Cultural tags
      let socialTags = JSON.parse(social_cultural_tags);  // Parse JSON string to array
      socialTags.forEach(tag => {
        let checkbox = document.querySelector(`input[name='social_cultural[]'][value='${tag}']`);
        if (checkbox) checkbox.checked = true;
      });

      // Populate checkboxes for Health & Wellness tags
      let healthTags = JSON.parse(health_wellness_tags);
      healthTags.forEach(tag => {
        let checkbox = document.querySelector(`input[name='health_wellness[]'][value='${tag}']`);
        if (checkbox) checkbox.checked = true;
      });

      // Populate checkboxes for Leisure & Recreation tags
      let leisureTags = JSON.parse(leisure_recreation_tags);
      leisureTags.forEach(tag => {
        let checkbox = document.querySelector(`input[name='leisure_recreation[]'][value='${tag}']`);
        if (checkbox) checkbox.checked = true;
      });

      // Populate checkboxes for Health & Wellness tags
      let communityTags = JSON.parse(community_services_tags);
      communityTags.forEach(tag => {
        let checkbox = document.querySelector(`input[name='community_services[]'][value='${tag}']`);
        if (checkbox) checkbox.checked = true;
      });

      // Populate radio button for Social & Cultural Levels
      let socialLevel = document.querySelector(`input[name='socialLikert'][value='${social_cultural_levels}']`);
      if (socialLevel) socialLevel.checked = true;

      // Populate radio button for Health & Wellness Levels
      let healthLevel = document.querySelector(`input[name='healthLikert'][value='${health_wellness_levels}']`);
      if (healthLevel) healthLevel.checked = true;

      // Populate radio button for Health & Wellness Levels
      let leisureLevel = document.querySelector(`input[name='leisureLikert'][value='${leisure_recreation_levels}']`);
      if (leisureLevel) leisureLevel.checked = true;

      // Populate radio button for Health & Wellness Levels
      let communityLevel = document.querySelector(`input[name='communityLikert'][value='${community_services_levels}']`);
      if (communityLevel) communityLevel.checked = true;

      // Populate checkboxes for Active and Public Transportation
      if (transportation_active === 'True') {
        document.getElementById('activeTransportation').checked = true;
      }

      if (transportation_public === 'True') {
        document.getElementById('publicTransportation').checked = true;
      }

      // Populate checkboxes for Back-up Power Supply and Water Supply
      if (backup_power_supply === 'True') {
        document.getElementById('backup_power_supply').checked = true;
      }
      if (backup_water_supply === 'True') {
        document.getElementById('backup_water_supply').checked = true;
      }

      // Update form action to handle editing
      const editingSpIdInput = document.getElementById('editingSpId');
      editingSpIdInput.value = spId;

    });
  });

  // Reset the form and hidden field when the modal is closed
  $('#createProfileModal').on('hidden.bs.modal', function () {
    document.getElementById('searchProfileForm').reset();
    document.getElementById('editingSpId').value = '';
  });

  // Code that applies to newSearch.html
  var cityMapElement = document.getElementById('cityMap');
  if (cityMapElement) {
    // Initialize the map with South Africa as default location
    var map = L.map('cityMap').setView([-30.5595, 22.9375], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    // ... existing code for newSearch.html
  }

  //populates the form every time a user selects a different searchProfile
  const searchProfileSelect = document.getElementById('searchProfileSelect');
  if (searchProfileSelect) {
    // Debugging Line: Log the selected option at the beginning
    console.log("Initially selected option:", searchProfileSelect.value);
    searchProfileSelect.addEventListener('change', () => {
      // Debugging Line: Log the selected option when it changes
      console.log("Selected option has been changed to:", searchProfileSelect.value);
      document.getElementById('searchProfileForm').submit();
    });
  }

  // Define function to set checkboxes as checked based on provided tag list
  function setCheckedCheckboxes(tagList, name) {
    tagList.forEach(function (tag) {
      const checkboxElement = document.querySelector(`input[name="${name}[]"][value="${tag}"]`);
      if (checkboxElement) {
        checkboxElement.checked = true;
      }
    });
  }

  const selectedProfileElement = document.getElementById("selectedProfileData");
  const rawData = selectedProfileElement.getAttribute('data-selected-profile');
  const cleanedData = decodeURIComponent(JSON.parse('"' + rawData.replace(/"/g, '\\"') + '"'));
  console.log("Data attribute: ", selectedProfileElement.getAttribute('data-selected-profile'));
  const selectedProfileData = JSON.parse(cleanedData);

  //const selectedProfileData = JSON.parse(selectedProfileElement.getAttribute('data-selected-profile'));
  if (searchProfileSelect && selectedProfileData) {
    searchProfileSelect.value = selectedProfileData.search_profileID;
  }

  // Check appropriate checkboxes
  setCheckedCheckboxes(selectedProfileData.social_cultural_tags, "social_cultural");
  setCheckedCheckboxes(selectedProfileData.health_wellness_tags, "health_wellness");
  setCheckedCheckboxes(selectedProfileData.leisure_recreation_tags, "leisure_recreation");
  setCheckedCheckboxes(selectedProfileData.community_services_tags, "community_services");

  // Add these lines to populate the age dropdown
  const ageSelect = document.getElementById("age");
  if (ageSelect && selectedProfileData.age) {
    ageSelect.value = selectedProfileData.age;
  }

  // Function to set the selected radio button for Likert scale
  function setLikertScaleValue(name, value) {
    const inputElement = document.querySelector(`input[name="${name}"][value="${value}"]`);
    if (inputElement) {
      inputElement.checked = true;
    }
  }

  // Add these lines to populate the Likert scale radio buttons
  setLikertScaleValue('socialLikert', selectedProfileData.social_cultural_levels);
  setLikertScaleValue('healthLikert', selectedProfileData.health_wellness_levels);
  setLikertScaleValue('leisureLikert', selectedProfileData.leisure_recreation_levels);
  setLikertScaleValue('communityLikert', selectedProfileData.community_services_levels);

  // Add these lines to populate the checkboxes for Transportation Preference
  const activeTransportCheckbox = document.getElementById("activeTransportation");
  const publicTransportCheckbox = document.getElementById("publicTransportation");

  if (activeTransportCheckbox && selectedProfileData.transportation_active) {
    activeTransportCheckbox.checked = true;
  }

  if (publicTransportCheckbox && selectedProfileData.transportation_public) {
    publicTransportCheckbox.checked = true;
  }


});
