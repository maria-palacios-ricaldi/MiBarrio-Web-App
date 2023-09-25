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

var map = null;

// JavaScript Code
document.addEventListener('DOMContentLoaded', function () {

  console.log("JS part of the script loaded!"); // a check if script has loaded correctly!

  if (window.location.pathname.endsWith('profile')) {

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

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })

  }

  if (window.location.pathname.endsWith('newSearch')) {
    // Code that applies to newSearch.html
    initializeMap();

    // Listen for changes in the dropdown to switch profiles
    const searchProfileSelect = document.getElementById('searchProfileSelect');
    if (searchProfileSelect) {
      console.log("searchProfileSelect listener added");  // Debugging Line
      searchProfileSelect.addEventListener('change', () => {
        console.log("searchProfileSelect changed");  // Debugging Line
        document.getElementById('action_type').value = 'profile_change';
        console.log("Setting action_type to 'profile_change'");  // Debugging Line
        document.getElementById('searchProfileForm').submit();
      });
    }

    // Extract selected profile data
    const selectedProfileElement = document.getElementById("selectedProfileData");
    const rawData = selectedProfileElement.getAttribute('data-selected-profile');
    const cleanedData = decodeURIComponent(JSON.parse('"' + rawData.replace(/"/g, '\\"') + '"'));
    const selectedProfileData = JSON.parse(cleanedData);

    // Store selectedProfileData in session storage
    sessionStorage.setItem("selectedProfileData", JSON.stringify(selectedProfileData));

    //const selectedProfileData = JSON.parse(selectedProfileElement.getAttribute('data-selected-profile'));
    if (searchProfileSelect && selectedProfileData) {
      searchProfileSelect.value = selectedProfileData.search_profileID;
    }

    document.getElementById('searchProfileSelect').addEventListener('change', function () {
      var selectedOption = this.options[this.selectedIndex];
      var selectedProfileName = selectedOption.text;
      document.getElementById('profile-name-cell').innerText = selectedProfileName;
      sessionStorage.setItem('selectedProfileName', selectedProfileName);  // Store selected profile name
    });


    function populateTables(selectedProfileData) {
      document.getElementById("social_cultural_level").textContent = selectedProfileData.social_cultural_levels;
      document.getElementById("social_cultural_tags").textContent = selectedProfileData.social_cultural_tags.join(", ");
      document.getElementById("health_wellness_level").textContent = selectedProfileData.health_wellness_levels;
      document.getElementById("health_wellness_tags").textContent = selectedProfileData.health_wellness_tags.join(", ");
      document.getElementById("leisure_recreation_level").textContent = selectedProfileData.leisure_recreation_levels;
      document.getElementById("leisure_recreation_tags").textContent = selectedProfileData.leisure_recreation_tags.join(", ");
      document.getElementById("community_services_level").textContent = selectedProfileData.community_services_levels;
      document.getElementById("community_services_tags").textContent = selectedProfileData.community_services_tags.join(", ");

      document.getElementById("public_transport").textContent = selectedProfileData.transportation_public ? "Selected" : "Not Selected";
      document.getElementById("active_transport").textContent = selectedProfileData.transportation_active ? "Selected" : "Not Selected";
    }

    populateTables(selectedProfileData);
    updateProfileNameCell();

    document.getElementById("nextStepBtn").addEventListener("click", function () {
      // Save the necessary data to session storage
      const selectedProfileId = $('#searchProfileSelect').val();

      sessionStorage.setItem("selectedProfileId", selectedProfileId);
      sessionStorage.setItem("nearestSuburbsData", JSON.stringify(nearestSuburbsData));

      // Navigate to newSearch2.html
      window.location.href = "newSearch2.html";
    });
  }

  if (window.location.pathname.endsWith('viewPastSearches')) {

    document.getElementById("toggleOrder").addEventListener("click", function () {
      var table = document.querySelector("table tbody");
      var rows = Array.from(table.rows);
      table.append(...rows.reverse());
    });

  }

  if (window.location.pathname.endsWith('newSearch2')) {

    initializeMap();
    // Code below refers to newSearch2.html
    const selectedProfileId = sessionStorage.getItem("selectedProfileId");
    const nearestSuburbsData = JSON.parse(sessionStorage.getItem("nearestSuburbsData"));

    updateMapWithNewData(nearestSuburbsData);


    console.log('Nearest Suburbs Data:', nearestSuburbsData);
    console.log('Is it an array?', Array.isArray(nearestSuburbsData));
    if (nearestSuburbsData && nearestSuburbsData.length > 0) {
      console.log('First element:', nearestSuburbsData[0]);
      console.log('Does the first element have a suburb__name?', 'suburb__name' in nearestSuburbsData[0]);
    }

    // Populate suburb dropdown based on nearest suburbs data
    const suburbSelect = document.getElementById("suburbSelect");
    suburbSelect.innerHTML = ""; // Clear existing options
    if (nearestSuburbsData) {
      nearestSuburbsData.slice(0, 5).forEach((suburb, index) => {
        const option = document.createElement("option");
        option.value = suburb.suburb__name;
        option.text = suburb.suburb__name;
        suburbSelect.add(option);
      });
    }

    // Retrieve selectedProfileData from session storage
    const selectedProfile = JSON.parse(sessionStorage.getItem("selectedProfileData"));

    // Update checkboxes based on selected profile
    if (selectedProfile) {
      document.getElementById("powerSupply").checked = selectedProfile.backup_power_supply;
      document.getElementById("waterSupply").checked = selectedProfile.backup_water_supply;
    }

    // Rent and Buy options
    const rentOptions = [
      { value: "", text: "Any" },
      { value: 1000, text: "R1000" },
      { value: 1500, text: "R1500" },
      { value: 2000, text: "R2000" },
      { value: 2500, text: "R2500" },
      { value: 3500, text: "R3500" },
      { value: 4000, text: "R4000" },
      { value: 4500, text: "R4500" },
      { value: 5000, text: "R5000" },
      { value: 6000, text: "R6000" },
      { value: 7000, text: "R7000" },
      { value: 8000, text: "R8000" },
      { value: 9000, text: "R9000" },
      { value: 10000, text: "R10000" },
      { value: 11000, text: "R11000" },
      { value: 12000, text: "R12000" },
      { value: 13000, text: "R13000" },
      { value: 14000, text: "R14000" },
      { value: 15000, text: "R15000" },
      { value: 16000, text: "R16000" },
      { value: 17000, text: "R17000" },
      { value: 18000, text: "R18000" },
      { value: 19000, text: "R19000" },
      { value: 20000, text: "R20000" },
      { value: 25000, text: "R25000" },
      { value: 30000, text: "R30000" },
      { value: 35000, text: "R35000" },
      { value: 40000, text: "R40000" },
      { value: 50000, text: "R50000" },
      { value: 60000, text: "R60000" },
      { value: 70000, text: "R70000" },
      { value: 80000, text: "R80000" },
    ];

    const buyOptions = [
      { value: "", text: "Any" },
      { value: 100000, text: "R100000" },
      { value: 150000, text: "R150000" },
      { value: 200000, text: "R200000" },
      { value: 250000, text: "R250000" },
      { value: 300000, text: "R300000" },
      { value: 350000, text: "R350000" },
      { value: 400000, text: "R400000" },
      { value: 450000, text: "R450000" },
      { value: 500000, text: "R500000" },
      { value: 600000, text: "R600000" },
      { value: 700000, text: "R700000" },
      { value: 800000, text: "R800000" },
      { value: 900000, text: "R900000" },
      { value: 1000000, text: "R1000000" },
      { value: 1250000, text: "R1250000" },
      { value: 1500000, text: "R1500000" },
      { value: 2000000, text: "R2000000" },
      { value: 2500000, text: "R2500000" },
      { value: 3000000, text: "R3000000" },
      { value: 3500000, text: "R3500000" },
      { value: 4000000, text: "R4000000" },
      { value: 4500000, text: "R4500000" },
      { value: 5000000, text: "R5000000" },
      { value: 6000000, text: "R6000000" },
      { value: 7000000, text: "R7000000" },
      { value: 8000000, text: "R8000000" },
      { value: 9000000, text: "R9000000" },
      { value: 10000000, text: "R10000000" },
      { value: 15000000, text: "R15000000" },
    ];

    // Function to populate options
    function populateOptions(selectElement, optionsArray) {
      // Clear existing options
      selectElement.innerHTML = '';

      // Populate new options
      optionsArray.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option.value;
        opt.textContent = option.text;
        selectElement.appendChild(opt);
      });
    }

    // Event listener for radio buttons
    document.querySelectorAll('input[name="type"]').forEach(radio => {
      radio.addEventListener('change', function () {
        const minPrice = document.getElementById('min-price');
        const maxPrice = document.getElementById('max-price');

        if (this.value === 'rent') {
          populateOptions(minPrice, rentOptions);
          populateOptions(maxPrice, rentOptions);
        } else if (this.value === 'buy') {
          populateOptions(minPrice, buyOptions);
          populateOptions(maxPrice, buyOptions);
        }
      });
    });

  }

});

