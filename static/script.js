document.addEventListener("DOMContentLoaded", function(){


    const sendBtn = document.getElementById("send-btn");
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");


    // ==========================
    // Send Message
    // ==========================


    sendBtn.addEventListener("click", sendMessage);



    input.addEventListener("keypress", function(e){

        if(e.key === "Enter"){

            sendMessage();

        }

    });





    // ==========================
    // Send Chat
    // ==========================


    function sendMessage(){


        let message = input.value.trim();


        if(message === "") return;



        addMessage(
            message,
            "user"
        );


        input.value="";



        showTyping();



        fetch("/chat",{


            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },


            body:JSON.stringify({

                message:message

            })


        })

        .then(response=>response.json())


        .then(data=>{


            hideTyping();


            addBotResponse(data);



        })


        .catch(error=>{


            hideTyping();


            addMessage(

                "⚠️ Something went wrong",

                "bot"

            );


        });



    }







    // ==========================
    // Add User Message
    // ==========================


    function addMessage(message,type){


        let div=document.createElement("div");


        div.className =
        type==="user"
        ?
        "message user-message"
        :
        "message bot-message";



        div.innerHTML = `


        <div class="avatar">

            ${type==="user"?"👤":"🌿"}

        </div>


        <div class="bubble">

            ${message}

        </div>


        `;



        chatBox.appendChild(div);


        chatBox.scrollTop =
        chatBox.scrollHeight;



    }







    // ==========================
    // Gemini Response Format
    // ==========================


    function addBotResponse(data){


        let div=document.createElement("div");


        div.className="message bot-message";



        div.innerHTML = `



        <div class="avatar bot-avatar">

            🌿

        </div>



        <div class="bubble">



        <h3>
        🌿 Rewrite
        </h3>

        <p>
        ${data.rewrite || ""}
        </p>



        <h3>
        📖 Meaning
        </h3>

        <p>
        ${data.meaning || ""}
        </p>



        <h3>
        😊 Emotion
        </h3>

        <p>
        ${data.emotion || ""}
        </p>



        <h3>
        💚 Sentiment
        </h3>

        <p>
        ${data.sentiment || ""}
        </p>




        <h3>
        🌱 Green Word
        </h3>

        <p>
        ${data.green_word || ""}
        </p>



        <h3>
        📘 Word Meaning
        </h3>

        <p>
        ${data.word_meaning || ""}
        </p>



        <h3>
        🌍 Eco Fact
        </h3>

        <p>
        ${data.eco_fact || ""}
        </p>




        <h3>
        ♻ Eco Tip
        </h3>

        <p>
        ${data.eco_tip || ""}
        </p>




        <h3>
        🌳 Sustainable Habit
        </h3>

        <p>
        ${data.sustainable_habit || ""}
        </p>




        <h3>
        🎯 Eco Challenge
        </h3>

        <p>
        ${data.challenge || ""}
        </p>



        </div>



        `;



        chatBox.appendChild(div);



        chatBox.scrollTop =
        chatBox.scrollHeight;



    }








    // ==========================
    // Typing Animation
    // ==========================


    function showTyping(){

        document
        .getElementById("typing")
        .classList.remove("hidden");

    }



    function hideTyping(){

        document
        .getElementById("typing")
        .classList.add("hidden");

    }







    // ==========================
    // Theme Toggle
    // ==========================


    document
    .getElementById("themeToggle")
    ?.addEventListener("click",()=>{


        document.body.classList.toggle("dark");


    });







    // ==========================
    // Navigation Buttons
    // ==========================


    document
    .getElementById("dashboardBtn")
    ?.addEventListener("click",()=>{

        window.location.href="/dashboard";

    });



    document
    .getElementById("chatHistoryBtn")
    ?.addEventListener("click",()=>{

        window.location.href="/chat-history-page";

    });



    document
    .getElementById("logoutBtn")
    ?.addEventListener("click",()=>{

        window.location.href="/logout";

    });






    // ==========================
    // Vocabulary History
    // ==========================


    document
    .getElementById("historyBtn")
    ?.addEventListener("click",()=>{


        document
        .getElementById("historyModal")
        .style.display="block";


        loadVocabulary();


    });



    document
    .getElementById("closeHistory")
    ?.addEventListener("click",()=>{


        document
        .getElementById("historyModal")
        .style.display="none";


    });







    function loadVocabulary(){


        fetch("/history")

        .then(res=>res.json())

        .then(data=>{


            let list =
            document.getElementById("historyList");


            list.innerHTML="";



            data.forEach(word=>{


                list.innerHTML += `


                <div class="history-item">

                <h3>
                🌱 ${word.word}
                </h3>

                <p>
                ${word.meaning}
                </p>

                </div>


                `;


            });



        });



    }



});