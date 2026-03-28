document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('[data-portal-sidebar]');
    const overlay = document.querySelector('[data-portal-overlay]');
    const toggle = document.querySelector('[data-portal-toggle]');

    if (toggle && sidebar && overlay) {
        const closeSidebar = () => {
            sidebar.classList.remove('is-open');
            overlay.classList.remove('is-open');
        };

        toggle.addEventListener('click', function () {
            sidebar.classList.toggle('is-open');
            overlay.classList.toggle('is-open');
        });

        overlay.addEventListener('click', closeSidebar);

        sidebar.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', closeSidebar);
        });
    }

    document.querySelectorAll('[data-tab-group]').forEach(function (group) {
        const tabs = group.querySelectorAll('[data-tab-target]');
        const panes = group.querySelectorAll('[data-tab-pane]');

        tabs.forEach(function (tab) {
            tab.addEventListener('click', function () {
                const target = tab.getAttribute('data-tab-target');
                tabs.forEach(function (item) {
                    item.classList.toggle('is-active', item === tab);
                });
                panes.forEach(function (pane) {
                    pane.classList.toggle('is-active', pane.getAttribute('data-tab-pane') === target);
                });
            });
        });
    });

    const contacts = document.querySelectorAll('[data-chat-contact]');
    const activeName = document.querySelector('[data-chat-active-name]');
    const activeStatus = document.querySelector('[data-chat-active-status]');
    const activeMessage = document.querySelector('[data-chat-active-message]');
    const buyerField = document.querySelector('input[name="buyer_name"]');
    const farmerField = document.querySelector('input[name="farmer_id"]');

    contacts.forEach(function (contact) {
        contact.addEventListener('click', function () {
            contacts.forEach(function (item) {
                item.classList.remove('is-active');
            });
            contact.classList.add('is-active');

            if (activeName) {
                activeName.textContent = contact.getAttribute('data-chat-name') || 'Buyer';
            }
            if (activeStatus) {
                activeStatus.textContent = contact.getAttribute('data-chat-status') || 'Conversation open';
            }
            if (activeMessage) {
                activeMessage.textContent = contact.getAttribute('data-chat-message') || 'Start talking about crop quality, price, and delivery here.';
            }
            if (buyerField) {
                buyerField.value = contact.getAttribute('data-chat-name') || '';
            }
            if (farmerField) {
                farmerField.value = contact.getAttribute('data-chat-farmer-id') || '';
            }
        });
    });
});
