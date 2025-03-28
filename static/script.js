function sendMail(){
    let parms = {
        name : document.getElementById("name").value, 
        email : document.getElementById("email").value, 
        message : document.getElementById("message").value,
    }

    emailjs.send("service_c4qznhp", "template_s5d0w0f", parms).then(alert("Email has been sent!!!"))
}