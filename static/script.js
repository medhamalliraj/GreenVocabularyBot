// ==========================================
// Green Vocabulary AI
// Version 2
// ==========================================

// DOM Elements

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const typing = document.getElementById("typing");

const themeBtn = document.getElementById("themeToggle");

const historyBtn = document.getElementById("historyBtn");

const dashboardBtn = document.getElementById("dashboardBtn");

const logoutBtn = document.getElementById("logoutBtn");

const chatHistoryBtn = document.getElementById("chatHistoryBtn");

const historyModal = document.getElementById("historyModal");

const closeHistory = document.getElementById("closeHistory");

const historyList = document.getElementById("historyList");

const historySearch = document.getElementById("historySearch");

// ==========================================
// Welcome Message
// ==========================================

window.onload = () => {

    loadTheme();

    addBotMessage(
`👋 Hello!

I'm your Green Vocabulary AI.

🌿 I can teach eco-friendly vocabulary.

♻ I can rewrite your sentences.

🌎 I can share eco facts.

💚 I can suggest sustainable habits.

Ask me anything!`
    );

};

// ==========================================
// Send Button
// ==========================================

sendBtn.addEventListener("click", sendMessage);

// Press Enter

userInput.addEventListener("keypress", function(e){

    if(e.key==="Enter"){

        sendMessage();

    }

});

// ==========================================
// Send Message
// ==========================================

async function sendMessage(){

    const message = userInput.value.trim();

    if(message==="") return;

    addUserMessage(message);

    userInput.value="";

    typing.classList.remove("hidden");

    try{

        const response = await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                message:message

            })

        });

        const data = await response.json();

        typing.classList.add("hidden");

        showAIResponse(data);

    }

    catch(error){

        typing.classList.add("hidden");

        addBotMessage("❌ Unable to connect to the server.");

        console.error(error);

    }

}

// ==========================================
// User Bubble
// ==========================================

function addUserMessage(text){

    chatBox.innerHTML += `

    <div class="message user-message">

        <div class="bubble">

            ${text}

        </div>

        <div class="avatar user-avatar">

            👤

        </div>

    </div>

    `;

    scrollBottom();

}

// ==========================================
// Bot Bubble
// ==========================================

function addBotMessage(text){

    chatBox.innerHTML += `

    <div class="message bot-message">

        <div class="avatar bot-avatar">

            🌿

        </div>

        <div class="bubble">

            ${text.replace(/\n/g,"<br>")}

        </div>

    </div>

    `;

    scrollBottom();

}

// ==========================================
// Scroll
// ==========================================

function scrollBottom(){

    chatBox.scrollTop = chatBox.scrollHeight;

}
// ==========================================
// Beautiful AI Response
// ==========================================

function showAIResponse(data){

    let html = "";

    if(data.rewrite){

        html += `
        <p><strong>🌿 Rewrite</strong><br>${data.rewrite}</p><br>
        `;
    }

    if(data.meaning){

        html += `
        <p><strong>📖 Meaning</strong><br>${data.meaning}</p><br>
        `;
    }

    if(data.emotion){

        html += `
        <p><strong>😊 Emotion</strong><br>${data.emotion}</p><br>
        `;
    }

    if(data.sentiment){

        html += `
        <p><strong>💚 Sentiment</strong><br>${data.sentiment}</p><br>
        `;
    }

    if(data.green_word){

        html += `
        <p><strong>🌱 Green Word</strong><br>${data.green_word}</p><br>
        `;
    }

    if(data.word_meaning){

        html += `
        <p><strong>📘 Word Meaning</strong><br>${data.word_meaning}</p><br>
        `;
    }

    if(data.eco_fact){

        html += `
        <p><strong>🌍 Eco Fact</strong><br>${data.eco_fact}</p><br>
        `;
    }

    if(data.eco_tip){

        html += `
        <p><strong>♻ Eco Tip</strong><br>${data.eco_tip}</p><br>
        `;
    }

    if(data.sustainable_habit){

        html += `
        <p><strong>🌳 Sustainable Habit</strong><br>${data.sustainable_habit}</p><br>
        `;
    }

    if(data.challenge){

        html += `
        <p><strong>🎯 Eco Challenge</strong><br>${data.challenge}</p>
        `;
    }

    if(html===""){

        html="<p>No response received.</p>";

    }

    chatBox.innerHTML += `

    <div class="message bot-message">

        <div class="avatar bot-avatar">

            🌿

        </div>

        <div class="bubble">

            ${html}

        </div>

    </div>

    `;

    scrollBottom();

}

// ==========================================
// Dashboard
// ==========================================

