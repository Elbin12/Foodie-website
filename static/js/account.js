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



function edit(field) {

    const input = document.querySelector('.edit_'+field);
    var id= document.getElementById(field);
    var but=document.getElementById(field+'button')


    if (input) {
        if (id.innerHTML==='Cancel'){
            input.readOnly=true;
            input.style.border='none';
            id.innerHTML='Edit';
            but.style.display='none';
        }
        else{
            input.readOnly = false;
            input.style.border = '2px solid black';
            id.innerHTML='Cancel';
            but.style.display='block';
        }
    }
}

function enableEdit(){
  var first_name= document.getElementById('first_name'); 
  var last_name= document.getElementById('last_name'); 
  var gender= document.getElementById('gender'); 
  var mobile= document.getElementById('mobile'); 
  var edit=document.getElementById('edit');
  var save=document.getElementById('save');
  var genderDisplay = document.getElementById('genderDisplay');
  var genderEdit = document.getElementById('genderEdit');
  var but= document.getElementById('sentOTP')

    if (edit.innerHTML==='Cancel'){
        first_name.readOnly=true;
        last_name.readOnly=true;
        mobile.readOnly=true;
        save.style.display='none';
        but.style.display='none';
        edit.innerHTML='Edit profile';
        genderDisplay.style.display = 'block';
        genderEdit.style.display = 'none';
    }
    else{
        edit.innerHTML='Cancel';
        first_name.readOnly=false;
        last_name.readOnly=false;
        mobile.readOnly=false;
        but.style.display='block';
        edit.innerHTML='Cancel';
        save.style.display='block';
        genderDisplay.style.display = 'none';
        genderEdit.style.display = 'block';
    }
}


function updateSelectedGender(selectedGender) {
  document.getElementById('selectedGender').value = selectedGender;
}

// function cancelEdit(){
//   event.preventDefault()
//   var edit=document.getElementById('edit');
//   cancel=document.getElementById('cancel');
//   var first_name= document.getElementById('first_name'); 
//   var last_name= document.getElementById('last_name'); 
//   var gender= document.getElementById('gender'); 
//   var mobile= document.getElementById('mobile'); 
//   var email= document.getElementById('email'); 
// }


function showaddress() {
    var element = document.getElementById('showaddress');

    if (element.style.display === 'none' || element.style.display === '') {
        console.log('vannu');
        element.style.setProperty('display', 'flex', 'important');
    }
}

function hideaddress(){
    var element = document.getElementById('showaddress');
    if (element.style.display === 'flex'){
        element.style.setProperty('display', 'none', 'important');
    }
}


function editaddress(uid){
    var element=document.getElementById('edit_'+uid);

    if (element.style.display === 'none' || element.style.display === '') {
        console.log('vannu');
        element.style.setProperty('display', 'flex', 'important');
    }

}


function canceladdress(uid){
    var element=document.getElementById('edit_'+uid);
    if (element.style.display === 'flex'){
        element.style.setProperty('display', 'none', 'important');
    }
}


function del_address(uid) {
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!"
    }).then((result) => {
      if (result.isConfirmed) {
        var divToRemove = document.getElementById('address_' + uid);
        // Make an AJAX request to the backend to delete the item
        fetch('/account/delete_address/', {
          method: 'post', // Assuming your backend handles DELETE requests for deletion
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: JSON.stringify({ 'uid': uid }),
        })
        .then(response => response.json())
        .then(data => {
          // Handle the response from the server
          if (data.success) {
            console.log(data)
            Swal.fire({
              title: "Deleted!",
              text: "Your item has been deleted.",
              icon: "success"
            });
            divToRemove.parentNode.removeChild(divToRemove);
          } else {
            Swal.fire({
              title: "Error!",
              text: "Failed to delete the item.",
              icon: "error"
            });
          }
        })
        .catch(error => {
          console.error('Error:', error);
          Swal.fire({
            title: "Error!",
            text: "An error occurred while trying to delete the item.",
            icon: "error"
          });
        });
      }
    });
  }




