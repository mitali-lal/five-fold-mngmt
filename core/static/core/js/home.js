// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initCounters();
    initScrollAnimations();
    initNavigation();
    initFeatureCards();
    initStoryCards();
    initBackToTop();
    initStatsAnimation();
    initMouseEffects();
    initLiveCounter();
});

// Animated counters
function initCounters() {
    const counters = document.querySelectorAll('[data-target]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                animateCounter(counter, target);
                observer.unobserve(counter);
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    });
    
    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 100;
    const duration = 1500;
    const stepTime = Math.abs(Math.floor(duration / target));
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, stepTime);
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.feature-card, .story-card, .entry-card, .stat-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Navigation
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link[data-scroll]');
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-links');
    
    // Smooth scrolling
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-scroll');
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                const headerOffset = 80;
                const elementPosition = targetSection.offsetTop;
                const offsetPosition = elementPosition - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                }
            }
        });
    });
    
    // Mobile toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            mobileToggle.classList.toggle('active');
        });
    }
    
    // Update active nav link on scroll
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY + 100;
        
        navLinks.forEach(link => {
            const targetId = link.getAttribute('data-scroll');
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                const sectionTop = targetSection.offsetTop;
                const sectionBottom = sectionTop + targetSection.offsetHeight;
                
                if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {
                    navLinks.forEach(l => l.classList.remove('active'));
                    link.classList.add('active');
                }
            }
        });
    });
}

// Interactive feature cards
function initFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    const exploreButtons = document.querySelectorAll('.feature-explore');
    
    featureCards.forEach((card, index) => {
        // Hover effect
        card.addEventListener('mouseenter', () => {
            card.style.zIndex = '10';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.zIndex = '1';
        });
        
        // Click effect
        card.addEventListener('click', () => {
            const icon = card.querySelector('.feature-icon');
            icon.style.transform = 'scale(1.1) rotate(5deg)';
            
            setTimeout(() => {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }, 300);
        });
    });
    
    // Explore buttons
    exploreButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const cardIndex = this.getAttribute('data-card');
            const targetCard = document.querySelector(`.feature-card[data-index="${cardIndex}"]`);
            
            if (targetCard) {
                // Animate the card
                targetCard.style.transform = 'scale(1.05)';
                targetCard.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.4)';
                
                setTimeout(() => {
                    targetCard.style.transform = 'translateY(-10px)';
                    targetCard.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
                }, 500);
                
                // Simulate navigation (in real app, this would redirect)
                console.log(`Navigating to feature ${cardIndex}`);
            }
        });
    });
}

// Story cards interaction
function initStoryCards() {
    const storyCards = document.querySelectorAll('.story-card');
    
    storyCards.forEach(card => {
        card.addEventListener('click', () => {
            const storyText = card.querySelector('.story-text');
            const originalHeight = storyText.style.height;
            
            if (storyText.classList.contains('expanded')) {
                storyText.classList.remove('expanded');
                storyText.style.height = '4.2em'; // 3 lines
            } else {
                storyText.classList.add('expanded');
                storyText.style.height = storyText.scrollHeight + 'px';
            }
        });
    });
}

// Back to top button
function initBackToTop() {
    const backToTop = document.querySelector('.back-to-top');
    
    if (!backToTop) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });
    
    backToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Stats animation
function initStatsAnimation() {
    const stats = document.querySelectorAll('.stat-card .stat-number[data-target]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumber = entry.target;
                const target = parseInt(statNumber.getAttribute('data-target'));
                
                let current = 0;
                const increment = target / 60;
                const duration = 2000;
                
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        statNumber.textContent = target;
                        clearInterval(timer);
                    } else {
                        statNumber.textContent = Math.floor(current);
                    }
                }, duration / 60);
                
                observer.unobserve(statNumber);
            }
        });
    }, {
        threshold: 0.5
    });
    
    stats.forEach(stat => observer.observe(stat));
}

// Mouse effects
function initMouseEffects() {
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth) * 100;
        const y = (e.clientY / window.innerHeight) * 100;
        
        document.querySelectorAll('.floating-circle').forEach((circle, index) => {
            const speed = 0.01 + (index * 0.005);
            const moveX = (x - 50) * speed;
            const moveY = (y - 50) * speed;
            
            circle.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });
}

