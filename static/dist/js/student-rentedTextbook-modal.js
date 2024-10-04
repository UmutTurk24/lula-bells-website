
// Function to hide the modal
function hideRentedTextbookModal() {
    const modal = document.getElementById('rentedTextbookModal');
    modal.classList.add('hidden');
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const modal = document.getElementById('rentedTextbookModal');
    if (event.target === modal) {
        hideRentedTextbookModal();
    }
});


function showRentedTextbookModal(dueDate, textbookName, notes, student) {
    const visitModal = document.getElementById('rentedTextbookModal');
    const visitDetailsContainer = document.getElementById('rentedTextbookDetails');

    console.log(visitModal);
    // Clear previous details
    visitDetailsContainer.innerHTML = '';

    // Set the modal title
    document.querySelector('#rentedTextbookModal h2').textContent = `Rented Item Details - ${dueDate}`;

    // Create and append textbookName
    const itemDiv = document.createElement('div');

    const itemNameSpan = document.createElement('span');
    itemNameSpan.textContent = textbookName;
    
    const returnCheckbox = document.createElement('input');
    returnCheckbox.type = 'checkbox';
    returnCheckbox.classList.add('ml-2');
    
    itemDiv.appendChild(itemNameSpan);
    itemDiv.appendChild(returnCheckbox);

    visitDetailsContainer.appendChild(itemDiv);

    // Create and append notes
    if (notes) {
        const notesDiv = document.createElement('div');
        notesDiv.classList.add('mb-2');

        const notesLabel = document.createElement('label');
        notesLabel.textContent = 'Notes:';
        notesDiv.appendChild(notesLabel);

        const notesInput = document.createElement('textarea');
        notesInput.textContent = notes;
        notesInput.classList.add('ml-2', 'w-full', 'h-24', 'border', 'border-gray-300', 'rounded-md', 'p-2', 'focus:outline-none', 'focus:border-indigo-500');
        notesDiv.appendChild(notesInput);

        visitDetailsContainer.appendChild(notesDiv);
    }


    // Add submit button
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';
    submitButton.classList.add('mt-4', 'px-4', 'py-2', 'bg-blue-500', 'text-white', 'rounded-md', 'focus:outline-none', 'focus:bg-blue-600');
    submitButton.addEventListener('click', function() {
        submitRentedTextbookForm(dueDate, textbookName, returnCheckbox.checked, student);
    });

    visitDetailsContainer.appendChild(submitButton);

    // Show the modal
    visitModal.classList.remove('hidden');
}

function submitRentedTextbookForm(dueDate, textbookName, isChecked, student) {
    // Construct the form data
    const data = { dueDate, textbookName, isChecked, student};

    console.log(data);

    // Submit the form (you need to specify the URL where to submit the form data)
    fetch('/inventory/update-rented-textbook', {
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
    .catch(error => {
        console.error('Error:', error);
    });

    // Hide the modal
    hideRentedTextbookModal();
}

function hideRentedTextbookModal() {
    const visitModal = document.getElementById('rentedTextbookModal');
    visitModal.classList.add('hidden');
}