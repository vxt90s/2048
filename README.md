# 2048 in Python (Pygame)

A clean, desktop implementation of the classic **2048** sliding tile puzzle built with Python and Pygame. Features smooth 60 FPS tile sliding animations, dynamic color scaling up to `8192+`, live window-title score tracking, and instant keyboard restarts.

## Features

* **Smooth Animations:** Frame-by-frame tile sliding movement rendered at 60 FPS.
* **Classic Visual Palette:** Distinct background and font color progression for tile values from `2` up to `8192+`.
* **Live Score Tracking:** Real-time score updates displayed directly in the application window title bar.
* **Game Over & Instant Reset:** Automatic board-lock detection with a semi-transparent Game Over overlay and single-key (`R`) restart.

## Controls
Key                               Action
↑ / ↓ / ← / →     Slide and merge tiles in the corresponding direction
R                 Restart the game (available on the Game Over screen)




## Prerequisites

* Python 3.7+
* `pygame`

## Installation & Setup

1. **Clone the repository:**
   bash
   git clone [https://github.com/vxt90s/2048.git](https://github.com/vxt90s/2048.git)
   cd 2048