function Up(uid) {
  event.preventDefault();
  console.log(uid)
    var qtyInput = document.querySelector('input[name="qty"][data-uid="' + uid + '"]');
    var final_price=document.getElementById('final_price_'+uid);
    var quantity=document.getElementById('quantity_'+uid);
    var price=document.getElementById('price_'+uid).innerText;
    var totalPrice=document.getElementById('totalPrice');
    console.log(qtyInput.value, final_price)

    var currentQty = parseInt(qtyInput.value);
    qtyInput.value = currentQty + 1;
    final_price.innerText=qtyInput.value*price;
    quantity.innerText=qtyInput.value


    if (document.getElementById('uid')){
      totalPrice=qtyInput.value*price;
      sentproduct(totalPrice, uid);
    }
    else{
      sentcart(qtyInput.value,uid);
    }
}

function Down(uid) {
  event.preventDefault();
    var qtyInput = document.querySelector('input[name="qty"][data-uid="' + uid + '"]');
    var final_price=document.getElementById('final_price_'+uid);
    var quantity=document.getElementById('quantity_'+uid);
    var price=document.getElementById('price_'+uid).innerText;
    var totalPrice=document.getElementById('totalPrice');

    var currentQty = parseInt(qtyInput.value);
    if (currentQty > 1){
      qtyInput.value = currentQty - 1;
      final_price.innerText=qtyInput.value*price;
      quantity.innerText=qtyInput.value;
      if (document.getElementById('uid')){
        totalPrice=qtyInput.value*price;
        sentproduct(totalPrice, uid);
      }
      else{
        sentcart(qtyInput.value,uid);
      }
    }
}



