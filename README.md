# É Osso 🦴
Proposta de jogo inspirado em Undertale baseado em Pygame.

# É Osso - Game README

## Overview
"É Osso" is a simple 2D game built with Pygame inspired by the bullet-dodging mechanics of Undertale. Players control a heart that must navigate through increasingly difficult levels while avoiding bones that move across the screen in various patterns.

## Features
- 9 progressively challenging levels
- Simple controls using arrow keys or WASD
- Level progression system with personal best tracking
- Death and victory sequences with custom animations
- Original sound effects and music
- Easter egg hidden in the game

## Installation Requirements
- Python 3.x
- Pygame library

## File Structure
É Osso/
├── fonts/
│   └── minecraftia.ttf
├── images/
│   ├── bone.png
│   ├── heart32x.png
│   ├── heart64x.png
│   ├── heartdead64x.png
│   ├── shadedicon.png
│   ├── startScreen.png
│   ├── startHoverScreen.png
│   ├── clickScreen.png
│   ├── playHoverScreen.png
│   ├── menuHoverScreen.png
│   └── deathScreenOverlay.png
├── sounds/
│   ├── menu.ogg
│   ├── sans.ogg
│   ├── determination.ogg
│   ├── holiday.ogg
│   ├── death1.wav
│   ├── death2.wav
│   ├── death3.wav
│   ├── newlevel1.wav
│   └── newlevel2.wav
└── game.py

## How to Play
1. Run `game.py`
2. Click "Play" on the start screen
3. Use arrow keys or WASD to move the heart
4. Avoid all bones that move across the screen
5. Progress through all 9 levels to win

## Game Mechanics
- **Movement**: Heart moves in eight directions (up, down, left, right, and diagonals)
- **Collision**: Touching any bone results in death
- **Levels**:
  - Level 1: Single bone moving left to right
  - Level 2: Faster bone movement
  - Level 3: Introduction of bones from top and bottom
  - Level 4: Bones move up and down while traveling horizontally
  - Level 5: Multiple bones appear in waves from right to left
  - Level 6: Bones appear from left to right
  - Level 7: Faster bone movement
  - Level 8: Complex bone movement patterns including direction changes
  - Level 9: Victory screen

## Game Controls
- **Movement**: Arrow keys or WASD
- **Exit**: Close window or press ESC in easter egg mode
- **Menu Navigation**: Mouse clicks

## Special Features
- **Progress Tracking**: The game records your highest level reached
- **Level Transitions**: Visual and audio cues between levels
- **Death Animation**: Custom animation sequence when colliding with bones
- **Easter Egg**: Hidden DVD logo-style animation (accessible from main menu)

## Credits
- Game developed with Pygame
- Features custom graphics and sound effects

Enjoy playing "É Osso"!
