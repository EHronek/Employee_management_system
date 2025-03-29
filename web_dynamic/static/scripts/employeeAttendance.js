document.addEventListener("DOMContentLoaded", function () {
    const checkInOutButton = document.getElementById("checkInOutButton");
    const checkInStatus = document.getElementById("checkInStatus");

    checkInOutButton.addEventListener("click", function () {
        const action = checkInOutButton.getAttribute("data-action");

        fetch("/employees/attendance", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `action=${action}`,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (action === "checkin") {
                    checkInOutButton.innerHTML = '<i class="fas fa-clock"></i> Check Out';
                    checkInOutButton.setAttribute("data-action", "checkout");
                    checkInStatus.textContent = "You are currently checked in.";
                    location.reload();
                } else {
                    checkInOutButton.innerHTML = '<i class="fas fa-clock"></i> Check In';
                    checkInOutButton.setAttribute("data-action", "checkin");
                    checkInStatus.textContent = "You are currently checked out.";
                    location.reload();
                }
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
