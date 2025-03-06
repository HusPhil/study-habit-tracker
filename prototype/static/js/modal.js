// Simplified Modal System using HTML dialog element
const modalSystem = {
    /**
     * Shows a dialog by ID
     * @param {string} dialogId - The ID of the dialog to show
     */
    show: function(dialogId) {
        const dialog = document.getElementById(dialogId);
        if (!dialog) return console.error(`Dialog with ID ${dialogId} not found`);
        
        // Show dialog with native showModal method
        if (typeof dialog.showModal === 'function') {
            dialog.showModal();
            dialog.classList.add('active');
            
            // Trigger custom event
            dialog.dispatchEvent(new CustomEvent('dialog:open'));
        } else {
            console.error('The <dialog> element is not supported by this browser.');
        }
        
        return dialog;
    },
    
    /**
     * Hides a dialog by ID
     * @param {string} dialogId - The ID of the dialog to hide
     */
    hide: function(dialogId) {
        const dialog = document.getElementById(dialogId);
        if (!dialog) return console.error(`Dialog with ID ${dialogId} not found`);
        
        // Hide dialog with native close method
        dialog.classList.remove('active');
        setTimeout(() => {
            dialog.close();
            
            // Trigger custom event
            dialog.dispatchEvent(new CustomEvent('dialog:close'));
        }, 100); // Reduced from 150ms to 100ms for even faster closing
        
        return dialog;
    },
    
    /**
     * Initialize all dialogs on the page
     */
    init: function() {
        // Initialize close buttons
        document.querySelectorAll('.rpg-dialog .close-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const dialog = btn.closest('.rpg-dialog');
                this.hide(dialog.id);
            });
        });
        
        // Add data attribute dialog triggers
        document.querySelectorAll('[data-dialog-target]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const dialogId = trigger.getAttribute('data-dialog-target');
                this.show(dialogId);
            });
        });
        
        // Cancel button handling
        document.querySelectorAll('.rpg-dialog .btn-secondary').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const dialog = btn.closest('.rpg-dialog');
                this.hide(dialog.id);
            });
        });
        
        // Handle ESC key by default with dialog
        
        console.log('🏰 Dialog system initialized successfully');
    }
};

// Initialize dialogs when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    modalSystem.init();
});