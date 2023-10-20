/*
*
* ******************************************************************
* Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
* All Rights Reserved.
* ******************************************************************
*
*/

const {app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const {spawn, exec} = require('child_process');
const {fs} = require("node:fs");


let mainWindow;
let serverProcess;


function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        'minWidth': 800,
        'minHeight': 600,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, 'js/DOM.js') // Updated preload path
        }
    });

    // Load the index.html file
    mainWindow.loadFile(path.join(__dirname, 'html/index.html'));

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function boot() {
    // Install Python requirements only at the first boot

    // Create a .thst file in the root directory if it doesn't exist
    // If it does exist, then don't install Python requirements



    const installCommand = 'pip3 install -r ../../backend/requirements.txt';

    exec(installCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`error: ${error.message}`);
            return;
        }

        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }

        console.log(`Python dependencies installed successfully.`);

    });
    // Start Flask server

    serverProcess = spawn('python3', [path.join(__dirname, '../../backend/production_server.py')]);

    console.log("setting")
    console.log(serverProcess.stdout.on)

    serverProcess.stdout.on('data', (data) => {
        console.error("this")
        console.log(`stdout: ${data}`);
    });

}

app.on('ready', () => {

    boot()

    // Install Python requirements

    console.log("set")

    serverProcess.stderr.on('data', (data) => {
        console.error("that")
        console.error(`stderr: ${data}`);
    });

    serverProcess.on('close', (code) => {
        console.log(`Flask process exited with code ${code}`);
    });

    // Create the browser window

    createWindow();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (mainWindow === null) createWindow();
});

app.on('before-quit', () => {
    process.kill(pid, 'SIGTERM');
});

ipcMain.on('hotspot-event', (event, arg) => {
    event.returnValue = 'Message received!'
    require('electron').shell.openExternal(`https://explorer.helium.com/hotspots/${arg}`);
});


