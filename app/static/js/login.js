// static/js/login.js
document.addEventListener("DOMContentLoaded", () => {
    const username = document.querySelector('input[name="username"]');
    const password = document.querySelector('input[name="password"]');
    const submitBtn = document.querySelector('button[type="submit"]');
    const span_phone = document.querySelector('#phone');
    const span_password = document.querySelector('#password');

    // safety: bail if required nodes missing
    if (!username || !password || !submitBtn) return;

    function updateButtonState() {
        const hasUsername = username.value.trim().length > 0;
        const hasPassword = password.value.trim().length > 0;

        const enabled = hasUsername && hasPassword;
        submitBtn.disabled = !enabled;
        submitBtn.setAttribute('aria-disabled', (!enabled).toString());

        // optional styling class
        submitBtn.classList.toggle("disabled", !enabled);
    }

    function updateSpans() {
        if (span_phone) {
            span_phone.style.display = username.value.trim().length > 0 ? "none" : "block";
        }
        if (span_password) {
            span_password.style.display = password.value.trim().length > 0 ? "none" : "block";
        }
    }

    // combined handler
    function onInput() {
        updateButtonState();
        updateSpans();
    }

    // attach listeners to both inputs (covers typing, paste, autofill triggers)
    ["input", "change", "paste"].forEach(ev => {
        username.addEventListener(ev, onInput);
        password.addEventListener(ev, onInput);
    });

    // initialize (handles autofill)
    onInput();

    // handle delayed autofill in some browsers
    setTimeout(onInput, 200);
    setTimeout(onInput, 1200);
});
