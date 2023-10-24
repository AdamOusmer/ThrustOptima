const axios = require('axios');
window.api = require('electron').ipcRenderer;

function get_data(){
    axios.get(`http://localhost:${port}/load`).then(
        response => {
            console.log(response.data);
        }).catch(error => {
            console.log(error);
        });
}


function display(){



}

function selected(){

}
