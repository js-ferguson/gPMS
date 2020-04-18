var stripe = Stripe('pk_test_8KxhXqzKZUmD5s8iD0o0bw6a00MF744eUs');

var elements = stripe.elements();

var style = {
    base: {
        color: '#32325d',
        lineHeight: '24px',
        width: '30em',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
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
//var card = elements.create('card', {
//  hidePostalCode: true,
//  style: {
//    base: {
//      iconColor: '#666EE8',
//      color: '#31325F',
//      lineHeight: '40px',
//      fontWeight: 300,
 //     fontFamily: 'Helvetica Neue',
//      fontSize: '15px',
//      border:'2px',

//      '::placeholder': {
//        color: '#CFD7E0',
//      },
//    },
//  }
//});

card.mount('#card-element');

function setOutcome(result) {
  var successElement = document.querySelector('.success');
  var errorElement = document.querySelector('.error');
  successElement.classList.remove('visible');
  errorElement.classList.remove('visible');

  if (result.token) {
    // In this example, we're simply displaying the token
    successElement.querySelector('.token').textContent = result.token.id;
    successElement.classList.add('visible');

    // In a real integration, you'd submit the form with the token to your backend server
    //var form = document.querySelector('form');
    //form.querySelector('input[name="token"]').setAttribute('value', result.token.id);
    //form.submit();
  } else if (result.error) {
    errorElement.textContent = result.error.message;
    errorElement.classList.add('visible');
  }
}

card.on('change', function(event) {
  setOutcome(event);
});

document.querySelector('form').addEventListener('submit', function(e) {
e.preventDefault();
var options = {
name: document.getElementById('name').value,
address_line1: document.getElementById('address-line1').value,
address_line2: document.getElementById('address-line2').value,
address_city: document.getElementById('address-city').value,
address_state: document.getElementById('address-state').value,
address_zip: document.getElementById('address-zip').value,
address_country: document.getElementById('address-country').value,
};
stripe.createToken(card, options).then(setOutcome);
});
