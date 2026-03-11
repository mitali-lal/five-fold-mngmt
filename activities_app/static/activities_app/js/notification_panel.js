function toggleNotifications() {
    const panel = document.getElementById("notification-panel");
    const overlay = document.getElementById("notification-overlay");

    if (!panel || !overlay) return;

    panel.classList.toggle("open");
    overlay.classList.toggle("open");
}
