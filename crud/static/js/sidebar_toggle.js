document.addEventListener('DOMContentLoaded', function() {
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const sidebarOverlay = document.getElementById('sidebar-overlay');
  const sidebarToggleIcon = document.getElementById('sidebar-toggle-icon');

  if (sidebarToggle && sidebar && sidebarOverlay) {

    sidebarToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      const isHidden = sidebar.classList.contains('-translate-x-full');
      sidebar.classList.toggle('-translate-x-full');
      sidebarOverlay.classList.toggle('hidden');
      sidebarToggle.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
      if (sidebarToggleIcon) {
        sidebarToggleIcon.style.transform = isHidden ? 'rotate(90deg)' : 'rotate(0deg)';
      }
    });

    const sidebarLinks = sidebar.querySelectorAll('a');
    sidebarLinks.forEach(link => {
      link.addEventListener('click', function() {
        if (window.innerWidth < 1024) {
          sidebar.classList.add('-translate-x-full');
          sidebarOverlay.classList.add('hidden');
          sidebarToggle.setAttribute('aria-expanded', 'false');
          if (sidebarToggleIcon) {
            sidebarToggleIcon.style.transform = 'rotate(0deg)';
          }
        }
      });
    });

    sidebarOverlay.addEventListener('click', function(e) {
      e.stopPropagation();
      sidebar.classList.add('-translate-x-full');
      sidebarOverlay.classList.add('hidden');
      sidebarToggle.setAttribute('aria-expanded', 'false');
      if (sidebarToggleIcon) {
        sidebarToggleIcon.style.transform = 'rotate(0deg)';
      }
    });

    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        if (window.innerWidth >= 1024) {
          sidebar.classList.remove('-translate-x-full');
          sidebarOverlay.classList.add('hidden');
          sidebarToggle.setAttribute('aria-expanded', 'true');
          if (sidebarToggleIcon) {
            sidebarToggleIcon.style.transform = 'rotate(0deg)';
          }
        } else {
          sidebar.classList.add('-translate-x-full');
          sidebarOverlay.classList.add('hidden');
          sidebarToggle.setAttribute('aria-expanded', 'false');
          if (sidebarToggleIcon) {
            sidebarToggleIcon.style.transform = 'rotate(0deg)';
          }
        }
      }, 250);
    });

  }
});