function sentproduct(totalPrice,uid){
  var discountPrice=document.getElementById('discountPrice');

  var requestBody = {
    'totalPrice':totalPrice,
    'uid': uid
};


  if (document.getElementById('selected_coupon')){
    var selected_coupon=document.getElementById('selected_coupon');
    coupon_uid = selected_coupon.value;
    var apply_button=document.getElementById('coupon_'+coupon_uid);
    console.log(selected_coupon, apply_button)

    requestBody.coupon = selected_coupon.value;
    console.log(requestBody)
  }
  fetch("/account/change/", {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if ('coupon_fail' in data){
        selected_coupon.remove();
        var totalPrice=document.getElementById('totalPrice');
        totalPrice.innerHTML=data.total;
        discountPrice.innerHTML = 0;
        apply_button.innerHTML = 'Apply';
        myFunction(data.coupon_fail)
      }
      else{
        console.log(data);
        var totalPrice=document.getElementById('totalPrice');
        totalPrice.innerHTML=data.total;
      }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function sentcart(newQty,uid){
  var discountPrice=document.getElementById('discountPrice');

  var requestBody = {
    'qty': newQty,
    'uid': uid
};


  if (document.getElementById('selected_coupon')){
    var selected_coupon=document.getElementById('selected_coupon');
    coupon_uid = selected_coupon.value;
    var apply_button=document.getElementById('coupon_'+coupon_uid);
    console.log(selected_coupon, apply_button)

    requestBody.coupon = selected_coupon.value;
    console.log(requestBody)
  }
  fetch("/account/change/", {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if ('coupon_fail' in data){
        selected_coupon.remove();
        var totalPrice=document.getElementById('totalPrice');
        totalPrice.innerHTML=data.total;
        discountPrice.innerHTML = 0;
        apply_button.innerHTML = 'Apply';
        myFunction(data.coupon_fail)
      }
      else{
        console.log(data);
        var totalPrice=document.getElementById('totalPrice');
        totalPrice.innerHTML=data.total;
        // change(uid, newQty,data.price,data.total);
      }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

if(document.getElementById('count')){
  var count=document.getElementById('count').value;
if (count==0){
  var error=document.getElementById('cart_zero');
  error.innerHTML='Your checkout is empty. Add some food items';
}
}





function hide(){
  event.preventDefault();
  if (document.getElementById('count')) {
    var count = document.getElementById('count').value;

    if (count != 0) {
        var delete_icons = document.getElementsByClassName('delete_icon');

        if (delete_icons.length > 0) {
            for (let i = 0; i < count; i++) {
                delete_icons[i].style.display = 'none';
            }
        }

        var address_section = document.getElementById('address-section');
        var payment_section = document.getElementById('payment-section');
        var order = document.getElementById('order');

        

        if (address_section && payment_section && order) {
            address_section.style.display = 'none';
            payment_section.style.display = 'block';
            order.style.display = 'block';
            var payment_method=document.getElementById('payment').value;
            console.log('segh',payment_method)
        } 
    }
}
}


 



function submitData(){
  var payment_method=document.getElementById('payment').value;
  if (payment_method=='select a method'){
      var paymentError=document.getElementById('paymentError');
      paymentError.innerText='Please select a payment method';
  }
  else{

    var radioButtons = document.querySelectorAll('input[name="address"]');
    var addressDetails = document.querySelectorAll('.address-detail');

  // Find the selected address
  var selectedAddress = findSelectedAddress(radioButtons, addressDetails);

  if (!selectedAddress) {
    console.error('No address selected');
    window.alert('No address selected');
    return;
  }

  console.log('Selected Address:', selectedAddress);
  
  if (document.getElementById('uid')){
    var uid=document.getElementById('uid').value;
    var product_name=document.getElementById('product_name_'+uid).innerHTML;
    var quantity=document.getElementById('quantity_'+uid).innerText;
    var unit_price=document.getElementById('price_'+uid).innerText;
    var final_price=document.getElementById('final_price_'+uid).innerText;
    var discountPrice = parseFloat(document.getElementById('discountPrice').innerText);
    var discount=document.getElementById('discountPrice');

    // if (!isNaN(discountPrice) && discountPrice>0){
    //   final_price=discountPrice;
    //   console.log(final_price)
    // }

    var requestBody = {
      'product_name': product_name,
      'quantity': quantity,
      'final_price': final_price,
      'unit_price': unit_price,
      'name':selectedAddress.name,
      'mob':selectedAddress.mobile_number,
      'address': selectedAddress.address,
      'payment_method':payment_method,
  };

  if (document.getElementById('selected_coupon')){
    var input=document.getElementById('selected_coupon');
    requestBody['selected_coupon'] = input.value;
    requestBody['discount'] = discount.innerText;
    
    console.log('opoin',input.value)
  }

  if (payment_method === 'Payment') {
    // Make a request to the server to get Razorpay order details
    fetch('/products/checkout/' + uid, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(requestBody),
    })
        .then(response => response.json())
        .then(data => {
          console.log(data)
            if ('expired' in data){
              myFunction(data.expired)
            }
            else{
              // Initialize Razorpay and open the checkout dialog
            var rzp1 = new Razorpay({
              key: data.razorpay_merchant_key,
              amount: data.razorpay_amount,
              currency: data.currency,
              name: "Foodie ",
              order_id: data.razorpay_order_id,
              callback_url: data.callback_url,
              handler: function (response) {
                  // Handle Razorpay response
                  console.log('Razorpay Payment ID:', response.razorpay_payment_id);
                  window.alert('Razorpay Payment ID:', response.razorpay_payment_id);
                  const headers = new Headers();
                  headers.append('Content-Type', 'application/json');
                  headers.append('X-CSRFToken', csrftoken);

                  // Now, send the order details to the server
                  sendOrderToServer(requestBody);
              },
              prefill: {
                  name: selectedAddress.name,
                  contact: selectedAddress.mobile_number,
              },
              notes: {
                  address: selectedAddress.address,
              },
              theme: {
                  color: '#3399cc',
              },
          });

          rzp1.open();
            }
        })
        .catch(error => {
            console.error('Error fetching Razorpay order details:', error);
        });
} 
else if( final_price > 1000 ){
  console.log("Products with above Rs. 1000 can't be purchased with Cash On Delivery. Please choose another method.")
  Swal.fire({
    position: "center",
    icon: "error",
    title: "Products with above Rs. 1000 can't be purchased with Cash On Delivery. Please choose another method.",
    showConfirmButton: false,
    timer: 1500
  });

}
else {
    // Handle other payment methods or send order details directly
    sendOrderToServer(requestBody, uid);
}
  }
  else{
    console.log('illla')
    var final_price=document.getElementById('totalPrice').innerText;
    var discountPrice = parseFloat(document.getElementById('discountPrice').innerText);
    var discount=document.getElementById('discountPrice');

    // if (!isNaN(discountPrice) && discountPrice>0){
    //   final_price=discountPrice;
    //   console.log(final_price)
    // }

    var requestBody = {
      'name':selectedAddress.name,
      'mob':selectedAddress.mobile_number,
      'address': selectedAddress.address,
      'final_price':final_price,
      'payment_method':payment_method,
  };

  if (document.getElementById('selected_coupon')){
    var input=document.getElementById('selected_coupon');
    requestBody['selected_coupon'] = input.value;
    requestBody['discount'] = discount.innerText;
    
    console.log(input.value)
  }

  if (payment_method === 'Payment') {
    // Make a request to the server to get Razorpay order details
    fetch('/products/checkout/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(requestBody),
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
                handler: function (response) {
                    // Handle Razorpay response
                    console.log('Razorpay Payment ID:', response.razorpay_payment_id);
                    window.alert('Razorpay Payment ID:', response.razorpay_payment_id);
                    const headers = new Headers();
                    headers.append('Content-Type', 'application/json');
                    headers.append('X-CSRFToken', csrftoken);

                },
                prefill: {
                    name: selectedAddress.name,
                    contact: selectedAddress.mobile_number,
                },
                notes: {
                    address: selectedAddress.address,
                },
                theme: {
                    color: '#d49948',
                },
            });

            rzp1.open();
        })
        .catch(error => {
            console.error('Error fetching Razorpay order details:', error);
        });
}
else if( final_price > 1000 ){
  console.log("Products with above Rs. 1000 can't be purchased with Cash On Delivery. Please choose another method.")
  Swal.fire({
    position: "center",
    icon: "error",
    title: "Products with above Rs. 1000 can't be purchased with Cash On Delivery. Please choose another method.",
    showConfirmButton: false,
    timer: 1500
  });

}

 else {
    // Handle other payment methods or send order details directly
    sendOrderToServer(requestBody);
}
}
}
}



function sendOrderToServer(orderDetails, uid='') {
  // Send the order details to the server
  if (uid !==''){
    fetch('/products/checkout/' + uid, {
      method: 'post',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify(orderDetails),
  })
      .then(response => response.json())
      .then(data => {
        console.log('n;lbhojfgjkmgl')
        console.log('Server Response:', data);
          // Handle the server response as needed
          if ('url' in data){
            console.log('Success:', data.url);
            console.log('Server Response:', data);
            Swal.fire({
              position: "center",
              icon: "success",
              title: "Order placed",
              showConfirmButton: false,
              timer: 1500
            });
            setTimeout(function () {
              window.location.href = data.url;
            }, 1400);
          }
          else if ('expired' in data) {
              myFunction(data.expired);
          }
          else if ('fail' in data){
            console.log(data.fail)
            Swal.fire({
              position: "center",
              icon: "error",
              title: data.fail,
              showConfirmButton: true,
            });
          }
      })
      .catch(error => {
        console.error('Error:', error);
  Swal.fire({
    position: "center",
    icon: "error",
    title: "An error occurred",
    showConfirmButton: true,
  });
      });
  }
  else{
    fetch('/products/checkout/', {
      method: 'post',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify(orderDetails),
  })
      .then(response => response.json())
      .then(data => {
          // Handle the server response as needed
          console.log('n;lbhojfgjkmgl')
        console.log('Server Response:', data);
          // Handle the server response as needed
          if ('url' in data){
            console.log('Success:', data.url);
            console.log('Server Response:', data);
            Swal.fire({
              position: "center",
              icon: "success",
              title: "Order placed",
              showConfirmButton: false,
              timer: 1500
            });
            setTimeout(function () {
              window.location.href = data.url;
            }, 1400);
          }
          else if ('expired' in data) {
              myFunction(data.expired);
          }
          else if ('fail' in data){
            console.log(data.fail)
            Swal.fire({
              position: "center",
              icon: "error",
              title: data.fail,
              showConfirmButton: true,
            });
          }
      })
      .catch(error => {
          console.error('Error processing order on the server:', error);
      });
  }
}

function findSelectedAddress(radioButtons, addressDetails) {
  var selectedAddressUid;

  // Find the UID of the checked radio button
  radioButtons.forEach(function (radioButton) {
    if (radioButton.checked) {
      selectedAddressUid = radioButton.value;
    }
  });

  // If no radio button is checked, return null
  if (!selectedAddressUid) {
    return null;
  }

  // Find the selected address div based on the UID
  var selectedAddressDiv = document.querySelector('.address-detail[data-uid="' + selectedAddressUid + '"]');

  // If the selected address div is not found, return null
  if (!selectedAddressDiv) {
    return null;
  }

  // Get the values from the selected address div
  var nameElement = selectedAddressDiv.querySelector('h6');
  var mobileNumberElement = selectedAddressDiv.querySelector('h6 + h6'); // Assuming mobile number is the next h6
  var addressElement = selectedAddressDiv.querySelector('p');

  // If any of the required elements is not found, return null
  if (!nameElement || !mobileNumberElement || !addressElement) {
    return null;
  }

  return {
    'name': nameElement.innerText.trim(),
    'mobile_number': mobileNumberElement.innerText.trim(),
    'address': addressElement.innerText.trim(),
  };
}

function del(uid) {
  Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!"
  }).then((result) => {
    if (result.isConfirmed) {
      var row = document.getElementById('product_row_'+uid)
      // Make an AJAX request to the backend to delete the item
      fetch('/account/delete/', {
        method: 'post', // Assuming your backend handles DELETE requests for deletion
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'uid': uid }),
      })
      .then(response => response.json())
      .then(data => {
        // Handle the response from the server
        if (data.success) {
          console.log(data)
          Swal.fire({
            title: "Deleted!",
            text: "Your item has been deleted.",
            icon: "success"
          });
          row.remove();
          var totalPrice=document.getElementById('totalPrice')
          var len=document.getElementById('totalItems')

          totalPrice.innerHTML=data.price
          len.innerHTML=data.len
          if (data.len===0){
            var message=document.getElementById('cart_zero');
            message.innerHTML='Your checkout is empty. Add some food item';
          }
          
        } else {
          Swal.fire({
            title: "Error!",
            text: "Failed to delete the item.",
            icon: "error"
          });
        }
      })
      .catch(error => {
        console.error('Error:', error);
        Swal.fire({
          title: "Error!",
          text: "An error occurred while trying to delete the item.",
          icon: "error"
        });
      });
    }
  });
}


