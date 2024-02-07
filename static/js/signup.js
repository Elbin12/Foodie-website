function validateForm() {
    console.log('working');
    var firstName = document.getElementById('first-name').value.trim();
    var lastName = document.getElementById('last-name').value.trim();
    var gender = document.querySelector('input[name="gender"]:checked');
    var email = document.getElementById('email').value.trim();
    var mobile = document.getElementById('mobile').value.trim();
    var password = document.getElementById('password').value.trim();
    var confirmPassword = document.getElementById('confirm-password').value.trim();

    var firstNameError = document.getElementById('first-nameError');
    var lastNameError = document.getElementById('last-nameError');
    var genderError = document.getElementById('genderError');
    var emailError = document.getElementById('emailError');
    var mobileError = document.getElementById('mobileError');
    var passwordError = document.getElementById('passwordError');
    var confirmPasswordError = document.getElementById('confirm_passwordError');

    // Reset error messages
    firstNameError.innerHTML = '';
    lastNameError.innerHTML = '';
    genderError.innerHTML = '';
    emailError.innerHTML = '';
    mobileError.innerHTML = '';
    passwordError.innerHTML = '';
    confirmPasswordError.innerHTML = '';

    // Your validation logic here...
    if (firstName === '') {
        firstNameError.innerHTML = 'First Name is required';
        return false;
    }

    if (firstName===lastName){
        lastNameError.innerHTML=  'First and Last names will not same'
        return false;
    }

    if (!gender) {
        genderError.innerHTML = 'Gender is required';
        return false;
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email === '') {
        emailError.innerHTML = 'Email is required';
        return false;
    } else if (!emailRegex.test(email)) {
        emailError.innerHTML = 'Enter a valid email address';
        return false;
    }

    if (mobile === '') {
        mobileError.innerHTML = 'Mobile is required';
        return false;
    }

    if (password === '') {
        passwordError.innerHTML = 'Password is required';
        return false;
    }

    if (confirmPassword === '') {
        confirmPasswordError.innerHTML = 'Confirm Password is required';
        return false;
    }

    if (password !== confirmPassword) {
        confirmPasswordError.innerHTML = 'Passwords do not match';
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


function updateSelectedGender(selectedGender) {
    document.getElementById('selectedGender').value = selectedGender;
  }



  function validate_password(e) {
    var password = document.getElementById('password').value;

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

    var email = document.getElementById('email').value;
    var emailError = document.getElementById('emailError');

    if (email===""){
        emailError.innerHTML = 'email is required';
    }
}



const emailInput = document.getElementById('email');
emailInput.addEventListener("input", validate_email);