/*
*
* ******************************************************************
* Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
* All Rights Reserved.
* ******************************************************************
*
*/

const database = require('./database/database.js');
const {exec} = require("child_process");



function installDependencies() {
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
}

async function boot() {
    if (await database.boot()) {
        installDependencies();

        await database.update('dependency', 'True');

        console.log('Python dependencies installed successfully.');
    }

    else {
        console.log('Python dependencies already installed.');
    }
}

module.exports =  {boot};
