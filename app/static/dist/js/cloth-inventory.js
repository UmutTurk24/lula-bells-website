let lastSort = { key: null, isAscending: true };
changeList = [];
clothes = [];

async function loadClothingData() {

    var clothInfos = {}
    // Fetch all of the clothes
    try {
        clothInfos = await fetch('/admin/dashboard/cloth-inventory', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });;
    
    } catch (error) {
        console.error('Error:', error);
    }
    
    clothInfos = await clothInfos.json();
    
    // Map the owned status
    clothes = clothInfos.map(clothInfo => {
        const name = clothInfo[0];
        return {
            name: name,
        };
    });
}

function displayItems(items) {
    clothTableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
                            <td class="border px-4 py-2">${item.name}</td>
                            <td class="border px-4 py-2">
                                <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="removeItem('${item.name}')">Remove</button>
                            </td>
                        `;
        clothTableBody.appendChild(row);
    });
}

function itemAdder(){
    document.getElementById('addItemForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;

        // Check if the item already exists
        if (clothes.find(cloth => cloth.name === name)) {
            alert('Item already exists');
            return;
        }

        // Update the displayed table
        clothes.push({ name });
        displayItems(clothes);

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

        clothes.sort((a, b) => {
            // Convert to lowercase for case-insensitive comparison
            let valA = a[key].toLowerCase();
            let valB = b[key].toLowerCase();

            if (valA < valB) return lastSort.isAscending ? -1 : 1;
            if (valA > valB) return lastSort.isAscending ? 1 : -1;
            return 0;
        });

        displayItems(clothes);
    };
}

function saveChangesButton() {
    document.getElementById('saveChangesButton').addEventListener('click', function () {
        // Send the change list to the server
        fetch('/admin/dashboard/cloth-inventory', {
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
    clothes = clothes.filter(cloth => cloth.name !== name);
    displayItems(clothes);

    // Update the changelist to be sent to the server
    changeList.push({ name, removed: true});
}

async function fillTable() {
    await loadClothingData();

    const clothTableBody = document.getElementById('clothTableBody');
    displayItems(clothes);

    // Adding a new item
    itemAdder();

    // Table's sorting functionality
    sortingFunction();

    // Saving changes functionality
    saveChangesButton();
}

fillTable();
