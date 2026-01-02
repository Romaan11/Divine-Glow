(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);

    // Initiate the wowjs
    if (typeof WOW === 'function') {   
        new WOW().init();
    }

    // Fixed Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-200px');
        }
    });

    //search
    const searchBtn = document.getElementById('searchButton');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            var searchContainer = document.querySelector('.search-container');
            var searchInput = document.querySelector('.search-container input');
            
        
            if (!searchContainer.classList.contains('open')) {
                searchContainer.classList.add('open');  
                searchInput.classList.add('open');  
            } else {
                searchContainer.classList.remove('open');  
                searchInput.classList.remove('open');  
            }
        });
    }
    
    //Signup
    function showToast(message) {
        const container = document.getElementById("toast-container");
        const toast = document.getElementById("toast-message");

        toast.innerText = message;
        container.style.display = "block";

        // fade in
        setTimeout(() => {
            toast.style.opacity = "1";
        }, 50);

        // fade out after 4 seconds
        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => {
                container.style.display = "none";
            }, 500);
        }, 4000);
    }

    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
            const p1 = document.querySelector('[name="password1"]').value;
            const p2 = document.querySelector('[name="password2"]').value;

            if (p1 !== p2) {
                event.preventDefault();
                showToast("Passwords do not match!");
            }
        });
    }


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function (e) {
        e.preventDefault();

        $('html, body').stop(true, true)

        .animate(
            { scrollTop: 0 },
            500,            
            'swing'       
        );
    });

    //Services
document.addEventListener('DOMContentLoaded', function() {
    const serviceWrapper = document.querySelector('.service-wrapper');
    const serviceSelect = document.querySelector('select[name="service"]');
    const serviceTooltip = document.getElementById('serviceTooltip');

    if (serviceWrapper && serviceSelect && serviceTooltip) {
        serviceTooltip.style.display = 'none';  
        serviceWrapper.style.position = 'relative'; 

        
        serviceWrapper.addEventListener('mousedown', function(event) {
            if (serviceSelect.disabled) {
                serviceTooltip.style.display = 'block';  

                // Hide after 3 seconds
                setTimeout(() => {
                    serviceTooltip.style.display = 'none';
                }, 3000);

                event.preventDefault(); 
            }
        });
    }
});


    // Pricing-carousel
    if ($('.pricing-carousel').length) {     
        $(".pricing-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 2000,
            dots: true,
            loop: true,
            margin: 25,
            nav: true,
            navText: [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ],
            responsive: {
                0:{ items:1 },
                576:{ items:2 },
                768:{ items:2 },
                992:{ items:3 },
                1200:{ items:4 }
            }
        });
    }

    // Testimonial-carousel
    if ($('.testimonial-carousel').length) {    
        $(".testimonial-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 2000,
            dots: true,
            loop: true,
            margin: 25,
            nav: true,
            navText: [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ],
            responsive: {
                0:{ items:1 },
                992:{ items:2 }
            }
        });
    }

    // Modal Video
    if ($('.btn-play').length && $('#videoModal').length) {  
        $(document).ready(function () {
            var $videoSrc;
            $('.btn-play').click(function () {
                $videoSrc = $(this).data("src");
            });

            $('#videoModal').on('shown.bs.modal', function () {
                $("#video").attr('src', $videoSrc + "?autoplay=1");
            });

            $('#videoModal').on('hide.bs.modal', function () {
                $("#video").attr('src', $videoSrc);
            });
        });
    }

    // Facts counter
    if ($('[data-toggle="counter-up"]').length) { 
        $('[data-toggle="counter-up"]').counterUp({
            delay: 5,
            time: 2000
        });
    }

})(jQuery);


// Contact
window.onload = function() {
    if (sessionStorage.getItem("formSubmitted")) {
        sessionStorage.removeItem("formSubmitted");
    }
}

// Form validation function
const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', function (event) {

        let isValid = true;
        let errorMessages = [];

        // Required fields
        const fields = ['name', 'email', 'phone', 'subject', 'message'];

        fields.forEach(function (field) {
            const input = document.getElementById(field);
            if (!input) return;

            const errorPopup = input.nextElementSibling;

            if (!input.value.trim()) {
                isValid = false;
                errorMessages.push(
                    field.charAt(0).toUpperCase() + field.slice(1) + ' is required.'
                );

                input.classList.add('is-invalid');

                if (errorPopup) {
                    errorPopup.style.display = 'flex';
                    errorPopup.classList.remove('hide');

                    setTimeout(() => {
                        errorPopup.classList.add('hide');
                        setTimeout(() => {
                            errorPopup.style.display = 'none';
                        }, 300);
                    }, 4000);
                }
            } else {
                input.classList.remove('is-invalid');

                if (errorPopup) {
                    errorPopup.classList.add('hide');
                    setTimeout(() => {
                        errorPopup.style.display = 'none';
                    }, 300);
                }
            }
        });

        // PHONE VALIDATION
        const phoneInput = document.getElementById('phone');
        if (phoneInput) {
            const phoneErrorPopup = phoneInput.nextElementSibling;
            const phone = phoneInput.value.trim();

            if (!/^(98|97)\d{8}$/.test(phone)) {
                isValid = false;
                errorMessages.push(
                    'Phone number must start with 98 or 97 and be exactly 10 digits.'
                );

                phoneInput.classList.add('is-invalid');

                if (phoneErrorPopup) {
                    phoneErrorPopup.style.display = 'flex';
                    phoneErrorPopup.classList.remove('hide');

                    setTimeout(() => {
                        phoneErrorPopup.classList.add('hide');
                        setTimeout(() => {
                            phoneErrorPopup.style.display = 'none';
                        }, 300);
                    }, 4000);
                }
            }
        }

        // EMAIL VALIDATION
        const emailInput = document.getElementById('email');
        if (emailInput) {
            const emailErrorPopup = emailInput.nextElementSibling;
            const email = emailInput.value.trim();

            if (!/\S+@\S+\.\S+/.test(email)) {
                isValid = false;
                errorMessages.push('Enter a valid email address.');

                emailInput.classList.add('is-invalid');

                if (emailErrorPopup) {
                    emailErrorPopup.style.display = 'flex';
                    emailErrorPopup.classList.remove('hide');

                    setTimeout(() => {
                        emailErrorPopup.classList.add('hide');
                        setTimeout(() => {
                            emailErrorPopup.style.display = 'none';
                        }, 300);
                    }, 4000);
                }
            }
        }

        if (!isValid) {
            event.preventDefault();

            const popupMessage = document.getElementById('popupMessage');
            const popupContent = document.getElementById('popupContent');

            if (popupMessage && popupContent) {
                popupContent.textContent = errorMessages.join(' ');
                popupMessage.style.backgroundColor = 'red';
                popupMessage.style.display = 'block';

                setTimeout(() => {
                    popupMessage.style.display = 'none';
                }, 4000);
            }
        }
    });
}

document.querySelectorAll('input, textarea').forEach(function (input) {
    input.addEventListener('input', function () {
        const errorPopup = input.nextElementSibling;

        if (input.classList.contains('is-invalid') && errorPopup) {
            input.classList.remove('is-invalid');
            errorPopup.classList.add('hide');

            setTimeout(() => {
                errorPopup.style.display = 'none';
            }, 300);
        }
    });
});

document.querySelectorAll('.error-icon').forEach(function (icon) {
    icon.addEventListener('click', function () {
        const errorPopup = icon.parentElement;
        if (errorPopup) {
            errorPopup.style.display = 'flex';
            errorPopup.classList.remove('hide');
        }
    });
});

// Feedback Form


// Newsletter AJAX form submission 
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("newsletter_form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            showNewsletterToast(data.message, data.success ? "success" : "error");

            if (data.success) {
                form.reset();
            }
        })
        .catch(() => {
            showNewsletterToast("Something went wrong!", "error");
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function showNewsletterToast(message, type) {

    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast-message ${type === "success" ? "toast-success" : "toast-error"}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = "slideOut 0.4s ease forwards";
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}