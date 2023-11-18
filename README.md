<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 25px;">
<img src="frontend/GUI/assets/img/ThrustOptima_Banner.png" alt="" style="height: 400px; border-radius: 25px">
</div>

# ThrustOptima

> By [Adam Ousmer](https://github.com/AdamOusmer)
> for [Space Concordia - Rocketry Division](https://spaceconcordia.ca/rocketry)

[![License](https://img.shields.io/badge/License-See%20License-blue.svg)](./LICENSE.md) [![Release](https://img.shields.io/badge/Release-None-green)](https://GitHub.com/AdamOusmer/ThrustOptima/releases/) [![Version](https://img.shields.io/badge/Version-None-red)](https://GitHub.com/AdamOusmer/ThrustOptima/releases/) [![Theory](https://img.shields.io/badge/Theory-See%20Theory-yellow)](Theory.md)

## Project Status

[![Status](https://img.shields.io/badge/Status-In%20Development-orange)]()

## Introduction

The main purpose of this software is to calculate the propensity of a rocket engine using a CT SCAN.

The software will be able to:

> - Calculate the propensity of every scan read from a DICOMDIR file.
>- Determine the edges of any objects that contain one external edge and an optional internal edge.
> - This software is using a custom .thst file for database and user's options and .optm files to save user's data.


_Future updates:_
> - 3D rendering of the CT scan.

## Installation

> _Available soon_

For now, please make sure that you have python 3.11 or higher installed on your computer. (in future updates we will
provide a standalone version of the software)

## Usage

> _Available soon_

For now, the main.js file is the main file to run the software. (in future updates we will provide a standalone version
of the software)

## Theory

This software is based on the following theory:

- [Medical Files (CT Scans)](Theory.md#medical-files-ct-scans)
- [Computer Vision](Theory.md#computer-vision)
- [Electron and Flask](Theory.md#electron-and-flask)

_Read the [theory](Theory.md) file for more information about the theory behind this software._

## Coding Practice and Style

### Naming Conventions

- Variables and functions names should be written using the snake_case naming style.
- Class names should be written using the PascalCase naming style.
- Constants should be written using the UPPER_CASE naming style.

### Comments

- Comments should be written in English and docstrings should be written in English.
- Docstring should contain:
  > - A description of the function.
  >- A description of the parameters.
  >- A description of the return value.

### Code Structure

In order to make the code more readable and understandable, the following rules should be followed when writing code for
this project.
These rules are made in order to make the code more readable, understandable, accessible, modulable and maintainable.

- The code should be structured in a way that is easy to read and understand.

#### Functions

- Functions used inside a unique function should be placed as a nested function.

#### Classes

- Class used to support another a unique class should be placed as an inner-class.
- Class used to support multiple classes should be placed in a separate file.

#### Modules

- Modules should be access using a controller class named (name of the class)_controller. The modules should never be
  accessed directly by the user or the main process of both the frontend and the backend.

## Dependencies

This software is
an [Electron](https://www.electronjs.org), [Flask](https://flask.palletsprojects.com/en/3.0.x/), [Waitress WSGI](https://pypi.org/project/waitress/)
and [Python](https://www.python.org) 3.11 project.
>
> It uses the following libraries for the frontend:
> - [axios](https://axios-http.com/docs/intro)
> - [sqlite3](https://www.sqlite.org/index.html)

> It uses the following libraries for the backend:
> - [Pydicom](https://pydicom.github.io/pydicom/dev/index.html#)
> - [Numpy](https://numpy.org/doc/)
> - [Tkinter](https://docs.python.org/3/library/tkinter.html)
> - [Matplotlib](https://matplotlib.org/stable/contents.html)
> - [scikit-image](https://scikit-image.org)
> - [OpenCV](https://docs.opencv.org/master/)
> - [Sqlite3](https://www.sqlite.org/index.html)

## Main Components of the Software

- [main.js](frontend/GUI/main.js)
- [thrust_optima.py](backend/src/thrust_optima.py)
- [scans.py](backend/src/Scans/scans.py)

### Main.js

This file is the main file of the software. It is responsible to initialize both the frontend and the backend and
install the python dependencies.
The backend is launched as a spawn process using node.js. At the launch of the application, the backend is initialized,
the port is retrieved and the frontend is launched.
It will then initialize the frontend database and send a http request to the backend to initialize his database.

```javascript
// main.js
app.on('ready', () => {
    boot.boot(); // Initialize the frontend database and install the required python packages

    // Start Flask server
    serverProcess = spawn('python3', [path.join(__dirname, '../../backend/src/thrust_optima.py')]);
    serverProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);

        if (data.includes("port=")) { // Retrieve the port
            console.log("port found")

            port = data.toString().replace("port=", "")
        }

        if (data.includes('Starting server...')) {
            // Server is fully functional, the GUI can be started and the server can be accessed
            createWindow();

            axios.get(`http://localhost:${port}/`).then( // Initialize the backend database
                response => {
                    console.log(response.data);
                    server_connected = true
                }
            ).catch(error => {
                console.error(error);
                serverProcess = spawn('python3', [path.join(__dirname, '../../backend/src/thrust_optima.py')])
                console.error("Server restarted")
            });
        }
    });
    // [...]
});
```

The main.js file is also responsible to send http requests to the backend to start the cleanup process and to close the
backend process when the application is closed before it quits.

```javascript
// main.js
app.on('before-quit', () => {
    axios.post(`http://localhost:${port}/cleanup`)
        .then(response => {
            console.log(response.data);
            serverProcess.kill('SIGINT');
        })
        .catch(error => {
            console.error(error);
            serverProcess = spawn('python3', [path.join(__dirname, '../../backend/src/thrust_optima.py')])
            console.error("Server restarted")
        });
});
```

## Credits

> Font :
> - [Playfair-Display](https://github.com/clauseggers/Playfair-Display)

## [License](LICENSE.md)

This project has been developed by [Adam Ousmer](https://github.com/AdamOusmer) for the exclusive usage
of [Space Concordia - Rocketry Division](https://spaceconcordia.ca/rocketry).

## References

> _Available soon_

## Contributing

### If you are part of Space Concordia - Rocketry Division

- You can fork this project and make a pull request to the main branch.

> You are allowed to use and access this project if you are using it for Space Concordia - Rocketry Division and with
> the approval of a lead. <br>

### If you are not part of Space Concordia - Rocketry Division

- You can fork this project and make a pull request to the main branch with written approval of Space Concordia -
  Rocketry Division.

## Contact

Please note that this project is developed for the exclusive usage
of [Space Concordia - Rocketry Division](https://spaceconcordia.ca/rocketry).

- Adam Ousmer
    - [adam.ousmer@spaceconcordia.ca](mailto:adam.ousmer@spaceconcordia.ca)

- Space Concordia - Rocketry Division
    - [https://spaceconcordia.ca/rocketry](https://spaceconcordia.ca/rocketry)
