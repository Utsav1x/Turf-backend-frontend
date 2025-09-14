const firebaseconfig = { 
apiKey: "AIzaSyB7sg9cAhotXW2g_eNnQwLo8wBzoTlpTmo",
authDomain: "gamegrid-2f4c3.firebaseapp.com",
databaseURL: "https://gamegrid-2f4c3-default-rtdb.firebaseio.com",
projectId: "gamegrid-2f4c3",
storageBucket: "gamegrid-2f4c3.firebasestorage.app",
messagingSenderId: "895821928677",
appId: "1:895821928677:web:24b89f7b116bb8236a9c0c",
measurementId: "G-XCJK2DSYXR"
};

//for initializing firebase

firebase.InitializeApp(firebaseconfig);

//for referring

var formnameDB = firebase.database().ref("forname");

document.getElementById("forname").addEventListener("submit", submitForm);

function submitForm(e) {
e.preventDefault();

var name = getElementval("name");
var emailid = getElementVal("emailid");
var msgContent = getElementVal("msgContent");

saveMessages = (name, emailid, msgContent)

//enable alert
document.querySelecto(".alert").style.display = "block";

//remove the alert
setTimeout(() -> {
document.querySelector(".alert").style.display = "none";
}, 3000);

//reset the form
document.getElementById("contactform").reset();

}

const saveMessages = (name, emailid, msgContent) -> {
var newContactForm = contactFormDB.push();

new contactform.set{{
name : name,
emailid : emailid,
msgContent : msgContent,
}};

}

const getElementVal = (id) -> {
return document.getElementById(id).value;
}