// Live counter animation
function initLiveCounter() {
    const counterNumbers = document.querySelectorAll('.counter-number');
    
    // Animate the counter numbers
    counterNumbers.forEach((counter, index) => {
        const target = parseInt(counter.getAttribute('data-count') || counter.textContent);
        let current = 0;
        
        // Start with zeros
        counter.textContent = '00000'.substring(0, 5 - target.toString().length) + '0';
        
        // Animate after delay
        setTimeout(() => {
            const increment = target / 100;
            const duration = 2000;
            const stepTime = Math.abs(Math.floor(duration / target));
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    const formatted = target.toString().padStart(5, '0');
                    counter.textContent = formatted;
                    clearInterval(timer);
                } else {
                    const formatted = Math.floor(current).toString().padStart(5, '0');
                    counter.textContent = formatted;
                }
            }, stepTime);
        }, index * 300); // Stagger the animations
    });
    
    // Update live count periodically (simulated)
    setInterval(() => {
        const liveCount = document.querySelector('.counter-item:first-child .counter-number');
        const current = parseInt(liveCount.textContent);
        const change = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
        
        if (current + change >= 0) {
            const newCount = current + change;
            liveCount.textContent = newCount.toString().padStart(5, '0');
            liveCount.setAttribute('data-count', newCount);
        }
    }, 5000); // Update every 5 seconds
}

// Parallax effect
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const rate = scrolled * -0.5;
    
    document.querySelectorAll('.floating-circle').forEach((circle, index) => {
        const speed = 0.1 + (index * 0.05);
        circle.style.transform = `translateY(${rate * speed}px)`;
    });
});

// Initialize entry cards hover effect
document.querySelectorAll('.entry-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        const role = this.getAttribute('data-role');
        const icon = this.querySelector('.entry-icon');
        
        // Add pulse animation to icon
        icon.style.animation = 'pulse 0.5s ease';
        
        setTimeout(() => {
            icon.style.animation = '';
        }, 500);
        
        // Highlight corresponding role
        document.querySelectorAll('.entry-card').forEach(c => {
            if (c !== this) {
                c.style.opacity = '0.7';
                c.style.transform = 'scale(0.98)';
            }
        });
    });
    
    card.addEventListener('mouseleave', function() {
        document.querySelectorAll('.entry-card').forEach(c => {
            c.style.opacity = '1';
            c.style.transform = '';
        });
    });
});

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        // Add focus styles
        document.querySelectorAll(':focus').forEach(el => {
            el.classList.add('keyboard-focus');
        });
    }
});

// Remove focus styles on click
document.addEventListener('click', () => {
    document.querySelectorAll('.keyboard-focus').forEach(el => {
        el.classList.remove('keyboard-focus');
    });
});

// Add CSS for keyboard focus
const style = document.createElement('style');
style.textContent = `
    .keyboard-focus {
        outline: 2px solid #1d4ed8 !important;
        outline-offset: 2px !important;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);

// Initialize everything
window.addEventListener('load', () => {
    // Add loaded class for fade-in effect
    document.body.classList.add('loaded');
    
    // Trigger initial animations
    setTimeout(() => {
        document.querySelectorAll('.feature-card, .story-card, .entry-card').forEach((el, index) => {
            setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }, 500);
});

// Add error handling
window.addEventListener('error', (e) => {
    console.error('Page error:', e.error);
});

// Add beforeunload for smooth transitions
window.addEventListener('beforeunload', () => {
    document.body.classList.add('page-transition');
});

// Carousel functionality
function initCarousel() {
    const track = document.querySelector('.carousel-track');
    const cards = document.querySelectorAll('.carousel-card');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    
    if (!track || !cards.length) return;
    
    let currentIndex = 0;
    const cardWidth = cards[0].offsetWidth + 30; // width + gap
    const visibleCards = Math.floor(track.parentElement.offsetWidth / cardWidth);
    const maxIndex = cards.length - visibleCards;
    
    // Update carousel position
    function updateCarousel() {
        const offset = -currentIndex * cardWidth;
        track.style.transform = `translateX(${offset}px)`;
        
        // Update dots
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
        
        // Update button states
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex >= maxIndex;
    }
    
    // Next button
    nextBtn.addEventListener('click', () => {
        if (currentIndex < maxIndex) {
            currentIndex++;
            updateCarousel();
        }
    });
    
    // Previous button
    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    });
    
    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentIndex = Math.min(index, maxIndex);
            updateCarousel();
        });
    });
    
    // Auto-advance carousel
    let autoSlide = setInterval(() => {
        if (currentIndex < maxIndex) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateCarousel();
    }, 5000);
    
    // Pause auto-slide on hover
    track.addEventListener('mouseenter', () => {
        clearInterval(autoSlide);
    });
    
    track.addEventListener('mouseleave', () => {
        autoSlide = setInterval(() => {
            if (currentIndex < maxIndex) {
                currentIndex++;
            } else {
                currentIndex = 0;
            }
            updateCarousel();
        }, 5000);
    });
    
    // Card click effects
    cards.forEach((card, index) => {
        card.addEventListener('click', function(e) {
            if (!this.classList.contains('explore-more')) {
                const dimension = this.getAttribute('data-dimension');
                
                // Add ripple effect
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.3);
                    transform: scale(0);
                    animation: ripple-animation 0.6s linear;
                    width: ${size}px;
                    height: ${size}px;
                    top: ${y}px;
                    left: ${x}px;
                    pointer-events: none;
                `;
                
                this.appendChild(ripple);
                
                // Remove ripple after animation
                setTimeout(() => {
                    ripple.remove();
                }, 600);
                
                // Show dimension details
                showDimensionDetails(dimension);
            }
        });
    });
    
    // Initialize
    updateCarousel();
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            updateCarousel();
        }, 250);
    });
}

