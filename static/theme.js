function getThemeAsString({ localStorageTheme, systemSettingDark }) {
  if (localStorageTheme !== null) {
    return localStorageTheme;
  }

  if (systemSettingDark.matches) {
    return "dark";
  }

  return "light";
}

function setColorTheme(theme) {
	let button = document.getElementById('theme-toggle')
	if (theme == 'dark') {
		document.documentElement.setAttribute('data-theme', 'dark');
		button.textContent='🌙';
		localStorage.setItem("theme", 'dark');
	}
	else {
		document.documentElement.setAttribute('data-theme', 'light');
		button.textContent='☀️';
		localStorage.setItem("theme", 'light');
	}
}

const localStorageTheme = localStorage.getItem("theme");
const systemSettingDark = window.matchMedia("(prefers-color-scheme: dark)");

let currentThemeSetting = getThemeAsString({ localStorageTheme, systemSettingDark });

document.documentElement.setAttribute('data-theme', currentThemeSetting)

window.onload = function(){
	setColorTheme(currentThemeSetting);
	document.getElementById('theme-toggle').addEventListener('click', switchColorMode);
};

function switchColorMode() {
	let button = document.getElementById('theme-toggle')
	
	if (document.documentElement.getAttribute('data-theme') != 'dark') {
		document.documentElement.setAttribute('data-theme', 'dark');
		button.textContent='🌙';
		localStorage.setItem("theme", 'dark');

	}
	else {
		document.documentElement.setAttribute('data-theme', 'light');
		button.textContent='☀️';
		localStorage.setItem("theme", 'light');
	};
}