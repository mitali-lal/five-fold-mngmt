// Global chart instance
let totalChart = null;

// Main click handler for attendance buttons
document.addEventListener("click", function (e) {
    const btn = e.target.closest(".btn-attendance");
    if (!btn) return;

    const url = btn.dataset.url;
    if (!url) return;

    console.log("Loading attendance from:", url);
    
    fetch(url)
        .then(res => {
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.text();
        })
        .then(html => {
            const panel = document.getElementById("attendancePanel");
            const content = document.getElementById("attendanceContent");

            if (!panel || !content) {
                console.error("Panel or content element not found!");
                return;
            }

            content.innerHTML = html;
            panel.classList.add("open");

            // Initialize everything
            initializePanel();
        })
        .catch(err => {
            console.error('Error loading attendance:', err);
            alert('Error loading attendance data. Please try again.');
        });
});

// Close panel function
function closePanel() {
    const panel = document.getElementById("attendancePanel");
    if (panel) {
        panel.classList.remove("open");
    }
    
    // Clean up chart
    if (totalChart) {
        totalChart.destroy();
        totalChart = null;
    }
}

// Initialize the entire panel
function initializePanel() {
    console.log("Initializing attendance panel...");
    
    // Set up event listeners
    setupEventListeners();
    
    // Create chart
    createChart();
    
    // Set default time period
    updateForTimePeriod('total');
}

// Set up all event listeners
function setupEventListeners() {
    // Tab switching
    document.querySelectorAll(".att-tab").forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
    
    // Time period selector
    const periodSelect = document.getElementById('timePeriodSelect');
    if (periodSelect) {
        periodSelect.addEventListener('change', function() {
            updateForTimePeriod(this.value);
        });
    }
    
    // Custom range apply button
    const applyBtn = document.querySelector('.btn-apply');
    if (applyBtn) {
        applyBtn.addEventListener('click', applyCustomRange);
    }
}

// Switch between tabs
function switchTab(tabName) {
    // Update active tab
    document.querySelectorAll(".att-tab").forEach(btn => {
        btn.classList.remove("active");
        if (btn.dataset.tab === tabName) btn.classList.add("active");
    });
    
    // Show active content
    document.querySelectorAll(".att-content").forEach(content => {
        content.classList.remove("active");
        if (content.id === `tab-${tabName}`) content.classList.add("active");
    });
    
    // Generate calendar if needed
    if (tabName === 'calendar') {
        const period = document.getElementById('timePeriodSelect').value;
        generateCalendarView(period);
    }
}