function setSearchActionType() {
  console.log("Inside setSearchActionType function");  // Debugging Line
  document.getElementById('action_type').value = 'search';
  console.log("Setting action_type to 'search'");  // Debugging Line
  if (map) {
    map.setView([-33.9249, 18.4241], 10);  // 10 is the zoom level, you can adjust this
    console.log("Map changed to CPT");  // Debugging Line

    // Update local storage with the new state
    const mapState = {
      lat: -33.9249,
      lng: 18.4241,
      zoom: 10
    };
    localStorage.setItem('mapState', JSON.stringify(mapState));
  }

}

async function getCrimeData(suburbName) {
  let crimeRate = null;
  try {
    const response = await fetch(`/get_crime_data/${suburbName}/`);
    const data = await response.json();
    crimeRate = data.crime_rate;
  } catch (error) {
    console.log("An error occurred:", error);
  }
  return crimeRate;
}

async function updateTableWithNewData(nearestSuburbsData) {
  const table = document.getElementById("suburbTable");
  table.innerHTML = "";

  for (let i = 0; i < 5 && i < nearestSuburbsData.length; i++) {
    const suburb = nearestSuburbsData[i];
    const row = table.insertRow();
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);
    const cell3 = row.insertCell(2);

    cell1.innerHTML = i + 1;
    cell2.innerHTML = suburb.suburb__name;
    const crimeRate = await getCrimeData(suburb.suburb__name);
    cell3.innerHTML = crimeRate !== null ? crimeRate : "Data not available";
  }
}

