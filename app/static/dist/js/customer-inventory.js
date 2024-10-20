let lastSort = { key: null, isAscending: true };
changeList = [];
customers = [];

async function loadCustomerData() {

    var customerInfos = {}
    // Fetch all of the customers
    try {
        customerInfos = await fetch('/admin/dashboard/customer-inventory', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

    } catch (error) {
        console.error('Error:', error);
    }

    customerInfos = await customerInfos.json();
    console.log(customerInfos);

    // Map the owned status
    customers = customerInfos.map(customerInfo => {
        const id = customerInfo[0];
        const name = customerInfo[1];
        const surname = customerInfo[2];
        const classYear = customerInfo[3];
        const email = customerInfo[4];
        const residence = customerInfo[5];

        return {
            id: id,
            name: name,
            surname: surname,
            classYear: classYear,
            email: email,
            residence: residence,
        };
    });
}

function displayItems(items) {
    customerTableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
                            <td class="border px-4 py-2">${item.id}</td>
                            <td class="border px-4 py-2">${item.name}</td>
                            <td class="border px-4 py-2">${item.surname}</td>
                            <td class="border px-4 py-2">${item.classYear}</td>
                            <td class="border px-4 py-2">${item.email}</td>
                            <td class="border px-4 py-2">${item.residence}</td>
                            <td class="border px-4 py-2">
                                <button class="bg-red-500 text-white px-4 py-2 rounded" onclick="removeItem('${item.id}')">Remove</button>
                            </td>
                        `;
        customerTableBody.appendChild(row);
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

        customers.sort((a, b) => {
            // Convert to lowercase for case-insensitive comparison
            let valA = a[key].toLowerCase();
            let valB = b[key].toLowerCase();

            if (valA < valB) return lastSort.isAscending ? -1 : 1;
            if (valA > valB) return lastSort.isAscending ? 1 : -1;
            return 0;
        });

        displayItems(customers);
    };
}

function saveChangesButton() {
    document.getElementById('saveChangesButton').addEventListener('click', function () {
        // Send the change list to the server
        fetch('/admin/dashboard/customer-inventory', {
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

function removeItem(id) {
    // Remove the item from the displayed table
    customers = customers.filter(customer => customer.id !== id);
    displayItems(customers);

    // Update the changelist to be sent to the server
    changeList.push({ id });
}



async function fillTable() {
    await loadCustomerData();

    const customerTableBody = document.getElementById('customerTableBody');
    displayItems(customers);

    // Table's sorting functionality
    sortingFunction();

    // Saving changes functionality
    saveChangesButton();
}

fillTable();
