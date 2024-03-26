var students = [];

async function fetchStudents() {
  try {
    const response = await fetch('/get-search-bar-info', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    students = data;
    console.log(students);
    // Convert the data to an array of student names
    return data.map(student => student);

  } catch (error) {
    console.error('Error:', error);
  }
}

students = fetchStudents();

const searchStudentInput = document.getElementById('searchStudentInput');
const searchResults = document.getElementById('searchResults');

searchStudentInput.addEventListener('input', function () {
  const searchTerm = this.value.trim().toLowerCase();

  if (searchTerm === '') {
    searchResults.innerHTML = '';
    searchResults.classList.add('hidden');
    return;
  }

  const filteredStudents = students.filter(student =>
    student.toLowerCase().includes(searchTerm)
  ).slice(0, 5); // Limit to 5 suggestions

  // Clear previous results
  searchResults.innerHTML = '';

  // Display matching results
  if (filteredStudents.length > 0) {
    searchResults.classList.remove('hidden');
    filteredStudents.forEach(student => {
      const resultItem = document.createElement('div');
      resultItem.textContent = student;
      resultItem.classList.add('px-4', 'py-2', 'cursor-pointer', 'hover:bg-gray-100');
      resultItem.addEventListener('click', function () {
        searchStudentInput.value = student;
        searchResults.classList.add('hidden');
        queryDatabase(student);
      });
      searchResults.appendChild(resultItem);
    });
  } else {
    searchResults.classList.add('hidden');
  }
});

// Hide suggestions when clicking outside the search box
window.addEventListener('click', function (event) {
  if (!searchResults.contains(event.target) && event.target !== searchStudentInput) {
    searchResults.classList.add('hidden');
  }
});



// Prevent dropdown from closing when clicking on input
searchStudentInput.addEventListener('click', function (event) {
  event.stopPropagation();
});

async function fetchStudentInfo(studentId) {
  try {
    const response = await fetch(`/get-searched-student-info?studentId=${studentId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Function to query the database with the selected student name
async function queryDatabase(student) {

  // Extract the id of the student (the last word in the student name string)
  const studentId = student.split(' ').pop();


  // Gather all student information from the database
  var studentInfo = await fetchStudentInfo(studentId);

  var student = studentInfo['studentInfo'];
  var previousVisits = studentInfo['previousVisits'];
  var wardrobeRentals = studentInfo['wardrobeRentals'];
  var textbookRentals = studentInfo['textbookRentals'];

  // Fill out the Student Information
  var studentNameField = document.getElementById('studentNameField');
  var studentIdField = document.getElementById('studentIdField');
  var studentEmailField = document.getElementById('studentEmailField');

  studentNameField.innerHTML = student[1] + " " + student[2];
  studentIdField.innerHTML = student[0];
  studentEmailField.innerHTML = student[3];

  // Update the agreement button if it hasn't been signed
  var agreementButton = document.getElementById('agreementButton');
  if (student[7] == 0) {
    agreementButton.classList.remove('bg-green-500');
    agreementButton.classList.add('bg-red-500');
    agreementButton.innerHTML = "Agreement Not Signed";
  }

  // Fill out the Previous Visits
  displayGroceryInfo(previousVisits, student);
  displayRentalInfo(wardrobeRentals, textbookRentals, student);

  const res = {
    id: student[0][0],
    name: student[0][1],
    lastName: student[0][2],
  };

  // Call a function to display the student information
  displayStudentInfo(res);
}

function displayRentalInfo(wardrobeRentals, textbookRentals, student) {
  let rentalsField = document.getElementById('rentedItemsWindow');
  rentalsField.innerHTML = "";

  wardrobeRentals.forEach(rental => {
    if (rental[4] == 0) {
      var clothId = rental[1];
      var dueDate = rental[3];
      var notes = rental[5];
      var renter = rental[6];

      // Format the date
      let date = new Date(dueDate);
      let dateString = date.getUTCMonth() + 1 + "/" + date.getUTCDate() + "/" + date.getUTCFullYear();


      const rentalInfo = "Clothing ID: " + clothId + ", Due Date: " + dateString;

      let div = document.createElement('div');
      div.textContent = rentalInfo;
      div.classList.add('mb-2', 'cursor-pointer', 'hover:bg-gray-400', 'bg-gray-200', 'p-2');
      div.addEventListener('click', () => showRentedClothModal(dateString, clothId, notes, renter, student));
      rentalsField.appendChild(div);
    }
  });

  textbookRentals.forEach(rental => {
    if (rental[4] == 0) {

      textbookName = rental[1];
      dueDate = rental[3];
      notes = rental[5];

      // Format the date
      let date = new Date(dueDate); 
      let dateString = date.getUTCMonth() + 1 + "/" + date.getUTCDate() + "/" + date.getUTCFullYear();




      const rentalInfo = "Textbook: " + textbookName + ", Due Date: " + dateString;

      let div = document.createElement('div');
      div.textContent = rentalInfo;
      div.classList.add('mb-2', 'cursor-pointer', 'hover:bg-gray-400', 'bg-gray-200', 'p-2');
      div.addEventListener('click', () => showRentedTextbookModal(dateString, textbookName, notes, student));

      rentalsField.appendChild(div);
    }
  });
}

function displayGroceryInfo(previousVisits, student) {
  // Fill out the Previous Visits
  var previousVisitsField = document.getElementById('previousVisitsWindow');
  previousVisitsField.innerHTML = "";

  // Group the item name and count based on the date
  let groupedVisits = {};
  previousVisits.forEach(visit => {
    
    let date = new Date(visit[2]);
    let dateString = date.getUTCMonth() + 1 + "/" + date.getUTCDate() + "/" + date.getUTCFullYear();

    if (groupedVisits[dateString] == undefined) {
      var itemName = visit[0];
      var itemCount = visit[1];

      // Add the itemName,itemCount pair to the array
      groupedVisits[dateString] = [{itemName, itemCount}];

    } else {
      var itemName = visit[0];
      var itemCount = visit[1];

      // Append the itemName,itemCount pair to the arrays
      groupedVisits[dateString].push({itemName, itemCount});
    }
  });

  // Iterate through the groupedVisits object
  for (const [key, value] of Object.entries(groupedVisits)) {
    let div = document.createElement('div');
    div.textContent = "Visit Date: " + key;
    div.classList.add('mb-2', 'cursor-pointer', 'hover:bg-gray-400', 'bg-gray-200', 'p-2');
    div.addEventListener('click', () => showGroceryModal(key, value, student));

    previousVisitsField.appendChild(div);
  }
}




// Function to display the student information
function displayStudentInfo(studentInfo) {
  // Hide the boxes section
  document.getElementById('boxesSection').classList.add('hidden');

  // Display the student information section
  const studentInfoSection = document.getElementById('studentInfoSection');
  studentInfoSection.classList.remove('hidden');
}
