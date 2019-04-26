// quiz constructor

function Quiz(questions) {
    this.score = 0;
    this.questions = questions;
    this.currentQuestionIndex = 0;
}

Quiz.prototype.guess = function(answer) {
    if(this.getCurrentQuestion().isCorrectAnswer(answer)) {
        this.downloadtemp++;
    }
    this.currentQuestionIndex++;
};


Quiz.prototype.getCurrentQuestion = function() {
    return this.questions[this.currentQuestionIndex];
};

Quiz.prototype.hasEnded = function() {
    return this.currentQuestionIndex >= this.questions.length;
};


// question

function Question(text, choices, answer) {
    this.text = text;
    this.choices = choices;
    this.answer = answer;
}

Question.prototype.isCorrectAnswer = function (choice) {
    return this.answer === choice;
};

// quiz ui

var QuizUI = {
    displayNext: function () {
        if (quiz.hasEnded()) {
            this.displayScore();
        } else {
            this.displayQuestion();
            this.displayChoices();
            this.displayProgress();
        }
    },
   displayQuestion: function() {
        this.populateIdWithHTML("question", quiz.getCurrentQuestion().text);
    },
   displayChoices: function() {
        var choices = quiz.getCurrentQuestion().choices;

        for(var i = 0; i < choices.length; i++) {
            this.populateIdWithHTML("choice" + i, choices[i]);
            this.guessHandler("guess" + i, choices[i]);
        }
    },

    displayScore: function() {
        var gameOverHTML = "<h1>Game Over</h1>";
        gameOverHTML += "<h2> Your score is: " + quiz.score + "</h2>";
        this.populateIdWithHTML("quiz", gameOverHTML);
		this.populateIdWithHTML("score", quizScore);
    },

    populateIdWithHTML: function(id, text) {
        var element = document.getElementById(id);
        element.innerHTML = text;
    },

    guessHandler: function(id, guess) {
        var button = document.getElementById(id);
        button.onclick = function() {
            quiz.guess(guess);
            QuizUI.displayNext();
        }
    },

  displayProgress: function() {
        var currentQuestionNumber = quiz.currentQuestionIndex + 1;
        this.populateIdWithHTML("progress", "Question " + currentQuestionNumber + " of " + quiz.questions.length);
    }
};




//Create Questions
var questions = [
    new Question("Which of the following is the correct syntax to print a page using JavaScript??", 
	[ "window.print();", "browser.print();", "navigator.print();", "document.print();"], "window.print();"),
    
	new Question("2Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),
	
	new Question("3Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),
	
	new Question("4Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),	
	new Question("5Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),
	
	
	new Question("6Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),
	
	
	new Question("7Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),
	
	
	new Question("8Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),
	
	
	new Question("9Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()"),
	
	
	new Question("10Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()")
	

];

//Create Quiz
var quiz = new Quiz(questions);

//Display Quiz
QuizUI.displayNext();
