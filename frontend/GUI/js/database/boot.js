const fs = require("fs");
const {exec} = require("child_process");
const sqlite3 = require('sqlite3').verbose();


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
    // Function that will check for Python dependencies and install them if they are not installed
    // This function will also read the .thst file and check for user settings

    const database = new sqlite3.Database('boot.thst', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error(err.message);
        }
    });

    let value

    // Check if the Python dependencies are installed
    database.get('SELECT data FROM boot WHERE name = ?', ['dependency'], (err, row) => {
        if (err) {
            console.error(err.message);
        }
        if (row) {
            value = row.data

            console.log(value)

            if (value === 'False') {
                installDependencies();

                update('dependency', 'True')
            } else {

                update('dependency', 'True')

                console.log("Python dependencies already installed")
            }
        }

    });

    database.close();
    return true;

}


async function createThstFile() {
    const database = new sqlite3.Database('boot.thst', (err) => {
        if (err) {
            console.error(err.message);
            return;
        }
        console.log("Connected to the boot.thst database.");
    });
    database.run('CREATE TABLE IF NOT EXISTS boot (name TEXT NOT NULL, data TEXT NOT NULL)', (err) => {
        if (err) {
            console.error(err.message);
            return;
        }

        console.log('Table boot created successfully.');
    });

    database.close();

}


function insert(name, data) {
    // Function that will insert a new setting into the .thst file

    console.log('setting')

    const database = new sqlite3.Database('boot.thst');

    const pointer = database.prepare('INSERT INTO boot VALUES (?, ?)');

    pointer.run(name, data);

    pointer.finalize();

    database.close();

    console.log('set')
}

async function update(name, data) {
    // Function that will update a setting in the .thst file

    const database = new sqlite3.Database('boot.thst', sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
            console.error(err.message);
        }

        database.run('UPDATE boot SET data = ? WHERE name = ?', [data, name], function (err) {
            if (err) {
                return console.error(err.message);
            }
            console.log(`Row(s) updated: ${this.changes}`);
        });

    });

    database.close();
}


module.exports = {
    boot,
    update
}