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

        // Hide after 4 seconds (slide + fade)
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
