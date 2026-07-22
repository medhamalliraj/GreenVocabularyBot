document.addEventListener("DOMContentLoaded", function(){


    loadChats();


    document
    .getElementById("search")
    .addEventListener("input", function(){


        loadChats(this.value);


    });


});





function loadChats(searchText=""){


    fetch("/chat-history")


    .then(response => response.json())


    .then(data => {


        const chatList =
        document.getElementById("chatList");


        chatList.innerHTML="";



        if(!data.success){

            chatList.innerHTML =
            "<p>User not logged in</p>";

            return;

        }



        let chats = data.chats;



        if(searchText.trim() !== ""){


            chats = chats.filter(chat =>


                chat.message
                .toLowerCase()
                .includes(
                    searchText.toLowerCase()
                )


            );


        }




        if(chats.length === 0){


            chatList.innerHTML =
            "<p>No conversations found 🌱</p>";

            return;


        }




        chats.forEach(chat => {



            let response = chat.response;



            try{

                response =
                JSON.parse(response);


            }

            catch(error){

                response =
                chat.response;

            }




            chatList.innerHTML += `


            <div class="chat-card">


                <h3>
                🌿 You:
                </h3>


                <p>
                ${chat.message}
                </p>



                <h3>
                🤖 Green AI:
                </h3>


                <p>
                ${
                    response.rewrite ||
                    response
                }
                </p>



                <p class="time">

                ${chat.time}

                </p>



                
                <button
class="continue-btn"
onclick="continueChat(${chat.id})">

Continue Chat

</button>


<button
class="delete-btn"
onclick="deleteChat(${chat.id})">

Delete

</button>


            </div>


            `;



        });


    });



}





function deleteChat(id){


    fetch(`/delete-chat/${id}`, {

        method:"DELETE"

    })


    .then(response => response.json())


    .then(data => {


        if(data.success){


            loadChats();


        }


    });


}
function continueChat(id){


    window.location.href =
    `/continue-chat/${id}`;


}