function apply_coupon(coupon_uid){
  var total=document.getElementById('totalPrice');
  total_amount=total.innerText;
  console.log(total_amount)
  var discountPrice=document.getElementById('discountPrice');
  var apply_button=document.getElementById('coupon_'+coupon_uid);
  var class_=document.querySelector('.coupon-container');
  if (document.getElementById('selected_coupon')) {
    var input = document.getElementById('selected_coupon');
    input.remove();
}
  if (apply_button.innerHTML=='Applied'){
    console.log('ata')
    input.remove();
    apply_button.innerHTML='Apply';
    apply_button.removeAttribute('name');
    discountPrice.innerText=0;
  }
  else{
    var buttons=document.getElementsByClassName('apply-button');
    for (var i = 0; i < buttons.length; i++) {
      if (buttons[i].innerHTML == 'Applied') {
          console.log('sgf');
          buttons[i].innerHTML = 'Apply';
          buttons[i].removeAttribute('name');
      }
  }
    fetch('/products/apply_coupon/', {
      method: 'post', // Assuming your backend handles DELETE requests for deletion
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ 'coupon_uid': coupon_uid, 'total':total_amount }),
    })
    .then(response => response.json())
    .then (data =>{
      if (data.success){
        apply_button.innerHTML='Applied';
        var input=document.createElement('input');
        input.type='hidden';
        input.id='selected_coupon';
        input.value=coupon_uid;
        class_.appendChild(input);
        apply_button.name='coupon';
        discountPrice.innerText=data.discount;
        discountPrice.parentElement.style.display='block';
      }
      else{
        myFunction(data.fail)
        discountPrice.innerText=0;
      }
    })

  }
}




