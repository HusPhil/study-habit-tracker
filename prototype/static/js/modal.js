const modalSystem = {
    show: function(dialogId) {
        const dialog = document.getElementById(dialogId);
        if (!dialog) return console.error(`Dialog with ID ${dialogId} not found`);
        
        if (typeof dialog.showModal === 'function') {
            dialog.showModal();
            dialog.classList.add('active');
            dialog.dispatchEvent(new CustomEvent('dialog:open'));
        } else {
            console.error('The <dialog> element is not supported by this browser.');
        }
        return dialog;
    },

    hide: function(dialogId) {
        const dialog = document.getElementById(dialogId);
        if (!dialog) return console.error(`Dialog with ID ${dialogId} not found`);
        
        dialog.classList.remove('active');
        setTimeout(() => {
            dialog.close();
            dialog.dispatchEvent(new CustomEvent('dialog:close'));
        }, 100); 
        
        return dialog;
    },

    init: function() {
        // ✅ Remove old event listeners before adding new ones
        document.querySelectorAll('.rpg-dialog .close-btn').forEach(btn => {
            btn.removeEventListener('click', modalSystem.closeHandler);
            btn.addEventListener('click', modalSystem.closeHandler);
        });

        document.querySelectorAll('[data-dialog-target]').forEach(trigger => {
            trigger.removeEventListener('click', modalSystem.openHandler);
            trigger.addEventListener('click', modalSystem.openHandler);
        });

        document.querySelectorAll('.rpg-dialog .btn-secondary').forEach(btn => {
            btn.removeEventListener('click', modalSystem.closeHandler);
            btn.addEventListener('click', modalSystem.closeHandler);
        });

        console.log('🏰 Dialog system reinitialized successfully');
    },

    openHandler: function(e) {
        e.preventDefault();
        const dialogId = e.currentTarget.getAttribute('data-dialog-target');
        modalSystem.show(dialogId);
    },

    closeHandler: function(e) {
        e.preventDefault();
        const dialog = e.currentTarget.closest('.rpg-dialog');
        modalSystem.hide(dialog.id);
    }
};