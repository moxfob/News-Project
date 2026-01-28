document.addEventListener('DOMContentLoaded', function() {
    const notifications = document.querySelectorAll('.notification');
    
    notifications.forEach((notification, index) => {
        setTimeout(() => {
            notification.classList.add('show');
        }, 100 * index);
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.remove('show');
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 5000);
    });

    document.querySelectorAll('.notification-close').forEach(button => {
        button.addEventListener('click', function() {
            const notification = this.parentElement;
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        });
    });
});