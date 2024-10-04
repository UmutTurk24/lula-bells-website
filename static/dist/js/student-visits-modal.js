// Function to hide the modal
function hideGroceryModal() {
    const modal = document.getElementById('groceryVisitModal');
    modal.classList.add('hidden');
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const modal = document.getElementById('groceryVisitModal');
    if (event.target === modal) {
        hideGroceryModal();
    }
});


function showGroceryModal(visitDate, visitDetails, student) {
    const visitModal = document.getElementById('groceryVisitModal');
    const visitDetailsContainer = document.getElementById('groceryVisitDetails');

    // Clear previous details
    visitDetailsContainer.innerHTML = '';

    // Set the modal title
    document.querySelector('#groceryVisitModal h2').textContent = `Visit Details - ${visitDate}`;

    // Iterate over the visit details and display them in the modal
    for (const detail of visitDetails) {
        const itemName = detail.itemName;
        const itemCount = detail.itemCount;

        const itemDiv = document.createElement('div');
        itemDiv.classList.add('mb-2');

        const itemNameSpan = document.createElement('span');
        itemNameSpan.textContent = itemName;

        const itemCountInput = document.createElement('input');
        itemCountInput.type = 'number';
        itemCountInput.value = itemCount;
        itemCountInput.classList.add('ml-2', 'w-16', 'border', 'border-gray-300', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'p-2', 'w-1/4');

        itemDiv.appendChild(itemNameSpan);
        itemDiv.appendChild(itemCountInput);
        visitDetailsContainer.appendChild(itemDiv);
    }

    // Add submit button
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';
    submitButton.classList.add('mt-4', 'px-4', 'py-2', 'bg-blue-500', 'text-white', 'rounded-md', 'focus:outline-none', 'focus:bg-blue-600');
    submitButton.addEventListener('click', function() {
        submitGroceryForm(visitDate, visitDetails, student);
    });

    visitDetailsContainer.appendChild(submitButton);

    // Show the modal
    visitModal.classList.remove('hidden');
}

function submitGroceryForm(visitDate, visitDetails, student) {

    // Get the updated item counts from the form
    const groceryVisitDetails = document.getElementById('groceryVisitDetails');

    // Update the each visit detail with the new item count
    for (let i = 0; i < groceryVisitDetails.children.length-1; i++) {
        const detail = groceryVisitDetails.children[i];
        const itemCount = detail.children[1].value;

        visitDetails[i].itemCount = itemCount;
    }

    // Construct the form data
    const data = { visitDate, visitDetails, student};

    // Submit the form (you need to specify the URL where to submit the form data)
    fetch('/inventory/update-grocery-visit', {
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
    hideGroceryModal();
}

function hideGroceryModal() {
    const visitModal = document.getElementById('groceryVisitModal');
    visitModal.classList.add('hidden');
}