let contact = document.getElementById('contactForm');
let inputs = document.querySelectorAll('.form-control');
let message = document.getElementById('successMessage');

function showMessage(event) {
    console.log('Hello')
    event.preventDefault();
    for(let i = 0; i < inputs.length; i++) {inputs[i].value = "";}
    message.hidden = false;
    setTimeout(() => {message.hidden = true}, 5000);
}

contact.addEventListener('submit', showMessage);