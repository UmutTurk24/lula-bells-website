let lastSort = { key: null, isAscending: true };
changeList = [];
kitchenwares = [];

async function loadKitchenwareData() {

    var kitchenwareInfos = {}
    // Fetch all of the kitchenwares
    try {
        kitchenwareInfos = await fetch('/admin/dashboard/kitchenware-inventory', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
    
    } catch (error) {
        console.error('Error:', error);
    }
    
    kitchenwareInfos = await kitchenwareInfos.json();
    console.log(kitchenwareInfos);
    
    // Map the owned status
    kitchenwares = kitchenwareInfos.map(groceryInfo => {
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
    kitchenwareTableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
                            <td class="border px-4 py-2">${item.name}</td>
                            <td class="border px-4 py-2">
                                <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="removeItem('${item.name}')">Remove</button>
                            </td>
                        `;
        kitchenwareTableBody.appendChild(row);
    });
}

function itemAdder(){
    document.getElementById('addItemForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;

        // Check if the item already exists
        if (kitchenwares.find(kitchenware => kitchenware.name === name)) {
            alert('Item already exists');
            return;
        }

        // Update the displayed table
        kitchenwares.push({ name,  });
        displayItems(kitchenwares);

        // Update the changelist to be sent to the server
        changeList.push({ name, removed: false });

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

        kitchenwares.sort((a, b) => {
            // Convert to lowercase for case-insensitive comparison
            let valA = a[key].toLowerCase();
            let valB = b[key].toLowerCase();

            if (valA < valB) return lastSort.isAscending ? -1 : 1;
            if (valA > valB) return lastSort.isAscending ? 1 : -1;
            return 0;
        });

        displayItems(kitchenwares);
    };
}

function saveChangesButton() {
    document.getElementById('saveChangesButton').addEventListener('click', function () {
        // Send the change list to the server
        fetch('/admin/dashboard/kitchenware-inventory', {
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
    kitchenwares = kitchenwares.filter(kitchenware => kitchenware.name !== name);
    displayItems(kitchenwares);

    // Update the changelist to be sent to the server
    changeList.push({ name, removed: true});
}

async function fillTable() {
    await loadKitchenwareData();

    const kitchenwareTableBody = document.getElementById('kitchenwareTableBody');
    displayItems(kitchenwares);

    // Adding a new item
    itemAdder();

    // Table's sorting functionality
    sortingFunction();

    // Saving changes functionality
    saveChangesButton();
}

fillTable();