let nearestSuburbsData = [];

async function getNearestSuburbs() {
  const selectedProfileId = $('#searchProfileSelect').val();

  try {
    const response = await $.ajax({
      type: 'POST',
      url: '/get_nearest_suburbs/',
      data: {
        'selected_profile_id': selectedProfileId,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }
    });
    nearestSuburbsData = response.nearest_suburbs;  // Assuming the server returns a key called 'nearest_suburbs'
    console.log("Updated Nearest Suburbs Data:", nearestSuburbsData); // Debugging Line
    updateMapWithNewData(nearestSuburbsData);
  } catch (error) {
    console.error('Error:', error);
  }
}

async function updateMapWithNewData(nearestSuburbsData) {
  console.log('Raw Data:', nearestSuburbsData);

  clearExistingLayers();
  setDefaultMapView();

  nearestSuburbsData.forEach((suburb, index) => {
    const coordinates = parseSuburbCoordinates(suburb.suburb__coordinates);
    const name = suburb.suburb__name;

    if (!coordinates) {
      return;
    }

    drawPolygon(coordinates);
    placeMarker(coordinates, name);
  });

  await updateTableWithNewData(nearestSuburbsData);
}

function clearExistingLayers() {
  markers.forEach(marker => map.removeLayer(marker));
  polygons.forEach(polygon => map.removeLayer(polygon));
  markers = [];
  polygons = [];
}

function setDefaultMapView() {
  const defaultState = {
    lat: -33.9249,
    lng: 18.4241,
    zoom: 10
  };
  map.setView([defaultState.lat, defaultState.lng], defaultState.zoom);
  localStorage.setItem('mapState', JSON.stringify(defaultState));
}

function parseSuburbCoordinates(coordString) {

  console.log("Received coordinate string: ", coordString);  // Add this line

  const matches = coordString.match(/(-?\d+\.\d+),(-?\d+\.\d+)/g);
  const coordArray = [];

  // Check if matches is not null
  if (matches !== null) {
    for (const match of matches) {
      const [lat, lng] = match.split(',').map(parseFloat);

      if (isNaN(lat) || isNaN(lng)) {
        console.error("Invalid coordinate pair:", lat, lng);
        return null;
      }
      coordArray.push([lat, lng]);
    }
  } else {
    console.error("No valid matches found for coordinates.");
    return null;
  }

  return coordArray;
}

function drawPolygon(coordinates) {
  const polygon = L.polygon(coordinates, { color: 'black', fillColor: '#004551', fillOpacity: 0.3 }).addTo(map);
  polygons.push(polygon);
}

function placeMarker(coordinates, name) {
  const [centroidLat, centroidLon] = calculateCentroid(coordinates);
  const marker = L.marker([centroidLat, centroidLon]).addTo(map).bindPopup(name).openPopup();
  markers.push(marker);
}

function calculateCentroid(coordinates) {
  const centroidLat = coordinates.reduce((acc, val) => acc + val[0], 0) / coordinates.length;
  const centroidLon = coordinates.reduce((acc, val) => acc + val[1], 0) / coordinates.length;
  return [centroidLat, centroidLon];
}

let markers = [];
let polygons = [];

function initializeMap() {
  var cityMapElement = document.getElementById('cityMap');
  if (!map && cityMapElement) {
    map = L.map('cityMap'); // Initialize without setting the view yet
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Check for a saved map state in local storage
    let initialLat, initialLng, initialZoom;
    const savedMapState = localStorage.getItem('mapState');
    if (savedMapState) {
      const mapState = JSON.parse(savedMapState);
      initialLat = mapState.lat;
      initialLng = mapState.lng;
      initialZoom = mapState.zoom;
    } else {
      // Use default values
      initialLat = -30.5595;
      initialLng = 22.9375;
      initialZoom = 5;
    }

    // Now set the view
    map.setView([initialLat, initialLng], initialZoom);

    // Update localStorage on map move
    map.on('moveend', function () {
      const center = map.getCenter();
      const zoom = map.getZoom();
      const mapState = {
        lat: center.lat,
        lng: center.lng,
        zoom: zoom
      };
      localStorage.setItem('mapState', JSON.stringify(mapState));
    });
  }

  console.log("Map initialized");
}

function updateProfileNameCell() {
  var storedProfileName = sessionStorage.getItem('selectedProfileName');
  if (storedProfileName) {
      document.getElementById('profile-name-cell').innerText = storedProfileName;
  }
}
