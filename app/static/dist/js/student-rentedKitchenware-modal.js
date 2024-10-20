
// Function to hide the modal
function hideRentedKitchenwareModal() {
    const modal = document.getElementById('rentedKitchenwareModal');
    modal.classList.add('hidden');
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const modal = document.getElementById('rentedKitchenwareModal');
    if (event.target === modal) {
        hideRentedKitchenwareModal();
    }
});


function showRentedKitchenwareModal(dueDate, kitchenwareName, notes, renter, student) {
    const visitModal = document.getElementById('rentedKitchenwareModal');
    const visitDetailsContainer = document.getElementById('rentedKitchenwareDetails');

    // Clear previous details
    visitDetailsContainer.innerHTML = '';

    // Set the modal title
    document.querySelector('#rentedKitchenwareModal h2').textContent = `Rented Item Details - ${dueDate}`;

    // Create and append kitchenwareName
    const itemDiv = document.createElement('div');

    const itemNameSpan = document.createElement('span');
    itemNameSpan.textContent = kitchenwareName;

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

    // Create and append renter
    if (renter) {
        const renterDiv = document.createElement('div');
        renterDiv.textContent = `Name of the renter: ${renter}`;
        renterDiv.classList.add('mb-2');
        visitDetailsContainer.appendChild(renterDiv);
    }


    // Add submit button
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';
    submitButton.classList.add('mt-4', 'px-4', 'py-2', 'bg-blue-500', 'text-white', 'rounded-md', 'focus:outline-none', 'focus:bg-blue-600');
    submitButton.addEventListener('click', function () {
        submitRentedKitchenwareForm(dueDate, kitchenwareName, returnCheckbox.checked, student);
    });

    visitDetailsContainer.appendChild(submitButton);

    // Show the modal
    visitModal.classList.remove('hidden');
}

function submitRentedKitchenwareForm(dueDate, kitchenwareName, isChecked, student) {
    // Construct the form data
    const data = { dueDate, kitchenwareName, isChecked, student };

    console.log(data);

    // Submit the form (you need to specify the URL where to submit the form data)
    fetch('/inventory/update-rented-kitchenware', {
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
    hideRentedKitchenwareModal();
}

function hideRentedKitchenwareModal() {
    const visitModal = document.getElementById('rentedKitchenwareModal');
    visitModal.classList.add('hidden');
}