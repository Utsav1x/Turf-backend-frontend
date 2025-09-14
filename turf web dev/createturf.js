async function createTurf(event) {
    event.preventDefault();

    // Get form values
    const turfname = document.getElementById('turfname').value;
    const location = document.getElementById('location').value;
    const startTime = document.getElementById('timing').value;
    const endTime = document.getElementById('timing').value;
    const username = document.getElementById('username').value;
    const rating = parseFloat(document.getElementById('rating').value);
    
    // Combine start and end time
    const timing = `${startTime} - ${endTime}`;

    const response = await fetch('http://localhost:8000/users', 
    {

        method : 'GET',
        headers: 
        {
            'Content-Type': 'application/json',
        }

    });
    console.log("username is"+username);
    const users = await response.json();
    console.log(users);
    let requireduser = null;
    for (const user of users) {
        if(user.name==username)
        {
            requireduser = user;
            break;
        }        
    }
    console.log(requireduser);
    // Create turf object
    const turfData = {
        turfname: turfname,
        location: location,
        timing: timing,
        rating: rating,
        ownerid: requireduser.id // You might want to get this from logged-in user session
    };

    try {
        const response = await fetch('http://localhost:8000/turfs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(turfData)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log('Success:', result);
        alert('Turf created successfully!');
        // Optionally redirect to turfs list page
        // window.location.href = 'turfs.html';
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating turf');
    }
}