function exportData() {
    if(confirm('Экспортировать данные системы?')) {
        window.location.href = "{% url 'export_data' %}";
    }
}

function clearCache() {
    if(confirm('Очистить кэш системы?')) {
        fetch("{% url 'clear_cache' %}")
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            });
    }
}

function openRoleModal() {
    document.getElementById('roleModal').style.display = 'block';
    updateRoleForm();
}

function closeRoleModal() {
    document.getElementById('roleModal').style.display = 'none';
}

function openResetPasswordModal() {
    document.getElementById('resetPasswordModal').style.display = 'block';
    document.getElementById('passwordPreview').style.display = 'none';
    document.getElementById('resetPasswordForm').reset();
}

function closeResetPasswordModal() {
    document.getElementById('resetPasswordModal').style.display = 'none';
}

function openStatusModal() {
    document.getElementById('statusModal').style.display = 'block';
    updateStatusInfo();
}

function closeStatusModal() {
    document.getElementById('statusModal').style.display = 'none';
}

function updateRoleForm() {
    const userSelect = document.getElementById('target_user_select');
    const roleSelect = document.getElementById('new_role');
    const selectedUser = userSelect.options[userSelect.selectedIndex];
    
    if (selectedUser && selectedUser.value) {
        const currentRoleId = selectedUser.getAttribute('data-current-role');
        
        if (currentRoleId) {
            for (let i = 0; i < roleSelect.options.length; i++) {
                if (roleSelect.options[i].value === currentRoleId) {
                    roleSelect.value = currentRoleId;
                    break;
                }
            }
        } else {
            roleSelect.value = '';
        }
    }
}

function updateStatusInfo() {
    const userSelect = document.getElementById('status_user_select');
    const selectedUser = userSelect.options[userSelect.selectedIndex];
    const statusInfo = document.getElementById('userStatusInfo');
    const statusSubmitBtn = document.getElementById('statusSubmitBtn');
    
    if (selectedUser && selectedUser.value) {
        const isActive = selectedUser.getAttribute('data-active') === 'True';
        
        document.getElementById('currentStatus').textContent = isActive ? 'Активен' : 'Неактивен';
        document.getElementById('currentStatus').style.color = isActive ? 'green' : 'red';
        
        const action = isActive ? 'деактивировать' : 'активировать';
        document.getElementById('actionText').textContent = action;
        
        document.getElementById('statusAction').value = isActive ? 'deactivate' : 'activate';
        statusSubmitBtn.textContent = isActive ? 'Деактивировать' : 'Активировать';
        statusSubmitBtn.className = isActive ? 'btn-primary danger' : 'btn-primary';
        
        statusInfo.style.display = 'block';
    } else {
        statusInfo.style.display = 'none';
    }
}

function submitStatusChange() {
    const userSelect = document.getElementById('status_user_select');
    if (!userSelect.value) {
        alert('Выберите пользователя!');
        return;
    }
    
    const isActive = userSelect.options[userSelect.selectedIndex].getAttribute('data-active') === 'True';
    const action = isActive ? 'деактивировать' : 'активировать';
    
    if (confirm(`Вы уверены что хотите ${action} пользователя?`)) {
        document.getElementById('statusForm').submit();
    }
}

document.getElementById('resetPasswordForm').onsubmit = function(e) {
    e.preventDefault();
    const userSelect = document.getElementById('reset_user_select');
    if (!userSelect.value) {
        alert('Выберите пользователя!');
        return;
    }
    
    if (confirm('Вы уверены что хотите сбросить пароль пользователя?')) {
        const randomPassword = generatePassword(12);
        document.getElementById('newPasswordText').textContent = randomPassword;
        document.getElementById('passwordPreview').style.display = 'block';
        
        const passwordField = document.createElement('input');
        passwordField.type = 'hidden';
        passwordField.name = 'new_password';
        passwordField.value = randomPassword;
        this.appendChild(passwordField);
        
        this.submit();
    }
};

function generatePassword(length) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < length; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return password;
}

window.onclick = function(event) {
    const modals = ['roleModal', 'resetPasswordModal', 'statusModal'];
    modals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        if (event.target === modal) {
            if (modalId === 'roleModal') closeRoleModal();
            if (modalId === 'resetPasswordModal') closeResetPasswordModal();
            if (modalId === 'statusModal') closeStatusModal();
        }
    });
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeRoleModal();
        closeResetPasswordModal();
        closeStatusModal();
    }
});