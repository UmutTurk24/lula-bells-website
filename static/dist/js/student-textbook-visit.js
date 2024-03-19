console.log('student-textbook-visit.js is being executed');


async function showAcademicModalMenu() {
    const academicModalMenu = document.getElementById('academicModalMenu');

    // Fetch all of the textbooks
    try {
        const response = fetch('/get-textbooks', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }

    academicModalMenu.classList.remove('hidden');
    
    // var textbookInfos = showAcademicModalMenu();
}


// Function to hide the pop-up menu
function hideAcademicPopupMenu() {
    const academicModalMenu = document.getElementById('academicModalMenu');
    academicModalMenu.classList.add('hidden');
}

// Function to save and exit
function saveAndExit() {
    // You can write your logic here to save selected textbooks and exit
    // For example, you can get selected textbooks and send them to the server
    console.log('Save and exit');
    hideAcademicPopupMenu();
}

// Event listener to hide the pop-up menu when clicking outside of it
document.addEventListener('click', function (event) {
    const academicModalMenu = document.getElementById('academicModalMenu');
    const triggerAcademicPopup = document.getElementById('triggerAcademicPopup');
    if (!academicModalMenu.contains(event.target) && !triggerAcademicPopup.contains(event.target)) {
        hideAcademicPopupMenu();
    }
});