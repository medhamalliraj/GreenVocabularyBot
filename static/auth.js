// ======================================
// Green Vocabulary AI
// Authentication JavaScript
// ======================================



// ================================
// SIGNUP FUNCTION
// ================================

const signupForm = document.getElementById("signupForm");


if(signupForm){


    signupForm.addEventListener("submit", async function(event){

        event.preventDefault();


        let name =
        document.getElementById("name").value;


        let email =
        document.getElementById("email").value;


        let password =
        document.getElementById("password").value;


        let confirmPassword =
        document.getElementById("confirmPassword").value;



        let message =
        document.getElementById("message");



        if(password !== confirmPassword){

            message.innerHTML =
            "❌ Passwords do not match";

            return;

        }



        try{


            let response =
            await fetch("/signup",{


                method:"POST",


                headers:{
                    "Content-Type":"application/json"
                },


                body:JSON.stringify({

                    name:name,
                    email:email,
                    password:password

                })


            });



            let data =
            await response.json();



            if(data.success){


                message.style.color =
                "green";


                message.innerHTML =
                "✅ Account created successfully";


                setTimeout(()=>{


                    window.location.href="/login";


                },1500);



            }

            else{


                message.style.color =
                "red";


                message.innerHTML =
                "❌ "+data.message;


            }



        }


        catch(error){


            console.log(error);


            message.innerHTML =
            "❌ Server error";


        }



    });


}





// ================================
// LOGIN FUNCTION
// ================================


const loginForm =
document.getElementById("loginForm");



if(loginForm){


    loginForm.addEventListener("submit", async function(event){


        event.preventDefault();



        let email =
        document.getElementById("email").value;


        let password =
        document.getElementById("password").value;



        let message =
        document.getElementById("message");



        try{


            let response =
            await fetch("/login",{


                method:"POST",


                headers:{


                    "Content-Type":"application/json"


                },


                body:JSON.stringify({


                    email:email,

                    password:password


                })


            });



            let data =
            await response.json();




            if(data.success){


                message.style.color =
                "green";


                message.innerHTML =
                "✅ Login successful";



                setTimeout(()=>{


                    window.location.href="/dashboard";


                },1500);



            }


            else{


                message.style.color =
                "red";


                message.innerHTML =
                "❌ "+data.message;


            }



        }


        catch(error){


            console.log(error);


            message.innerHTML =
            "❌ Server error";


        }



    });



}