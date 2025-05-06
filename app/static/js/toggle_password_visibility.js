function togglePasswordVisiblity(passwordID, iconID) {
    const field = document.getElementById(passwordID);
    const icon = document.getElementById(iconID);
    
    if (field.getAttribute("type") == "password") {
        icon.classList.replace("fa-eye", "fa-eye-slash");
        field.setAttribute("type", "text");
    } else {
        icon.classList.replace("fa-eye-slash", "fa-eye");
        field.setAttribute("type", "password");
    }
}