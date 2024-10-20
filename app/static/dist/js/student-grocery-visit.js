

async function showGroceryModalMenu() {
    const groceryModalMenu = document.getElementById('groceryModalMenu');

    var groceryInfos = {}
    // Fetch all of the groceries
    try {
        groceryInfos = await fetch('/inventory/get-groceries', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
    } catch (error) {
        console.error('Error:', error);
    }

    groceryInfos = await groceryInfos.json();

    console.log(groceryInfos);

    // Map the groceryInfos to the grocery names and cost
    const groceries = groceryInfos.map(groceryInfo => {
        const name = groceryInfo[0];
        const count = groceryInfo[1];
        const cost = groceryInfo[2];
        return {
            name: name,
            count: count,
            cost: cost,
        };
    });

    groceryModalMenu.classList.remove('hidden');
    
    const searchGroceryInput = document.getElementById('searchGroceryInput');
    const groceriesSearchResults = document.getElementById('grocerySearchResults');
    const selectedGroceries = document.getElementById('selectedGroceries');

    searchGroceryInput.addEventListener('input', function () {
        const searchTerm = this.value.trim().toLowerCase();

        if (searchTerm === '') {
            groceriesSearchResults.innerHTML = '';
            groceriesSearchResults.classList.add('hidden');
            return;
        }

        const filteredGrocery = groceries.filter(grocery =>
            grocery['name'].toLowerCase().includes(searchTerm)
        ).slice(0, 5); // Limit to 5 suggestions

        // Clear previous results
        groceriesSearchResults.innerHTML = '';

        // Display matching results
        if (filteredGrocery.length > 0) {
            groceriesSearchResults.classList.remove('hidden');
            filteredGrocery.forEach(grocery => {
                const resultItem = document.createElement('div');
                resultItem.textContent = grocery['name'];
                resultItem.classList.add('px-4', 'py-2', 'cursor-pointer', 'hover:bg-gray-100');
                resultItem.addEventListener('click', function () {
                    searchGroceryInput.value = grocery['name'];
                    groceriesSearchResults.classList.add('hidden');

                    // Add the grocery to the list of selected groceries
                    const selectedGrocery = document.createElement('div');
                    selectedGrocery.classList.add('bg-white', 'rounded-lg', 'shadow-md', 'p-2', 'mb-1');

                    const groceryInfo = document.createElement('div');
                    groceryInfo.classList.add('flex', 'items-center', 'justify-between', 'mb-1');
                    
                    const textSpanItem = document.createElement('span');
                    textSpanItem.textContent = 'Item: ';
                    textSpanItem.classList.add('text-gray-600', 'mr-2');

                    const nameSpan = document.createElement('span');
                    nameSpan.textContent = grocery['name'];
                    nameSpan.classList.add('text-gray-800');

                    const nameDiv = document.createElement('div');
                    nameDiv.classList.add('flex', 'items-center')
                    nameDiv.appendChild(textSpanItem);
                    nameDiv.appendChild(nameSpan);

                    const textSpanCost = document.createElement('span');
                    textSpanCost.textContent = 'Price: ';
                    textSpanCost.classList.add('text-gray-600', 'mr-2');

                    const costSpan = document.createElement('span');
                    costSpan.textContent = grocery['cost'];
                    costSpan.classList.add('text-gray-800');

                    const costDiv = document.createElement('div');
                    costDiv.classList.add('flex', 'items-center')
                    costDiv.appendChild(textSpanCost);
                    costDiv.appendChild(costSpan);

                    const textSpanStock = document.createElement('span');
                    textSpanStock.textContent = 'In Stock: ';
                    textSpanStock.classList.add('text-gray-600', 'mr-2');

                    const stockSpan = document.createElement('span');
                    stockSpan.textContent = grocery['count'];
                    stockSpan.classList.add('text-gray-800');

                    const stockDiv = document.createElement('div');
                    stockDiv.classList.add('flex', 'items-center')
                    stockDiv.appendChild(textSpanStock);
                    stockDiv.appendChild(stockSpan);

                    groceryInfo.appendChild(nameDiv);
                    groceryInfo.appendChild(stockDiv);
                    groceryInfo.appendChild(costDiv);

                    const inputDiv = document.createElement('div');
                    inputDiv.classList.add('flex', 'items-center', 'mt-1');

                    // Add a value input to specify the quantity of the grocery
                    const quantityInput = document.createElement('input');
                    quantityInput.type = 'number';
                    quantityInput.classList.add('border', 'border-gray-300', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'block', 'p-1.5', 'w-16', 'ml-2', 'mr-16');

                    const textQuantityInput = document.createElement('span');
                    textQuantityInput.textContent = 'Purchase Amount: ';
                    textQuantityInput.classList.add('text-gray-600', 'mr-2');


                    
                    // Add a button to remove the grocery from the list
                    const removeButton = document.createElement('button');
                    removeButton.textContent = ' Remove';
                    removeButton.classList.add('ml-2', 'text-red-500', 'hover:text-red-700');
                    removeButton.addEventListener('click', function () {
                        selectedGrocery.remove();
                    });
                    
                    inputDiv.appendChild(textQuantityInput);
                    inputDiv.appendChild(quantityInput);
                    inputDiv.appendChild(removeButton);
                    selectedGrocery.appendChild(groceryInfo);
                    selectedGrocery.appendChild(inputDiv);
                    selectedGroceries.appendChild(selectedGrocery);
                });
                groceriesSearchResults.appendChild(resultItem);
            });
        } else {
            groceriesSearchResults.classList.add('hidden');
        }
    });
    
}


// Function to hide the pop-up menu
function hideGroceryPopupMenu() {
    const groceryModalMenu = document.getElementById('groceryModalMenu');
    groceryModalMenu.classList.add('hidden');
}

// Function to save and exit
function savegroceryAndExit() {
    // Check if the user has selected any groceries
    const selectedGrocery = document.getElementById('selectedGroceries');
    if (selectedGrocery.children.length === 0) {
        alert('Please select at least one grocery');
        return;
    }

    // The selectedGrocery div contains a div with two span children, the first span contains the name of the grocery and the second span contains the rented status
    // We want to convert this to a dictionary of name and rented status
    const currentGroceries = Array.from(selectedGrocery.children).map(grocery => {
        const name = grocery.children[0].children[0].children[0].textContent;
        const count = grocery.children[1].children[1].value;   
        return {
            name: name.trimEnd(),
            count: count,
        };
    });

    // Get the student id (very unsafe) 
    const studentId = document.getElementById('studentIdField').textContent;

    // Send the groceries and the student id to the server
    const data = {
        studentId: studentId,
        groceries: currentGroceries,
    };
    
    // Update the purchased status of the groceries
    fetch('/inventory/buy-groceries', {
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

    hideGroceryPopupMenu();
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const groceryModalMenu = document.getElementById('groceryModalMenu');
    const triggerGroceryPopup = document.getElementById('triggerGroceryPopup');
    if (event.target === groceryModalMenu || event.target === triggerGroceryPopup) {
        hideGroceryPopupMenu();
    }
});
