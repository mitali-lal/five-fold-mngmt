document.addEventListener("DOMContentLoaded", () => {

    /* TAB SWITCHING */
    document.querySelectorAll(".tab").forEach(tab => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            tab.classList.add("active");
            document.getElementById(tab.dataset.tab + "-content").classList.add("active");
        });
    });

    /* DUMMY STUDENTS */
    const list = document.getElementById("studentList");
    document.getElementById("addDummyStudentBtn")?.addEventListener("click", () => {
        const name = prompt("Enter student name:");
        if (!name) return;
        const li = document.createElement("li");
        li.textContent = `${name} (Temporary)`;
        list.appendChild(li);
    });

    /* SAVE CONFIRMATION */
    const dialog = document.getElementById("confirmDialog");
    document.getElementById("saveBtn").onclick = () => dialog.classList.add("show");
    document.getElementById("confirmCancel").onclick = () => dialog.classList.remove("show");

    document.getElementById("confirmSave").onclick = () => {
        dialog.classList.remove("show");
        alert("Changes saved (backend integration later)");
    };

    document.getElementById("cancelBtn").onclick = () => location.reload();
});
