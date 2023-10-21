const fs = require("fs");
const {exec} = require("child_process");
const sqlite3 = require('sqlite3').verbose();

let database

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
        insert('dependency', 'True')

    });
}

export function boot() {
    // Function that will check for Python dependencies and install them if they are not installed
    // This function will also read the .thst file and check for user settings

    // Create a .thst file in the root directory if it doesn't exist
    // If it does exist, then don't install Python requirements

    if (!fs.existsSync('../../boot.thst')) {

        console.log("Creating .thst file...");

        createThstFile();

        installDependencies();

        insert('dependency', 'True')

        return;
    }

    // If the .thst file exists, then check if the Python dependencies are installed

    database = new sqlite3.Database('../../../../boot.thst', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error(err.message);
        } else {
            console.log('Connected to the database');
        }

    });

    // Check if the Python dependencies are installed
    database.run('SELECT value FROM settings WHERE name = "dependency"', (err, row) => {
        if (err) {
            console.error(err.message);
        } else {
            console.log(row.value);
            if (row.value === 'False') {
                installDependencies();
            }
        }
    });

    database.close();

}


function createThstFile() {
    // Function that will create a .thst file in the root directory
    // This file will contain user settings

    database = new sqlite3.Database('../../../../boot.thst')

    database.run('CREATE TABLE settings (name TEXT, value TEXT)')

    insert('theme', 'light')
    insert('language', 'english')
    insert('server', 'http://localhost:')
    insert('port', '5000')

    insert('dependency', 'False')

    database.close()

}

function insert(name, value) {
    // Function that will insert a new setting into the .thst file
    const pointer = database.prepare('INSERT INTO settings VALUES (?, ?)')

    pointer.run(name, value)

    pointer.finalize()
    pointer.close()
}

function update(name, value) {
    // Function that will update a setting in the .thst file
    database = new sqlite3.Database('../../../../boot.thst', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error(err.message);
        } else {
            console.log('Connected to the database');
        }
    });
    database.run('UPDATE users SET name = ? WHERE value = ?', [name, value], function (err) {
        if (err) {
            return console.error(err.message);
        }
        console.log(`Row(s) updated: ${this.changes}`);
    });

    database.close();
}
