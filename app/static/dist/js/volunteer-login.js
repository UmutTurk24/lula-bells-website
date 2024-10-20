

document.getElementById('volunteer-login-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the default form submission

    const username = document.getElementById('volunteer-username').value;
    const password = document.getElementById('volunteer-password').value;

    await fetch('/volunteer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.result == 0) {
                window.location.replace("https://127.0.0.1:5010/inventory");
            } else {
                window.alert('Incorrect username and/or password');
            }
        })
});