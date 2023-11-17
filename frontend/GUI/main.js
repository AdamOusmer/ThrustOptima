/*
*
* ******************************************************************
* Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
* All Rights Reserved.
* ******************************************************************
*
* This file is the main file for the Electron GUI. It is responsible for starting the Flask server and the Electron GUI.
*
* When the application 'ready', the thrust_optima.py file is spawned as a child process. The stdout of the process is used
* to determine when the server is fully functional. The port number is also extracted from the stdout. Once the server is
* started, the stdout will contain the message "port='... '" followed by 'Starting server...' enabling the fronted to access
* the backend. The GUI is then started and the server is accessed at the index route to initialize the backend database.
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
let server_connected = false

let port = "";


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
    mainWindow.loadFile(path.join(__dirname, 'html/index.html')).then(r => console.log("Loaded index.html"));

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', () => {


    boot.boot();

    // Start Flask server

    serverProcess = spawn('python3', [path.join(__dirname, '../../backend/ThrustOptimaAnalyzer/thrust_optima.py')]);

    serverProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);

        if (data.includes("port=")){
            console.log("port found")

            port = data.toString().replace("port=", "")
        }

        if (data.includes('Starting server...')) {
            // Server is fully functional, the GUI can be started and the server can be accessed
            createWindow();

            axios.get(`http://localhost:${port}/`).then(
                response => {
                    console.log(response.data);
                    server_connected = true
                }
            ).catch(error => {
                console.log(error);

                // TODO save error in database

                serverProcess = spawn('python3', [path.join(__dirname, '../../backend/ThrustOptimaAnalyzer/thrust_optima.py')])
                console.error("Server restarted")
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

app.on('before-quit', async () => { // Async is required for the axios call to work properly and entirely
    await axios.post(`http://localhost:${port}/cleanup`)
        .then(response => {
            console.log(response.data);

            serverProcess.kill('SIGINT');
        })
        .catch(error => {
            console.error(error);

            serverProcess = spawn('python3', [path.join(__dirname, '../../backend/ThrustOptimaAnalyzer/thrust_optima.py')])
            console.error("Server restarted")

        });

});

ipcMain.on('hotspot-event', (event, arg) => {
    event.returnValue = 'Message received!'
    require('electron').shell.openExternal(`https://explorer.helium.com/hotspots/${arg}`).then();
});


module.exports = {
    port
}


