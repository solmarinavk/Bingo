/**
 * TOEFL Master - Main JavaScript
 * Interactive functionality for the TOEFL study platform
 */

// ========================================
// Mobile Navigation
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.navbar') && navLinks?.classList.contains('active')) {
            navLinks.classList.remove('active');
            mobileMenuBtn?.classList.remove('active');
        }
    });

    // Initialize tabs
    initTabs();

    // Initialize word counters
    initWordCounters();
});

// ========================================
// Tab Functionality
// ========================================
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            const tabContainer = this.closest('section') || this.closest('.container');

            // Remove active class from all tabs in this container
            tabContainer.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Remove active class from all tab contents in this container
            tabContainer.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });

            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(tabId);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// ========================================
// Reading/Listening Exercise Functions
// ========================================
function checkReadingAnswers(exerciseId) {
    const container = document.getElementById(exerciseId);
    if (!container) return;

    const questionBlocks = container.querySelectorAll('.question-block');
    let correct = 0;
    let total = questionBlocks.length;

    questionBlocks.forEach(block => {
        const options = block.querySelectorAll('.option');
        let answered = false;

        options.forEach(option => {
            const input = option.querySelector('input');
            const isCorrect = option.getAttribute('data-correct') === 'true';

            if (input && input.checked) {
                answered = true;
                if (isCorrect) {
                    option.classList.add('correct');
                    correct++;
                } else {
                    option.classList.add('incorrect');
                    // Show correct answer
                    options.forEach(opt => {
                        if (opt.getAttribute('data-correct') === 'true') {
                            opt.classList.add('correct');
                        }
                    });
                }
            }
        });

        // If not answered, show correct answer
        if (!answered) {
            options.forEach(opt => {
                if (opt.getAttribute('data-correct') === 'true') {
                    opt.classList.add('correct');
                }
            });
        }
    });

    // Show results
    const resultsContainer = document.getElementById(`results-${exerciseId}`);
    const scoreDisplay = document.getElementById(`score-${exerciseId}`);

    if (resultsContainer && scoreDisplay) {
        scoreDisplay.textContent = `${correct}/${total}`;
        resultsContainer.classList.remove('hidden');
    }

    // Disable all options
    container.querySelectorAll('.option input').forEach(input => {
        input.disabled = true;
    });
}

function resetExercise(exerciseId) {
    const container = document.getElementById(exerciseId);
    if (!container) return;

    // Reset all options
    container.querySelectorAll('.option').forEach(option => {
        option.classList.remove('selected', 'correct', 'incorrect');
        const input = option.querySelector('input');
        if (input) {
            input.checked = false;
            input.disabled = false;
        }
    });

    // Hide results
    const resultsContainer = document.getElementById(`results-${exerciseId}`);
    if (resultsContainer) {
        resultsContainer.classList.add('hidden');
    }
}

