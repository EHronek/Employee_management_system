        // Open Announcement Details Modal
        function openModal() {
            document.getElementById('announcementModal').style.display = 'flex';
        }

        // Close Announcement Details Modal
        function closeModal() {
            document.getElementById('announcementModal').style.display = 'none';
        }

        // Close modal when clicking outside the modal content
        window.onclick = function (event) {
            const modal = document.getElementById('announcementModal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };