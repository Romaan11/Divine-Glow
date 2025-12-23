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
    document.getElementById('searchButton').addEventListener('click', function() {
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


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
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
document.getElementById('contactForm').addEventListener('submit', function(event) {
    var isValid = true;
    var errorMessages = [];
    
    // Check if all fields are filled
    var fields = ['name', 'email', 'phone', 'subject', 'message'];
    fields.forEach(function(field) {
        var input = document.getElementById(field);
        var errorPopup = input.nextElementSibling;

        if (!input.value.trim()) {
            isValid = false;
            errorMessages.push(field.charAt(0).toUpperCase() + field.slice(1) + " is required.");
            input.classList.add('is-invalid');
            if (errorPopup){
                errorPopup.style.display = 'flex';
                errorPopup.classList.remove('hide');
                
                setTimeout(function() {
                    errorPopup.classList.add('hide');
                    setTimeout(function() {
                        errorPopup.style.display = 'none'; 
                    }, 300); 
                }, 4000);
            }
        } else{
            input.classList.remove('is-invalid');
            if (errorPopup) {
                errorPopup.classList.add('hide'); 
                setTimeout(function() {
                    errorPopup.style.display = 'none'; 
                }, 300); 
            }
        }
    });

    // Phone number validation (must start with 98 or 97, only 10 digits)
    var phone = document.getElementById('phone').value;
    var phoneErrorPopup = document.getElementById('phone').nextElementSibling;
    if (!/^(98|97)\d{8}$/.test(phone)) {
        isValid = false;
        errorMessages.push('Phone no. must start with 98 or 97 and be exactly 10 digits.');
        document.getElementById('phone').classList.add('is-invalid');
        if (phoneErrorPopup) {
            phoneErrorPopup.style.display = 'flex'; 
            phoneErrorPopup.classList.remove('hide');
            
            setTimeout(function() {
                phoneErrorPopup.classList.add('hide');
                setTimeout(function() {
                    phoneErrorPopup.style.display = 'none'; 
                }, 300);
            }, 4000);
        }
    } else {
        if (phoneErrorPopup) {
            phoneErrorPopup.classList.add('hide'); 
            setTimeout(function() {
                phoneErrorPopup.style.display = 'none';
            }, 300); 
        }
    }

    // Email validation (checking if it contains @ symbol)
    var email = document.getElementById('email').value;
    var emailErrorPopup = document.getElementById('email').nextElementSibling;
    if (!/\S+@\S+\.\S+/.test(email)) {
        isValid = false;
        errorMessages.push('Enter a valid email address.');
        document.getElementById('email').classList.add('is-invalid');
        if (emailErrorPopup) {
            emailErrorPopup.style.display = 'flex'; 
            emailErrorPopup.classList.remove('hide');
            
            setTimeout(function() {
                emailErrorPopup.classList.add('hide');
                setTimeout(function() {
                    emailErrorPopup.style.display = 'none'; 
                }, 300); 
            }, 4000);
        }
    } else {
        if (emailErrorPopup) {
            emailErrorPopup.classList.add('hide'); 
            setTimeout(function() {
                emailErrorPopup.style.display = 'none'; 
            }, 300); 
        }
    }

    // Display error messages if form is invalid
    if (!isValid) {
        event.preventDefault();
        var popupMessage = document.getElementById('popupMessage');
        var popupContent = document.getElementById('popupContent');
        popupContent.textContent = errorMessages.join(' ');
        popupMessage.style.backgroundColor = "red"; 
        popupMessage.style.display = "block";
        setTimeout(function() {
            popupMessage.style.display = "none";
        }, 4000);
    }
});

// Real-time error removal on input change
document.querySelectorAll('input, textarea').forEach(function(input) {
    input.addEventListener('input', function() {
        var errorPopup = input.nextElementSibling; 
        if (input.classList.contains('is-invalid') && errorPopup) {
            
            input.classList.remove('is-invalid');
            errorPopup.classList.add('hide');
            setTimeout(function() {
                errorPopup.style.display = 'none'; 
            }, 300);
        }
    });
});

// Clicking the error icon to show the error message again
document.querySelectorAll('.error-icon').forEach(function(icon) {
    icon.addEventListener('click', function() {
        var errorPopup = icon.parentElement; 
        errorPopup.style.display = 'flex'; 
        errorPopup.classList.remove('hide');
    });
});




// Newsletter AJAX form submission
document.getElementById("newsletter_form").addEventListener("submit", function (e) {
    e.preventDefault();

    const form = this;
    const formData = new FormData(form);
    const messageDiv = document.getElementById("newsletter_message");

    // Reset message styles
    messageDiv.className = "";
    messageDiv.style.display = "block";
    messageDiv.style.opacity = "1";
    messageDiv.style.maxHeight = "200px";
    messageDiv.style.marginBottom = "14px";
    messageDiv.style.transition = "all 0.4s ease";

    fetch(form.action, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {

        if (data.success) {
            messageDiv.classList.add("newsletter-success");
            messageDiv.innerHTML = data.message;
            form.reset();
        } else {
            messageDiv.classList.add("newsletter-error");
            messageDiv.innerHTML = data.message;
        }

        
        setTimeout(() => {
            messageDiv.style.opacity = "0";
            messageDiv.style.maxHeight = "0";
            messageDiv.style.marginBottom = "0";

            setTimeout(() => {
                messageDiv.style.display = "none";
            }, 400);
        }, 4000);
    })
    .catch(() => {
        messageDiv.classList.add("newsletter-error");
        messageDiv.innerHTML = "Something went wrong!";

        setTimeout(() => {
            messageDiv.style.opacity = "0";
            messageDiv.style.maxHeight = "0";
            messageDiv.style.marginBottom = "0";

            setTimeout(() => {
                messageDiv.style.display = "none";
            }, 400);
        }, 4000);
    });
});


