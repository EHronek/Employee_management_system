// Check-In/Check-Out Logic
const checkInOutButton = document.getElementById('checkInOutButton');
const checkInStatus = document.getElementById('checkInStatus');
let isCheckedIn = false;

checkInOutButton.addEventListener('click', () => {
    if (isCheckedIn) {
        checkInOutButton.innerHTML = '<i class="fas fa-clock"></i>Check In';
        checkInStatus.textContent = 'You are currently checked out.';
        isCheckedIn = false;
    } else {
        checkInOutButton.innerHTML = '<i class="fas fa-clock"></i>Check Out';
        checkInStatus.textContent = 'You checked in at ' + new Date().toLocaleTimeString();
        isCheckedIn = true;
    }
});

// Chart.js for Monthly Attendance Summary
const attendanceBarChart = new Chart(document.getElementById('attendanceBarChart'), {
    type: 'bar',
    data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [{
            label: 'Hours Worked',
            data: [40, 38, 42, 35],
            backgroundColor: '#2563eb',
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 50, // Set a fixed maximum value for the y-axis
                ticks: {
                    stepSize: 10, // Set step size for y-axis ticks
                }
            }
        }
    }
});
