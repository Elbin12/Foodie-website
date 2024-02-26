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

let image = document.querySelector('.img');
image.addEventListener('mouseleave', function(){
    let lens = document.getElementById('lens');
    console.log('Mouse left image');
    lens.style.display = 'none';
});


function passUid(uid){
    uid=uid
    document.getElementById('big_'+uid).addEventListener('mouseover', function(){
        imageZoom('big_'+uid)
    })
}

function imageZoom(imgID){

    let img=document.getElementById(imgID);
    let lens = document.getElementById('lens');

    console.log('Image zoom function called');
    console.log('Image source:', img.src);

    lens.style.backgroundImage= `url(${img.src})`;
    
    let ratio = 5;
    lens.style.backgroundSize=(img.width * ratio) + 'px ' + (img.height * ratio) + 'px';
    


    img.addEventListener("mousemove", moveLens);
    lens.addEventListener("mousemove",moveLens);
    img.addEventListener("touchmove",moveLens)

    function moveLens(event) {
        console.log('Mouse moved over image');
    
        let pos = getCursor(event);
        console.log('pos:', pos);
    
        let lensWidth = 300; // Adjust as needed
        let lensHeight = 300; // Adjust as needed
    
        let positionLeft = pos.x - (lensWidth / 2);
        let positionTop = pos.y - (lensHeight / 2);
    
        console.log('Lens position:', { left: positionLeft, top: positionTop });
    
        // Adjust lens position to stay within image boundaries
        if (positionLeft < 0) {
            positionLeft = 0;
        }
        if (positionTop < 0) {
            positionTop = 0;
        }
        if (positionLeft > img.width - lensWidth) {
            positionLeft = img.width - lensWidth;
        }
        if (positionTop > img.height - lensHeight) {
            positionTop = img.height - lensHeight;
        }
    
        lens.style.display = 'block';
    
        // Adjust background position to show zoomed image within lens
        lens.style.backgroundSize = (img.width * ratio) + 'px ' + (img.height * ratio) + 'px';
        lens.style.backgroundPosition = "-" + (pos.x * ratio - lensWidth / 2) + 'px' + " -" + (pos.y * ratio - lensHeight / 2) + 'px';
    }

    function getCursor(e){
        let bounds=img.getBoundingClientRect();
        console.log('e',e);
        console.log('bounds',bounds)
        let x=e.pageX-bounds.left;
        let y=e.pageY-bounds.top;
        x=x - window.scrollX;
        y=y-window.screenY;
        return {'x':x , 'y':y};
    }
}




// image selecting 


function showImage(uid,product){
    var big_image=document.getElementById('big_'+product);
    var small_image=document.getElementById('small_'+uid);

    image = big_image.src;
    big_image.src=small_image.src;
}


function add_to_cart(uid){
    values=document.querySelectorAll('.values-select');
    selectedValues=[]
    values.forEach(function(value){
        var selectedKey = value.getAttribute('data-key');
        var selectedValue = value.value;
        selectedValues.push(selectedValue);
    })
    console.log(selectedValues, uid)
    fetch('/account/add_to_cart/',{
        method: 'post', // Assuming your backend handles DELETE requests for deletion
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'uid': uid, 'selected_values':selectedValues }),
    })
    .then(response => response.json())
    .then(data =>{
        if (data.success){
            myFunction(data.success)
        }
        if (data.exists){
            myFunction(data.exists)
        }
        if(data.fail){
            myFunction(data.fail)
        }
    })

}



function myFunction(text) {
    var x = document.getElementById("snackbar");
    x.innerHTML=text
    x.classList.add("showing");
    setTimeout(function(){ x.classList.remove("showing"); }, 3000);
  }

var radioButtons = document.getElementsByName('selectedValue');
radioButtons[0].checked='checked';


  function changevalue(value,uid) {
    var radioButtons = document.getElementsByName('selectedValue');
    for (var i = 0; i < radioButtons.length; i++) {
        radioButtons[i].checked = (radioButtons[i].value === value);
    }
    console.log( value, uid)

    fetch('/products/get_value_price/',{
        method: 'post', // Assuming your backend handles DELETE requests for deletion
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'value': value, 'uid':uid }),
    })
    .then(response => response.json())
    .then(data =>{
        var product_price=document.getElementById('product_price');
        product_price.innerHTML='₹ '+data.new_price;
    })
}