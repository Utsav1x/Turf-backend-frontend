async function loadBooking() {
    const API_URL = "http://127.0.0.1:8000/booking"
    try {
        const response = await fetch(API_URL);
        if(!response.ok) 
        {
            throw new Error("Response was not ok");
        }
        const booking = await response.json();
        console.log(booking)
        renderBooking(booking);
    } catch(error){
        document.getElementById("booking-container").innerHTML = "Error loading bookings.";
        console.error(error);
    }
}

function renderBooking(bookings) {
    let html = "";
    for (const booking of bookings) {
        console.log(booking)
        html += `
            <div class="booking-card">
                <h3>${booking.userid}</h3>
                <p>slotid: ${booking.slotid}</p>
                <p>Bookingtime: ${booking.bookingtime}</p>
                <p>Paymentmethod: ${booking.paymentmethod}</p>
                <p>Paymentdonestatus: ${booking.paymentdonestatus}</p>
                <p>Approved: ${booking.approved}</p>
            </div>
        `;
    }
    document.getElementById("booking-container").innerHTML = html;
}