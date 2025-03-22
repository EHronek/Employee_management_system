
        // Initialize Select2 for searchable dropdowns
        $(document).ready(function () {
            $('.searchable-dropdown').select2({
                placeholder: "Select an option",
                allowClear: true
            });
        });

        // Form Validation
        const form = document.getElementById('editEmployeeForm');
        const requiredFields = form.querySelectorAll('input[required], select[required]');

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            let isValid = true;

            // Validate required fields
            requiredFields.forEach(field => {
                if (!field.value) {
                    field.closest('.form-group').classList.add('invalid');
                    isValid = false;
                } else {
                    field.closest('.form-group').classList.remove('invalid');
                }
            });

            // Validate employment status
            const employmentStatus = form.querySelector('input[name="employmentStatus"]:checked');
            if (!employmentStatus) {
                form.querySelector('.radio-group').closest('.form-group').classList.add('invalid');
                isValid = false;
            } else {
                form.querySelector('.radio-group').closest('.form-group').classList.remove('invalid');
            }

            if (isValid) {
                // Show loading indicator
                const submitButton = form.querySelector('button[type="submit"]');
                submitButton.disabled = true;
                submitButton.querySelector('.loading-indicator').classList.add('active');

                // Simulate form submission (replace with actual API call)
                setTimeout(() => {
                    alert('Employee details updated successfully!');
                    submitButton.disabled = false;
                    submitButton.querySelector('.loading-indicator').classList.remove('active');
                }, 2000);
            }
        });