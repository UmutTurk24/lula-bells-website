let lastSort = { key: null, isAscending: true };
changeList = [];
users = [];

async function loadUserData() {

    var userInfos = {}
    // Fetch all of the users
    try {
        userInfos = await fetch('/admin/dashboard/user-inventory', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

    } catch (error) {
        console.error('Error:', error);
    }

    userInfos = await userInfos.json();
    console.log(userInfos);

    // Map the owned status
    users = userInfos.map(userInfo => {
        const name = userInfo[1];
        const role = userInfo[3];

        return {
            name: name,
            role: role,
        };
    });
}

function displayItems(items) {
    userTableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
                            <td class="border px-4 py-2">${item.name}</td>
                            <td class="border px-4 py-2">${item.role}</td>
                            <td class="border px-4 py-2">
                                <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="removeItem('${item.name}')">Remove</button>
                                <button class="bg-blue-500 text-white px-4 py-2 rounded" onclick="editItem('${item.name}')">Edit</button>
                            </td>
                        `;
        userTableBody.appendChild(row);
    });
}

function itemAdder() {
    document.getElementById('addItemForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;

        // Check if the item already exists
        if (users.find(user => user.name === username)) {
            alert('Item already exists');
            return;
        }

        // Update the displayed table
        users.push({ username, role, });
        displayItems(users);

        // Update the changelist to be sent to the server
        changeList.push({ username, password, role, opCode: 0 });

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

        users.sort((a, b) => {
            // Convert to lowercase for case-insensitive comparison
            let valA = a[key].toLowerCase();
            let valB = b[key].toLowerCase();

            if (valA < valB) return lastSort.isAscending ? -1 : 1;
            if (valA > valB) return lastSort.isAscending ? 1 : -1;
            return 0;
        });

        displayItems(users);
    };
}

function saveChangesButton() {
    document.getElementById('saveChangesButton').addEventListener('click', function () {
        // Send the change list to the server
        fetch('/admin/dashboard/user-inventory', {
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
    users = users.filter(user => user.name !== name);
    displayItems(users);

    // Update the changelist to be sent to the server
    changeList.push({ username: name, password: 0, role: 'user', opCode: 1 });
}

function editItem(name) {
    // Change the quantity and/or cost of the item
    users = users.map(user => {
        if (user.name === name) {
            user.role = prompt('Enter the new role (admin or user):', user.role);
            while (user.role !== 'admin' && user.role !== 'user') {
                user.role = prompt('Enter the new role (admin or user):', user.role);
            }
        }
        return user;
    });

    displayItems(users);

    // Get the new quantity and cost
    const role = users.find(user => user.name === name).role;

    // Update the changelist to be sent to the server
    changeList.push({ username: name, password: 0, role, opCode: 2 });
}

async function fillTable() {
    await loadUserData();

    const userTableBody = document.getElementById('userTableBody');
    displayItems(users);

    // Adding a new item
    itemAdder();

    // Table's sorting functionality
    sortingFunction();

    // Saving changes functionality
    saveChangesButton();
}

fillTable();