// Show dimension details modal
function showDimensionDetails(dimension) {
    const dimensionData = {
        physical: {
            title: "Physical Development",
            icon: "fa-running",
            description: "Promoting health, wellness, sports, yoga, and physical activities for holistic well-being and lifelong fitness habits.",
            activities: ["Sports", "Yoga & Meditation", "Health Workshops", "Outdoor Adventures", "Fitness Training"],
            stats: {
                participation: "100%",
                facilities: "45+ Sports",
                events: "Monthly"
            }
        },
        practical: {
            title: "Practical Skills",
            icon: "fa-tools",
            description: "Developing hands-on skills, vocational training, industry exposure, and real-world application of knowledge.",
            activities: ["Workshops", "Industry Visits", "Projects", "Internships", "Skill Labs"],
            stats: {
                placement: "92%",
                workshops: "60+ Annually",
                partnerships: "150+ Companies"
            }
        },
        aesthetic: {
            title: "Aesthetic Expression",
            icon: "fa-palette",
            description: "Cultivating artistic sensibility, creative expression, cultural appreciation, and emotional intelligence.",
            activities: ["Arts & Crafts", "Music & Dance", "Theatre", "Literary Arts", "Cultural Events"],
            stats: {
                artForms: "25+",
                events: "50+ Annual",
                clubs: "15+"
            }
        },
        moral: {
            title: "Moral Values",
            icon: "fa-hands-helping",
            description: "Building character, ethical values, social responsibility, community engagement, and compassionate leadership.",
            activities: ["Community Service", "Ethics Workshops", "Leadership Programs", "Social Projects", "Value Education"],
            stats: {
                serviceHours: "5000+",
                projects: "30+ Active",
                impact: "1000+ Beneficiaries"
            }
        },
        intellectual: {
            title: "Intellectual Growth",
            icon: "fa-brain",
            description: "Fostering academic excellence, critical thinking, research aptitude, and intellectual curiosity.",
            activities: ["Research Projects", "Seminars", "Academic Clubs", "Competitions", "Library Resources"],
            stats: {
                excellence: "85%+",
                publications: "200+ Papers",
                conferences: "National & International"
            }
        }
    };
    
    const data = dimensionData[dimension];
    if (!data) return;
    
    // Create modal HTML
    const modalHTML = `
        <div class="dimension-modal" id="dimension-modal">
            <div class="modal-content">
                <button class="modal-close">&times;</button>
                <div class="modal-header">
                    <div class="modal-icon">
                        <i class="fas ${data.icon}"></i>
                    </div>
                    <h3>${data.title}</h3>
                </div>
                <div class="modal-body">
                    <p>${data.description}</p>
                    
                    <div class="modal-stats">
                        ${Object.entries(data.stats).map(([key, value]) => `
                            <div class="modal-stat">
                                <span class="stat-value">${value}</span>
                                <span class="stat-label">${key.replace(/([A-Z])/g, ' $1').toUpperCase()}</span>
                            </div>
                        `).join('')}
                    </div>
                    
                    <div class="modal-activities">
                        <h4>Key Activities:</h4>
                        <div class="activities-grid">
                            ${data.activities.map(activity => `
                                <span class="activity-tag">${activity}</span>
                            `).join('')}
                        </div>
                    </div>
                    
                    <a href="#features" class="modal-explore-btn" data-scroll="features">
                        Explore ${data.title} <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add modal styles
    const modalStyles = `
        .dimension-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            opacity: 0;
            animation: modalFadeIn 0.3s ease forwards;
            backdrop-filter: blur(10px);
        }
        
        @keyframes modalFadeIn {
            to { opacity: 1; }
        }
        
        .modal-content {
            background: rgba(20, 20, 20, 0.95);
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 90%;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            transform: translateY(20px);
            animation: modalSlideUp 0.3s ease 0.1s forwards;
        }
        
        @keyframes modalSlideUp {
            to { transform: translateY(0); }
        }
        
        .modal-close {
            position: absolute;
            top: 20px;
            right: 20px;
            background: none;
            border: none;
            color: white;
            font-size: 2rem;
            cursor: pointer;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background 0.3s ease;
        }
        
        .modal-close:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .modal-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .modal-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #1d4ed8, #9333ea);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 2.5rem;
        }
        
        .modal-header h3 {
            font-size: 2rem;
            font-weight: 700;
            color: white;
        }
        
        .modal-body {
            color: rgba(255, 255, 255, 0.9);
        }
        
        .modal-body p {
            line-height: 1.6;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .modal-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .modal-stat {
            text-align: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
        }
        
        .stat-value {
            display: block;
            font-size: 1.8rem;
            font-weight: 700;
            color: #1d4ed8;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.7);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .modal-activities h4 {
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: white;
        }
        
        .activities-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        .activity-tag {
            background: rgba(29, 78, 216, 0.2);
            border: 1px solid rgba(29, 78, 216, 0.4);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        
        .modal-explore-btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #1d4ed8, #9333ea);
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }
        
        .modal-explore-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(29, 78, 216, 0.4);
        }
    `;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = modalStyles;
    document.head.appendChild(styleSheet);
    
    // Add ripple animation
    const rippleStyle = `
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    
    const rippleStyleSheet = document.createElement('style');
    rippleStyleSheet.textContent = rippleStyle;
    document.head.appendChild(rippleStyleSheet);
    
    // Close modal functionality
    const modal = document.getElementById('dimension-modal');
    const closeBtn = modal.querySelector('.modal-close');
    const exploreBtn = modal.querySelector('.modal-explore-btn');
    
    closeBtn.addEventListener('click', () => {
        modal.style.animation = 'modalFadeOut 0.3s ease forwards';
        modal.querySelector('.modal-content').style.animation = 'modalSlideDown 0.3s ease forwards';
        
        setTimeout(() => {
            modal.remove();
            styleSheet.remove();
            rippleStyleSheet.remove();
        }, 300);
    });
    
    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeBtn.click();
        }
    });
    
    // Close on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal) {
            closeBtn.click();
        }
    });
    
    // Explore button scroll
    exploreBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeBtn.click();
        
        // Scroll to features section
        setTimeout(() => {
            const featuresSection = document.getElementById('features');
            if (featuresSection) {
                featuresSection.scrollIntoView({ behavior: 'smooth' });
            }
        }, 350);
    });
}

