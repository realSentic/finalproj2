document.addEventListener('DOMContentLoaded', () => {
    const addForm = document.getElementById('add_inventory');
    const editForm = document.getElementById('edit-form');

    const current_stock = document.getElementById('current_stock');
    const reorder_level = document.getElementById('reorder_level');
    const unit_cost = document.getElementById('unit_cost');

    const edit_cost = document.getElementById('edit-unit-cost');
    const edit_reorder = document.getElementById('edit-reorder-level');

    if (editForm) { 
        editForm.addEventListener('submit', (e) => {
            let valid = true;

            document.getElementById('edit-reorder-error').classList.add('hidden');
            document.getElementById('edit-cost-error').classList.add('hidden');

            if (Number(edit_reorder.value) <= 9 || edit_reorder.value === '') {
                document.getElementById('edit-reorder-error').classList.remove('hidden');
                valid = false;
            }

            if (Number(edit_cost.value) <= 0 || edit_cost.value === '') {
                document.getElementById('edit-cost-error').classList.remove('hidden');
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
            }
        })
    }

    if (addForm) {
        addForm.addEventListener('submit', (e) => {
            let valid = true;

            document.getElementById('current_stock_error').classList.add('hidden');
            document.getElementById('reorder_level_error').classList.add('hidden');
            document.getElementById('unit_cost_error').classList.add('hidden');

            if (Number(current_stock.value) <= 0 || current_stock.value === '') {
                document.getElementById('current_stock_error').classList.remove('hidden');
                valid = false;
            }

            if (Number(reorder_level.value) <= 9) {
                document.getElementById('reorder_level_error').classList.remove('hidden');
                valid = false;
            }

            if (Number(unit_cost.value) <= 0 || unit_cost.value === '') {
                document.getElementById('unit_cost_error').classList.remove('hidden');
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
            }
        })
    }
})