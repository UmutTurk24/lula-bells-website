// Function to show the modal
function showModal(visitDetails) {
    const modal = document.getElementById('visitModal');
    const visitDetailsElement = document.getElementById('visitDetails');
    visitDetailsElement.textContent = visitDetails;
    modal.classList.remove('hidden');
}

// Function to hide the modal
function hideModal() {
    const modal = document.getElementById('visitModal');
    modal.classList.add('hidden');
}

// Close the modal when clicking outside the modal
window.addEventListener('click', function (event) {
    const modal = document.getElementById('visitModal');
    if (event.target === modal) {
        hideModal();
    }
});