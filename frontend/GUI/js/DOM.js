/*
*
* ******************************************************************
* Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
* All Rights Reserved.
* ******************************************************************
*
*/

// Script to open external links in the default browser instead of a new electron window

const {shell} = require('electron');

window.api = require('electron').ipcRenderer;

document.addEventListener('DOMContentLoaded', () => {
    // Get all anchor elements with target="_blank"
    const links = document.querySelectorAll('a[target="_blank"][href*="http"], a[target="_blank"][href*="https"]');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();

            const url = link.getAttribute('href');
            shell.openExternal(url);
        });
    });
});


