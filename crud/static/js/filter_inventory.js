  function filterInventory() {
  const search = document.getElementById('searchInput').value.toLowerCase().trim();
  const categoryVal = document.getElementById('categoryFilter').value;
  const stockVal = document.getElementById('stockFilter').value;

  const categoryBlocks = document.querySelectorAll('.category-block');
  let anyVisible = false;

  categoryBlocks.forEach(block => {
    const blockCategory = block.dataset.category;

    if (categoryVal && blockCategory !== categoryVal) {
      block.classList.add('hidden');
      return;
    }

    const rows = block.querySelectorAll('.item-row');
    let visibleRows = 0;

    rows.forEach(row => {
      const name = row.dataset.name;
      const stock = row.dataset.stock;
      const matchesSearch = !search || name.includes(search);
      const matchesStock = !stockVal || stock === stockVal;

      if (matchesSearch && matchesStock) {
        row.classList.remove('hidden');
        visibleRows++;
      } else {
        row.classList.add('hidden');
      }
    });

    const emptyRow = block.querySelector('.empty-row');
    if (visibleRows > 0 || (!search && !stockVal && emptyRow)) {
      block.classList.remove('hidden');
      anyVisible = true;
    } else {
      block.classList.add('hidden');
    }
  });

  document.getElementById('noResults').classList.toggle('hidden', anyVisible);
}

function clearFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('categoryFilter').value = '';
  document.getElementById('stockFilter').value = '';
  filterInventory();
}
