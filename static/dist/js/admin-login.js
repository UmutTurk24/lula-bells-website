

document.getElementById('admin-login-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the default form submission

    const username = document.getElementById('admin-username').value;
    const password = document.getElementById('admin-password').value;

    await fetch('/admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result == 0) {
            window.location.replace("https://127.0.0.1:5000/admin/dashboard");
        } else {
            window.alert('Incorrect username and/or password');

        }

    })

    

});