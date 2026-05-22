document.addEventListener('DOMContentLoaded', () => {
    const loadingScreen = document.getElementById('loading-screen');

    function showLoader() {
        loadingScreen.classList.remove('hidden');
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                loadingScreen.classList.remove('opacity-0');
            });
        });
    }

    function hideLoader() {
        loadingScreen.classList.add('opacity-0');
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
        }, 500);
    }

    window.addEventListener('load', hideLoader);

    window.addEventListener('pageshow', (e) => {
        if (e.persisted) hideLoader();
    });

    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link || !link.href || link.href.startsWith('#') || link.target) return;

        const url = new URL(link.href);
        if (url.pathname.includes('export')) return;

        e.preventDefault();
        showLoader();
        setTimeout(() => { window.location.href = link.href; }, 50);
    });

    document.addEventListener('submit', (e) => {
        const csvInput = document.getElementById('csvFileInput');
        if (csvInput && csvInput.closest('form') === e.target) return;

        const addForm = document.getElementById('add_inventory');
        if (addForm && addForm === e.target) return;

        const editForm = document.getElementById('edit-form');
        if (editForm && editForm === e.target) return;

        const addSupplierForm = document.getElementById('addSupplierForm');
        if (addSupplierForm && addSupplierForm === e.target) return; 

        showLoader();
    });
});