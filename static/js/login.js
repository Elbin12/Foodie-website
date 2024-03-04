


function validate_password(e) {
    var password = document.getElementById('password').value.trim();

    var passwordError = document.getElementById('passwordError');
    passwordError.innerHTML = '';

    if (password===""){
        passwordError.innerHTML = 'password is required';
    }
    var upperCaseLetters = /[A-Z]/g;
    if (!password.match(upperCaseLetters)){
        passwordError.innerHTML="must contain at least one uppercase letter.";
    }
    var lowerCaseLetters = /[a-z]/g;
    if (!password.match(lowerCaseLetters)){
        passwordError.innerHTML+="<br>    must contain at least one lowercase letter.";
    }
    var num = /[0-9]/g;
    if (!password.match(num)){
        passwordError.innerHTML+="<br> Password must contain numbers.";
    }
    if (password.length<8){
        passwordError.innerHTML+="<br> Password must contain 8 characters.";
    }

}

const passwordInput = document.getElementById('password');
passwordInput.addEventListener("input", validate_password);


function validate_email(e){

    var email = document.getElementById('email').value.trim();
    var emailError = document.getElementById('emailError');

    if (email===""){
        emailError.innerHTML = 'email is required';
    }
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!email.match(emailRegex)){
        emailError.innerHTML = 'enter a valid email';
    }
}



const emailInput = document.getElementById('email');
emailInput.addEventListener("input", validate_email);



function validateForm(){
    var email = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value.trim();

    var emailError = document.getElementById('emailError');
    var passwordError = document.getElementById('passwordError');

    emailError.innerHTML = '';
    passwordError.innerHTML = '';

    if (email===""){
        emailError.innerHTML = 'email is required';
        return false;
    }
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!email.match(emailRegex)){
        emailError.innerHTML = 'enter a valid email';
        return false;
    }

    if (password===""){
        passwordError.innerHTML = 'password is required';
        return false;
    }
    var upperCaseLetters = /[A-Z]/g;
    if (!password.match(upperCaseLetters)){
        passwordError.innerHTML="Password must contain at least one uppercase letter.";
        return false;
    }
    var lowerCaseLetters = /[a-z]/g;
    if (!password.match(lowerCaseLetters)){
        passwordError.innerHTML="must contain at least one lowercase letter.";
        return false;
    }
    var num = /[0-9]/g;
    if (!password.match(num)){
        passwordError.innerHTML+="<br> Password must contain numbers.";
        return false;
    }
    if (password.length<8){
        passwordError.innerHTML+="<br> Password must contain 8 characters.";
        return false;
    }

    return true;
}