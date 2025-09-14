async function createSlots(event) {
    event.preventDefault();
    
    const datetime = document.getElementById('datetime').value;
    const turfname = document.getElementById('turfname').value;
    const price = parseInt(document.getElementById('price').value);
    const availableInputs = document.querySelectorAll('input[name="available"]:checked');
    const available = availableInputs.length > 0 ? availableInputs[0].value : '';

    const response = await fetch ('http://localhost:8000/turfs',
    {
        method : 'GET',
        headers:
        {
            'Content-Available': 'application/json',
        }
    });
    const turfs = await response.json();
    let requiredturf = null;
    for(const turf of turfs)
    {
        if(turf.turfname==turfname)
        {
            requiredturf=turf;
            break;
        }
    }
    console.log(requiredturf);
    const slotData = {
        datetime: datetime,
        turfname: turfname,
        price: price,
        available: available,
        turfid: requiredturf.id
    };

    try{
        const response = await fetch('http://localhost:8000/slots',
            {
                method: 'POST',
                headers: {
                    'Content-available': 'application/json',
                },
                body: JSON.stringify(slotData)
            });

            if(!response.ok) {
                throw new Error('Netword response was not ok');
            }

            const result = await response.json();
            console.log('Success:', result);
            alert('Turf created successfully!');
    } catch(error) {
        console.error('Error:', error);
        alert('Error creating slots');
    }
}