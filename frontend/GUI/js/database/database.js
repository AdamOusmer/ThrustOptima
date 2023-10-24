/*
*
* ******************************************************************
* Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
* All Rights Reserved.
* ******************************************************************
*
* This file contains the definition of all interaction with the database.
*
*/


const sqlite3 = require('sqlite3').verbose();

async function boot() {
    /*
    This function is designed to be used in the boot.js
    It will get from the database the value of dependency and will return it.
    */

    const database = new sqlite3.Database('boot.thst', (err) => {
        if (err) {
            console.error(err.message);
        }
    });

    let value = "";
    database.get('SELECT data FROM boot WHERE name = ?', ['dependency'], (err, row) => {
        if (err) {
            console.error(err.message);
        }
        if (row) {
            value = row.data;
        }

    });

    database.close();
    return value;

}


function insert(name, data) {
    // Function that will insert a new setting into the .thst file

    const database = new sqlite3.Database('boot.thst');

    const pointer = database.prepare('INSERT INTO boot VALUES (?, ?)');

    pointer.run(name, data);

    pointer.finalize();

    database.close();
}

async function update(name, data) {
    // Function that will update a setting in the .thst file

    const database = new sqlite3.Database('boot.thst', sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
            console.error(err.message);
        }

        database.run('UPDATE boot SET data = ? WHERE name = ?', [data, name], function (err) {
            if (err) {

                insert(name, data)
                return console.error(err.message);
            }
            console.log(`Row(s) updated: ${this.changes}`);
        });

    });

    database.close();
}

async function get_value(name) {
    // Function that will get a setting from the .thst file

    const database = new sqlite3.Database('boot.thst', sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error(err.message);
        }
    });

    let value

    database.get('SELECT data FROM boot WHERE name = ?', [name], (err, row) => {
        if (err) {
            console.error(err.message);
        }
        if (row) {
            value = row.data
        }

    });

    database.close();

    return value
}


module.exports = {
    boot,
    update,
    get_value
}