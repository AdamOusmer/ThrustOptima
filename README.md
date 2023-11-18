<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 25px;">
<img src="frontend/GUI/assets/img/ThrustOptima_Banner.png" alt="" style="height: 400px; border-radius: 25px">
</div>

# ThrustOptima
>By [Adam Ousmer](https://github.com/AdamOusmer) for [Space Concordia - Rocketry Division](https://spaceconcordia.ca/rocketry)

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

For now, please make sure that you have python 3.11 or higher installed on your computer. (in future updates we will provide a standalone version of the software)


## Usage

> _Available soon_

For now, the main.js file is the main file to run the software. (in future updates we will provide a standalone version of the software)

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
  >- A description of the function.
  >- A description of the parameters.
  >- A description of the return value.

### Code Structure
#### Functions 
- The code should be structured in a way that is easy to read and understand.
- Functions used inside a unique function should be placed as a nested function.
- Class used to support another a unique class should be placed as an inner-class

## Dependencies
 This software is an [Electron](https://www.electronjs.org), [Flask](https://flask.palletsprojects.com/en/3.0.x/), [Waitress WSGI](https://pypi.org/project/waitress/) and [Python](https://www.python.org) 3.11 project.
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


## Credits

> Font :
> - [Playfair-Display](https://github.com/clauseggers/Playfair-Display)

## [License](LICENSE.md)

This project has been developed by [Adam Ousmer](https://github.com/AdamOusmer) for the exclusive usage of [Space Concordia - Rocketry Division](https://spaceconcordia.ca/rocketry).


## References

> _Available soon_


## Contributing

### If you are part of Space Concordia - Rocketry Division
- You can fork this project and make a pull request to the main branch.
> You are allowed to use and access this project if you are using it for Space Concordia - Rocketry Division and with the approval of a lead. <br>

### If you are not part of Space Concordia - Rocketry Division
- You can fork this project and make a pull request to the main branch with written approval of Space Concordia - Rocketry Division.

## Contact
Please note that this project is developed for the exclusive usage of [Space Concordia - Rocketry Division](https://spaceconcordia.ca/rocketry).

- Adam Ousmer 
    - [adam.ousmer@spaceconcordia.ca](mailto:adam.ousmer@spaceconcordia.ca)

- Space Concordia - Rocketry Division
    - [https://spaceconcordia.ca/rocketry](https://spaceconcordia.ca/rocketry)
