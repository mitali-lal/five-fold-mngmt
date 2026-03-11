// Tabs
document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

        tab.classList.add("active");
        document.getElementById(tab.dataset.tab + "-content").classList.add("active");
    });
});

// Delete dialog
const deleteBtn = document.getElementById("deleteBtn");
const deleteDialog = document.getElementById("deleteDialog");
const cancelDelete = document.getElementById("cancelDelete");

deleteBtn.addEventListener("click", () => {
    deleteDialog.classList.add("show");
});

cancelDelete.addEventListener("click", () => {
    deleteDialog.classList.remove("show");
});

// Dirty form warning
let formChanged = false;
document.querySelectorAll("input, textarea").forEach(el => {
    el.addEventListener("change", () => formChanged = true);
});

window.addEventListener("beforeunload", function (e) {
    if (formChanged) {
        e.preventDefault();
        e.returnValue = "";
    }
});
