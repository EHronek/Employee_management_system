
// Form Submission
const leaveRequestForm = document.getElementById('leaveRequestForm');
leaveRequestForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Leave request submitted successfully!');
    leaveRequestForm.reset();
});

// Cancel Leave Request
const cancelButtons = document.querySelectorAll('.leave-request-status .status-card.pending button');
cancelButtons.forEach(button => {
    button.addEventListener('click', () => {
        if (confirm('Are you sure you want to cancel this leave request?')) {
            alert('Leave request canceled successfully!');
        }
    });
});