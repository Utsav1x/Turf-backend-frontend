async function loadTurfs() {
    const API_URL = "http://127.0.0.1:8000/turfs";

    try {
        const response = await fetch(API_URL)
        if(!response.ok) {
            throw new Error("Response has error");
        }

        const turfs = await response.json();
        renderTurfs(turfs);
    }
    catch (error) {
        document.getElementById("turfs-container").innerHTML = "Error loading turfs.";
        console.error(error);
    }

}

function renderTurfs(turfs) {
    let html = "";
    for(const turf of turfs) {
        html += `
        <div class="turf-card">
          <h3>${turf.turfname}</h3>
          <p>Location: ${turf.location}</p>
          <p>Timing: ${turf.timing}</p>
          <p>Owner ID: ${turf.ownerid}</p>
          <p>Rating: ${turf.rating}</p>
        </div>
        `
    }
    document.getElementById("turfs-container").innerHTML = html;
}

