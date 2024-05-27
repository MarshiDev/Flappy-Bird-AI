<h1 style="text-align: center;">Flappy Bird-AI</h1>
<h2>What is this?</h2>
Flappy Bird-AI is a simulation written in python using pygame, that aims to help to understand how genetic algorithms work. It uses those to train an AI to play a very basic implementation of the retro-game Flappy Bird.

## Installation
Clone the project to your computer using git clone or by downloading it as a zip file. Make sure to install all the required python packages using ```pip install -r requirements.txt```. Then run the main.py file using ```python path/to/your/main.py```

## Controls
Upon running the main.py file, many Flappy Birds will begin to flap around and begin learning. To pause the simulation, you can press ***p***. While paused, you can step forward using ***w***.<br>
<img width="60%" alt="flappybird-ai" src="https://github.com/MarshiDev/Flappy-Bird-AI/assets/97107764/5cf637e7-e75e-403e-a197-6e1bd96e0bed"><br>
<i>(Disclaimer: after stepping forward a lot, the simulation will stop spawning pipes and ultimately crash. This bug will likely be patched in the future.)</i><br><br>
If you want to spectate only a single Flappy Bird, you can press ***i*** to toggle the isolating function. Pressing ***e*** will make you enter player vs. ai - mode. This will restart the simulation with the current population of Flappy Birds.
A red-tinted Flappy Bird will appear as the player, by holding space you can fly up when this mode is active and you will fly down automatically if you are not holding space. You can use this mode to test your skills and explore the intelligence of a trained AI.<br>
<img width="60%" alt="flappybird-ai: player vs. AI" src="https://github.com/MarshiDev/Flappy-Bird-AI/assets/97107764/a431f713-6496-4bc5-b8cb-cf93a17aecd1">