// Option selection handling
document.addEventListener('click', function(e) {
    const option = e.target.closest('.option');
    if (option && !option.querySelector('input')?.disabled) {
        const input = option.querySelector('input');
        if (input) {
            input.checked = true;

            // Update visual selection
            const questionBlock = option.closest('.question-block');
            if (questionBlock) {
                questionBlock.querySelectorAll('.option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                option.classList.add('selected');
            }
        }
    }
});

// ========================================
// Vocabulary Functions
// ========================================
function checkVocabAnswers() {
    const questionBlocks = document.querySelectorAll('.exercise-container .question-block');
    let correct = 0;

    questionBlocks.forEach(block => {
        const options = block.querySelectorAll('.option');

        options.forEach(option => {
            const input = option.querySelector('input');
            const isCorrect = option.getAttribute('data-correct') === 'true';

            if (input && input.checked) {
                if (isCorrect) {
                    option.classList.add('correct');
                    correct++;
                } else {
                    option.classList.add('incorrect');
                }
            }

            if (isCorrect) {
                option.classList.add('correct');
            }

            if (input) input.disabled = true;
        });
    });

    alert(`Score: ${correct}/${questionBlocks.length} correct!`);
}

function resetVocabExercise() {
    const questionBlocks = document.querySelectorAll('.exercise-container .question-block');

    questionBlocks.forEach(block => {
        const options = block.querySelectorAll('.option');

        options.forEach(option => {
            option.classList.remove('selected', 'correct', 'incorrect');
            const input = option.querySelector('input');
            if (input) {
                input.checked = false;
                input.disabled = false;
            }
        });
    });
}

// ========================================
// Flashcard System
// ========================================
const vocabularyData = {
    academic: [
        { word: 'analyze', type: '(verb)', definition: 'To examine something in detail in order to understand it better or discover more about it.', example: '"Scientists analyze data to find patterns."' },
        { word: 'approach', type: '(noun/verb)', definition: 'A way of dealing with something; to come near or nearer to something.', example: '"The researchers took a different approach to the problem."' },
        { word: 'assess', type: '(verb)', definition: 'To evaluate or estimate the nature, ability, or quality of something.', example: '"Teachers assess student performance regularly."' },
        { word: 'assume', type: '(verb)', definition: 'To suppose something is true without proof; to take on a responsibility.', example: '"We cannot assume that the results will be the same."' },
        { word: 'benefit', type: '(noun/verb)', definition: 'An advantage or profit gained from something.', example: '"Exercise has many health benefits."' },
        { word: 'concept', type: '(noun)', definition: 'An abstract idea or general notion.', example: '"The concept of democracy varies across cultures."' },
        { word: 'consist', type: '(verb)', definition: 'To be composed or made up of.', example: '"The committee consists of twelve members."' },
        { word: 'context', type: '(noun)', definition: 'The circumstances that form the setting for an event or idea.', example: '"You need to understand the historical context."' },
        { word: 'derive', type: '(verb)', definition: 'To obtain something from a specified source.', example: '"Many English words derive from Latin."' },
        { word: 'establish', type: '(verb)', definition: 'To set up on a permanent basis; to prove or show to be true.', example: '"The company was established in 1990."' },
        { word: 'evident', type: '(adjective)', definition: 'Plain or obvious; clearly seen or understood.', example: '"It was evident that she had prepared well."' },
        { word: 'factor', type: '(noun)', definition: 'A circumstance or element contributing to a result.', example: '"Cost is an important factor in this decision."' },
        { word: 'identify', type: '(verb)', definition: 'To recognize or establish what something is.', example: '"Scientists identified a new species."' },
        { word: 'indicate', type: '(verb)', definition: 'To point out or show; to be a sign of.', example: '"The data indicates a positive trend."' },
        { word: 'interpret', type: '(verb)', definition: 'To explain the meaning of something.', example: '"Historians interpret events differently."' },
        { word: 'involve', type: '(verb)', definition: 'To include as a necessary part; to engage in an activity.', example: '"The project involves extensive research."' },
        { word: 'method', type: '(noun)', definition: 'A particular way of doing something.', example: '"The scientific method requires testing hypotheses."' },
        { word: 'occur', type: '(verb)', definition: 'To happen or take place.', example: '"Earthquakes occur frequently in this region."' },
        { word: 'significant', type: '(adjective)', definition: 'Important or large enough to have an effect.', example: '"There was a significant increase in sales."' },
        { word: 'theory', type: '(noun)', definition: 'A system of ideas intended to explain something.', example: '"Darwin\'s theory of evolution changed biology."' }
    ],
    science: [
        { word: 'hypothesis', type: '(noun)', definition: 'A proposed explanation for a phenomenon, made as a starting point for further investigation.', example: '"The researcher tested her hypothesis through experiments."' },
        { word: 'experiment', type: '(noun/verb)', definition: 'A scientific procedure to test a hypothesis or demonstrate a fact.', example: '"The experiment confirmed our predictions."' },
        { word: 'variable', type: '(noun)', definition: 'An element that may change or be changed in an experiment.', example: '"Temperature was the independent variable."' },
        { word: 'organism', type: '(noun)', definition: 'An individual animal, plant, or single-celled life form.', example: '"Bacteria are single-celled organisms."' },
        { word: 'cell', type: '(noun)', definition: 'The smallest structural unit of an organism.', example: '"The human body contains trillions of cells."' },
        { word: 'evolution', type: '(noun)', definition: 'The gradual development of species over time.', example: '"Evolution occurs through natural selection."' },
        { word: 'species', type: '(noun)', definition: 'A group of organisms that can reproduce with each other.', example: '"Scientists discovered a new species of frog."' },
        { word: 'ecosystem', type: '(noun)', definition: 'A biological community of interacting organisms and their environment.', example: '"Coral reefs are complex ecosystems."' },
        { word: 'molecule', type: '(noun)', definition: 'A group of atoms bonded together.', example: '"Water is a simple molecule with two hydrogen atoms."' },
        { word: 'compound', type: '(noun)', definition: 'A substance formed by chemical combination of elements.', example: '"Salt is a compound of sodium and chlorine."' },
        { word: 'element', type: '(noun)', definition: 'A substance that cannot be broken down into simpler substances.', example: '"Gold is a chemical element."' },
        { word: 'phenomenon', type: '(noun)', definition: 'A fact or event that can be observed.', example: '"Lightning is a natural phenomenon."' },
        { word: 'data', type: '(noun)', definition: 'Facts and statistics collected for analysis.', example: '"The data supports the hypothesis."' },
        { word: 'research', type: '(noun/verb)', definition: 'Systematic investigation to establish facts.', example: '"Medical research has extended human lifespan."' },
        { word: 'evidence', type: '(noun)', definition: 'Information indicating whether something is true.', example: '"There is strong evidence for climate change."' },
        { word: 'conclusion', type: '(noun)', definition: 'A judgment reached by reasoning.', example: '"The conclusion was based on careful analysis."' },
        { word: 'correlation', type: '(noun)', definition: 'A mutual relationship between two things.', example: '"There is a correlation between diet and health."' },
        { word: 'catalyst', type: '(noun)', definition: 'A substance that speeds up a chemical reaction.', example: '"Enzymes act as biological catalysts."' },
        { word: 'synthesis', type: '(noun)', definition: 'The combination of components to form a connected whole.', example: '"The synthesis of new materials is expensive."' },
        { word: 'theory', type: '(noun)', definition: 'A well-tested explanation for natural phenomena.', example: '"The theory of relativity changed physics."' }
    ],
    social: [
        { word: 'demographic', type: '(adjective/noun)', definition: 'Relating to the structure of populations; statistical data about a population\'s characteristics.', example: '"Demographic changes are affecting the economy."' },
        { word: 'economy', type: '(noun)', definition: 'The system of production and consumption of goods and services.', example: '"The global economy is interconnected."' },
        { word: 'policy', type: '(noun)', definition: 'A course of action adopted by a government or organization.', example: '"Education policy affects all students."' },
        { word: 'culture', type: '(noun)', definition: 'The ideas, customs, and social behavior of a society.', example: '"Culture shapes our worldview."' },
        { word: 'society', type: '(noun)', definition: 'People living together in an organized community.', example: '"Technology has transformed modern society."' },
        { word: 'institution', type: '(noun)', definition: 'An established organization or practice in society.', example: '"Marriage is a social institution."' },
        { word: 'ideology', type: '(noun)', definition: 'A system of ideas and ideals forming the basis of a theory.', example: '"Political ideologies vary widely."' },
        { word: 'revolution', type: '(noun)', definition: 'A dramatic and wide-reaching change; an overthrow of government.', example: '"The Industrial Revolution changed everything."' },
        { word: 'immigration', type: '(noun)', definition: 'The movement of people into a country to live permanently.', example: '"Immigration has shaped American culture."' },
        { word: 'urbanization', type: '(noun)', definition: 'The process of population shift from rural to urban areas.', example: '"Urbanization is accelerating in developing countries."' },
        { word: 'infrastructure', type: '(noun)', definition: 'Basic physical structures needed for society to function.', example: '"The city invested in infrastructure improvements."' },
        { word: 'hierarchy', type: '(noun)', definition: 'A system ranking people according to status or authority.', example: '"Corporate hierarchies are becoming flatter."' },
        { word: 'inequality', type: '(noun)', definition: 'Difference in size, degree, or circumstances; lack of equality.', example: '"Income inequality has increased significantly."' },
        { word: 'globalization', type: '(noun)', definition: 'The process of international integration.', example: '"Globalization has connected world markets."' },
        { word: 'legislation', type: '(noun)', definition: 'Laws collectively; the process of making laws.', example: '"New legislation protects workers\' rights."' },
        { word: 'democracy', type: '(noun)', definition: 'A system of government by the whole population.', example: '"Democracy requires citizen participation."' },
        { word: 'sovereignty', type: '(noun)', definition: 'Supreme power or authority; self-governance.', example: '"Nations protect their sovereignty."' },
        { word: 'migration', type: '(noun)', definition: 'Movement from one place to another.', example: '"Human migration patterns have changed."' },
        { word: 'conflict', type: '(noun/verb)', definition: 'A serious disagreement or argument; to clash.', example: '"The conflict lasted for decades."' },
        { word: 'consensus', type: '(noun)', definition: 'General agreement among a group.', example: '"The committee reached a consensus."' }
    ],
    transitions: [
        { word: 'consequently', type: '(adverb)', definition: 'As a result; therefore. Used to show cause and effect relationships.', example: '"The budget was cut; consequently, several programs were eliminated."' },
        { word: 'furthermore', type: '(adverb)', definition: 'In addition; besides. Used to add more information.', example: '"The plan is cost-effective; furthermore, it\'s environmentally friendly."' },
        { word: 'nevertheless', type: '(adverb)', definition: 'In spite of that; however. Shows contrast despite previous statement.', example: '"The task was difficult; nevertheless, she completed it on time."' },
        { word: 'moreover', type: '(adverb)', definition: 'As a further matter; besides. Adds supporting information.', example: '"The product is affordable; moreover, it\'s high quality."' },
        { word: 'therefore', type: '(adverb)', definition: 'For that reason; consequently. Shows logical conclusion.', example: '"He studied hard; therefore, he passed the exam."' },
        { word: 'however', type: '(adverb)', definition: 'But; nevertheless. Introduces contrasting information.', example: '"The weather was bad; however, the event continued."' },
        { word: 'although', type: '(conjunction)', definition: 'In spite of the fact that; even though.', example: '"Although it was late, she continued working."' },
        { word: 'whereas', type: '(conjunction)', definition: 'In contrast or comparison with the fact that.', example: '"Some prefer coffee, whereas others prefer tea."' },
        { word: 'meanwhile', type: '(adverb)', definition: 'At the same time; during the intervening time.', example: '"The CEO gave a speech; meanwhile, staff prepared for the event."' },
        { word: 'subsequently', type: '(adverb)', definition: 'After a particular thing has happened; afterward.', example: '"She graduated and subsequently found a job."' },
        { word: 'similarly', type: '(adverb)', definition: 'In a similar way; likewise.', example: '"Japan\'s economy grew; similarly, Korea experienced growth."' },
        { word: 'conversely', type: '(adverb)', definition: 'In an opposite way or from an opposite viewpoint.', example: '"Rich countries pollute more; conversely, they have better healthcare."' },
        { word: 'alternatively', type: '(adverb)', definition: 'As another option or possibility.', example: '"You can take the bus; alternatively, you could walk."' },
        { word: 'nonetheless', type: '(adverb)', definition: 'In spite of that; nevertheless.', example: '"The risks were high; nonetheless, they proceeded."' },
        { word: 'hence', type: '(adverb)', definition: 'As a consequence; for this reason.', example: '"Costs increased; hence, prices rose."' },
        { word: 'thus', type: '(adverb)', definition: 'As a result; in this way.', example: '"She trained daily, thus improving her skills."' },
        { word: 'ultimately', type: '(adverb)', definition: 'Finally; in the end.', example: '"Ultimately, the decision was unanimous."' },
        { word: 'primarily', type: '(adverb)', definition: 'For the most part; mainly.', example: '"The course focuses primarily on writing skills."' },
        { word: 'specifically', type: '(adverb)', definition: 'In a precise manner; particularly.', example: '"The report specifically mentions cost overruns."' },
        { word: 'essentially', type: '(adverb)', definition: 'Used to emphasize the basic or fundamental nature.', example: '"The two approaches are essentially the same."' }
    ]
};

const flashcardState = {
    academic: { index: 0, known: [], unknown: [] },
    science: { index: 0, known: [], unknown: [] },
    social: { index: 0, known: [], unknown: [] },
    transitions: { index: 0, known: [], unknown: [] }
};

function flipCard(category) {
    const card = document.getElementById(`flashcard-${category}`);
    if (card) {
        card.classList.toggle('flipped');
    }
}

function nextWord(category) {
    const data = vocabularyData[category];
    const state = flashcardState[category];

    if (!data || !state) return;

    // Unflip card first
    const card = document.getElementById(`flashcard-${category}`);
    if (card) {
        card.classList.remove('flipped');
    }

    // Move to next word
    state.index = (state.index + 1) % data.length;

    // Update display after a short delay
    setTimeout(() => updateFlashcard(category), 300);
}

function markWord(category, known) {
    const data = vocabularyData[category];
    const state = flashcardState[category];

    if (!data || !state) return;

    const currentWord = data[state.index].word;

    if (known) {
        if (!state.known.includes(currentWord)) {
            state.known.push(currentWord);
        }
    } else {
        if (!state.unknown.includes(currentWord)) {
            state.unknown.push(currentWord);
        }
    }

    nextWord(category);
    updateProgress(category);
}

function updateFlashcard(category) {
    const data = vocabularyData[category];
    const state = flashcardState[category];

    if (!data || !state) return;

    const word = data[state.index];

    const wordEl = document.getElementById(`word-${category}`);
    const defEl = document.getElementById(`def-${category}`);

    if (wordEl) {
        wordEl.textContent = word.word;
        const hintEl = wordEl.nextElementSibling;
        if (hintEl && hintEl.classList.contains('flashcard-hint')) {
            hintEl.textContent = word.type;
        }
    }

    if (defEl) {
        defEl.innerHTML = `${word.definition}<br><br><em>${word.example}</em>`;
    }

    updateProgress(category);
}

function updateProgress(category) {
    const data = vocabularyData[category];
    const state = flashcardState[category];

    if (!data || !state) return;

    const progressText = document.getElementById(`progress-${category}`);
    const progressBar = document.getElementById(`progress-fill-${category}`);

    if (progressText) {
        progressText.textContent = `${state.index + 1} / ${data.length}`;
    }

    if (progressBar) {
        const percentage = ((state.index + 1) / data.length) * 100;
        progressBar.style.width = `${percentage}%`;
    }
}

// ========================================
// Timer Functions
// ========================================
let writingTimerInterval = null;
let discussionTimerInterval = null;
let miniTestTimerInterval = null;

function startWritingTimer() {
    if (writingTimerInterval) {
        clearInterval(writingTimerInterval);
    }

    let timeLeft = 20 * 60; // 20 minutes in seconds
    const timerDisplay = document.getElementById('writing-timer');
    const progressBar = document.getElementById('writing-progress');

    writingTimerInterval = setInterval(() => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;

        if (timerDisplay) {
            timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }

        if (progressBar) {
            const percentage = (timeLeft / (20 * 60)) * 100;
            progressBar.style.width = `${percentage}%`;
        }

        if (timeLeft <= 0) {
            clearInterval(writingTimerInterval);
            alert('Time is up!');
        }

        timeLeft--;
    }, 1000);
}

