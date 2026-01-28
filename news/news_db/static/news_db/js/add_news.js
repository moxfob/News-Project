document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    const titleInput = document.getElementById('title');
    const shortDescInput = document.getElementById('short_description');
    const descInput = document.getElementById('description');
    
    if (titleInput) {
        const titleCounter = document.createElement('div');
        titleCounter.className = 'char-counter';
        titleCounter.textContent = `0/200`;
        titleInput.parentNode.appendChild(titleCounter);
        
        titleInput.addEventListener('input', function() {
            const count = this.value.length;
            titleCounter.textContent = `${count}/200`;
            titleCounter.className = 'char-counter';
            if (count > 180) titleCounter.classList.add('warning');
            if (count > 195) titleCounter.classList.add('error');
        });
    }
    
    if (shortDescInput) {
        const shortDescCounter = document.createElement('div');
        shortDescCounter.className = 'char-counter';
        shortDescCounter.textContent = `0/75`;
        shortDescInput.parentNode.appendChild(shortDescCounter);
        
        shortDescInput.addEventListener('input', function() {
            const count = this.value.length;
            shortDescCounter.textContent = `${count}/75`;
            shortDescCounter.className = 'char-counter';
            if (count > 65) shortDescCounter.classList.add('warning');
            if (count > 70) shortDescCounter.classList.add('error');
            
            if (count > 75) {
                this.value = this.value.substring(0, 75);
                shortDescCounter.textContent = `75/75`;
                shortDescCounter.classList.add('error');
            }
        });
    }
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            if (file) {
                if (!file.type.startsWith('image/')) {
                    alert('Пожалуйста, выберите файл изображения');
                    this.value = '';
                    return;
                }
                
                if (file.size > 5 * 1024 * 1024) {
                    alert('Файл слишком большой. Максимальный размер: 5MB');
                    this.value = '';
                    return;
                }
                
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.alt = 'Предпросмотр изображения';
                    
                    const removeBtn = document.createElement('button');
                    removeBtn.type = 'button';
                    removeBtn.className = 'remove-image';
                    removeBtn.innerHTML = '×';
                    removeBtn.onclick = function() {
                        imageInput.value = '';
                        imagePreview.innerHTML = `
                            <div class="preview-placeholder">
                                <span>📷</span>
                                <p>Нажмите для выбора изображения</p>
                                <small>Рекомендуемый размер: 1200×630 px</small>
                            </div>
                        `;
                    };
                    
                    imagePreview.innerHTML = '';
                    imagePreview.appendChild(img);
                    imagePreview.appendChild(removeBtn);
                };
                
                reader.readAsDataURL(file);
            }
        });
    }
    
    const dateInput = document.getElementById('published_date');
    if (dateInput && !dateInput.value) {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        dateInput.value = `${year}-${month}-${day}T${hours}:${minutes}`;
    }
    
    const form = document.querySelector('.add-news-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            let errorMessage = '';
            
            if (!titleInput.value.trim()) {
                isValid = false;
                errorMessage = 'Введите заголовок новости\n';
                titleInput.style.borderColor = '#e03131';
            } else {
                titleInput.style.borderColor = '';
            }
            
            if (!shortDescInput.value.trim()) {
                isValid = false;
                errorMessage += 'Введите краткое описание\n';
                shortDescInput.style.borderColor = '#e03131';
            } else if (shortDescInput.value.length < 10) {
                isValid = false;
                errorMessage += 'Краткое описание должно содержать не менее 10 символов\n';
                shortDescInput.style.borderColor = '#e03131';
            } else {
                shortDescInput.style.borderColor = '';
            }
            
            if (!descInput.value.trim()) {
                isValid = false;
                errorMessage += 'Введите текст новости\n';
                descInput.style.borderColor = '#e03131';
            } else if (descInput.value.length < 50) {
                isValid = false;
                errorMessage += 'Текст новости должен содержать не менее 50 символов\n';
                descInput.style.borderColor = '#e03131';
            } else {
                descInput.style.borderColor = '';
            }
            
            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, исправьте следующие ошибки:\n\n' + errorMessage);
                return false;
            }
            
            const submitBtn = this.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.innerHTML = '<span>📤 Публикация...</span>';
                submitBtn.disabled = true;
            }
            
            return true;
        });
    }
    
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    function autoSave() {
        if (titleInput.value || shortDescInput.value || descInput.value) {
            const data = {
                title: titleInput.value,
                shortDescription: shortDescInput.value,
                description: descInput.value,
                timestamp: new Date().getTime()
            };
            localStorage.setItem('news_draft', JSON.stringify(data));
        }
    }
    
    if (titleInput && shortDescInput && descInput) {
        const draft = localStorage.getItem('news_draft');
        if (draft) {
            try {
                const data = JSON.parse(draft);
                const hoursAgo = (new Date().getTime() - data.timestamp) / (1000 * 60 * 60);
                if (hoursAgo < 24) {
                    if (confirm('У вас есть несохраненный черновик. Загрузить его?')) {
                        titleInput.value = data.title || '';
                        shortDescInput.value = data.shortDescription || '';
                        descInput.value = data.description || '';
                        
                        if (titleInput.dispatchEvent) titleInput.dispatchEvent(new Event('input'));
                        if (shortDescInput.dispatchEvent) shortDescInput.dispatchEvent(new Event('input'));
                    }
                } else {
                    localStorage.removeItem('news_draft');
                }
            } catch (e) {
                console.error('Error loading draft:', e);
            }
        }
        
        let saveTimer;
        [titleInput, shortDescInput, descInput].forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(saveTimer);
                saveTimer = setTimeout(autoSave, 10000);
            });
        });
        
        form.addEventListener('submit', function() {
            localStorage.removeItem('news_draft');
        });
    }
});