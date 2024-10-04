

async function showAcademicModalMenu() {
    const academicModalMenu = document.getElementById('academicModalMenu');

    var textbookInfos = {}
    // Fetch all of the textbooks
    try {
        textbookInfos = await fetch('/inventory/get-textbooks', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });;
        
    } catch (error) {
        console.error('Error:', error);
    }

    textbookInfos = await textbookInfos.json();


    // Map the textbookInfos to the textbook names and rented information (if 0 'rented', otherwise 'not rented')
    const textbooks = textbookInfos.map(textbookInfo => {
        const name = textbookInfo[0];
        const rented = textbookInfo[2] === 0 ? 'rented' : 'available';
        return {
            name: name,
            rented_status: rented
        };
    });

    academicModalMenu.classList.remove('hidden');

    console.log(textbooks);
    console.log(academicModalMenu);
    
    const searchAcademicInput = document.getElementById('searchAcademicInput');
    const academicSearchResults = document.getElementById('academicSearchResults');
    const selectedTextbooks = document.getElementById('selectedTextbooks');

    searchAcademicInput.addEventListener('input', function () {
        const searchTerm = this.value.trim().toLowerCase();

        if (searchTerm === '') {
            academicSearchResults.innerHTML = '';
            academicSearchResults.classList.add('hidden');
            return;
        }

        const filteredTextbooks = textbooks.filter(textbook =>
            textbook['name'].toLowerCase().includes(searchTerm)
        ).slice(0, 5); // Limit to 5 suggestions

        // Clear previous results
        academicSearchResults.innerHTML = '';

        // Display matching results
        if (filteredTextbooks.length > 0) {
            academicSearchResults.classList.remove('hidden');
            filteredTextbooks.forEach(textbook => {
                const resultItem = document.createElement('div');
                resultItem.textContent = textbook['name'] + ' ' + textbook['rented_status'];
                resultItem.classList.add('px-4', 'py-2', 'cursor-pointer', 'hover:bg-gray-100');
                resultItem.addEventListener('click', function () {
                    searchAcademicInput.value = textbook['name'] + ' ' + textbook['rented_status'];
                    // searchAcademicInput.value = textbook;
                    academicSearchResults.classList.add('hidden');

                    // Add the textbook to the list of selected textbooks
                    const selectedTextbook = document.createElement('div');
                    const nameSpan = document.createElement('span');
                    nameSpan.textContent = textbook['name'] + ' ';
                    const rentedSpan = document.createElement('span');
                    rentedSpan.textContent = textbook['rented_status'];
                    selectedTextbook.appendChild(nameSpan);
                    selectedTextbook.appendChild(rentedSpan);
                    selectedTextbook.classList.add('px-4', 'py-2', 'border-b', 'border-gray-200');

                    // Add a button to remove the textbook from the list
                    const removeButton = document.createElement('button');
                    removeButton.textContent = ' Remove';
                    removeButton.classList.add('ml-2', 'text-red-500', 'hover:text-red-700');
                    removeButton.addEventListener('click', function () {
                        selectedTextbook.remove();
                    });
                    selectedTextbook.appendChild(removeButton);
                    selectedTextbooks.appendChild(selectedTextbook);
                });
                academicSearchResults.appendChild(resultItem);
            });
        } else {
            academicSearchResults.classList.add('hidden');
        }
    });
    
}


// Function to hide the pop-up menu
function hideAcademicPopupMenu() {
    const academicModalMenu = document.getElementById('academicModalMenu');
    academicModalMenu.classList.add('hidden');
}

// Function to save and exit
function saveTextbookAndExit() {
    // Check if the user has selected any textbooks
    const selectedTextbooks = document.getElementById('selectedTextbooks');
    if (selectedTextbooks.children.length === 0) {
        alert('Please select at least one textbook');
        return;
    }

    // The selectedTextbooks div contains a div with two span children, the first span contains the name of the textbook and the second span contains the rented status
    // We want to convert this to a dictionary of name and rented status
    const currentTextbooks = Array.from(selectedTextbooks.children).map(textbook => {
        const name = textbook.children[0].textContent;
        const rented = textbook.children[1].textContent;
        return {
            name: name.trimEnd(),
            rentedStatus: rented
        };
    });

    // Check if any of the textbooks are already rented into a dictionary of name and rented status
    for (let i = 0; i < currentTextbooks.length; i++) {
        if (currentTextbooks[i].rentedStatus === 'rented') {
            alert(`The following textbook is already rented: ${currentTextbooks[i].name}`);
            return;
        }
    }

    // Check if the due date is empty
    if (document.getElementById('textbookDueDate').value === '') {
        alert('Please enter a due date');
        return;
    }

    // Get the due date
    const dueDate = document.getElementById('textbookDueDate').value;

    // Get the student id (very unsafe) 
    const studentId = document.getElementById('studentIdField').textContent;

    // Send the textbooks and the student id to the server
    const data = {
        studentId: studentId,
        textbooks: currentTextbooks,
        dueDate: dueDate,
    };
    
    // Update the rented status of the textbooks
    fetch('/inventory/rent-textbooks', {
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

    hideAcademicPopupMenu();
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const academicModalMenu = document.getElementById('academicModalMenu');
    const triggerAcademicPopup = document.getElementById('triggerAcademicPopup');
    if (event.target === academicModalMenu || event.target === triggerAcademicPopup) {
        hideAcademicPopupMenu();
    }
});
