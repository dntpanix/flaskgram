// static/js/login.js

document.addEventListener("DOMContentLoaded", () => {
    const username = document.querySelector('input[name="username"]');
    const password = document.querySelector('input[name="password"]');
    const submitBtn = document.querySelector('button[type="submit"]');

    function updateButtonState() {
        const hasUsername = username.value.trim().length > 0;
        const hasPassword = password.value.trim().length > 0;

        submitBtn.disabled = !(hasUsername && hasPassword);

        // optional: add disabled styling if needed
        if (submitBtn.disabled) {
            submitBtn.classList.add("disabled");
        } else {
            submitBtn.classList.remove("disabled");
        }
    }

    username.addEventListener("input", updateButtonState);
    password.addEventListener("input", updateButtonState);

    // initialize on page load
    updateButtonState();
});
