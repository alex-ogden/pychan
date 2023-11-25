const modeToggle = document.getElementById('mode-toggle');
const body = document.body;

modeToggle.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  
  const isDarkMode = body.classList.contains('dark-mode');
  if (isDarkMode) {
    // Switch to dark mode
    localStorage.setItem('theme', 'dark');
  } else {
    // Switch to light mode
    localStorage.setItem('theme', 'light');
  }
});

// Check for user's preferred theme in localStorage
const userPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
const theme = localStorage.getItem('theme');
if ((theme === 'dark' && userPrefersDark) || theme === 'light') {
  body.classList.add('dark-mode');
}
