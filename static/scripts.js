document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const inputs = form.querySelectorAll('input');
            let valid = true;
            inputs.forEach(input => {
                if (input.type !== 'submit' && input.value.trim() === '') {
                    valid = false;
                    input.classList.add('invalid');
                } else {
                    input.classList.remove('invalid');
                }
            });
            if (!valid) {
                event.preventDefault();
                alert('Please fill out all fields.');
            }
        });
    });
});
