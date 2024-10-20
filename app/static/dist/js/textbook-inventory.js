let lastSort = { key: null, isAscending: true };
changeList = [];
textbooks = [];

async function loadTextbookData() {

    var textbookInfos = {}
    // Fetch all of the textbooks
    try {
        textbookInfos = await fetch('/admin/dashboard/textbook-inventory', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });;
    
    } catch (error) {
        console.error('Error:', error);
    }
    
    textbookInfos = await textbookInfos.json();
    
    // Map the owned status
    textbooks = textbookInfos.map(textbookInfo => {
        const name = textbookInfo[0];
        const owned = textbookInfo[1] === 0 ? 'Not Owned' : 'Owned';
        return {
            name: name,
            ownedStatus: owned
        };
    });
}

function displayItems(items) {
    textbookTableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
                            <td class="border px-4 py-2">${item.name}</td>
                            <td class="border px-4 py-2">${item.ownedStatus}</td>
                            <td class="border px-4 py-2">
                                <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="removeItem('${item.name}')">Remove</button>
                            </td>
                        `;
        textbookTableBody.appendChild(row);
    });
}

function itemAdder(){
    document.getElementById('addItemForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const ownedStatus = document.getElementById('ownedStatus').checked;

        // Check if the item already exists
        if (textbooks.find(textbook => textbook.name === name)) {
            alert('Item already exists');
            return;
        }

        // Update the displayed table
        textbooks.push({ name, ownedStatus: ownedStatus ? 'Owned' : 'Not Owned'});
        displayItems(textbooks);

        // Update the changelist to be sent to the server
        changeList.push({ name, ownedStatus, removed: false });

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

        textbooks.sort((a, b) => {
            // Convert to lowercase for case-insensitive comparison
            let valA = a[key].toLowerCase();
            let valB = b[key].toLowerCase();

            if (valA < valB) return lastSort.isAscending ? -1 : 1;
            if (valA > valB) return lastSort.isAscending ? 1 : -1;
            return 0;
        });

        displayItems(textbooks);
    };
}

function saveChangesButton() {
    document.getElementById('saveChangesButton').addEventListener('click', function () {
        // Send the change list to the server
        fetch('/admin/dashboard/textbook-inventory', {
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
    textbooks = textbooks.filter(textbook => textbook.name !== name);
    displayItems(textbooks);

    // Update the changelist to be sent to the server
    changeList.push({ name, ownedStatus, removed: true});
}

async function fillTable() {
    await loadTextbookData();

    const textbookTableBody = document.getElementById('textbookTableBody');
    displayItems(textbooks);

    // Adding a new item
    itemAdder();

    // Table's sorting functionality
    sortingFunction();

    // Saving changes functionality
    saveChangesButton();
}

fillTable();
