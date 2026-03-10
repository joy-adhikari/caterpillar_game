# Caterpillar Game

#### Video Demo: https://youtu.be/U-qQDXNydD8

---

## Description

**Caterpillar Game** is a classic arcade-style game inspired by the traditional Snake game, developed as my **CS50 Final Project**. The goal of the game is simple: control a growing caterpillar, eat fruits to increase your score, and avoid collisions with walls or with the caterpillar’s own body. While the core idea is familiar, the implementation focuses on clean structure, multiple game states, user-friendly controls, and visual polish, making it a complete and playable desktop game rather than a minimal demo.

The project is written in **Python** using the **Pygame** library. Pygame provides the tools required for handling graphics, keyboard input, sound, and timing, making it suitable for building a real-time interactive game. This project demonstrates my understanding of event-driven programming, game loops, object-oriented design, and state management.

---

## Motivation and Learning Process

I initially learned the fundamentals of a snake-style game from online resources, including YouTube tutorials, to understand how movement, collision detection, and grid-based games work. From there, I extended the project significantly by designing my own structure, adding features, fixing bugs, and improving usability. I also used AI-based tools (such as ChatGPT) as a learning aid to clarify concepts, debug errors, and refine certain parts of the code. In accordance with CS50’s academic honesty policy, any such assistance was treated as supportive guidance, not a replacement for my own work, and the final design and implementation reflect my understanding.

---

## Gameplay Overview

When the game starts, the player is presented with a **menu screen** that explains the controls and allows the game to begin. Once started, the caterpillar moves continuously across a grid-based board. The player controls its direction using the keyboard arrow keys. Each time the caterpillar eats a fruit, its length increases and the score goes up.

The game ends when the caterpillar collides with the boundary of the screen or with its own body. When this happens, a **Game Over screen** is displayed, clearly informing the player that the session has ended. The player can then choose to exit the game or restart, depending on the implemented controls.

A **pause feature** is also included, allowing the player to temporarily stop the game. This improves usability and demonstrates proper state handling in a real-time application.

---

## Key Features

- **Grid-based movement**: The caterpillar moves smoothly on a fixed grid, ensuring predictable and fair gameplay.
- **Multiple game states**: The game includes menu, playing, paused, and game-over states, each handled explicitly in the code.
- **Score tracking**: The score increases as the caterpillar eats fruits and is displayed on the screen.
- **Collision detection**: The game accurately detects collisions with walls and the caterpillar’s own body.
- **Randomized fruit spawning**: Fruits spawn at random positions while avoiding the caterpillar’s body.
- **Visual overlays**: Transparent overlays are used for pause and game-over screens to enhance visual clarity.
- **Keyboard controls**: Intuitive controls using arrow keys, with additional keys for pausing and quitting.

---

## Technical Design

The project follows an **object-oriented design**. Separate classes are used to represent the caterpillar, the fruit, and the main game controller. This separation of concerns makes the code easier to read, debug, and extend. The main game loop is responsible for handling events, updating the game state, and rendering graphics at a fixed frame rate.

Pygame’s event system is used to capture keyboard input, while its rendering functions handle drawing the background, caterpillar segments, fruit, text, and overlays. Timing is managed using a clock to ensure consistent speed across different systems.

---

## Challenges and Solutions

One of the main challenges was managing the **drawing order** of elements on the screen, especially when implementing pause and game-over overlays. Incorrect draw order initially caused black or invisible screens. This was resolved by carefully structuring the render sequence so that the background is drawn first, followed by game elements, and finally overlays and text.

Another challenge was ensuring that the fruit never spawns inside the caterpillar’s body. This was solved by checking generated positions against the caterpillar’s segments and regenerating the fruit position if necessary.

---

## Academic Honesty and AI Usage

For this final project, I made limited use of AI-based tools as permitted by CS50’s guidelines. These tools were used to:
- Clarify Python and Pygame concepts
- Help debug specific errors
- Improve code readability and structure

All design decisions, logic, and final implementation are my own, and I understand the code I have written. Any AI assistance is acknowledged in the code comments where applicable.

---

## Conclusion

The Caterpillar Game represents my progress throughout CS50, combining foundational programming concepts with practical problem-solving and creativity. While inspired by a classic game, this project goes beyond a basic tutorial by incorporating multiple game states, polished UI elements, and thoughtful structure. It demonstrates my ability to learn from resources, apply knowledge independently, and build a complete, functional software project from start to finish.

