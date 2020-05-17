var stripe = Stripe('pk_test_8KxhXqzKZUmD5s8iD0o0bw6a00MF744eUs');

var elements = stripe.elements();

var style = {
    base: {
        color: '#32325d',
        lineHeight: '24px',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        },
        'border-color': '#aab7c4',
    },
    invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
    }
};

var card = elements.create('card', {
    hidePostalCode: true,
    style: style,
});

card.mount('#card-element');

// Toggle the selected subscription
function toggleSublist(sub) {
    const sublist = document.getElementById('sublist');

    sublist.setAttribute('value', sub);
    displaySub(sublist);
}

function displaySub(sublist) {
   // const sublist = document.getElementById('sublist');
    successElement.className = '';
    successElement.querySelector('.selected-sub').textContent = sublist.value;
}

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    stripe.createToken(card).then(function(result) {
        if (result.error) {
            // Inform the user if there was an error.
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            // Send the token to your server.
            stripeTokenHandler(result.token);
        }
    });
});

var successElement = document.getElementById('display-selected-sub');
//document.querySelector('.wrapper').addEventListener('click', function() {
//    successElement.className = 'is-hidden';
//});

function stripeTokenHandler(token) {
    // Insert the token ID into the form so it gets submitted to the server
    var form = document.getElementById('payment-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);
    // Submit the form
    form.submit();
}

// Get all buttons with class="btn-lg" inside the container
var btns = document.getElementsByClassName("btn-lg");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}
