const { use } = require("react");

async function loadUsers() {
    const API_URL = "http://127.0.0.1:8000/users"
    try {
        const response = await fetch(API_URL);
        if(!response.ok) 
        {
            throw new Error("Response was not ok");
        }
        const user = await response.json();
        console.log(user)
        renderUser(user);
    } catch(error){
        document.getElementById("user-container").innerHTML = "Error loading users.";
        console.error(error);
    }
}

function renderUser(users) {
    let html = "";
    for (const user of users) {
        console.log(user)
        html += `
            <div class="user-card">
                <h3>${user.name}</h3>
                <p>Email: ${user.email}</p>
                <p>Password: ${user.password}</p>
                <p>Number: ${user.number}</p>
                <p>Type: ${user.type}</p>
            </div>
        `;
    }
    document.getElementById("user-container").innerHTML = html;
}