function startDiscussionTimer() {
    if (discussionTimerInterval) {
        clearInterval(discussionTimerInterval);
    }

    let timeLeft = 10 * 60; // 10 minutes in seconds
    const timerDisplay = document.getElementById('discussion-timer');
    const progressBar = document.getElementById('discussion-progress');

    discussionTimerInterval = setInterval(() => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;

        if (timerDisplay) {
            timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }

        if (progressBar) {
            const percentage = (timeLeft / (10 * 60)) * 100;
            progressBar.style.width = `${percentage}%`;
        }

        if (timeLeft <= 0) {
            clearInterval(discussionTimerInterval);
            alert('Time is up!');
        }

        timeLeft--;
    }, 1000);
}

function resetWritingArea(textareaId) {
    const textarea = document.getElementById(textareaId);
    if (textarea) {
        textarea.value = '';
        updateWordCount(textarea);
    }

    // Reset timer displays
    if (textareaId === 'integrated-response') {
        if (writingTimerInterval) {
            clearInterval(writingTimerInterval);
        }
        const timerDisplay = document.getElementById('writing-timer');
        const progressBar = document.getElementById('writing-progress');
        if (timerDisplay) timerDisplay.textContent = '20:00';
        if (progressBar) progressBar.style.width = '100%';
    } else if (textareaId === 'discussion-response') {
        if (discussionTimerInterval) {
            clearInterval(discussionTimerInterval);
        }
        const timerDisplay = document.getElementById('discussion-timer');
        const progressBar = document.getElementById('discussion-progress');
        if (timerDisplay) timerDisplay.textContent = '10:00';
        if (progressBar) progressBar.style.width = '100%';
    }
}

