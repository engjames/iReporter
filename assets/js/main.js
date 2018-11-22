
// function to authenticate users and admin
function authenticateUsers(){
  var email = document.querySelector("#email").value;
  var password = document.querySelector("#field").value;
  if(email==='user@gmail.com' && password ==="user123"){
     window.location.href ="red_flag.html";
  }else if(email==='admin@gmail.com' && password ==="admin123"){
    var email = document.querySelector("#email").value;
    var password = document.querySelector("#field").value;
    window.location.href ="admin_manage_redflags.html";

  }
}
  