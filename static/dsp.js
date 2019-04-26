

function Quiz(questions) {
    this.score = 0;
    this.questions = questions;
    this.currentQuestionIndex = 0;
}

Quiz.prototype.guess = function(answer) {
    if(this.getCurrentQuestion().isCorrectAnswer(answer)) {
        this.score++;
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
        var gameOverHTML = "<h1>Quiz Over</h1>";
        var quizScore = quiz.score;
        gameOverHTML += "<h2> Your score is: " + quiz.score + "</h2>";
        this.populateIdWithHTML("quiz", gameOverHTML);
        this.populateIdWithHTML("score", quizScore);
        this.populateIdWithHTML("score1", quiz.score);
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
    new Question("In what era did Jean-Baptiste Joseph Fourier publish his work?", 
	[ "1620s",
        "1920s",
        "1720s", 
		"1820s"], 
		"1820s"),
		
    new Question("Approximately what percentage of the human body's sensory receptors are in the eyes?", 
	["80%",
	"70%%",
    "50%",
	"60%"], 
	"70%"),

        new Question("What language is OpenCV written in??", 
		["Python",
		"C++",
    "Java",
	"Ruby"], 
	"Python"),

        new Question("What technique converts an infinite-length signal to a finite-length signal?", 
		["Windowing",
		"Decimation",
		"Sampling",
		"Sampling"], "Windowing"),

        new Question("An FIR is a ________ Impulse Response Filter", [
		"Frequency",
		"Fast",
    "Finite",
	"Filtered"], "Finite"),

        new Question("A _______ is a function that maps an independent variable to a dependent variable", 
		["signal",
		"variable",
    "dot product.",
	"filter."], "signal"),

        new Question("What is numpy?", ["a package for scientific computing in Python",
		"a package for image processing in python",
    "a package for plotting in python",
	"a package for handling csv files in python"], 
	"a package for scientific computing in Python"),

        new Question("Numpys main object is?", 
		["a tuple",
		"a multidimensional array",
    "a pointer",
	"python list"], 
	"a multidimensional array"),

        new Question("The amplitude of a light wave relates to its", 
		["brightness",
		"pitch",
    "reflection",
	"hue"], "brightness"),

        new Question("Euler's equation, gives the fundamental relationship between __________ and __________", 
		["the logarithmic functions and the trigonometric functions",
		"the complex exponential function and the trigonometric functions",
    "the real exponential function and the trigonometric functions",
	"logarithms and sinusoids"], 
	"the complex exponential function and the trigonometric functions")
];

//Create Quiz
var quiz = new Quiz(questions);

//Display Quiz
QuizUI.displayNext();
