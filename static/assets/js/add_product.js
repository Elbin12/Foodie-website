function validateForm(){
    var product_name = document.getElementById('product_name').value;
    var category = document.getElementById('category').value;
    var sub_category = document.getElementById('sub_category').value;
    var description = document.getElementById('description').value;
    var image = document.getElementById('image').value;
    var price = document.getElementById('price').value;

    var product_nameError = document.getElementById('product_nameError');
    var categoryError = document.getElementById('categoryError');
    var sub_categoryError = document.getElementById('sub_categoryError');
    var descriptionError = document.getElementById('descriptionError');
    var imageError = document.getElementById('imageError');
    var priceError = document.getElementById('priceError');

    product_nameError.innerHTML = '';
    categoryError.innerHTML = '';
    sub_categoryError.innerHTML = '';
    descriptionError.innerHTML = '';
    priceError.innerHTML='';
    imageError.innerHTML='';

    if (product_name===""){
        product_nameError.innerHTML = 'product name is required';
        return false;
    }

    if (category===""){
        categoryError.innerHTML = 'category is required';
        return false;
    }

    if (sub_category===""){
        sub_categoryError.innerHTML = 'sub category is required';
        return false;
    }

    if (description===""){
        descriptionError.innerHTML = 'description is required';
        return false;
    }

    if (image===""){
        imageError.innerHTML = 'image is required';
        return false;
    }

    if (price==="" ){
        priceError.innerHTML = 'price is required';
        return false;
    }
    price = parseFloat(price);

    if (price<0){
        priceError.innerHTML = 'Price must be positive';
        return false;
    }



    return true;
}



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


// let but=document.getElementById('category');

// but.onchange= function(e){
//     let category=document.getElementById('category').value;
//     get_sub_category(category);

// }

function get_sub_category(){

    let category=document.getElementById('category').value;

    fetch("/product/get_sub_categories/", {

        method: 'post',
        headers: {
            // 'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body : JSON.stringify({'category':category})
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        show(data);
    })
}

function show(data){

    let option = '';
    document.getElementById('sub_category').innerHTML='';
    document.getElementById('sub_category').innerHTML+='<option value="" selected></option>';


    for (let sub_category of data.sub_categories){
        option += `<option>
        ${sub_category.sub_category_name}
        </option>`
    }
    document.getElementById('sub_category').innerHTML+=option;

}



function addimage(){
    var input = document.createElement("input");
    input.type = "file";

    input.name='image';
    input.className="form-control";

    var add_image = document.getElementById("add-image");

    add_image.appendChild(input);
}



function selected(attribute){
    var inputElement=document.getElementById(attribute);

    if (inputElement.name==""){
        inputElement.value=attribute;
        inputElement.name=attribute;
    }
    else{
        inputElement.value="";
        inputElement.name="";
    }
}

function addFile(uid){

    var savebutton = document.getElementById('save_'+uid)
    var input = document.getElementById('new_'+uid);
    var imagePreview=document.getElementById('preview_'+uid)
    
    if (input && savebutton){
        input.remove();
        savebutton.remove();
        imagePreview.remove();
    }
    else{
        var input = document.createElement("input");
        var savebutton=document.createElement("button");
        var imagePreview = document.createElement("img");

        input.type = "file";
        input.name='new_image';
        input.className="form-control";
        input.id='new_'+uid;

        savebutton.id='save_'+uid;
        savebutton.className = 'btn btn-md rounded font-sm hover-up';
        savebutton.textContent = 'Change Image';

        imagePreview.id = 'preview_' + uid;
        imagePreview.className = 'img-preview';
    
        var add_image = document.getElementById('button_'+uid);
    
        savebutton.onclick = function() {
            event.preventDefault();
            sendNewImage(uid);
            
        };

        add_image.appendChild(input);
        add_image.appendChild(savebutton);
        add_image.appendChild(imagePreview);

    }
}


function sendNewImage(uid){

    var new_image_file=document.getElementById('new_'+uid);
    var imagePreview = document.getElementById('remove_' + uid);
    var image_name=document.getElementById('a_'+uid);
    
    var savebutton = document.getElementById('save_'+uid)
    var input = document.getElementById('new_'+uid);


    const formData = new FormData();
    formData.append('new_image', new_image_file.files[0]);
    formData.append('uid', uid);



    fetch("/product/edit_image/", {

        method: 'post',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body : formData
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.image) {
            imagePreview.src = data.image;
            image_name.textContent=data.image_name;
            savebutton.remove();
            input.remove();
        }
        else{
            alert(data.error)
        }
    })
}



function del_image(uid) {
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
        var row = document.getElementById('button_'+uid)
        // Make an AJAX request to the backend to delete the item
        fetch('/product/delete_image/', {
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
            Swal.fire({
              title: "Deleted!",
              text: "Image deleted successfully.",
              icon: "success"
            });
            row.remove();
          } 
          else {
            Swal.fire({
              title: "Error!",
              text: "Failed to delete the image.",
              icon: "error"
            });
          }
        })
      }
    });
  }


