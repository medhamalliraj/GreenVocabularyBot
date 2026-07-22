document.addEventListener("DOMContentLoaded", function(){

    loadDashboard();

});


function loadDashboard(){


    fetch("/dashboard-data")

    .then(response => response.json())

    .then(data => {


        if(data.success){


            document.getElementById("welcome").innerHTML =
            "Welcome " + data.name + " 🌱";


            document.getElementById("chatCount").innerHTML =
            data.total_chats;


            document.getElementById("wordCount").innerHTML =
            data.total_words;



            let chatList = document.getElementById("chatList");


            chatList.innerHTML = "";



            data.chats.forEach(chat => {


                let div = document.createElement("div");


                div.className = "chat-item";


               


let responseText = chat.response;


try {

    let ai = JSON.parse(responseText);


    responseText = `

    🌿 <b>Nature Rewrite:</b><br>
    ${ai.rewrite || ""}

    <br><br>

    🌱 <b>Meaning:</b><br>
    ${ai.meaning || ""}

    <br><br>

    🌍 <b>Eco Fact:</b><br>
    ${ai.eco_fact || ""}

    <br><br>

    🍃 <b>Green Word:</b><br>
    ${ai.green_word || ""}

    <br><br>

    📖 <b>Word Meaning:</b><br>
    ${ai.word_meaning || ""}

    `;


}
catch(error){

    console.log(error);

}



div.innerHTML = `

<b>🌿 You:</b><br>
${chat.message}

<br><br>

<b>🤖 Green AI:</b><br>

${responseText}

`;


                chatList.appendChild(div);


            });



        }


    })

    .catch(error => {

        console.log(error);

    });


}



function openChat(){

    window.location.href="/";

}



function logout(){

    window.location.href="/logout";

}