// Function to show the create student modal
function showStudentAgreementModal() {
    const createStudentAgreementModal = document.getElementById('agreementModal');
    createStudentAgreementModal.classList.remove('hidden');
}


// Function to hide the create student modal
function hideStudentAgreementModal() {
    const createStudentAgreementModal = document.getElementById('agreementModal');
    createStudentAgreementModal.classList.add('hidden');
}

const createStudentAgreementButton = document.getElementById('createStudentAgreementButton');

function triggerStudentAgreement() {
    // Send the data to the application
    const studentId = document.getElementById('studentIdField').innerHTML;
    const data = { agreement: true, studentId: studentId };

    fetch('/inventory/update-student-agreement', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            hideStudentAgreementModal();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    

}

// Close the modal when clicking on the close button
// closeModalButton.addEventListener('click', function () {
//     hideStudentAgreementModal();
// });

window.addEventListener('click', function (event) {
    const createStudentAgreementModal = document.getElementById('agreementModal');

    if (event.target === createStudentAgreementModal) {
        hideStudentAgreementModal();
    }
});
