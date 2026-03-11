document.addEventListener("DOMContentLoaded", () => {
    const percentages = document.querySelectorAll(".attendance-percent");
    let total = 0;

    percentages.forEach(p => {
        total += parseInt(p.dataset.value);
    });

    const avg = percentages.length ? (total / percentages.length).toFixed(1) : 0;
    document.getElementById("avgAttendance").innerText = avg;
});
