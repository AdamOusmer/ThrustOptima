const {app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const {spawn} = require('child_process');

let mainWindow;
let flaskProcess;

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

app.on('ready', () => {

    console.log(path.join(__dirname, '../../backend/thrust_optima.py'))

    flaskProcess = spawn('python3', [path.join(__dirname, '../../backend/thrust_optima.py')]);


    flaskProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    flaskProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    flaskProcess.on('close', (code) => {
        console.log(`Flask process exited with code ${code}`);
    });

    createWindow();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (mainWindow === null) createWindow();
});

app.on('before-quit', () => {
    flaskProcess.close();
    mainWindow.removeAllListeners('close');
    mainWindow.close();
});

ipcMain.on('hotspot-event', (event, arg) => {
    event.returnValue = 'Message received!'
    require('electron').shell.openExternal(`https://explorer.helium.com/hotspots/${arg}`);
});


