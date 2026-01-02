// browse_activities.js - COMPLETE WORKING VERSION

class BrowseActivities {
    constructor() {
        this.searchTimeout = null;
        this.currentSearch = '';
        this.currentFilter = 'all';
        this.allCards = [];
    }

    initialize() {
        console.log('Initializing BrowseActivities...');
        
        // Collect all cards first
        this.collectAllCards();
        
        // Setup everything
        this.updateSeatIndicators();
        this.setupSearch();
        this.setupFilters();
        this.setupCardClicks();
        
        console.log('BrowseActivities initialized with', this.allCards.length, 'cards');
    }

    collectAllCards() {
        this.allCards = Array.from(document.querySelectorAll('.activity-card'));
        console.log('Collected', this.allCards.length, 'activity cards');
    }


    updateSeatIndicators() {
        console.log('Updating seat indicators...');
        document.querySelectorAll('.seats-fill').forEach(fill => {
            const filled = parseInt(fill.dataset.seatsFilled);
            const total = parseInt(fill.dataset.seatsTotal);
            
            if (total > 0) {
                const percentage = (filled / total) * 100;
                fill.style.width = `${percentage}%`;
                
                // Update color based on availability
                if (percentage >= 100) {
                    fill.style.background = 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)';
                }
            } else {
                fill.style.width = '0%';
            }
        });
    }

    setupSearch() {
        const searchInput = document.getElementById('searchInput');
        if (!searchInput) {
            console.error('Search input not found!');
            return;
        }

        console.log('Setting up search...');
        searchInput.addEventListener('input', (e) => {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                this.currentSearch = e.target.value.toLowerCase().trim();
                console.log('Searching for:', this.currentSearch);
                this.applyAllFilters();
            }, 300);
        });
    }

    setupFilters() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        if (filterButtons.length === 0) {
            console.error('Filter buttons not found!');
            return;
        }

        console.log('Setting up filters...');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                console.log('Filter clicked:', btn.dataset.filter);
                
                // Update active filter
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Apply filter
                this.currentFilter = btn.dataset.filter;
                this.applyAllFilters();
            });
        });
    }

    applyAllFilters() {
        console.log('Applying filters - Search:', this.currentSearch, 'Filter:', this.currentFilter);
        
        let visibleCount = 0;
        
        this.allCards.forEach(card => {
            let shouldShow = true;
            
            // Apply fold filter
            if (this.currentFilter !== 'all') {
                const fold = card.dataset.fold;
                if (fold !== this.currentFilter) {
                    shouldShow = false;
                }
            }
            
            // Apply search filter
            if (shouldShow && this.currentSearch) {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const teacher = card.querySelector('.teacher-name').textContent.toLowerCase();
                const foldBadge = card.querySelector('.fold-badge').textContent.toLowerCase();
                
                const matchesSearch = title.includes(this.currentSearch) || 
                                     teacher.includes(this.currentSearch) || 
                                     foldBadge.includes(this.currentSearch);
                
                if (!matchesSearch) {
                    shouldShow = false;
                }
            }
            
            // Update display
            card.style.display = shouldShow ? 'flex' : 'none';
            if (shouldShow) visibleCount++;
        });
        
        console.log('Filter result:', visibleCount, 'cards visible');
    }

    setupCardClicks() {
        console.log('Setting up card clicks...');
        document.addEventListener('click', (e) => {
            const card = e.target.closest('.activity-card');
            if (card && !e.target.closest('.btn-register')) {
                const activityId = card.dataset.id;
                console.log('Card clicked, navigating to activity:', activityId);
                window.location.href = `/activities/student/activity/${activityId}/`;
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Starting BrowseActivities...');
    try {
        const browseApp = new BrowseActivities();
        browseApp.initialize();
        window.browseApp = browseApp;
        console.log('BrowseActivities initialized successfully!');
    } catch (error) {
        console.error('Error initializing BrowseActivities:', error);
    }
});