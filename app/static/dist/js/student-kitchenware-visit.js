

async function showKitchenwareModalMenu() {
    const kitchenwareModalMenu = document.getElementById('kitchenwareModalMenu');

    var kitchenwareInfos = {}
    // Fetch all of the kitchenwares
    try {
        kitchenwareInfos = await fetch('/inventory/get-kitchenwares', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });;
        
    } catch (error) {
        console.error('Error:', error);
    }

    kitchenwareInfos = await kitchenwareInfos.json();


    // Map the kitchenwareInfos to the kitchenware names and rented information (if 0 'rented', otherwise 'not rented')
    const kitchenwares = kitchenwareInfos.map(kitchenwareInfo => {
        const name = kitchenwareInfo[0];
        const rented = kitchenwareInfo[2] === 0 ? 'rented' : 'available';
        return {
            name: name,
            rented_status: rented
        };
    });



    kitchenwareModalMenu.classList.remove('hidden');
    
    const searchKitchenwareInput = document.getElementById('searchKitchenwareInput');
    const kitchenwareSearchResults = document.getElementById('kitchenwareSearchResults');
    const selectedKitchenware = document.getElementById('selectedKitchenware');

    searchKitchenwareInput.addEventListener('input', function () {
        const searchTerm = this.value.trim().toLowerCase();

        if (searchTerm === '') {
            kitchenwareSearchResults.innerHTML = '';
            kitchenwareSearchResults.classList.add('hidden');
            return;
        }

        const filteredKitchenware = kitchenwares.filter(kitchenware =>
            kitchenware['name'].toLowerCase().includes(searchTerm)
        ).slice(0, 5); // Limit to 5 suggestions

        // Clear previous results
        kitchenwareSearchResults.innerHTML = '';

        // Display matching results
        if (filteredKitchenware.length > 0) {
            kitchenwareSearchResults.classList.remove('hidden');
            filteredKitchenware.forEach(kitchenware => {
                const resultItem = document.createElement('div');
                resultItem.textContent = kitchenware['name'] + ' ' + kitchenware['rented_status'];
                resultItem.classList.add('px-4', 'py-2', 'cursor-pointer', 'hover:bg-gray-100');
                resultItem.addEventListener('click', function () {
                    searchKitchenwareInput.value = kitchenware['name'] + ' ' + kitchenware['rented_status'];
                    // searchKitchenwareInput.value = kitchenware;
                    kitchenwareSearchResults.classList.add('hidden');

                    // Add the kitchenware to the list of selected kitchenwares
                    const selectedkitchenware = document.createElement('div');
                    const nameSpan = document.createElement('span');
                    nameSpan.textContent = kitchenware['name'] + ' ';
                    const rentedSpan = document.createElement('span');
                    rentedSpan.textContent = kitchenware['rented_status'];
                    selectedkitchenware.appendChild(nameSpan);
                    selectedkitchenware.appendChild(rentedSpan);
                    selectedkitchenware.classList.add('px-4', 'py-2', 'border-b', 'border-gray-200');

                    // Add a button to remove the kitchenware from the list
                    const removeButton = document.createElement('button');
                    removeButton.textContent = ' Remove';
                    removeButton.classList.add('ml-2', 'text-red-500', 'hover:text-red-700');
                    removeButton.addEventListener('click', function () {
                        selectedkitchenware.remove();
                    });
                    selectedkitchenware.appendChild(removeButton);
                    selectedKitchenware.appendChild(selectedkitchenware);
                });
                kitchenwareSearchResults.appendChild(resultItem);
            });
        } else {
            kitchenwareSearchResults.classList.add('hidden');
        }
    });
    
}


// Function to hide the pop-up menu
function hideKitchenwarePopupMenu() {
    const kitchenwareModalMenu = document.getElementById('kitchenwareModalMenu');
    kitchenwareModalMenu.classList.add('hidden');
}

// Function to save and exit
function saveKitchenwareAndExit() {
    // Check if the user has selected any kitchenwares
    const selectedKitchenware = document.getElementById('selectedKitchenware');
    if (selectedKitchenware.children.length === 0) {
        alert('Please select at least one kitchenware');
        return;
    }

    // The selectedKitchenware div contains a div with two span children, the first span contains the name of the kitchenware and the second span contains the rented status
    // We want to convert this to a dictionary of name and rented status
    const currentkitchenwares = Array.from(selectedKitchenware.children).map(kitchenware => {
        const name = kitchenware.children[0].textContent;
        const rented = kitchenware.children[1].textContent;
        return {
            name: name.trimEnd(),
            rentedStatus: rented
        };
    });

    // Check if any of the kitchenwares are already rented into a dictionary of name and rented status
    for (let i = 0; i < currentkitchenwares.length; i++) {
        if (currentkitchenwares[i].rentedStatus === 'rented') {
            alert(`The following kitchenware is already rented: ${currentkitchenwares[i].name}`);
            return;
        }
    }

    // Check if the due date is empty
    if (document.getElementById('kitchenwareDueDate').value === '') {
        alert('Please enter a due date');
        return;
    }

    // Get the due date
    const dueDate = document.getElementById('kitchenwareDueDate').value;

    // Get the student id (very unsafe) 
    const studentId = document.getElementById('studentIdField').textContent;

    // Send the kitchenwares and the student id to the server
    const data = {
        studentId: studentId,
        kitchenwares: currentkitchenwares,
        dueDate: dueDate,
    };
    
    // Update the rented status of the kitchenwares
    fetch('/inventory/rent-kitchenwares', {
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

    hideKitchenwarePopupMenu();
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const kitchenwareModalMenu = document.getElementById('kitchenwareModalMenu');
    const triggerKitchenwarePopup = document.getElementById('triggerKitchenwarePopup');
    if (event.target === kitchenwareModalMenu || event.target === triggerKitchenwarePopup) {
        hideKitchenwarePopupMenu();
    }
});