dashboardBtn.addEventListener("click",()=>{

    window.location.href="/dashboard";

});

// ==========================================
// Logout
// ==========================================

logoutBtn.addEventListener("click",()=>{

    window.location.href="/logout";

});

// ==========================================
// Chat History
// ==========================================

chatHistoryBtn.addEventListener("click",()=>{

    window.location.href="/chat-history-page";

});

// ==========================================
// Theme
// ==========================================

themeBtn.addEventListener("click",()=>{

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")){

        localStorage.setItem("theme","dark");

        themeBtn.innerHTML="☀";

    }

    else{

        localStorage.setItem("theme","light");

        themeBtn.innerHTML="🌙";

    }

});

function loadTheme(){

    const theme=localStorage.getItem("theme");

    if(theme==="dark"){

        document.body.classList.add("dark-mode");

        themeBtn.innerHTML="☀";

    }

}
// ==========================================
// HISTORY MODAL
// ==========================================

// Open History

historyBtn.addEventListener("click", () => {

    historyModal.classList.add("show");

    loadHistory();

});

// Close History

closeHistory.addEventListener("click", () => {

    historyModal.classList.remove("show");

});

// Click Outside

window.addEventListener("click", (e) => {

    if(e.target === historyModal){

        historyModal.classList.remove("show");

    }

});

// ESC Key

document.addEventListener("keydown",(e)=>{

    if(e.key==="Escape"){

        historyModal.classList.remove("show");

    }

});

// ==========================================
// LOAD VOCABULARY HISTORY
// ==========================================

async function loadHistory(){

    historyList.innerHTML = "Loading...";

    try{

        const response = await fetch("/history");

        const data = await response.json();

        if(data.length===0){

            historyList.innerHTML=`
                <div class="history-empty">
                    🌱 No vocabulary learned yet.
                </div>
            `;

            return;

        }

        let html="";

        data.forEach((item,index)=>{

            html+=`

            <div class="history-card">

                <h3>

                    🌿 ${item.word}

                </h3>

                <p>

                    ${item.meaning}

                </p>

            </div>

            `;

        });

        historyList.innerHTML=html;

    }

    catch(error){

        historyList.innerHTML=`
            <div class="history-empty">
                Unable to load history.
            </div>
        `;

        console.error(error);

    }

}

// ==========================================
// SEARCH HISTORY
// ==========================================

historySearch.addEventListener("keyup",function(){

    const value=this.value.toLowerCase();

    const cards=document.querySelectorAll(".history-card");

    cards.forEach(card=>{

        const text=card.innerText.toLowerCase();

        if(text.includes(value)){

            card.style.display="block";

        }

        else{

            card.style.display="none";

        }

    });

});
// ==========================================
// FINAL UTILITIES
// ==========================================

// Clear Search When Modal Closes

function resetHistorySearch(){

    if(historySearch){

        historySearch.value="";

    }

    const cards=document.querySelectorAll(".history-card");

    cards.forEach(card=>{

        card.style.display="block";

    });

}

// Close Button

closeHistory.addEventListener("click",()=>{

    resetHistorySearch();

});

// Outside Click

window.addEventListener("click",(e)=>{

    if(e.target===historyModal){

        resetHistorySearch();

    }

});

// ==========================================
// AUTO SCROLL
// ==========================================

function smoothScroll(){

    chatBox.scrollTo({

        top:chatBox.scrollHeight,

        behavior:"smooth"

    });

}

// Override scrollBottom()

scrollBottom = smoothScroll;

// ==========================================
// INPUT FOCUS
// ==========================================

window.addEventListener("load",()=>{

    if(userInput){

        userInput.focus();

    }

});

// ==========================================
// DISABLE SEND BUTTON WHILE REQUEST RUNS
// ==========================================

const originalSendMessage = sendMessage;

sendMessage = async function(){

    if(sendBtn.disabled) return;

    sendBtn.disabled = true;

    sendBtn.style.opacity = "0.6";

    sendBtn.style.cursor = "not-allowed";

    try{

        await originalSendMessage();

    }

    finally{

        sendBtn.disabled = false;

        sendBtn.style.opacity = "1";

        sendBtn.style.cursor = "pointer";

        userInput.focus();

    }

};

// ==========================================
// EMPTY HISTORY MESSAGE
// ==========================================

function showEmptyHistory(message){

    historyList.innerHTML = `

    <div class="history-empty">

        ${message}

    </div>

    `;

}

// ==========================================
// CONSOLE MESSAGE
// ==========================================

console.log("🌿 Green Vocabulary AI Loaded Successfully!");

console.log("Version 2 UI Ready");

// ==========================================
// END OF FILE
// ==========================================