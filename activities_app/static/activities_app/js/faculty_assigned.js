document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const searchInput = document.getElementById('searchInput');
    const filterStatus = document.getElementById('filterStatus');
    const sortActivities = document.getElementById('sortActivities');
    const clearFilters = document.getElementById('clearFilters');
    const cards = document.querySelectorAll('.activity-card');
    const activityGrid = document.getElementById('activityGrid');
    const viewButtons = document.querySelectorAll('.view-btn');
    const totalStudentsElement = document.getElementById('totalStudents');

    // Initialize view toggle
    viewButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const view = this.dataset.view;
            viewButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            if (view === 'list') {
                activityGrid.classList.add('list-view');
            } else {
                activityGrid.classList.remove('list-view');
            }
        });
    });

    // Calculate total students
    function calculateTotalStudents() {
        let total = 0;
        cards.forEach(card => {
            const studentCount = parseInt(card.dataset.students) || 0;
            total += studentCount;
        });
        if (totalStudentsElement) {
            totalStudentsElement.textContent = total;
        }
    }

    // Initialize total students
    calculateTotalStudents();

    // Search and Filter Functionality
    function performSearch() {
        const searchQuery = searchInput.value.toLowerCase().trim();
        const statusFilter = filterStatus.value;
        const sortBy = sortActivities.value;
        
        let filteredCards = Array.from(cards);
        
        // Apply search filter
        if (searchQuery) {
            filteredCards = filteredCards.filter(card => {
                const title = card.dataset.title;
                const category = card.dataset.category;
                return title.includes(searchQuery) || category.includes(searchQuery);
            });
        }
        
        // Apply status filter
        if (statusFilter !== 'all') {
            filteredCards = filteredCards.filter(card => {
                const statusElement = card.querySelector('.badge-status');
                return statusElement.classList.contains(statusFilter);
            });
        }
        
        // Sort cards
        switch(sortBy) {
            case 'title':
                filteredCards.sort((a, b) => {
                    const titleA = a.querySelector('.activity-title').textContent.toLowerCase();
                    const titleB = b.querySelector('.activity-title').textContent.toLowerCase();
                    return titleA.localeCompare(titleB);
                });
                break;
                
            case 'students':
                filteredCards.sort((a, b) => {
                    const studentsA = parseInt(a.dataset.students) || 0;
                    const studentsB = parseInt(b.dataset.students) || 0;
                    return studentsB - studentsA;
                });
                break;
                
            default:
                // Default order (as in HTML)
                break;
        }
        
        // Update UI
        updateCardVisibility(filteredCards);
        updateActivityCount(filteredCards);
    }

    function updateCardVisibility(visibleCards) {
        // First hide all cards
        cards.forEach(card => {
            card.style.display = 'none';
            card.classList.remove('visible');
        });
        
        // Show filtered cards with animation
        visibleCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.display = 'block';
                card.classList.add('visible');
            }, index * 50);
        });
        
        // Reorder cards in grid
        if (activityGrid) {
            visibleCards.forEach(card => {
                activityGrid.appendChild(card);
            });
        }
    }

    function updateActivityCount(visibleCards) {
        const countElement = document.querySelector('.activity-info h3');
        if (countElement) {
            countElement.textContent = `${visibleCards.length} Activities Assigned`;
        }
    }

    // Clear all filters
    function clearAllFilters() {
        searchInput.value = '';
        filterStatus.value = 'all';
        sortActivities.value = 'date';
        performSearch();
    }

    // Setup button click handlers
    function setupButtonHandlers() {
        // Resource Request buttons
        

        
    }

    // Add animation styles
    function addAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .activity-card {
                opacity: 0;
                transform: translateY(10px);
                transition: opacity 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .activity-card.visible {
                opacity: 1;
                transform: translateY(0);
            }
            
            .action-btn {
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .badge-type {
                transition: all 0.2s ease;
            }
            
            .activity-card:hover .badge-type {
                transform: scale(1.05);
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .activity-card.visible {
                animation: fadeIn 0.4s ease forwards;
            }
        `;
        document.head.appendChild(style);
    }

    // Event Listeners
    searchInput.addEventListener('input', performSearch);
    filterStatus.addEventListener('change', performSearch);
    sortActivities.addEventListener('change', performSearch);
    clearFilters.addEventListener('click', clearAllFilters);

    // Initialize
    addAnimationStyles();
    setupButtonHandlers();
    
    // Animate cards on load
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('visible');
        }, index * 100);
    });

    // Perform initial search
    performSearch();
});