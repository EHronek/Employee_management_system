// Chart.js for Attendance Trends
const attendanceLineChart = new Chart(document.getElementById('attendanceLineChart'), {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Hours Worked',
            data: [160, 150, 170, 165, 180, 175],
            borderColor: '#2563eb',
            fill: false,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 200, // Set a fixed maximum value for the y-axis
                ticks: {
                    stepSize: 25, // Set step size for y-axis ticks
                }
            }
        }
    }
});

// Chart.js for Performance Metrics
const performanceBarChart = new Chart(document.getElementById('performanceBarChart'), {
    type: 'bar',
    data: {
        labels: ['Communication', 'Teamwork', 'Productivity', 'Leadership'],
        datasets: [{
            label: 'Performance Rating',
            data: [4.5, 4.0, 4.7, 4.2],
            backgroundColor: '#2563eb',
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 5, // Set a fixed maximum value for the y-axis
                ticks: {
                    stepSize: 1, // Set step size for y-axis ticks
                }
            }
        }
    }
});
