// activity_detail.js - FOR 3-COLUMN LAYOUT

class ActivityDetail {
    constructor() {
        // Get activity ID from the URL
        const pathParts = window.location.pathname.split('/');
        this.activityId = pathParts[pathParts.length - 2];
        console.log('Activity ID:', this.activityId);
        this.initialize();
    }

    initialize() {
        console.log('Initializing ActivityDetail for 3-column layout...');
        
        // Store activity ID
        localStorage.setItem('currentActivityId', this.activityId);
        
        // Setup everything
        this.setupTabs();
        this.setupRating();
        this.setupButtons();
        this.loadFeedbacks();
        
        console.log('ActivityDetail initialized successfully');
    }

    setupTabs() {
        console.log('Setting up vertical tabs...');
        const tabs = document.querySelectorAll('.tab');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabId = tab.getAttribute('data-tab');
                console.log('Tab clicked:', tabId);
                
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked tab
                tab.classList.add('active');
                
                // Show corresponding content
                const content = document.getElementById(`${tabId}-content`);
                if (content) {
                    content.classList.add('active');
                    console.log('Showing content for:', tabId);
                }
            });
        });
        
        // Activate first tab by default
        if (tabs.length > 0) {
            tabs[0].classList.add('active');
            tabContents[0].classList.add('active');
        }
    }


    setupRating() {
        console.log('Setting up rating stars...');
        const stars = document.querySelectorAll('.star');
        stars.forEach(star => {
            star.addEventListener('click', () => {
                const rating = star.getAttribute('data-rating');
                console.log('Star clicked, rating:', rating);
                this.setRating(rating);
            });
        });
    }

    setRating(rating) {
        console.log('Setting rating to:', rating);
        const stars = document.querySelectorAll('.star');
        stars.forEach(star => {
            const starRating = parseInt(star.getAttribute('data-rating'));
            if (starRating <= rating) {
                star.classList.add('active');
                star.textContent = '★';
            } else {
                star.classList.remove('active');
                star.textContent = '☆';
            }
        });
        const ratingInput = document.getElementById('rating');
        if (ratingInput) {
            ratingInput.value = rating;
        }
    }

    setupButtons() {
        console.log('Setting up all buttons...');
        
        // Register button
        const registerBtn = document.getElementById('registerBtn');
        if (registerBtn) {
            registerBtn.addEventListener('click', () => {
                console.log('Register button clicked');
                this.openRegisterDialog();
            });
        }
        
        // Share button
        const shareBtn = document.getElementById('shareBtn');
        if (shareBtn) {
            shareBtn.addEventListener('click', () => {
                console.log('Share button clicked');
                this.shareActivity();
            });
        }
        
        // Print button
        const printBtn = document.getElementById('printBtn');
        if (printBtn) {
            printBtn.addEventListener('click', () => {
                console.log('Print button clicked');
                window.print();
            });
        }
        
        // Cancel button
        const cancelBtn = document.getElementById('cancelBtn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                console.log('Cancel button clicked');
                this.closeRegisterDialog();
            });
        }
        
        // Confirm button
        const confirmBtn = document.getElementById('confirmBtn');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', () => {
                console.log('Confirm button clicked');
            });
        }
        
        // Submit feedback button
        const submitFeedbackBtn = document.getElementById('submitFeedbackBtn');
        if (submitFeedbackBtn) {
            submitFeedbackBtn.addEventListener('click', () => {
                console.log('Submit feedback button clicked');
                this.submitFeedback();
            });
        }
    }

    loadFeedbacks() {
        console.log('Loading feedbacks...');
        const feedbacks = JSON.parse(localStorage.getItem('activityFeedbacks') || '{}');
        const activityFeedbacks = feedbacks[this.activityId] || [];
        const feedbackList = document.getElementById('feedbackList');
        
        if (feedbackList && activityFeedbacks.length > 0) {
            const feedbackItems = activityFeedbacks.map(fb => `
                <div class="feedback-item">
                    <div class="feedback-meta">
                        <span>${new Date(fb.timestamp).toLocaleDateString()}</span>
                        <span>${'★'.repeat(fb.rating)}${'☆'.repeat(5 - fb.rating)}</span>
                    </div>
                    <p>${fb.comment}</p>
                </div>
            `).join('');
            
            // Add to existing feedbacks
            feedbackList.innerHTML += feedbackItems;
        }
    }

    async shareActivity() {
        console.log('Sharing activity...');
        try {
            if (navigator.share) {
                await navigator.share({
                    title: document.title,
                    text: 'Check out this Five Fold activity from Banasthali Vidyapith!',
                    url: window.location.href
                });
            } else {
                await navigator.clipboard.writeText(window.location.href);
                this.showToast('Activity link copied to clipboard!');
            }
        } catch (error) {
            console.error('Error sharing:', error);
        }
    }

    showToast(message) {
        console.log('Showing toast:', message);
        // Remove existing toast
        const existingToast = document.querySelector('.toast');
        if (existingToast) existingToast.remove();

        // Create new toast
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    openRegisterDialog() {
        console.log('Opening register dialog');
        document.getElementById('registerDialog').classList.add('show');
    }

    closeRegisterDialog() {
        console.log('Closing register dialog');
        document.getElementById('registerDialog').classList.remove('show');
    }

    
    submitFeedback() {
    // 🔒 single source of truth
    if (!IS_REGISTERED) {
        this.showToast('You must be registered to submit feedback');
        return;
    }

    const rating = document.getElementById('rating').value;
    const comment = document
        .querySelector('#feedbackForm textarea')
        .value.trim();

    if (rating == 0) {
        this.showToast('Please select a rating');
        return;
    }

    if (!comment) {
        this.showToast('Please enter a comment');
        return;
    }

    // TEMP: frontend-only storage (until backend feedback)
    const feedback = {
        rating: parseInt(rating),
        comment: comment,
        timestamp: new Date().toISOString(),
    };

    const feedbacks = JSON.parse(
        localStorage.getItem('activityFeedbacks') || '{}'
    );

    if (!feedbacks[this.activityId]) {
        feedbacks[this.activityId] = [];
    }

    feedbacks[this.activityId].push(feedback);
    localStorage.setItem(
        'activityFeedbacks',
        JSON.stringify(feedbacks)
    );

    this.showToast('Feedback submitted successfully!');
    document.querySelector('#feedbackForm textarea').value = '';
    this.setRating(0);
    this.loadFeedbacks();
}

}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Starting ActivityDetail...');
    try {
        const activityDetail = new ActivityDetail();
        window.activityDetail = activityDetail;
        console.log('ActivityDetail created successfully!');
    } catch (error) {
        console.error('Error creating ActivityDetail:', error);
    }
});