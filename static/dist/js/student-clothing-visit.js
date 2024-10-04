

async function showClothingModalMenu() {
    const clothingModalMenu = document.getElementById('clothingModalMenu');

    var clothingInfos = {}
    // Fetch all of the clothes
    try {
        clothingInfos = await fetch('/inventory/get-clothes', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

    } catch (error) {
        console.error('Error:', error);
    }

    clothingInfos = await clothingInfos.json();


    // Map the clothingInfos to the cloth names and rented information (if 0 'rented', otherwise 'not rented')
    const clothes = clothingInfos.map(clothingInfo => {
        const name = clothingInfo[0];
        const rented = clothingInfo[2] === 0 ? 'rented' : 'available';
        return {
            name: name,
            rented_status: rented
        };
    });



    clothingModalMenu.classList.remove('hidden');

    const searchClothingInput = document.getElementById('searchClothingInput');
    const clothingSearchResults = document.getElementById('clothingSearchResults');
    const selectedClothes = document.getElementById('selectedClothes');

    searchClothingInput.addEventListener('input', function () {
        const searchTerm = this.value.trim().toLowerCase();

        if (searchTerm === '') {
            clothingSearchResults.innerHTML = '';
            clothingSearchResults.classList.add('hidden');
            return;
        }

        const filteredClothings = clothes.filter(cloth =>
            cloth['name'].toLowerCase().includes(searchTerm)
        ).slice(0, 5); // Limit to 5 suggestions

        // Clear previous results
        clothingSearchResults.innerHTML = '';

        // Display matching results
        if (filteredClothings.length > 0) {
            clothingSearchResults.classList.remove('hidden');
            filteredClothings.forEach(cloth => {
                const resultItem = document.createElement('div');
                resultItem.textContent = cloth['name'] + ' ' + cloth['rented_status'];
                resultItem.classList.add('px-4', 'py-2', 'cursor-pointer', 'hover:bg-gray-100');
                resultItem.addEventListener('click', function () {
                    searchClothingInput.value = cloth['name'] + ' ' + cloth['rented_status'];
                    // searchClothingInput.value = cloth;
                    clothingSearchResults.classList.add('hidden');

                    // Add the cloth to the list of selected clothes
                    const selectedClothing = document.createElement('div');
                    const nameSpan = document.createElement('span');
                    nameSpan.textContent = cloth['name'] + ' ';
                    const rentedSpan = document.createElement('span');
                    rentedSpan.textContent = cloth['rented_status'];
                    selectedClothing.appendChild(nameSpan);
                    selectedClothing.appendChild(rentedSpan);
                    selectedClothing.classList.add('px-4', 'py-2', 'border-b', 'border-gray-200');

                    // Add a button to remove the cloth from the list
                    const removeButton = document.createElement('button');
                    removeButton.textContent = ' Remove';
                    removeButton.classList.add('ml-2', 'text-red-500', 'hover:text-red-700');
                    removeButton.addEventListener('click', function () {
                        selectedClothing.remove();
                    });
                    selectedClothing.appendChild(removeButton);
                    selectedClothes.appendChild(selectedClothing);
                });
                clothingSearchResults.appendChild(resultItem);
            });
        } else {
            clothingSearchResults.classList.add('hidden');
        }
    });

}


// Function to hide the pop-up menu
function hideClothesPopupMenu() {
    const clothingModalMenu = document.getElementById('clothingModalMenu');
    clothingModalMenu.classList.add('hidden');
}

// Function to save and exit
function saveClothesAndExit() {
    // Check if the user has selected any clothes
    const selectedClothes = document.getElementById('selectedClothes');
    if (selectedClothes.children.length === 0) {
        alert('Please select at least one cloth');
        return;
    }

    // The selectedClothes div contains a div with two span children, the first span contains the name of the cloth and the second span contains the rented status
    // We want to convert this to a dictionary of name and rented status
    const currentClothings = Array.from(selectedClothes.children).map(cloth => {
        const name = cloth.children[0].textContent;
        const rented = cloth.children[1].textContent;
        return {
            name: name.trimEnd(),
            rentedStatus: rented
        };
    });

    // Check if any of the clothes are already rented into a dictionary of name and rented status
    for (let i = 0; i < currentClothings.length; i++) {
        if (currentClothings[i].rentedStatus === 'rented') {
            alert(`The following cloth is already rented: ${currentClothings[i].name}`);
            return;
        }
    }

    // Check if the due date is empty
    if (document.getElementById('clothingDueDate').value === '') {
        alert('Please enter a due date');
        return;
    }

    // Get the due date
    const dueDate = document.getElementById('clothingDueDate').value;

    // Get the student id (very unsafe) 
    const studentId = document.getElementById('studentIdField').textContent;

    // Send the clothes and the student id to the server
    const data = {
        studentId: studentId,
        clothes: currentClothings,
        dueDate: dueDate,
    };

    // Update the rented status of the clothes
    fetch('/inventory/rent-clothes', {
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


    hideClothesPopupMenu();
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const clothingModalMenu = document.getElementById('clothingModalMenu');
    const triggerClothingPopup = document.getElementById('triggerClothingPopup');
    if (event.target === clothingModalMenu || event.target === triggerClothingPopup) {
        hideClothesPopupMenu();
    }
});
