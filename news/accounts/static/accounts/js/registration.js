document.addEventListener('DOMContentLoaded', function() {
    const password1 = document.querySelector('input[name="password1"]');
    const password2 = document.querySelector('input[name="password2"]');
    
    function validatePasswords() {
        if (password1.value && password2.value && password1.value !== password2.value) {
            password2.style.borderColor = '#e74c3c';
        } else {
            password2.style.borderColor = '#ddd';
        }
    }
    
    if (password1 && password2) {
        password1.addEventListener('input', validatePasswords);
        password2.addEventListener('input', validatePasswords);
    }

    if (password1) {
        password1.addEventListener('input', function() {
            const password = this.value;
            const lengthValid = password.length >= 8;
            
            if (password && !lengthValid) {
                this.style.borderColor = '#e74c3c';
            } else if (password) {
                this.style.borderColor = '#2ecc71';
            } else {
                this.style.borderColor = '#ddd';
            }
        });
    }
});