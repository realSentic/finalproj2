function checkPasswordMatch() {
  const newPw = document.getElementById('newPassword').value;
  const confirmPw = document.getElementById('confirmPassword').value;
  const msg = document.getElementById('passwordMatchMsg');

  if (confirmPw.length === 0) {
    msg.classList.add('hidden');
    return;
  }

  if (newPw === confirmPw) {
    msg.textContent = '✓ Passwords match';
    msg.className = 'text-xs mt-1 text-green-700 font-semibold';
  } else {
    msg.textContent = '✗ Passwords do not match';
    msg.className = 'text-xs mt-1 text-red-700 font-semibold';
  }
  msg.classList.remove('hidden');
}