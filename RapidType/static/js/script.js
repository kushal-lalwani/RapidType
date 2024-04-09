let textType = 1;
let testTime = 15;
let testStarted = false;
let inputText;
let wpmData = [];

const promptTextElement = document.getElementById("prompt-text");
const typingInput = document.getElementById("typing-input");


function setTextType(type, e) {
    textType = type;
    document.querySelectorAll('.text-type').forEach(link => link.classList.remove('selected'));

    e.classList.add('selected');

    refreshTextPrompt(textType);
}

function setTestTime(time, e) {
    testTime = time;
    document.querySelectorAll('.test-time').forEach(link => link.classList.remove('selected'));

    e.classList.add('selected');
    document.getElementById('countdown').innerText = time;
}

let promptText;
async function getRandomTextPrompt(textType) {
    try {

        const url = `/get-random-text-prompt/?textType=${textType}`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Failed to fetch random text');
        }
        return await response.text();
    } catch (error) {
        console.error('Error fetching random text:', error);
        return '';
    }
}


async function refreshTextPrompt(textType) {
    promptText = await getRandomTextPrompt(textType);
    setup();
}

function setup() {

    promptTextElement.innerHTML = promptText.split('').map(char => `<span>${char}</span>`).join('');


    typingInput.addEventListener("input", function () {
        if (!testStarted) {
            startTest(); 
        }

        inputText = this.value;
        let promptChars = promptTextElement.querySelectorAll('span');

        promptChars.forEach((char, index) => {
            if (index < inputText.length) {
                char.classList.remove('incorrect-char');
                char.classList.add(inputText[index] === char.textContent ? 'correct-char' : 'incorrect-char');
            } else {
                char.classList.remove('correct-char', 'incorrect-char');
            }
        });

        createCursor(promptChars[inputText.length - 1]);
    });
};

refreshTextPrompt(textType);


function startTest() {
    let countdown = testTime;
    let charactersTypedThisInterval = 0; 
    if (!testStarted) {
        testStarted = true;

        const startTimer = setInterval(() => {
            countdown--;
            document.getElementById("countdown").innerHTML = countdown;
        
            if (countdown <= 0) {
                clearInterval(startTimer);
                const charactersTyped = inputText.trim().replace(/\s+/g, '').length;
                const timeIntervalInMinutes = (testTime - countdown) / 60; 
                const wpmLastInterval = Math.round((charactersTyped / 5) / timeIntervalInMinutes); 
                wpmData.push(wpmLastInterval); 
                
                showResult();
            }
            else if (inputText.length >= promptText.length) {
                clearInterval(startTimer);
                
                showResult(testTime - countdown);
            }
            else {
                let charactersTyped = inputText.trim().replace(/\s+/g, '').length;
                let charactersTypedThisSec = charactersTyped - charactersTypedThisInterval;

                if (countdown % 3 === 0) {
                    const timeIntervalInMinutes = 3 / 60; 
                    const wpmThisInterval = Math.round((charactersTypedThisSec / 5) / timeIntervalInMinutes);
                    wpmData.push(wpmThisInterval);
                    charactersTypedThisInterval = charactersTyped;
                }
            }
        }, 1000);
    }
}




function showResult(time = 0) {

    sendWPMDataToDjango(wpmData)
    const promptText = promptTextElement.textContent;
    const resultdiv = document.getElementById('result');
    resultdiv.classList.remove('hide');
    const navbar = document.querySelector('#sec-nav');
    navbar.remove();

    const span = document.querySelector('#countdown');
    span.remove();
    document.querySelector('.retest').remove();
    document.querySelector('.timer').remove();

    const textContainer = document.querySelector('.text-container');
    textContainer.remove();



    if (time != 0) {
        let charactersTyped = inputText.trim().replace(/\s+/g, '').length;
        let fullTextWpm = Math.round((charactersTyped / 5) / (time/60));
        let fullTextAccuracy = calculateAccuracy(inputText,promptText);
        saveTestResult(fullTextWpm, fullTextAccuracy);
        document.getElementById('wpmValue').innerText = fullTextWpm;
        document.getElementById('accuracyValue').innerText = fullTextAccuracy + '%';

    }
    else {

        const wpm = calculateWPM(inputText);
        const accuracy = calculateAccuracy(inputText, promptText);
        
        saveTestResult(wpm, accuracy);
        
        document.getElementById('wpmValue').innerText = wpm;
        document.getElementById('accuracyValue').innerText = accuracy + '%';
    }
}

function saveTestResult(wpm, accuracy) {
    let textTypeWord;
    if (textType === 1) {
        textTypeWord = 'Normal'
    }
    else if (textType == 2) {
        textTypeWord = 'Punctuation'
    }
    else if(textType == 3) {
        textTypeWord = 'Top Row'
    }
    else if(textType == 4) {
        textTypeWord = 'Home Row'
    }
    else{
        textTypeWord = 'Bottom Row'
    }
    const data = {
        wpm: wpm,
        accuracy: accuracy,
        testTime: testTime,
        textType: textTypeWord
    };

    const csrftoken = getCSRFToken()
    fetch('/save-test-result/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                console.log('Test result saved');
            } else {
                console.error('Failed to save test result');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function sendWPMDataToDjango(wpmData) {

    const csrftoken = getCSRFToken();

    fetch('/generate-graph/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ wpm_data: wpmData })
    })
    .then(response => {
        if (!response.ok) {
     
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.blob();
    })
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        let img = document.getElementById('graph-img');
        img.src = imageUrl;
    })
    .catch(error => {
  
        console.error('Error:', error);
    });
}


function getCSRFToken() {
    const csrfCookie = document.cookie.split(';')
        .find(cookie => cookie.trim().startsWith('csrftoken='));
    if (csrfCookie) {
        return csrfCookie.split('=')[1];
    }
    return '';
}






function calculateWPM(inputText) {
    const charactersTyped = inputText.trim().replace(/\s+/g, '').length;

    const wpm = Math.round((charactersTyped / 5) / (testTime / 60));
    return wpm;
}

function calculateAccuracy(inputText, promptText) {
    let correctChars = 0;
    for (let i = 0; i < inputText.length; i++) {
        if (inputText[i] === promptText[i]) {
            correctChars++;
        }
    }

    const accuracy = Math.round((correctChars / inputText.length) * 100);

    return accuracy;
}
let img = document.getElementById('graph-img');
let spinner = document.getElementById('spinner');
let loadingMessage = document.getElementById('loading-message');

img.onload = function() {
    spinner.style.display = 'none'; 
    loadingMessage.style.display = 'none'; 
    img.classList.remove('d-none'); 
};

function createCursor(cursorPosition) {
    
    let existingCursor = document.querySelector('.cursor');
    if (existingCursor) {
        existingCursor.remove();
    }

    let cursor = document.createElement('span');
    cursor.classList.add('cursor');
    cursor.textContent = '|'; 

    if (cursorPosition) {
        cursor.style.left = cursorPosition.offsetLeft + cursorPosition.offsetWidth + 'px';
        cursor.style.top = cursorPosition.offsetTop + 'px';
    } else {

        cursor.style.left = '0';
        cursor.style.top = '0';
    }

    promptTextElement.appendChild(cursor);
}