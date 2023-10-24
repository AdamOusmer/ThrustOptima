/*
*
* ******************************************************************
* Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
* All Rights Reserved.
* ******************************************************************
*
*/

// TODO add the python interpreter to the package

const {app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const {spawn, exec} = require('child_process');
const axios = require('axios');
const boot = require('./js/boot.js');


let mainWindow;
let serverProcess;


// Create the browser window and load the index.html file
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        'minWidth': 800,
        'minHeight': 600,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, 'js/DOM.js')
        }
    });

    // Load the index.html file
    mainWindow.loadFile(path.join(__dirname, 'html/index.html'));

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', () => {


    boot.boot();

    // Start Flask server

    serverProcess = spawn('python3', [path.join(__dirname, '../../backend/thrust_optima.py')]);

    serverProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);

        if (data.includes('Starting server...')) {
            // Server is fully functional, the GUI can be started and the server can be accessed
            createWindow();

            axios.get(`http://localhost:5000/`).then(
                response => {
                    console.log(response.data);
                }
            ).catch(error => {
                console.log(error);
            });
        }
    });

    serverProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    serverProcess.on('close', (code) => {
        console.log(`Flask process exited with code ${code}`);
    });

});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (mainWindow === null) createWindow();
});

app.on('before-quit', () => {
    axios.post(`http://localhost:5000/cleanup`)
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.error(error);
        });
});

ipcMain.on('hotspot-event', (event, arg) => {
    event.returnValue = 'Message received!'
    require('electron').shell.openExternal(`https://explorer.helium.com/hotspots/${arg}`);
});


