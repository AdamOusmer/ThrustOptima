/*
*   *******************************************************************
*   Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
*   All Rights Reserved.
*   ******************************************************************
 */

const axios = require('axios');
window.api = require('electron').ipcRenderer;

const {port} = require('../../main.js')

let json_data = null;

function get_data(){
    axios.get(`http://localhost:${port}/load`).then(
        response => {
            json_data = response.data;
            console.log(json_data);
            display();

        }).catch(error => {
            console.log(error);
        });
}


function display(){

    let arr = json_data["data"];

    for (let i = 0; i < arr.length; i++){
        let option = document.createElement("option");
        option.value = i.toString();
        option.text = arr[i]["name"];
        document.getElementById("load").appendChild(option);
    }

}

function selected(){

}
