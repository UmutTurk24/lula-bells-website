let lastSort = { key: null, isAscending: true };
changeList = [];
groceries = [];

async function loadTextbookData() {

    var groceryInfos = {}
    // Fetch all of the groceries
    try {
        groceryInfos = await fetch('/admin/dashboard/grocery-inventory', {
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
    
    // Map the owned status
    groceries = groceryInfos.map(groceryInfo => {
        const name = groceryInfo[0];
        const quantity = groceryInfo[1];
        const cost = groceryInfo[2];

        return {
            name: name,
            quantity: quantity,
            cost: cost,
        };
    });
}

function displayItems(items) {
    groceryTableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
                            <td class="border px-4 py-2">${item.name}</td>
                            <td class="border px-4 py-2">${item.quantity}</td>
                            <td class="border px-4 py-2">${item.cost}</td>
                            <td class="border px-4 py-2">
                                <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="removeItem('${item.name}')">Remove</button>
                                <button class="bg-blue-500 text-white px-4 py-2 rounded" onclick="editItem('${item.name}')">Edit</button>
                            </td>
                        `;
        groceryTableBody.appendChild(row);
    });
}

function itemAdder(){
    document.getElementById('addItemForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const quantity = document.getElementById('quantity').value;
        const cost = document.getElementById('cost').value;

        // Check if the item already exists
        if (groceries.find(grocery => grocery.name === name)) {
            alert('Item already exists');
            return;
        }

        // Update the displayed table
        groceries.push({ name, quantity, cost });
        displayItems(groceries);

        // Update the changelist to be sent to the server
        changeList.push({ name, quantity, cost, opCode: 0 });

        e.target.reset();
    });
}

function sortingFunction() {
    // Sorting function
    window.sortTable = (key) => {
        // Check if the same key was clicked, toggle sort direction; else, sort ascending
        if (lastSort.key === key) {
            lastSort.isAscending = !lastSort.isAscending;
        } else {
            lastSort = { key: key, isAscending: true };
        }

        groceries.sort((a, b) => {
            // Convert to lowercase for case-insensitive comparison
            let valA = a[key].toLowerCase();
            let valB = b[key].toLowerCase();

            if (valA < valB) return lastSort.isAscending ? -1 : 1;
            if (valA > valB) return lastSort.isAscending ? 1 : -1;
            return 0;
        });

        displayItems(groceries);
    };
}

function saveChangesButton() {
    document.getElementById('saveChangesButton').addEventListener('click', function () {
        // Send the change list to the server
        fetch('/admin/dashboard/grocery-inventory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ changeList }),
        });

        // Clear the change list, and display a success message
        changeList = [];
        alert('Changes saved successfully');
    });
}

function removeItem(name) {
    // Remove the item from the displayed table
    groceries = groceries.filter(grocery => grocery.name !== name);
    displayItems(groceries);

    // Update the changelist to be sent to the server
    changeList.push({ name, password: '0', role: '0', opCode: 1});
}

function editItem(name) {
    // Change the quantity and/or cost of the item
    groceries = groceries.map(grocery => {
        if (grocery.name === name) {
            grocery.quantity = prompt('Enter the new quantity:', grocery.quantity);
            grocery.cost = prompt('Enter the new cost:', grocery.cost);
        }
        return grocery;
    });

    displayItems(groceries);

    // Get the new quantity and cost
    const quantity = groceries.find(grocery => grocery.name === name).quantity;
    const cost = groceries.find(grocery => grocery.name === name).cost;

    // Update the changelist to be sent to the server
    changeList.push({ name, quantity, cost, opCode: 2 });
}

async function fillTable() {
    await loadTextbookData();

    const groceryTableBody = document.getElementById('groceryTableBody');
    displayItems(groceries);

    // Adding a new item
    itemAdder();

    // Table's sorting functionality
    sortingFunction();

    // Saving changes functionality
    saveChangesButton();
}

fillTable();
