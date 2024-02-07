function popup(categoryId){
    var sub_category=document.getElementById('delete');
    categoryId.href='{% url "adminpage:delete_category" 0 %}'.replace(0, categoryId);
}


function validate(){
    var sub_category=document.getElementById('sub_category').value.trim();
    var sub_categoryError=document.getElementById('sub_categoryError');

    sub_categoryError.innerHTML="";

    if (sub_category===""){
        sub_categoryError.innerHTML='Sub category is required';
        return false;
    }
    return true
}