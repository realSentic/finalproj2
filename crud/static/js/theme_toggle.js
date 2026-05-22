function applyThemeButtonState() {
    const toggleButton = document.getElementById('theme-toggle');
    const toggleLabel = document.getElementById('theme-toggle-label');
    if (!toggleButton || !toggleLabel) return;

    const isDark = document.documentElement.classList.contains('dark');
    toggleButton.setAttribute('aria-pressed', isDark ? 'true' : 'false');
    toggleLabel.textContent = isDark ? 'Dark mode' : 'Light mode';
}
