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




function category(){
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var sortbyprice=document.getElementById('sortbyprice').value;
    
    // Filter checked checkboxes
    const checkedCategories = Array.from(checkboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);

    fetch('/products/shop_page/',{
        method: 'post', // Assuming your backend handles DELETE requests for deletion
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'categories': checkedCategories, 'sortbyprice': sortbyprice }),
    })
    .then(response => response.json())
    .then(data=>{
        const productsContainer = document.querySelector('.row.product');
productsContainer.innerHTML = ''; // Clear existing products

data.products.forEach(product => {
    var collapse=document.getElementById('collapseOne');
    setTimeout(function() {
        collapse.classList.remove('show');
    }, 50);

    const div=document.createElement('div');
    div.style.width = '20%';

    const productItem = document.createElement('div');
    productItem.classList.add('product__item');

    const productPic = document.createElement('div');
    productPic.classList.add('product__item__pic', 'set-bg');
    productPic.style.backgroundImage = `url(${product.product.image})`;

    const productHover = document.createElement('ul');
    productHover.classList.add('product__hover');

    const productHoverItem = document.createElement('li');
    const heartIcon = document.createElement('i');
    heartIcon.className = 'fas fa-heart';
    heartIcon.style.color = '#fff';
    productHoverItem.appendChild(heartIcon);

    productHover.appendChild(productHoverItem);
    productPic.appendChild(productHover);

    const productText = document.createElement('div');
    productText.classList.add('product__item__text');

    const h6 = document.createElement('h6');
    h6.innerHTML = product.product.name;

    const addToCartLink = document.createElement('a');
    addToCartLink.href = '#';
    addToCartLink.className = 'add-cart';
    addToCartLink.innerHTML = '+ Add To Cart';

    const rating = document.createElement('div');
    rating.className = 'rating';

    const h5 = document.createElement('h5');
    h5.innerHTML = `₹${product.product.price}`;

    productText.appendChild(h6);
    productText.appendChild(addToCartLink)
    for (let i = 0; i < 5; i++) {
        const star = document.createElement('i');
        star.className = 'fa fa-star-o';
        star.style.marginRight='.5px';
        rating.appendChild(star);
    }
    productText.appendChild(rating);
    productText.appendChild(h5);

    productItem.appendChild(productPic);
    productItem.appendChild(productText);

    div.appendChild(productItem)

    productsContainer.appendChild(div);


});
    })
}