function myFunction(text) {
  var x = document.getElementById("snackbar");
  x.innerHTML=text
  x.classList.add("showing");
  setTimeout(function(){ x.classList.remove("showing"); }, 3000);
}







function sent(){
  event.preventDefault();
  var emailError=document.getElementById('emailError');
  var email=document.getElementById('email').value;
  var otp = document.getElementById('OTP');
  var submit = document.getElementById('submit');
  var ok = document.getElementById('sentOTP');

  fetch("/account/verify/", {

  method: 'post',
  headers: {
      // 'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
  },
  body : JSON.stringify({ 'email':email})
})
.then(response => {
  return response.json()
})
.then(data => {
  console.log(data);
  if ('success' in data){
      ok.style.display='none';
      otp.style.display='block';
      submit.style.display='block';
      emailError.textContent=data.success;
  }
  else{
    emailError.textContent=data.fail;
  }
})
}



function sentotp(){
  email=document.getElementById('email');
  otp=document.getElementById('OTP').value;
  emailError=document.getElementById('emailError');
  console.log('agr', otp);

  fetch("/account/check_otp/", {

    method: 'post',
    headers: {
        // 'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body : JSON.stringify({'otp':otp})
  })
  .then(response => {
    return response.json()
  })
  .then(data => {
    console.log(data);
    var otp = document.getElementById('OTP');
    var submit = document.getElementById('submit');
    if (data.success){
      otp.style.display='none';
      submit.style.display='none';
      email.readOnly=false;
      emailError.textContent=data.success;
    }
    else{
      otp.style.display='none';
      submit.style.display='none';
      emailError.textContent=data.fail;
    }

  })
}





function edit_address_from_checkout(uid){
  console.log('Inside edit_address function with UID:', uid);

  var name=document.getElementById('edit_name_'+uid).value;
  var mobile=document.getElementById('edit_mobile_'+uid).value;
  var pincode=document.getElementById('edit_pincode_'+uid).value;
  var locality=document.getElementById('edit_locality_'+uid).value;
  var shipping_address=document.getElementById('edit_address_'+uid).value;
  var city=document.getElementById('edit_city_'+uid).value;
  var state=document.getElementById('edit_state_'+uid).value;

  body={
    'uid':uid,
    'name':name,
    'mobile':mobile,
    'pincode':pincode,
    'locality':locality,
    'shipping_address':shipping_address,
    'city':city,
    'state':state,
  }

  fetch("/account/edit_address_from_checkout/", {

    method: 'post',
    headers: {
        // 'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body : JSON.stringify(body)
  })
  .then(response => {
    return response.json()
  })
  .then(data =>{
    var element=document.getElementById('edit_'+uid);
    if (element.style.display === 'flex'){
        element.style.setProperty('display', 'none', 'important');
    }
    myFunction(data.success)
  })

}




function edit_address_validateForm(uid) {
  console.log('Function called with UID:', uid);
  var edit_name = document.getElementById('edit_name_' + uid).value;
  console.log('edit_name:', edit_name);
  
  var edit_mobile = document.getElementById('edit_mobile_' + uid).value;
  var edit_pincode = document.getElementById('edit_pincode_' + uid).value;
  var edit_address = document.getElementById('edit_address_' + uid).value;
  var edit_city = document.getElementById('edit_city_' + uid).value;
  var edit_state = document.getElementById('edit_state_' + uid).value;
  var edit_locality = document.getElementById('edit_locality_' + uid).value;

  var edit_nameError = document.getElementById('edit_name_Error' + uid);
  var edit_mobileError = document.getElementById('edit_mobile_' + uid + 'Error');
  var edit_pincodeError = document.getElementById('edit_pincode_' + uid + 'Error');
  var edit_addressError = document.getElementById('edit_address_' + uid + 'Error');
  var edit_cityError = document.getElementById('edit_city_' + uid + 'Error');
  var edit_stateError = document.getElementById('edit_state_' + uid + 'Error');
  var edit_localityError = document.getElementById('edit_locality_' + uid + 'Error');

  edit_nameError.innerHTML = '';
  edit_mobileError.innerHTML = '';
  edit_pincodeError.innerHTML = '';
  edit_addressError.innerHTML = '';
  edit_cityError.innerHTML = '';
  edit_stateError.innerHTML = '';
  edit_localityError.innerHTML = '';

  if (edit_name.trim() === "") {
      edit_nameError.innerHTML = 'Username is required';
  }

  else if (edit_mobile.trim() === "") {
      edit_mobileError.innerHTML = 'Mobile number is required';
  }

  else if (edit_pincode.trim() === "") {
      edit_pincodeError.innerHTML = 'Pincode is required';
  }

  else if (edit_address.trim() === "") {
      edit_addressError.innerHTML = 'Address is required';
  }

  else if (edit_city.trim() === "") {
      edit_cityError.innerHTML = 'City is required';
  }

  else if (edit_state.trim() === "") {
      edit_stateError.innerHTML = 'State is required';
  }

  else if (edit_locality.trim() === "") {
      edit_localityError.innerHTML = 'Locality is required';
  }
  else{
    edit_address_from_checkout(uid)
  }
  
}




function add_address_from_checkout(){
  var name=document.getElementById('add_name').value;
  var mobile=document.getElementById('add_mobile').value;
  var pincode=document.getElementById('add_pincode').value;
  var locality=document.getElementById('add_locality').value;
  var shipping_address=document.getElementById('add_address').value;
  var city=document.getElementById('add_city').value;
  var state=document.getElementById('add_state').value;

  body={
    'name':name,
    'mobile':mobile,
    'pincode':pincode,
    'locality':locality,
    'shipping_address':shipping_address,
    'city':city,
    'state':state,
  }

  fetch("/account/add_address_from_checkout/", {

    method: 'post',
    headers: {
        // 'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body : JSON.stringify(body)
  })
  .then(response => {
    return response.json()
  })
  .then(data =>{
    var element = document.getElementById('showaddress');
    if (element.style.display === 'flex'){
        element.style.setProperty('display', 'none', 'important');
    }
    myFunction(data.success)
  })

}




// address validation edit and add 

function add_address_validateForm(){
  var add_name = document.getElementById('add_name').value;
  var add_mobile = document.getElementById('add_mobile').value;
  var add_pincode = document.getElementById('add_pincode').value;
  var add_address = document.getElementById('add_address').value;
  var add_city = document.getElementById('add_city').value;
  var add_state = document.getElementById('add_state').value;
  var add_locality = document.getElementById('add_locality').value;

  var add_nameError = document.getElementById('add_nameError');
  var add_mobileError = document.getElementById('add_mobileError');
  var add_pincodeError = document.getElementById('add_pincodeError');
  var add_addressError = document.getElementById('add_addressError');
  var add_cityError = document.getElementById('add_cityError');
  var add_stateError = document.getElementById('add_stateError');
  var add_localityError = document.getElementById('add_localityError');

  add_nameError.innerHTML = '';
  add_mobileError.innerHTML = '';
  add_pincodeError.innerHTML = '';
  add_addressError.innerHTML = '';
  add_cityError.innerHTML = '';
  add_stateError.innerHTML = '';
  add_localityError.innerHTML = '';

  if (add_name.trim()===""){
      add_nameError.innerHTML = 'Username is required';

  }

  else if (add_mobile.trim()===""){
    add_mobileError.innerHTML = 'mobile is required';
  }

  else if (add_pincode.trim()===""){
    add_pincodeError.innerHTML = 'pincode is required';
  }
  
  else if (add_locality.trim()===""){
    add_localityError.innerHTML = 'locality is required';
  }

  else if (add_address.trim()===""){
    add_addressError.innerHTML = 'address is required';
  }

  else if (add_city.trim()===""){
    add_cityError.innerHTML = 'city is required';
  }

  else if (add_state.trim()===""){
    add_stateError.innerHTML = 'state is required';
  }
  else{
    add_address_from_checkout()
  }
  
}




function add_address_validate() {
  var add_name = document.getElementById('add_name').value;
  var add_mobile = document.getElementById('add_mobile').value;
  var add_pincode = document.getElementById('add_pincode').value;
  var add_address = document.getElementById('add_address').value;
  var add_city = document.getElementById('add_city').value;
  var add_state = document.getElementById('add_state').value;
  var add_locality = document.getElementById('add_locality').value;

  var add_nameError = document.getElementById('add_nameError');
  var add_mobileError = document.getElementById('add_mobileError');
  var add_pincodeError = document.getElementById('add_pincodeError');
  var add_addressError = document.getElementById('add_addressError');
  var add_cityError = document.getElementById('add_cityError');
  var add_stateError = document.getElementById('add_stateError');
  var add_localityError = document.getElementById('add_localityError');

  add_nameError.innerHTML = '';
  add_mobileError.innerHTML = '';
  add_pincodeError.innerHTML = '';
  add_addressError.innerHTML = '';
  add_cityError.innerHTML = '';
  add_stateError.innerHTML = '';
  add_localityError.innerHTML = '';


  var alpha = /^[A-Za-z]+$/;
  if (add_name.trim() === "") {
      add_nameError.innerHTML = 'Username is required';
      return false;
  }

  if ( !add_name.match(alpha)) {
    add_nameError.innerHTML = 'Username must only have alphabets';
    return false;
}

  if (add_mobile.trim() === "") {
      add_mobileError.innerHTML = 'Mobile is required';
      return false;
  }
  var mobile_match = /^[0-9]+$/;
    if( !add_mobile.match(mobile_match) ){
      add_mobileError.innerHTML = 'Mobile number have only numbers';
        return false;
    }
    if (add_mobile.length !== 10){
      add_mobileError.innerHTML = 'Mobile number have only 10 digits';
        return false;
    }


  if (add_pincode.trim() === "") {
      add_pincodeError.innerHTML = 'Pincode is required';
      return false;
  }

  if (add_locality.trim() === "") {
      add_localityError.innerHTML = 'Locality is required';
      return false;
  }

  if (add_address.trim() === "") {
      add_addressError.innerHTML = 'Address is required';
      return false;
  }

  if (add_city.trim() === "") {
      add_cityError.innerHTML = 'City is required';
      return false;
  }

  if (add_state.trim() === "") {
      add_stateError.innerHTML = 'State is required';
      return false;
  }

  return true;
}


function edit_address_validate(uid){

  console.log('Function called with UID:', uid);
  var edit_name = document.getElementById('edit_name_' + uid).value;
  console.log('edit_name:', edit_name);
  
  var edit_mobile = document.getElementById('edit_mobile_' + uid).value;
  var edit_pincode = document.getElementById('edit_pincode_' + uid).value;
  var edit_address = document.getElementById('edit_address_' + uid).value;
  var edit_city = document.getElementById('edit_city_' + uid).value;
  var edit_state = document.getElementById('edit_state_' + uid).value;
  var edit_locality = document.getElementById('edit_locality_' + uid).value;

  var edit_nameError = document.getElementById('edit_name_Error' + uid);
  var edit_mobileError = document.getElementById('edit_mobile_' + uid + 'Error');
  var edit_pincodeError = document.getElementById('edit_pincode_' + uid + 'Error');
  var edit_addressError = document.getElementById('edit_address_' + uid + 'Error');
  var edit_cityError = document.getElementById('edit_city_' + uid + 'Error');
  var edit_stateError = document.getElementById('edit_state_' + uid + 'Error');
  var edit_localityError = document.getElementById('edit_locality_' + uid + 'Error');

  edit_nameError.innerHTML = '';
  edit_mobileError.innerHTML = '';
  edit_pincodeError.innerHTML = '';
  edit_addressError.innerHTML = '';
  edit_cityError.innerHTML = '';
  edit_stateError.innerHTML = '';
  edit_localityError.innerHTML = '';

  var alpha = /^[A-Za-z]+$/;
  if (edit_name.trim() === "") {
      edit_nameError.innerHTML = 'Username is required';
      return false;
  }

  if ( !edit_name.match(alpha)) {
    edit_nameError.innerHTML = 'Username must have only alphabets';
    return false;
}

  if (edit_mobile.trim() === "") {
      edit_mobileError.innerHTML = 'Mobile number is required';
      return false;
  }

  var mobile_match = /^[0-9]+$/;
    if( !edit_mobile.match(mobile_match) ){
      edit_mobileError.innerHTML = 'Mobile number have only numbers';
        return false;
    }
    if (edit_mobile.length !== 10){
      edit_mobileError.innerHTML = 'Mobile number have only 10 digits';
        return false;
    }

  if (edit_pincode.trim() === "") {
      edit_pincodeError.innerHTML = 'Pincode is required';
      return false;
  }

  if (edit_address.trim() === "") {
      edit_addressError.innerHTML = 'Address is required';
      return false;
  }

  if (edit_city.trim() === "") {
      edit_cityError.innerHTML = 'City is required';
      return false;
  }

  if (edit_state.trim() === "") {
      edit_stateError.innerHTML = 'State is required';
      return false;
  }

  if (edit_locality.trim() === "") {
      edit_localityError.innerHTML = 'Locality is required';
      return false;
  }
  else{
    edit_address_from_checkout(uid)
  }

}