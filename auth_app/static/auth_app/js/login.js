// Login Page Interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const loginForm = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const rememberMe = document.getElementById('rememberMe');
    const roleButtons = document.querySelectorAll('.role-btn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const altLoginButtons = document.querySelectorAll('.alt-login-btn');
    
    // Toggle password visibility
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Update icon
            const icon = this.querySelector('i');
            icon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
        });
    }
    
    // Role selection
    roleButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            roleButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Add role to form (optional)
            const role = this.getAttribute('data-role');
            console.log(`Selected role: ${role}`);
            
            // You could add a hidden input to submit with the form
            addRoleToForm(role);
        });
    });
    
    function addRoleToForm(role) {
        // Remove existing role input
        const existingInput = document.querySelector('input[name="role"]');
        if (existingInput) {
            existingInput.remove();
        }
        
        // Add new hidden input
        const roleInput = document.createElement('input');
        roleInput.type = 'hidden';
        roleInput.name = 'role';
        roleInput.value = role;
        loginForm.appendChild(roleInput);
    }
    
    // Form submission with loading animation
    if (loginForm && submitBtn) {
        loginForm.addEventListener('submit', function(e) {
            // Basic validation
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!username || !password) {
                e.preventDefault();
                showError('Please fill in all required fields');
                return;
            }
            
            if (password.length < 8) {
                e.preventDefault();
                showError('Password must be at least 8 characters long');
                return;
            }
            
            // Show loading animation
            showLoading();
            
            // Simulate network delay (remove in production)
            setTimeout(() => {
                // Form will submit normally
                // If there's an error, it will be shown by Django
            }, 1000);
        });
    }
    
    // Alternative login buttons
    altLoginButtons.forEach(button => {
        button.addEventListener('click', function() {
            const provider = this.classList.contains('google-btn') ? 'Google' : 'Microsoft';
            console.log(`Initiating ${provider} login...`);
            
            // Show loading
            showLoading();
            
            // In a real implementation, you would redirect to OAuth endpoint
            // For now, show a message
            setTimeout(() => {
                hideLoading();
                alert(`${provider} login integration would be implemented here.`);
            }, 1500);
        });
    });
    
    // Forgot password
    const forgotLink = document.querySelector('.forgot-link');
    if (forgotLink) {
        forgotLink.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Password reset functionality would be implemented here.');
        });
    }
    
    // Auto-focus username field
    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        setTimeout(() => {
            usernameInput.focus();
        }, 300);
    }
    
    // Check for saved credentials
    function checkSavedCredentials() {
        const savedUsername = localStorage.getItem('ffms_username');
        const savedRemember = localStorage.getItem('ffms_remember') === 'true';
        
        if (savedUsername && savedRemember && usernameInput) {
            usernameInput.value = savedUsername;
            rememberMe.checked = true;
        }
    }
    
    // Save credentials if "Remember me" is checked
    if (rememberMe) {
        rememberMe.addEventListener('change', function() {
            if (this.checked && usernameInput && usernameInput.value) {
                localStorage.setItem('ffms_username', usernameInput.value);
                localStorage.setItem('ffms_remember', 'true');
            } else {
                localStorage.removeItem('ffms_username');
                localStorage.removeItem('ffms_remember');
            }
        });
    }
    
    // Initialize
    checkSavedCredentials();
    addRoleToForm('student'); // Default role
    
    // Helper functions
    function showError(message) {
        // Remove existing error alerts
        const existingAlert = document.querySelector('.error-alert');
        if (existingAlert) {
            existingAlert.remove();
        }
        
        // Create new error alert
        const errorAlert = document.createElement('div');
        errorAlert.className = 'error-alert';
        errorAlert.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <span>${message}</span>
        `;
        
        // Insert after form header
        const formHeader = document.querySelector('.form-header');
        if (formHeader) {
            formHeader.insertAdjacentElement('afterend', errorAlert);
        }
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorAlert.parentNode) {
                errorAlert.style.opacity = '0';
                errorAlert.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    if (errorAlert.parentNode) {
                        errorAlert.remove();
                    }
                }, 300);
            }
        }, 5000);
    }
    
    function showLoading() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
            submitBtn.disabled = true;
            submitBtn.querySelector('.btn-text').textContent = 'Authenticating...';
        }
    }
    
    function hideLoading() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = 'Sign In';
        }
    }
    
    // If there's a Django error, add animation
    const djangoError = document.querySelector('.error-alert');
    if (djangoError) {
        setTimeout(() => {
            djangoError.style.animation = 'shake 0.5s ease-in-out';
        }, 100);
        
        // Add shake animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                20%, 40%, 60%, 80% { transform: translateX(5px); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add floating label effect
    const inputs = document.querySelectorAll('.input-with-icon input');
    inputs.forEach(input => {
        // Add floating effect on focus
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
        
        // Add character counter for password
        if (input.type === 'password') {
            input.addEventListener('input', function() {
                const length = this.value.length;
                const hint = this.closest('.form-group').querySelector('.input-hint');
                if (hint && length > 0) {
                    hint.textContent = `${length}/8 characters`;
                    hint.style.color = length >= 8 ? '#10b981' : '#ef4444';
                }
            });
        }
    });
});