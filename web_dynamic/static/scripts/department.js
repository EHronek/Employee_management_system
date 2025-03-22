        // Chart.js for Department Analytics
    const ctx = document.getElementById('departmentChart').getContext('2d');
    const departmentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['HR', 'IT', 'Finance', 'Marketing', 'Operations'],
            datasets: [{
                label: 'Budget Allocation',
                data: [500000, 750000, 600000, 450000, 800000],
                backgroundColor: '#2563eb',
                borderColor: '#1e40af',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Open Create New Department Form
    const createDepartmentBtn = document.querySelector('.create-department-btn');
    createDepartmentBtn.addEventListener('click', () => {
        alert('Open Create New Department Form');
        // Replace with modal or form logic
    });