// ========================================
// Word Counter
// ========================================
function initWordCounters() {
    const textareas = document.querySelectorAll('.writing-area');

    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            updateWordCount(this);
        });
    });
}

function updateWordCount(textarea) {
    const text = textarea.value.trim();
    const wordCount = text === '' ? 0 : text.split(/\s+/).length;

    // Find the corresponding word count display
    const container = textarea.closest('.exercise-container') || textarea.closest('.content-section');
    if (container) {
        let countDisplay;
        if (textarea.id === 'integrated-response') {
            countDisplay = document.getElementById('word-count-integrated');
        } else if (textarea.id === 'discussion-response') {
            countDisplay = document.getElementById('word-count-discussion');
        }

        if (countDisplay) {
            countDisplay.textContent = wordCount;
        }
    }
}

// ========================================
// Recording Functionality (Simulated)
// ========================================
let isRecording = false;
let recordingInterval = null;
let recordingTime = 0;

function toggleRecording(button) {
    isRecording = !isRecording;

    const statusEl = button.nextElementSibling;
    const timeEl = statusEl?.nextElementSibling;

    if (isRecording) {
        button.classList.add('recording');
        if (statusEl) statusEl.textContent = 'Grabando...';
        recordingTime = 0;

        recordingInterval = setInterval(() => {
            recordingTime++;
            if (timeEl) {
                const minutes = Math.floor(recordingTime / 60);
                const seconds = recordingTime % 60;
                timeEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')} / 0:45`;
            }

            if (recordingTime >= 45) {
                toggleRecording(button);
            }
        }, 1000);
    } else {
        button.classList.remove('recording');
        if (statusEl) statusEl.textContent = 'Grabacion finalizada. Haz clic para grabar de nuevo.';
        clearInterval(recordingInterval);
    }
}

