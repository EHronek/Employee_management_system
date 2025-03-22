// Open Change Password Modal
document.getElementById('changePasswordBtn').addEventListener('click', function() {
    document.getElementById('changePasswordModal').style.display = 'block';
  });
  
  // Close Modal
  document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('changePasswordModal').style.display = 'none';
  });
  
  // Handle Change Password Form Submission
  document.getElementById('changePasswordForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
  
    if (newPassword !== confirmPassword) {
      alert('New passwords do not match!');
      return;
    }
  
    // Simulate password change (replace with API call)
    alert('Password changed successfully!');
    document.getElementById('changePasswordModal').style.display = 'none';
  });
  
  // Handle Personal Info Form Submission
  document.getElementById('personalInfoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Personal information updated successfully!');
  });