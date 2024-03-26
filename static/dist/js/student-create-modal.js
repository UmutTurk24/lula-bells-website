
// Function to show the create student modal
function showCreateStudentModal() {
    const createStudentModal = document.getElementById('createStudentModal');
    createStudentModal.classList.remove('hidden');
}

// Function to hide the create student modal
function hideCreateStudentModal() {
    const createStudentModal = document.getElementById('createStudentModal');
    createStudentModal.classList.add('hidden');
}

const createStudentButton = document.getElementById('createStudentButton');
const saveStudentButton = document.getElementById('saveStudentButton');
const createStudentModal = document.getElementById('createStudentModal');
const closeModalButton = document.getElementById('closeModalButton');

createStudentButton.addEventListener('click', function () {
    showCreateStudentModal();
});

saveStudentButton.addEventListener('click', function () {
    const id = document.getElementById('id').value
    const name = document.getElementById('name').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const classYear = document.getElementById('classYear').value;
    const residence = document.getElementById('residence').value;

    // Here, you can send the form data to your database
    // You can perform validations before sending the data

    // Array to hold the IDs of the empty fields
    const emptyFields = [];

    // Check if any field is empty
    if (id.trim() === '') emptyFields.push('id');
    if (name.trim() === '') emptyFields.push('name');
    if (lastName.trim() === '') emptyFields.push('lastName');
    if (email.trim() === '') emptyFields.push('email');
    if (classYear.trim() === '') emptyFields.push('classYear');
    if (residence.trim() === '') emptyFields.push('residence');

    // If any field is empty, turn its border red
    emptyFields.forEach(fieldId => {
        document.getElementById(fieldId).style.borderColor = 'red';
    });

    if (emptyFields.length == 0) {
        // If all fields are filled, send the data to the application
        const data = { id, name, lastName, email, classYear, residence };

        fetch('/register-student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

        // Clear the form fields
        document.getElementById('id').value = '';
        document.getElementById('name').value = '';
        document.getElementById('lastName').value = '';
        document.getElementById('email').value = '';
        document.getElementById('classYear').value = '';

        // Turn the fields into regular colors
        document.getElementById('id').style.borderColor = '';
        document.getElementById('name').style.borderColor = '';
        document.getElementById('lastName').style.borderColor = '';
        document.getElementById('email').style.borderColor = '';
        document.getElementById('classYear').style.borderColor = '';
    
        // Hide the modal after saving
        hideCreateStudentModal();
    }

});

// Close the modal when clicking on the close button
closeModalButton.addEventListener('click', function () {
    hideCreateStudentModal();
});

window.addEventListener('click', function (event) {

    if (event.target === createStudentModal) {
        hideCreateStudentModal();
    }
});
