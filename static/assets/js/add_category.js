function popup(categoryId){
    var category=document.getElementById('delete');
    categoryId.href='{% url "adminpage:delete_category" 0 %}'.replace(0, categoryId);
}


function validate(){
    var category=document.getElementById('category').value.trim();
    var categoryError=document.getElementById('categoryError');

    categoryError.innerHTML="";

    if (category===""){
        categoryError.innerHTML='Category is required';
        return false;
    }
    return true
}