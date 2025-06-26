// static/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const form = document.querySelector('form');
    const textArea = document.getElementById('text');
    const submitBtn = document.querySelector('button[type="submit"]');
    const exampleBtns = document.querySelectorAll('.example-btn');
    
    // Add loading state to form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            // Show loading state
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading"></span> Analyzing...';
            submitBtn.disabled = true;
            
            // Add a small delay to show loading (optional)
            setTimeout(() => {
                // Form will submit normally
            }, 500);
        });
    }
    
    // Handle example button clicks
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const exampleText = this.textContent.replace(/"/g, '');
            if (textArea) {
                textArea.value = exampleText;
                textArea.focus();
                
                // Add a subtle animation
                textArea.style.background = '#e3f2fd';
                setTimeout(() => {
                    textArea.style.background = '';
                }, 1000);
            }
        });
    });
    
    // Character counter for textarea
    if (textArea) {
        const maxLength = 500; // Set reasonable limit
        
        // Create character counter element
        const counterDiv = document.createElement('div');
        counterDiv.className = 'text-end text-muted small mt-1';
        counterDiv.id = 'char-counter';
        textArea.parentNode.appendChild(counterDiv);
        
        // Update character count
        function updateCharCount() {
            const currentLength = textArea.value.length;
            counterDiv.textContent = `${currentLength}/${maxLength} characters`;
            
            // Change color if approaching limit
            if (currentLength > maxLength * 0.8) {
                counterDiv.className = 'text-end text-warning small mt-1';
            } else if (currentLength > maxLength * 0.9) {
                counterDiv.className = 'text-end text-danger small mt-1';
            } else {
                counterDiv.className = 'text-end text-muted small mt-1';
            }
        }
        
        // Initial count
        updateCharCount();
        
        // Update on input
        textArea.addEventListener('input', updateCharCount);
        
        // Prevent typing beyond limit
        textArea.addEventListener('keydown', function(e) {
            if (this.value.length >= maxLength && 
                !['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
                e.preventDefault();
            }
        });
    }
    
    // Auto-resize textarea
    if (textArea) {
        textArea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 200) + 'px';
        });
    }
    
    // Add keyboard shortcut (Ctrl+Enter to submit)
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter' && textArea && textArea.value.trim()) {
            form.submit();
        }
    });
    
    // Clear button functionality
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'btn btn-outline-secondary btn-sm ms-2';
    clearBtn.innerHTML = '<i class="fas fa-times"></i> Clear';
    clearBtn.style.display = 'none';
    
    if (textArea && submitBtn) {
        submitBtn.parentNode.appendChild(clearBtn);
        
        // Show/hide clear button
        textArea.addEventListener('input', function() {
            clearBtn.style.display = this.value.trim() ? 'inline-block' : 'none';
        });
        
        // Clear button click
        clearBtn.addEventListener('click', function() {
            textArea.value = '';
            textArea.focus();
            this.style.display = 'none';
            if (document.getElementById('char-counter')) {
                document.getElementById('char-counter').textContent = '0/500 characters';
            }
        });
    }
});

// API function for programmatic access
async function analyzeSentiment(text) {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return { error: 'Failed to analyze sentiment' };
    }
}