// ========================================
// Mini Test Functions
// ========================================
function submitMiniTest() {
    const questions = document.querySelectorAll('[id^="mini-q"]');
    let correct = 0;
    let answered = 0;

    questions.forEach(question => {
        const options = question.querySelectorAll('.option');
        let questionAnswered = false;

        options.forEach(option => {
            const input = option.querySelector('input');
            const isCorrect = option.getAttribute('data-correct') === 'true';

            if (input && input.checked) {
                questionAnswered = true;
                if (isCorrect) {
                    option.classList.add('correct');
                    correct++;
                } else {
                    option.classList.add('incorrect');
                }
            }

            if (isCorrect && !option.classList.contains('correct')) {
                option.classList.add('correct');
            }

            if (input) input.disabled = true;
        });

        if (questionAnswered) answered++;
    });

    // Update progress
    const progressText = document.getElementById('test-progress');
    const progressBar = document.getElementById('test-progress-bar');
    if (progressText) progressText.textContent = `${answered} / 10`;
    if (progressBar) progressBar.style.width = `${(answered / 10) * 100}%`;

    // Show results
    const resultsContainer = document.getElementById('mini-test-results');
    const scoreDisplay = document.getElementById('mini-test-score');
    const correctDisplay = document.getElementById('result-correct');
    const incorrectDisplay = document.getElementById('result-incorrect');
    const levelDisplay = document.getElementById('result-level');
    const feedbackDisplay = document.getElementById('level-feedback');

    if (scoreDisplay) scoreDisplay.textContent = `${correct}/10`;
    if (correctDisplay) correctDisplay.textContent = correct;
    if (incorrectDisplay) incorrectDisplay.textContent = 10 - correct;

    // Determine level and feedback
    let level, feedback;
    if (correct >= 9) {
        level = 'Avanzado';
        feedback = 'Excelente! Estas muy bien preparado para el TOEFL. Enfocate en mantener tu nivel y practicar con tests completos bajo condiciones de tiempo real.';
    } else if (correct >= 7) {
        level = 'Alto-Intermedio';
        feedback = 'Muy bien! Tienes una base solida. Trabaja en las areas donde tuviste errores y practica mas ejercicios de listening y reading.';
    } else if (correct >= 5) {
        level = 'Intermedio';
        feedback = 'Buen comienzo! Necesitas mas practica en todas las secciones. Dedica tiempo al vocabulario academico y las estrategias de cada seccion.';
    } else {
        level = 'Basico';
        feedback = 'Hay mucho por mejorar, pero no te desanimes! Empieza con el vocabulario basico y practica diariamente. Usa todos los recursos de esta plataforma.';
    }

    if (levelDisplay) levelDisplay.textContent = level;
    if (feedbackDisplay) feedbackDisplay.innerHTML = `<p style="color: var(--text-secondary);">${feedback}</p>`;

    if (resultsContainer) resultsContainer.classList.remove('hidden');

    // Stop timer
    if (miniTestTimerInterval) {
        clearInterval(miniTestTimerInterval);
    }
}

