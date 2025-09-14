async function loadSlots() {
    const API_URL = "http://127.0.0.1:8000/slots"
    try {
        const response = await fetch(API_URL);
        if(!response.ok) 
        {
            throw new Error("Response was not ok");
        }
        const slot = await response.json();
        console.log(slot)
        renderSlots(slot);
    } catch(error){
        document.getElementById("slots-container").innerHTML = "Error loading slots.";
        console.error(error);
    }
}

function renderSlots(slots) {
    let html = "";
    for (const slot of slots) {
        console.log(slot)
        html += `
            <div class="slot-card">
                <h3>${slot.datetime}</h3>
                <p>Turfid: ${slot.turfid}</p>
                <p>Price: ${slot.price}</p>
                <p>Available: ${slot.available}</p>
            </div>
        `;
    }
    document.getElementById("slots-container").innerHTML = html;
}