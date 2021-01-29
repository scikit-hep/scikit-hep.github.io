

window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', event => {
  if (event.matches) {
      jtd.setTheme('dark');
  } else {
      jtd.setTheme('light');
  }
});

jtd.setTheme('dark');

