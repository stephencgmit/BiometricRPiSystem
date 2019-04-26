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

    new Question("Which of the following is not a keyword in Java??", 
	[ "static", "Boolean", "void", "private"], "Boolean"),
    
	new Question("What is the size of long variable?", 
	["8 bit","16 bit", "64 bit", "32 bit"], "64 bit"),
	
	new Question("What is the default value of byte variable?", 
	["0","0.0", "null", "not defined"], "0"),
	
	new Question("What is polymorphism?", 
	["Polymorphism is a technique to define different objects of same type."
	,"Polymorphism is the ability of an object to take on many forms.", 
	"Polymorphism is a technique to define different methods of same type.", 
	"None of the above."], 
	"Polymorphism is the ability of an object to take on many forms."),
	new Question("What is an applet?", 
	["An applet is a Java program that runs in a Web browser.",
	"Applet is a standalone java program.", 
	"Applet is a tool.", 
	"Applet is a run time environment."], 
	"An applet is a Java program that runs in a Web browser."),
	
	
	new Question("Method Overriding is an example of??", 
	["Static Binding.","Dynamic Binding.", "Both of the above.", "None of the above."], "Dynamic Binding.")
	
	
	new Question("What is Deserialization???", 
	["Deserialization is the process of restoring state of an object from a byte stream.",
	"Serialization is the process of restoring state of an object from an object.", 
	"Both of the above", 
	"None of the above."], "Deserialization is the process of restoring state of an object from a byte stream."),
	
	
	new Question("Can a top level class be private or protected?", 
	["True","Sometimes", "Depends", "False"], "False"),
	
	
	new Question("What is a marker interface???", 
	["marker interface is an interface with single method, marker().",
	"marker interface is an interface with single method, mark().", 
	"marker interface is an interface with no method.", "None of the above."], 
	"marker interface is an interface with no method."),
	
	
	new Question("Which built-in method adds one or more elements to the end of an array and returns the new length of the array??", 
	["last()","put()", "push()", "None of the above."], "push()")



];

//Create Quiz
var quiz = new Quiz(questions);

//Display Quiz
QuizUI.displayNext();