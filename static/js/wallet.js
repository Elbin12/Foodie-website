function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');



function payment(){
    var amount=document.getElementById('amount').value;

    fetch('/account/wallet/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'amount':amount}),
    })
    .then(response => response.json())
    .then(data => {
            // Initialize Razorpay and open the checkout dialog
            var rzp1 = new Razorpay({
                key: data.razorpay_merchant_key,
                amount: data.razorpay_amount,
                currency: data.currency,
                name: "Dj Razorpay",
                order_id: data.razorpay_order_id,
                callback_url: data.callback_url,
                // handler: function (response) {
                //     // Handle Razorpay response
                //     console.log('Razorpay Payment ID:', response.razorpay_payment_id);
                //     window.alert('Razorpay Payment ID:', response.razorpay_payment_id);
                //     const headers = new Headers();
                //     headers.append('Content-Type', 'application/json');
                //     headers.append('X-CSRFToken', csrftoken);
                // },
                theme: {
                    color: '#3399cc',
                },
            });

            rzp1.open();
        })
        .catch(error => {
            console.error('Error fetching Razorpay order details:', error);
        });
}