// Create and render chart
function createChart() {
    console.log("Creating chart...");
    
    const wrapper = document.querySelector(".attendance-wrapper");
    if (!wrapper) {
        console.error("No attendance wrapper found!");
        return;
    }
    
    // Get data from HTML data attributes
    const present = parseInt(wrapper.dataset.present) || 0;
    const absent = parseInt(wrapper.dataset.absent) || 0;
    
    // Parse week data (still needed for other functionality)
    let weekLabels = [];
    let weekData = [];
    
    try {
        const labelsJson = wrapper.dataset.weekLabels;
        const dataJson = wrapper.dataset.weekData;
        
        if (labelsJson && labelsJson !== 'null' && labelsJson !== 'undefined') {
            weekLabels = JSON.parse(labelsJson);
        }
        
        if (dataJson && dataJson !== 'null' && dataJson !== 'undefined') {
            weekData = JSON.parse(dataJson);
        }
    } catch (error) {
        console.warn("Error parsing week data:", error);
    }
    
    console.log("Chart data loaded:", { present, absent, weekLabels, weekData });
    
    // Destroy existing chart
    if (totalChart) totalChart.destroy();
    
    // Create Total Attendance Chart (Doughnut)
    const totalCanvas = document.getElementById("totalChart");
    if (totalCanvas) {
        const ctx = totalCanvas.getContext('2d');
        totalChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["Present", "Absent"],
                datasets: [{
                    data: [present, absent],
                    backgroundColor: ["#10b981", "#ef4444"],
                    borderWidth: 2,
                    borderColor: '#fff',
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? Math.round((context.raw / total) * 100) : 0;
                                return `${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '65%'
            }
        });
        console.log("Chart created successfully");
    } else {
        console.error("Chart canvas not found!");
    }
}

// Update everything for a specific time period
function updateForTimePeriod(period) {
    console.log("Updating for period:", period);
    
    // Show/hide custom range
    const customRange = document.getElementById('customRange');
    if (period === 'custom') {
        if (customRange) customRange.style.display = 'flex';
        return;
    } else {
        if (customRange) customRange.style.display = 'none';
    }
    
    // Get data for this period
    const data = getDataForPeriod(period);
    
    // Update statistics
    updateStatistics(data);
    
    // Update chart
    updateChart(data);
    
    // Update calendar if on calendar tab
    if (document.querySelector('.att-tab.active').dataset.tab === 'calendar') {
        generateCalendarView(period);
    }
}

// Get data for specific time period
function getDataForPeriod(period) {
    const wrapper = document.querySelector(".attendance-wrapper");
    const basePresent = parseInt(wrapper.dataset.present) || 0;
    const baseAbsent = parseInt(wrapper.dataset.absent) || 0;
    
    let present, absent;
    
    switch(period) {
        case 'week':
            present = 4;  // 4 days present this week
            absent = 1;   // 1 day absent
            break;
        case 'month':
            present = 18; // 18 days present this month
            absent = 4;   // 4 days absent
            break;
        case 'last_month':
            present = 16; // 16 days present last month
            absent = 6;   // 6 days absent
            break;
        default: // total
            present = basePresent;
            absent = baseAbsent;
    }
    
    const total = present + absent;
    const percent = total > 0 ? Math.round((present / total) * 100) : 0;
    
    return { present, absent, total, percent };
}

// Update statistics display
function updateStatistics(data) {
    const { present, absent, total, percent } = data;
    
    // Update stat values
    document.getElementById('stat-present').textContent = present;
    document.getElementById('stat-absent').textContent = absent;
    document.getElementById('stat-total').textContent = total;
    
    // Update progress
    document.getElementById('progress-percent').textContent = percent + '%';
    document.getElementById('progress-fill').style.width = percent + '%';
    
    // Update warning
    const warningBox = document.getElementById('warning-box');
    if (percent < 50) {
        const required = Math.max(0, Math.ceil((0.5 * total - present) / 0.5));
        warningBox.innerHTML = `⚠️ You need <strong id="required-classes">${required}</strong> more classes to reach 50% attendance`;
        warningBox.style.display = 'flex';
    } else {
        warningBox.style.display = 'none';
    }
}

// Update chart with new data
function updateChart(data) {
    const { present, absent } = data;
    
    if (totalChart) {
        totalChart.data.datasets[0].data = [present, absent];
        totalChart.update();
        console.log("Chart updated with new data:", { present, absent });
    }
}

// Generate calendar view
function generateCalendarView(period) {
    const calendarView = document.getElementById('calendarView');
    if (!calendarView) return;
    
    let html = '';
    
    if (period === 'week') {
        html = `
            <div class="week-calendar">
                <div class="week-day present">
                    <div class="week-day-info">
                        <div class="week-day-name">Mon</div>
                        <div class="week-day-date">${getCurrentWeekDay(1)}</div>
                        <div class="week-day-full">Monday</div>
                    </div>
                    <div class="week-status-container">
                        <div class="week-status present">Present</div>
                        ✅
                    </div>
                </div>
                <div class="week-day holiday">
                    <div class="week-day-info">
                        <div class="week-day-name">Tue</div>
                        <div class="week-day-date">${getCurrentWeekDay(2)}</div>
                        <div class="week-day-full">Tuesday (Holiday)</div>
                    </div>
                    <div class="week-status-container">
                        <div class="week-status holiday">Holiday</div>
                        🏖️
                    </div>
                </div>
                <div class="week-day present">
                    <div class="week-day-info">
                        <div class="week-day-name">Wed</div>
                        <div class="week-day-date">${getCurrentWeekDay(3)}</div>
                        <div class="week-day-full">Wednesday</div>
                    </div>
                    <div class="week-status-container">
                        <div class="week-status present">Present</div>
                        ✅
                    </div>
                </div>
                <div class="week-day present">
                    <div class="week-day-info">
                        <div class="week-day-name">Thu</div>
                        <div class="week-day-date">${getCurrentWeekDay(4)}</div>
                        <div class="week-day-full">Thursday</div>
                    </div>
                    <div class="week-status-container">
                        <div class="week-status present">Present</div>
                        ✅
                    </div>
                </div>
                <div class="week-day present">
                    <div class="week-day-info">
                        <div class="week-day-name">Fri</div>
                        <div class="week-day-date">${getCurrentWeekDay(5)}</div>
                        <div class="week-day-full">Friday</div>
                    </div>
                    <div class="week-status-container">
                        <div class="week-status present">Present</div>
                        ✅
                    </div>
                </div>
                <div class="week-day absent">
                    <div class="week-day-info">
                        <div class="week-day-name">Sat</div>
                        <div class="week-day-date">${getCurrentWeekDay(6)}</div>
                        <div class="week-day-full">Saturday</div>
                    </div>
                    <div class="week-status-container">
                        <div class="week-status absent">Absent</div>
                        ❌
                    </div>
                </div>
                <div class="week-day weekend">
                    <div class="week-day-info">
                        <div class="week-day-name">Sun</div>
                        <div class="week-day-date">${getCurrentWeekDay(0)}</div>
                        <div class="week-day-full">Sunday</div>
                    </div>
                    <div class="week-status-container">
                        <div class="week-status holiday">Weekend</div>
                        🏖️
                    </div>
                </div>
            </div>
            <div class="week-summary">
                <h5>This Week Summary</h5>
                <div class="week-stats">
                    <div class="week-stat">
                        <div class="stat-label">Present:</div>
                        <div class="stat-value present">4 days</div>
                    </div>
                    <div class="week-stat">
                        <div class="stat-label">Absent:</div>
                        <div class="stat-value absent">1 day</div>
                    </div>
                    <div class="week-stat">
                        <div class="stat-label">Holidays:</div>
                        <div class="stat-value holiday">2 days</div>
                    </div>
                </div>
            </div>
        `;
    } else if (period === 'month') {
        html = `
            <div class="calendar-header">
                <h4>This Month</h4>
                <div class="calendar-legend">
                    <span class="legend-item"><span class="legend-dot present"></span> Present</span>
                    <span class="legend-item"><span class="legend-dot absent"></span> Absent</span>
                    <span class="legend-item"><span class="legend-dot holiday"></span> Holiday</span>
                </div>
            </div>
            <div class="calendar-grid">
                <div class="calendar-day-header">Sun</div>
                <div class="calendar-day-header">Mon</div>
                <div class="calendar-day-header">Tue</div>
                <div class="calendar-day-header">Wed</div>
                <div class="calendar-day-header">Thu</div>
                <div class="calendar-day-header">Fri</div>
                <div class="calendar-day-header">Sat</div>
                
                <!-- Sample month calendar -->
                <div class="calendar-day weekend">1</div>
                <div class="calendar-day present">2</div>
                <div class="calendar-day holiday">3</div>
                <div class="calendar-day present">4</div>
                <div class="calendar-day present">5</div>
                <div class="calendar-day present">6</div>
                <div class="calendar-day weekend">7</div>
                <div class="calendar-day present">8</div>
                <div class="calendar-day holiday">9</div>
                <div class="calendar-day present">10</div>
                <div class="calendar-day present">11</div>
                <div class="calendar-day present">12</div>
                <div class="calendar-day weekend">13</div>
                <div class="calendar-day absent">14</div>
                <div class="calendar-day holiday">15</div>
                <div class="calendar-day present">16</div>
                <div class="calendar-day present">17</div>
                <div class="calendar-day present">18</div>
                <div class="calendar-day weekend">19</div>
                <div class="calendar-day present">20</div>
                <div class="calendar-day holiday">21</div>
                <div class="calendar-day present">22</div>
                <div class="calendar-day present">23</div>
                <div class="calendar-day present">24</div>
                <div class="calendar-day weekend">25</div>
                <div class="calendar-day absent">26</div>
                <div class="calendar-day holiday">27</div>
                <div class="calendar-day present">28</div>
                <div class="calendar-day present">29</div>
                <div class="calendar-day present">30</div>
                <div class="calendar-day weekend">31</div>
            </div>
        `;
    } else {
        html = `
            <div class="calendar-placeholder">
                <h4>${period === 'month' ? 'This Month' : period === 'last_month' ? 'Last Month' : 'Total'} Attendance</h4>
                <p>${period === 'week' ? '4 days present, 1 absent, 2 holidays' : 
                   period === 'month' ? '18 days present, 4 absent' : 
                   period === 'last_month' ? '16 days present, 6 absent' : 
                   'Overall attendance summary'}</p>
            </div>
        `;
    }
    
    calendarView.innerHTML = html;
}

// Helper function to get current week day dates
function getCurrentWeekDay(dayOffset) {
    const today = new Date();
    const currentDay = today.getDay(); // 0 = Sunday, 1 = Monday, etc.
    const diff = dayOffset - currentDay;
    const targetDate = new Date(today);
    targetDate.setDate(today.getDate() + diff);
    return targetDate.getDate();
}

// Apply custom date range
function applyCustomRange() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    if (startDate && endDate) {
        alert(`Custom range selected: ${startDate} to ${endDate}\n\nThis would filter attendance data in a real implementation.`);
    } else {
        alert('Please select both start and end dates.');
    }
}

// Close panel when clicking outside (optional)
document.addEventListener('click', function(e) {
    const panel = document.getElementById("attendancePanel");
    if (panel && panel.classList.contains('open')) {
        if (!panel.contains(e.target) && !e.target.closest('.btn-attendance')) {
            closePanel();
        }
    }
});

// Close with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closePanel();
    }
});