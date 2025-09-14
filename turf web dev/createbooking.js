async function validateForm() {
    const username = document.getElementById('username').value;
    const turfname = document.getElementById('turfname').value;

    if(username && turfname) {
        await fetchAndPopulateSlots(turfname);
    }
}

async function fetchAndPopulateSlots(turfname) {
    try {
        const turfResponse = await fetch('http://localhost:8000/turfs', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const turfs = await turfResponse.json();
        const requiredTurf = turfs.find(turf => turf.turfname === turfname);
        
        if (!requiredTurf) {
            throw new Error('Turf not found');
        }

        const slotResponse = await fetch('http://localhost:8000/slots', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const slots =  await slotResponse.json();

        const slotsSelect = document.getElementById('slotid');
        slotsSelect.disabled = false;

        slotsSelect.innerHTML = '<option value="">Select a slot</option>';

        slots.forEach(slot => {
            if(slot.available) {
                const option = document.createElement('option');
                option.value = slot.slotid;
                option.textContent = `${slot.datetime} - $${slot.price}`;
                slotsSelect.appendChild(option);
            }
        });
    } catch (error) {
        console.error('Error fetching slots:', error);
        alert('Error fetching slots: ' + error.message);
    }
}

async function createBooking(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const slotid = document.getElementById('slotid').value;
    const turfname = parseInt(document.getElementById('turfname').value);
    const paymentmethod = document.getElementById('paymentmethod').value;
    const paymentdonestatusInputs = document.querySelectorAll('input[name="paymentdonestatus"]:checked');
    const paymentdonestatus = paymentdonestatusInputs.length > 0 ? paymentdonestatusInputs[0].value : '';
    const approvedInputs = document.querySelectorAll('input[name="approved"]:checked');
    const approved = approvedInputs.length > 0 ? approvedInputs[0].value : '';

    

}
