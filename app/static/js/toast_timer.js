// Initialize all toasts when the page loads
document.addEventListener('DOMContentLoaded', function () {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toastEl => {
        const toast = new bootstrap.Toast(toastEl);
        toast.show(); // Auto-shows + starts timer
    });
});