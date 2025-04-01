document.addEventListener("DOMContentLoaded", function () {
    let forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("submit", function (event) {
            // Only prevent default for AJAX forms
            if (form.classList.contains("ajax-form")) {
                event.preventDefault();

                let formData = new FormData(this);

                fetch(form.action, { 
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"  // Django detects AJAX request
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.redirect_url) {
                        window.location.href = data.redirect_url;
                    } else if (data.error) {
                        showMessage(data.error, "error");
                    }
                })
                .catch(error => console.error("Error:", error));
            }
            // Else: Normal form submission proceeds as usual
        });
    });

    // Logout Function (Fix for AJAX Logout)
    let logoutForm = document.querySelector("#logoutForm");
    if (logoutForm) {
        logoutForm.addEventListener("submit", function (event) {
            event.preventDefault();

            fetch("/logout/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                },
            })
            .then(() => window.location.href = "/login")
            .catch(error => console.error("Error:", error));
        });
    }
});

// CSRF Token Helper
function getCSRFToken() {
    let name = "csrftoken=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let cookieArray = decodedCookie.split(";");
    for (let c of cookieArray) {
        c = c.trim();
        if (c.startsWith(name)) {
            return c.substring(name.length);
        }
    }
    return "";
}

// Function to Show Messages
function showMessage(message, type) {
    // Remove existing messages before adding a new one
    document.querySelectorAll(".alert-box").forEach(box => box.remove());

    let alertBox = document.createElement("div");
    alertBox.className = `alert-box alert-box--${type}`;
    alertBox.innerHTML = `<p>${message}</p><span class="alert-box__close"></span>`; // No extra "×"

    let container = document.querySelector(".message-container") || document.querySelector("form");
    if (container) {
        container.prepend(alertBox);
    } else {
        document.body.prepend(alertBox);
    }

    // Close button functionality
    let closeBtn = alertBox.querySelector(".alert-box__close");
    if (closeBtn) {
        closeBtn.addEventListener("click", () => alertBox.remove());
    }

    // Fade-out effect before removal
    setTimeout(() => {
        alertBox.style.transition = "opacity 0.5s";
        alertBox.style.opacity = "0";
        setTimeout(() => alertBox.remove(), 500); // Remove after fading out
    }, 3000);
}
document.addEventListener("DOMContentLoaded", function () {
    const cookieBanner = document.getElementById("cookie-banner");

    if (!cookieBanner) {
        console.error("Cookie banner not found!");
        return; // Stop execution if banner is missing
    }

    // Hide the banner if cookies were accepted before
    if (localStorage.getItem("cookiesAccepted") === "true") {
        cookieBanner.style.display = "none";
    }

    // Attach event listener safely
    const acceptBtn = document.getElementById("cookie-btn");
    if (acceptBtn) {
        acceptBtn.addEventListener("click", function () {
            cookieBanner.style.display = "none";
            localStorage.setItem("cookiesAccepted", "true");
        });
    } else {
        console.error("Accept button not found!");
    }
});
