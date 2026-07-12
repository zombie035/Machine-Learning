document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictForm');
    const predictBtn = document.getElementById('predictBtn');

    if (form) {
        form.addEventListener('submit', () => {
            // Add loading class to button to show spinner
            predictBtn.classList.add('loading');
        });
    }
});
