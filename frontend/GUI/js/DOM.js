const { shell } = require('electron');

window.api = require('electron').ipcRenderer;

document.addEventListener('DOMContentLoaded', () => {
    // Get all anchor elements with target="_blank"
    const links = document.querySelectorAll('a[target="_blank"]');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default behavior (opening in the same window)

            const url = link.getAttribute('href');
            shell.openExternal(url); // Open link in external browser
        });
    });
});
