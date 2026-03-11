// Complete Notification System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all modules
    initComposeForm();
    initDraftsPage();
    initSentPage();
    initModals();
    initToasts();
    
    // Tab highlighting based on current page
    highlightActiveTab();
});

// Compose Form Functions
function initComposeForm() {
    const form = document.getElementById('notificationForm');
    if (!form) return;
    
    // Notification Type Selection
    const typeOptions = document.querySelectorAll('.type-option');
    typeOptions.forEach(option => {
        option.addEventListener('click', function() {
            typeOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            document.getElementById('notificationType').value = this.dataset.type;
        });
    });
    
    // Recipient Selection
    const recipientOptions = document.querySelectorAll('.recipient-option');
    recipientOptions.forEach(option => {
        option.addEventListener('click', function() {
            recipientOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            const radio = this.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
            
            // If custom selection, show student selector modal
            if (this.querySelector('input[value="custom"]')) {
                showStudentSelector();
            }
        });
    });
    
    // Schedule Option Toggle
    const scheduleCheckbox = document.getElementById('scheduleCheckbox');
    const datetimePicker = document.getElementById('datetimePicker');
    
    if (scheduleCheckbox && datetimePicker) {
        scheduleCheckbox.addEventListener('change', function() {
            datetimePicker.style.display = this.checked ? 'flex' : 'none';
            if (this.checked) {
                setDefaultScheduleTime();
            }
        });
    }
    
    function setDefaultScheduleTime() {
        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        const dateInput = document.getElementById('scheduleDate');
        const timeInput = document.getElementById('scheduleTime');
        
        if (dateInput) {
            dateInput.value = tomorrow.toISOString().split('T')[0];
        }
        
        if (timeInput) {
            timeInput.value = '09:00';
        }
    }
    
    // Attachment Handling
    const attachBtn = document.getElementById('attachFileBtn');
    const fileInput = document.getElementById('fileInput');
    const attachmentList = document.getElementById('attachmentList');
    
    if (attachBtn && fileInput) {
        attachBtn.addEventListener('click', () => fileInput.click());
        
        fileInput.addEventListener('change', function() {
            Array.from(this.files).forEach(file => {
                if (validateFile(file)) {
                    addAttachment(file);
                }
            });
            this.value = '';
        });
    }
    
    function validateFile(file) {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const allowedTypes = [
            'image/jpeg', 'image/png', 'image/gif',
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ];
        
        if (file.size > maxSize) {
            showToast('Error', 'File size must be less than 10MB', 'error');
            return false;
        }
        
        if (!allowedTypes.includes(file.type)) {
            showToast('Error', 'File type not allowed', 'error');
            return false;
        }
        
        return true;
    }
    
    function addAttachment(file) {
        const item = document.createElement('div');
        item.className = 'attachment-item';
        
        const size = formatFileSize(file.size);
        const icon = getFileIcon(file.type);
        
        item.innerHTML = `
            <div class="attachment-info">
                <i class="fas ${icon} attachment-icon"></i>
                <div>
                    <div class="attachment-name">${file.name}</div>
                    <div class="attachment-size">${size}</div>
                </div>
            </div>
            <button type="button" class="remove-attachment">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        item.querySelector('.remove-attachment').addEventListener('click', function() {
            item.remove();
            showToast('Success', 'Attachment removed', 'success');
        });
        
        attachmentList.appendChild(item);
        showToast('Success', 'File attached successfully', 'success');
    }
    
    function getFileIcon(type) {
        if (type.startsWith('image/')) return 'fa-file-image';
        if (type.includes('pdf')) return 'fa-file-pdf';
        if (type.includes('word')) return 'fa-file-word';
        if (type.includes('excel') || type.includes('spreadsheet')) return 'fa-file-excel';
        return 'fa-file';
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Form Validation & Confirmation
    form.addEventListener('submit', function(e) {
        const submitButton = e.submitter;
        
        if (submitButton.name === 'send') {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
            
            const confirmation = confirm('Send this notification to all selected recipients?');
            if (!confirmation) {
                e.preventDefault();
                return false;
            }
            
            // Show sending state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            submitButton.disabled = true;
            
            // Add loading overlay
            addLoadingOverlay('Sending notification...');
            
        } else if (submitButton.name === 'save') {
            if (!confirm('Save this notification as a draft?')) {
                e.preventDefault();
                return false;
            }
            
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
            submitButton.disabled = true;
        }
        
        return true;
    });
    
    function validateForm() {
        const subject = document.getElementById('subject');
        const message = document.getElementById('message');
        let isValid = true;
        
        if (!subject.value.trim()) {
            showError(subject, 'Subject is required');
            isValid = false;
        }
        
        if (!message.value.trim()) {
            showError(message, 'Message is required');
            isValid = false;
        }
        
        return isValid;
    }
    
    function showError(element, message) {
        element.style.borderColor = '#ef4444';
        element.focus();
        
        // Add error message
        let errorMsg = element.parentElement.querySelector('.error-message');
        if (!errorMsg) {
            errorMsg = document.createElement('div');
            errorMsg.className = 'error-message';
            errorMsg.style.color = '#ef4444';
            errorMsg.style.fontSize = '12px';
            errorMsg.style.marginTop = '0.25rem';
            element.parentElement.appendChild(errorMsg);
        }
        errorMsg.textContent = message;
        
        // Remove error after 5 seconds
        setTimeout(() => {
            element.style.borderColor = '';
            if (errorMsg) errorMsg.remove();
        }, 5000);
    }
}

// Drafts Page Functions
function initDraftsPage() {
    const draftsPage = document.querySelector('.notification-list-item.draft-item');
    if (!draftsPage) return;
    
    // Checkbox selection
    const selectAllBtn = document.getElementById('selectAllBtn');
    const draftCheckboxes = document.querySelectorAll('.draft-checkbox');
    const deleteSelectedBtn = document.getElementById('deleteSelectedBtn');
    
    if (selectAllBtn) {
        let allSelected = false;
        selectAllBtn.addEventListener('click', function() {
            allSelected = !allSelected;
            draftCheckboxes.forEach(cb => cb.checked = allSelected);
            this.innerHTML = allSelected ? 
                '<i class="far fa-check-square"></i> Deselect All' :
                '<i class="far fa-square"></i> Select All';
            updateDeleteButton();
        });
    }
    
    if (draftCheckboxes.length > 0) {
        draftCheckboxes.forEach(cb => {
            cb.addEventListener('change', updateDeleteButton);
        });
    }
    
    function updateDeleteButton() {
        const selectedCount = document.querySelectorAll('.draft-checkbox:checked').length;
        if (deleteSelectedBtn) {
            deleteSelectedBtn.disabled = selectedCount === 0;
            deleteSelectedBtn.innerHTML = selectedCount > 0 ?
                `<i class="fas fa-trash"></i> Delete (${selectedCount})` :
                '<i class="fas fa-trash"></i> Delete Selected';
        }
    }
    
    // Individual draft actions
    document.querySelectorAll('.delete-draft-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const draftId = this.dataset.id;
            showDeleteConfirmation(draftId, false);
        });
    });
    
    document.querySelectorAll('.send-draft-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const draftId = this.dataset.id;
            if (confirm('Send this draft as a notification?')) {
                // In real app: AJAX request to send draft
                showToast('Success', 'Notification sent successfully', 'success');
                // Reload after delay
                setTimeout(() => location.reload(), 1500);
            }
        });
    });
    
    // Bulk delete
    if (deleteSelectedBtn) {
        deleteSelectedBtn.addEventListener('click', function() {
            const selected = Array.from(document.querySelectorAll('.draft-checkbox:checked'))
                .map(cb => cb.value);
            if (selected.length > 0) {
                showDeleteConfirmation(selected, true);
            }
        });
    }
    
    // Search functionality
    const searchInput = document.getElementById('searchDrafts');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            document.querySelectorAll('.draft-item').forEach(item => {
                const title = item.querySelector('.list-item-title').textContent.toLowerCase();
                const content = item.querySelector('.list-item-content').textContent.toLowerCase();
                item.style.display = (title.includes(query) || content.includes(query)) ? '' : 'none';
            });
        });
    }
}

// Sent Page Functions
function initSentPage() {
    const sentPage = document.querySelector('.notification-list-item:not(.draft-item)');
    if (!sentPage) return;
    
    // View details buttons
    document.querySelectorAll('.view-details').forEach(btn => {
        btn.addEventListener('click', function() {
            const notificationId = this.dataset.id;
            loadNotificationDetails(notificationId);
        });
    });
    
    // Resend buttons
    document.querySelectorAll('.resend-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const notificationId = this.dataset.id;
            if (confirm('Resend this notification?')) {
                // In real app: AJAX request to resend
                showToast('Success', 'Notification resent successfully', 'success');
            }
        });
    });
    
    // Export button
    const exportBtn = document.querySelector('.export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            // In real app: Generate and download CSV
            showToast('Info', 'Exporting notification history...', 'info');
            // Simulate export
            setTimeout(() => {
                showToast('Success', 'Export completed successfully', 'success');
            }, 2000);
        });
    }
}

// Modal Functions
function initModals() {
    // Close modal buttons
    document.querySelectorAll('.modal-close, .cancel-delete').forEach(btn => {
        btn.addEventListener('click', function() {
            closeAllModals();
        });
    });
    
    // Close modal when clicking outside
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeAllModals();
            }
        });
    });
    
    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

function showDeleteConfirmation(ids, isBulk) {
    const modal = document.getElementById('deleteModal');
    const confirmBtn = modal.querySelector('.confirm-delete');
    
    // Update modal message
    const message = modal.querySelector('.modal-body p');
    if (isBulk) {
        message.textContent = `Are you sure you want to delete ${ids.length} selected drafts? This action cannot be undone.`;
    } else {
        message.textContent = 'Are you sure you want to delete this draft? This action cannot be undone.';
    }
    
    // Set up confirmation
    confirmBtn.onclick = function() {
        // In real app: AJAX delete request
        showToast('Success', isBulk ? 'Drafts deleted successfully' : 'Draft deleted successfully', 'success');
        closeAllModals();
        
        // Reload page after delay
        setTimeout(() => location.reload(), 1500);
    };
    
    // Show modal
    modal.classList.add('active');
}

function loadNotificationDetails(notificationId) {
    const modal = document.getElementById('detailsModal');
    const contentDiv = document.getElementById('detailsContent');
    
    // Show loading
    contentDiv.innerHTML = `
        <div class="loading-state">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Loading details...</p>
        </div>
    `;
    
    modal.classList.add('active');
    
    // Simulate API call
    setTimeout(() => {
        // Mock data - replace with actual API call
        const mockData = {
            subject: "Exam Schedule Update",
            type: "Activity Update",
            sent_date: "Jan 15, 2024 10:30 AM",
            recipients: 45,
            opened: 38,
            attachments: 2,
            message: "Dear Students,\n\nPlease note that the exam schedule has been updated. The new schedule is available on the portal. Make sure to check it regularly for any further updates.\n\nBest regards,\nFaculty"
        };
        
        contentDiv.innerHTML = `
            <div class="details-content">
                <div class="detail-row">
                    <div class="detail-label">Subject</div>
                    <div class="detail-value">${mockData.subject}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Notification Type</div>
                    <div class="detail-value">${mockData.type}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Sent Date & Time</div>
                    <div class="detail-value">${mockData.sent_date}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Message Content</div>
                    <div class="detail-value">${mockData.message}</div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-label">Delivery Statistics</div>
                    <div class="detail-value">
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <span>📨 Sent to: ${mockData.recipients} students</span>
                            <span>👁️ Opened by: ${mockData.opened} students</span>
                            <span>📊 Open rate: ${Math.round((mockData.opened/mockData.recipients)*100)}%</span>
                            <span>📎 Attachments: ${mockData.attachments} file(s)</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }, 1000);
}

