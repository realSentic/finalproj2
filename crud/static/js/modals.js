function openDeleteModal(itemId, itemName) {
  document.getElementById('delete-item-name').innerText = itemName;
  document.getElementById('delete-form').action = `/inventory/delete/${itemId}/`;
  document.getElementById('delete-modal').classList.remove('hidden');
}

function closeDeleteModal() {
    document.getElementById('delete-modal').classList.add('hidden');
  }

  function openEditModal(itemId, itemName, unit, currentStock, reorderLevel, unitCost, categoryId) {
  document.getElementById('edit-item-name').value = itemName;
  document.getElementById('edit-unit').value = unit;
  document.getElementById('edit-current-stock').value = currentStock;
  document.getElementById('edit-reorder-level').value = reorderLevel;
  document.getElementById('edit-unit-cost').value = unitCost;
  document.getElementById('edit-category').value = categoryId;
  document.getElementById('edit-form').action = `/inventory/update/${itemId}/`;
  document.getElementById('edit-modal').classList.remove('hidden');
}

function closeEditModal() {
  document.getElementById('edit-modal').classList.add('hidden');
}



function openAddCategoryModal() {
  document.getElementById('add-category-modal').classList.remove('hidden');
  const card = document.getElementById('add-category-modal').querySelector('.motion-preset-pop');
  card.classList.remove('motion-preset-pop');
  void card.offsetWidth;
  card.classList.add('motion-preset-pop');
}

function closeAddCategoryModal() {
  document.getElementById('add-category-modal').classList.add('hidden');
}

function openEditCategoryModal(categoryId, categoryName) {
  document.getElementById('edit-category-name').value = categoryName;
  document.getElementById('edit-category-form').action = `/category/update/${categoryId}/`;
  document.getElementById('edit-category-modal').classList.remove('hidden');
  const card = document.getElementById('edit-category-modal').querySelector('.motion-preset-pop');
  card.classList.remove('motion-preset-pop');
  void card.offsetWidth;
  card.classList.add('motion-preset-pop');
}

function closeEditCategoryModal() {
  document.getElementById('edit-category-modal').classList.add('hidden');
}

function openDeleteCategoryModal(categoryId, categoryName) {
    const modal = document.getElementById("delete-category-modal");
    const form = document.getElementById("delete-category-form");
    const nameSpan = document.getElementById("delete-category-name");

    nameSpan.textContent = categoryName;

    form.action = `/category/delete/${categoryId}/`;

    modal.classList.remove("hidden");
  }

  function closeDeleteCategoryModal() {
    document.getElementById("delete-category-modal").classList.add("hidden");
  }


  function openEditSupplierModal(id, name, contact, email, phone, address) {
  document.getElementById('edit_supplier_name').value = name;
  document.getElementById('edit_contact_person').value = contact;
  document.getElementById('edit_email').value = email;
  document.getElementById('edit_phone_number').value = phone;
  document.getElementById('edit_address').value = address;
  document.getElementById('editSupplierForm').action = `/supplier/update/${id}/`;
  document.getElementById('editSupplierModal').classList.remove('hidden');
}

function closeEditSupplierModal() {
  document.getElementById('editSupplierModal').classList.add('hidden');
}

function openDeleteSupplierModal(id, name) {
  document.getElementById('deleteSupplierName').textContent = name;
  document.getElementById('deleteSupplierForm').action = `/supplier/delete/${id}/`;
  document.getElementById('deleteSupplierModal').classList.remove('hidden');
}

function closeDeleteSupplierModal() {
  document.getElementById('deleteSupplierModal').classList.add('hidden');
}