// Update the initialization function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initCounters();
    initScrollAnimations();
    initNavigation();
    initFeatureCards();
    initStoryCards();
    initBackToTop();
    initStatsAnimation();
    initMouseEffects();
    initLiveCounter();
    initCarousel(); // Add this line
    
    // Add smooth scrolling for all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.offsetTop;
                const offsetPosition = elementPosition - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Add smooth hover effects for contact social links
function initContactEffects() {
    const socialLinks = document.querySelectorAll('.social-link');
    
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.1)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Call this in DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // ... existing initialization code ...
    initContactEffects();
});

// Add parallax effect for carousel
function initCarouselParallax() {
    const carouselSection = document.querySelector('.fivefold-carousel');
    
    if (!carouselSection) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.3;
        
        carouselSection.style.backgroundPositionY = `${rate}px`;
    });
}

// Add to initialization
document.addEventListener('DOMContentLoaded', function() {
    // ... existing initialization code ...
    initCarouselParallax();
});

// Concentric Circles Interaction - Fixed Version
function initConcentricCircles() {
    const circles = document.querySelectorAll('.circle-layer');
    const container = document.querySelector('.concentric-container');
    const core = document.querySelector('.concentric-core');
    
    if (!circles.length || !container) return;
    
    // Disable auto-rotate initially
    let autoRotateEnabled = false;
    let autoRotateInterval;
    let currentIndex = 0;
    
    // Initial state
    circles.forEach(circle => {
        circle.style.opacity = '0.5';
        circle.style.transform = 'scale(0.98)';
        circle.classList.add('no-parallax');
    });
    
    // Function to highlight a specific circle
    function highlightCircle(circle) {
        // Remove active class from all circles first
        circles.forEach(c => {
            c.classList.remove('active');
            c.style.opacity = '0.5';
            c.style.transform = 'scale(0.98)';
            c.style.zIndex = '1';
        });
        
        // Highlight the selected circle
        circle.classList.add('active');
        circle.style.opacity = '1';
        circle.style.transform = 'scale(1.05)';
        circle.style.zIndex = '20';
        
        // Create ripple effect
        createRippleEffect(circle);
        
        // Update core content
        updateCoreContent(circle);
    }
    
    // Click event with proper event handling
    circles.forEach(circle => {
        // Mouse enter event
        circle.addEventListener('mouseenter', function(e) {
            // Stop event from bubbling to container
            e.stopPropagation();
            
            // Only highlight if not already active
            if (!this.classList.contains('active')) {
                highlightCircle(this);
            }
        });
        
        // Mouse leave event
        circle.addEventListener('mouseleave', function(e) {
            e.stopPropagation();
            
            // Don't reset if this circle is currently clicked/active
            if (!this.classList.contains('active')) {
                this.style.opacity = '0.5';
                this.style.transform = 'scale(0.98)';
                this.style.zIndex = '1';
            }
        });
        
        // Click event - Make it the active circle
        circle.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            
            // Set as active circle
            highlightCircle(this);
            
            // Get circle data
            const layer = this.getAttribute('data-layer');
            const type = this.getAttribute('data-stage') || 
                         this.getAttribute('data-support') || 
                         this.getAttribute('data-metric') || 
                         this.getAttribute('data-competency');
            
            // Click animation
            this.style.animation = 'circle-pulse 0.6s ease';
            setTimeout(() => {
                this.style.animation = '';
            }, 600);
            
            // Show details
            showLayerDetails(layer, type);
            
            console.log(`Clicked layer ${layer}: ${type}`);
        });
    });
    
    // Container mouse move - REMOVED PARALLAX to prevent movement
    container.addEventListener('mousemove', (e) => {
        // Optional: Add subtle effect if needed, but no major movement
        const rect = container.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const deltaX = e.clientX - centerX;
        const deltaY = e.clientY - centerY;
        
        // Very subtle rotation instead of movement
        const rotation = deltaX * 0.0005; // Very small rotation
        
        // Apply only to non-active circles
        circles.forEach(circle => {
            if (!circle.classList.contains('active')) {
                // Very subtle effect - can remove if not needed
                circle.style.transform = `scale(0.98) rotate(${rotation}deg)`;
            }
        });
    });
    
    // Reset all circles when clicking outside
    document.addEventListener('click', function(e) {
        // Check if click is outside any circle
        const clickedCircle = e.target.closest('.circle-layer');
        const clickedContainer = e.target.closest('.concentric-container');
        
        if (!clickedCircle && clickedContainer) {
            // Clicked in container but not on a circle
            circles.forEach(circle => {
                circle.classList.remove('active');
                circle.style.opacity = '0.5';
                circle.style.transform = 'scale(0.98)';
                circle.style.zIndex = '1';
            });
            resetCoreContent();
        }
    });
    
    // Optional: Auto-rotate toggle
    const toggleAutoRotate = () => {
        autoRotateEnabled = !autoRotateEnabled;
        
        if (autoRotateEnabled) {
            autoRotateInterval = setInterval(() => {
                highlightCircle(circles[currentIndex]);
                currentIndex = (currentIndex + 1) % circles.length;
            }, 2000);
        } else {
            clearInterval(autoRotateInterval);
        }
    };
    
    // Add auto-rotate controls (optional)
    const addControls = () => {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'circle-controls';
        controlsDiv.innerHTML = `
            <button class="control-btn" id="toggle-rotate">Auto Rotate</button>
            <button class="control-btn" id="reset-circles">Reset</button>
        `;
        
        container.parentElement.appendChild(controlsDiv);
        
        // Toggle auto-rotate
        document.getElementById('toggle-rotate').addEventListener('click', toggleAutoRotate);
        
        // Reset all circles
        document.getElementById('reset-circles').addEventListener('click', () => {
            circles.forEach(circle => {
                circle.classList.remove('active');
                circle.style.opacity = '0.5';
                circle.style.transform = 'scale(0.98)';
                circle.style.zIndex = '1';
            });
            resetCoreContent();
        });
    };
    
    // Initialize controls
    addControls();
}