function closeAllModals() {
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.classList.remove('active');
    });
}

// Toast Notification Functions
function initToasts() {
    // Create toast container if it doesn't exist
    if (!document.querySelector('.toast-container')) {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
}

function showToast(title, message, type = 'success') {
    const container = document.querySelector('.toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'fa-check-circle' :
                 type === 'error' ? 'fa-exclamation-circle' :
                 type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
    
    toast.innerHTML = `
        <i class="fas ${icon} toast-icon"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close">&times;</button>
    `;
    
    // Close button
    toast.querySelector('.toast-close').addEventListener('click', () => {
        toast.remove();
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
    
    container.appendChild(toast);
}

// Utility Functions
function addLoadingOverlay(message = 'Processing...') {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        font-family: inherit;
    `;
    
    overlay.innerHTML = `
        <i class="fas fa-spinner fa-spin" style="font-size: 48px; color: #3b82f6; margin-bottom: 1rem;"></i>
        <h3 style="color: #111827; margin-bottom: 0.5rem;">${message}</h3>
        <p style="color: #6b7280;">Please wait...</p>
    `;
    
    document.body.appendChild(overlay);
    return overlay;
}

function highlightActiveTab() {
    const currentPath = window.location.pathname;
    const tabs = document.querySelectorAll('.tab-item a');
    
    tabs.forEach(tab => {
        const href = tab.getAttribute('href');
        if (href && currentPath.includes(href.split('/').pop())) {
            tab.parentElement.classList.add('active');
        }
    });
}

// Student Selector Modal (for custom recipient selection)
function showStudentSelector() {
    // In real app: This would show a modal with student list for selection
    showToast('Info', 'Student selection feature would open here', 'info');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add CSS for loading overlay
    const style = document.createElement('style');
    style.textContent = `
        .loading-overlay {
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
});
function toggleNotifications() {
    const panel = document.getElementById("notification-panel");
    const overlay = document.getElementById("notification-overlay");

    panel.classList.toggle("open");
    overlay.classList.toggle("open");
}
