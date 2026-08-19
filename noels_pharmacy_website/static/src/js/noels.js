(function () {
    "use strict";

    function ready(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback, { once: true });
        } else {
            callback();
        }
    }

    ready(function () {
        const header = document.querySelector(".noels-header");
        const toggle = document.querySelector("[data-noels-menu-toggle]");
        const menu = document.querySelector("[data-noels-mobile-menu]");

        if (toggle && menu) {
            toggle.addEventListener("click", function () {
                const open = document.body.classList.toggle("noels-menu-open");
                toggle.setAttribute("aria-expanded", open ? "true" : "false");
            });
            menu.querySelectorAll("a").forEach(function (link) {
                link.addEventListener("click", function () {
                    document.body.classList.remove("noels-menu-open");
                    toggle.setAttribute("aria-expanded", "false");
                });
            });
        }

        if (header) {
            const updateHeader = function () {
                header.classList.toggle("is-scrolled", window.scrollY > 24);
            };
            updateHeader();
            window.addEventListener("scroll", updateHeader, { passive: true });
        }

        document.querySelectorAll("[data-noels-slider]").forEach(function (slider) {
            const slides = Array.from(slider.querySelectorAll("[data-noels-slide]"));
            const dots = Array.from(slider.querySelectorAll("[data-noels-slide-to]"));
            const previous = slider.querySelector("[data-noels-slide-prev]");
            const next = slider.querySelector("[data-noels-slide-next]");
            const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
            const editorMode = document.body.classList.contains("editor_enable");
            let activeIndex = Math.max(0, slides.findIndex(function (slide) {
                return slide.classList.contains("is-active");
            }));
            let autoplayTimer = null;

            if (slides.length < 2) return;

            const setSlideFocus = function (slide, enabled) {
                slide.querySelectorAll("a, button, input, select, textarea, [tabindex]").forEach(function (element) {
                    if (enabled) {
                        element.removeAttribute("tabindex");
                    } else {
                        element.setAttribute("tabindex", "-1");
                    }
                });
            };

            const showSlide = function (index) {
                activeIndex = (index + slides.length) % slides.length;
                slides.forEach(function (slide, slideIndex) {
                    const active = slideIndex === activeIndex;
                    slide.classList.toggle("is-active", active);
                    slide.setAttribute("aria-hidden", active ? "false" : "true");
                    setSlideFocus(slide, active);
                });
                dots.forEach(function (dot, dotIndex) {
                    const active = dotIndex === activeIndex;
                    dot.classList.toggle("is-active", active);
                    dot.setAttribute("aria-current", active ? "true" : "false");
                });
            };

            const stopAutoplay = function () {
                if (autoplayTimer) {
                    window.clearInterval(autoplayTimer);
                    autoplayTimer = null;
                }
            };

            const startAutoplay = function () {
                if (reducedMotion || editorMode || autoplayTimer || document.hidden) return;
                autoplayTimer = window.setInterval(function () {
                    showSlide(activeIndex + 1);
                }, 7000);
            };

            const restartAutoplay = function () {
                stopAutoplay();
                startAutoplay();
            };

            if (previous) {
                previous.addEventListener("click", function () {
                    showSlide(activeIndex - 1);
                    restartAutoplay();
                });
            }
            if (next) {
                next.addEventListener("click", function () {
                    showSlide(activeIndex + 1);
                    restartAutoplay();
                });
            }
            dots.forEach(function (dot) {
                dot.addEventListener("click", function () {
                    showSlide(Number(dot.dataset.noelsSlideTo || 0));
                    restartAutoplay();
                });
            });

            slider.addEventListener("mouseenter", stopAutoplay);
            slider.addEventListener("mouseleave", startAutoplay);
            slider.addEventListener("focusin", stopAutoplay);
            slider.addEventListener("focusout", function (event) {
                if (!slider.contains(event.relatedTarget)) startAutoplay();
            });
            slider.addEventListener("keydown", function (event) {
                if (event.key === "ArrowLeft") {
                    showSlide(activeIndex - 1);
                    restartAutoplay();
                } else if (event.key === "ArrowRight") {
                    showSlide(activeIndex + 1);
                    restartAutoplay();
                }
            });
            document.addEventListener("visibilitychange", function () {
                if (document.hidden) stopAutoplay();
                else startAutoplay();
            });

            showSlide(activeIndex);
            startAutoplay();
        });

        const uploadInput = document.querySelector("[data-noels-upload-input]");
        const uploadLabel = document.querySelector("[data-noels-upload-label]");
        const uploadZone = document.querySelector("[data-noels-upload-zone]");
        if (uploadInput && uploadLabel && uploadZone) {
            const updateUpload = function () {
                const count = uploadInput.files ? uploadInput.files.length : 0;
                uploadLabel.textContent = count
                    ? count + (count === 1 ? " file selected" : " files selected")
                    : "PDF, PNG, JPG or JPEG · Up to 5 files · 10 MB each";
                uploadZone.classList.toggle("has-files", count > 0);
            };
            uploadInput.addEventListener("change", updateUpload);
            ["dragenter", "dragover"].forEach(function (eventName) {
                uploadZone.addEventListener(eventName, function (event) {
                    event.preventDefault();
                    uploadZone.classList.add("is-dragging");
                });
            });
            ["dragleave", "drop"].forEach(function (eventName) {
                uploadZone.addEventListener(eventName, function () {
                    uploadZone.classList.remove("is-dragging");
                });
            });
        }

        const fulfillmentInputs = document.querySelectorAll('input[name="fulfillment"]');
        const deliveryAddress = document.querySelector("[data-noels-delivery-address]");
        const updateFulfillment = function () {
            if (!deliveryAddress) return;
            const chosen = document.querySelector('input[name="fulfillment"]:checked');
            const delivery = chosen && chosen.value === "delivery";
            deliveryAddress.classList.toggle("is-visible", delivery);
            const textarea = deliveryAddress.querySelector("textarea");
            if (textarea) textarea.required = Boolean(delivery);
        };
        fulfillmentInputs.forEach(function (input) {
            input.addEventListener("change", updateFulfillment);
        });
        updateFulfillment();

        document.querySelectorAll(".noels-form").forEach(function (form) {
            form.addEventListener("submit", function () {
                const button = form.querySelector('button[type="submit"]');
                if (button && form.checkValidity()) {
                    button.disabled = true;
                    button.classList.add("is-loading");
                    button.dataset.originalText = button.textContent;
                    button.textContent = "Submitting…";
                }
            });
        });
    });
})();
