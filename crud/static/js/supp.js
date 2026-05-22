console.log('supplier validation loaded')

document.addEventListener('DOMContentLoaded', () => {

    const editSupplierForm = document.getElementById('editSupplierForm');
    const editSupplierName = document.getElementById('edit_supplier_name');
    const editSupplierEmail = document.getElementById('edit_email');
    const editSupplierPhone = document.getElementById('edit_phone_number');

    const addSupplierForm = document.getElementById('addSupplierForm');
    console.log('addSupplierForm:', addSupplierForm)
    const addSupplierName = document.getElementById('supplier_name');
    const addSupplierEmail = document.getElementById('email');
    const addSupplierPhone = document.getElementById('phone_number');

    if (addSupplierForm) {
        addSupplierForm.addEventListener('submit', (e) => {
            console.log('add supplier form submitted!')
            let valid = true;


            document.getElementById('name-error').classList.add('hidden');
            document.getElementById('email-error').classList.add('hidden');
            document.getElementById('phone-error').classList.add('hidden');

            if (addSupplierName.value.trim() === '') {
                document.getElementById('name-error').classList.remove('hidden');
                valid = false;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(addSupplierEmail.value.trim())) {
                document.getElementById('email-error').classList.remove('hidden');
                valid = false;
            }

            const phoneRegex = /^[0-9]{7,15}$/;
            if (!phoneRegex.test(addSupplierPhone.value.trim())) {
                document.getElementById('phone-error').classList.remove('hidden');
                document.getElementById('phone-error').textContent = "Please enter a valid phone number (digits only, 7-15 characters).";
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
                e.stopImmediatePropagation();
            }
        })
    };


    if (editSupplierForm) {
        editSupplierForm.addEventListener('submit', (e) => {
            let valid = true;

            document.getElementById('edit-name-error').classList.add('hidden');
            document.getElementById('edit-email-error').classList.add('hidden');
            document.getElementById('edit-phone-error').classList.add('hidden');

            if (editSupplierName.value.trim() === '') {
                document.getElementById('edit-name-error').classList.remove('hidden');
                valid = false;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(editSupplierEmail.value.trim())) {
                document.getElementById('edit-email-error').classList.remove('hidden');
                valid = false;
            }

            const phoneRegex = /^[0-9]{7,15}$/;
            if (!phoneRegex.test(editSupplierPhone.value.trim())) {
                document.getElementById('edit-phone-error').classList.remove('hidden');
                document.getElementById('edit-phone-error').textContent = "Please enter a valid phone number (digits only, 7-15 characters).";
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
                e.stopImmediatePropagation();
            }
        });
    }
});