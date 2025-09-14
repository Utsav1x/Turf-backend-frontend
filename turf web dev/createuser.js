async function createUser(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Get form values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const number = parseInt(document.getElementById('number').value);
    
    // Get selected type (radio/checkbox)
    const typeInputs = document.querySelectorAll('input[name="type"]:checked');
    const type = typeInputs.length > 0 ? typeInputs[0].value : '';

    // Create user object
    const userData = {
        name: name,
        email: email,
        password: password,
        number: number,
        type: type
    };

    try {
        const response = await fetch('http://localhost:8000/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log('Success:', result);
        // Redirect or show success message
        alert('User created successfully!');
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating user');
    }
}