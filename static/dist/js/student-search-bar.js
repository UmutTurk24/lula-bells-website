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
    
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

students = fetchStudents();

const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');

searchInput.addEventListener('input', function () {
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
                searchInput.value = student;
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
document.addEventListener('click', function (event) {
    if (!searchResults.contains(event.target) && event.target !== searchInput) {
        searchResults.classList.add('hidden');
    }
});

// Prevent dropdown from closing when clicking on input
searchInput.addEventListener('click', function (event) {
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

    console.log(studentInfo);

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
    var previousVisitsField = document.getElementById('previousVisitsWindow');
    previousVisitsField.innerHTML = "";


    // For each visit, create a new div element and append it
    previousVisits.forEach(visit => {
        let div = document.createElement('div');

        // Format the date
        let date = new Date(visit[0]);
        let dateString = date.toLocaleDateString();

        div.textContent = "Visit Date: " + dateString + ", Item Count: " + visit[1];
        div.classList.add('mb-2', 'cursor-pointer', 'hover:bg-gray-400', 'bg-gray-200', 'p-2');
        div.setAttribute('onclick', `showModal('${visit[3]}${visit[4]}')`);
        previousVisitsField.appendChild(div);
    });

    

    // Gather textbooks rented by this student

    // Gather kitchenware rented by this student

    // Gather clothing items rented by this student


    
    
    const res = {
        id: student[0][0],
        name: student[0][1],
        lastName: student[0][2],
    };

    

    // Here, you can send an AJAX request to your backend to query the database
    // and retrieve student information based on the selected student name
    // For demonstration purposes, let's assume we have retrieved the student information
    

    // Call a function to display the student information
    displayStudentInfo(res);
}
// Function to display the student information
function displayStudentInfo(studentInfo) {
    // Hide the boxes section
    document.getElementById('boxesSection').classList.add('hidden');

    // Display the student information section
    const studentInfoSection = document.getElementById('studentInfoSection');
    // studentInfoSection.innerHTML = `
    //     <h2 class="text-xl font-bold mb-4">${studentInfo.name} ${studentInfo.lastName}</h2>
    //     <p><strong>Class Year:</strong> ${studentInfo.classYear}</p>
    //     <p><strong>Student ID:</strong> ${studentInfo.id}</p>
    // `;
    studentInfoSection.classList.remove('hidden');
}
