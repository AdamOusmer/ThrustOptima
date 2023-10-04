const { app, BrowserWindow } = require('electron');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 800,
        webPreferences: {
            nodeIntegration: true
        }
    });

    mainWindow.loadFile('index.html');

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {

    const activeHandles = process.getProcessMemoryInfo()
    console.log(activeHandles);

    app.exit(0);
    process.exit(0)

});

app.on('activate', function () {
    if (mainWindow === null) createWindow();
});
