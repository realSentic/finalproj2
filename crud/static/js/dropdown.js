const btn = document.getElementById('profile-menu-button');
const menu = document.getElementById('profile-dropdown');
if (btn && menu) {
  btn.addEventListener('click', () => menu.classList.toggle('hidden'));
  document.addEventListener('click', (e) => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.add('hidden');
    }
  });
}