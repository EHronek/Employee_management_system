// Initialize Select2 for searchable dropdown
$(document).ready(function () {
    $('.searchable-dropdown').select2({
        placeholder: "Select a manager",
        allowClear: true
    });
});

// Form Validation
const form = document.getElementById('newDepartmentForm');
const departmentNameInput = document.getElementById('departmentName');
const errorMessage = document.querySelector('.error-message');

departmentNameInput.addEventListener('input', () => {
    if (departmentNameInput.value.length > 128) {
        departmentNameInput.parentElement.classList.add('invalid');
    } else {
        departmentNameInput.parentElement.classList.remove('invalid');
    }
});

// Form Submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Show loading indicator
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.querySelector('.loading-indicator').classList.add('active');

    // Simulate form submission (replace with actual API call)
    setTimeout(() => {
        alert('Department created successfully!');
        submitButton.disabled = false;
        submitButton.querySelector('.loading-indicator').classList.remove('active');
        form.reset();
    }, 2000);
});