function resetMiniTest() {
    const questions = document.querySelectorAll('[id^="mini-q"]');

    questions.forEach(question => {
        const options = question.querySelectorAll('.option');

        options.forEach(option => {
            option.classList.remove('selected', 'correct', 'incorrect');
            const input = option.querySelector('input');
            if (input) {
                input.checked = false;
                input.disabled = false;
            }
        });
    });

    // Reset progress
    const progressText = document.getElementById('test-progress');
    const progressBar = document.getElementById('test-progress-bar');
    if (progressText) progressText.textContent = '0 / 10';
    if (progressBar) progressBar.style.width = '0%';

    // Hide results
    const resultsContainer = document.getElementById('mini-test-results');
    if (resultsContainer) resultsContainer.classList.add('hidden');

    // Reset timer
    const timerDisplay = document.getElementById('mini-test-timer');
    if (timerDisplay) timerDisplay.textContent = '15:00';

    if (miniTestTimerInterval) {
        clearInterval(miniTestTimerInterval);
    }
}

// ========================================
// Smooth Scroll for Anchor Links
// ========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ========================================
// Initialize on Page Load
// ========================================
window.addEventListener('load', function() {
    // Initialize flashcards if on vocabulary page
    Object.keys(vocabularyData).forEach(category => {
        updateFlashcard(category);
    });
});
