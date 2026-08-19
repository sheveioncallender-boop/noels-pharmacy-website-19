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

