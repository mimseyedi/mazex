# mazex
[![pypi](https://img.shields.io/pypi/v/mazex.svg)](https://pypi.org/project/mazex/) [![license](https://img.shields.io/github/license/mimseyedi/mazex.svg)](https://github.com/mimseyedi/mazex/blob/master/LICENSE)

![img1](https://raw.githubusercontent.com/mimseyedi/mazex/master/docs/images/mazex_poster.png)

mazex is a simple game under the terminal where you have to find the way to the goal in the maze with the most optimal path and solve the challenges.

## Table of Contents: <a class="anchor" id="contents"></a>
* [What is mazex?](#what_is)
* [How to install?](#install)
* [Gameplay](#gameplay)

  * [run command](#run_cmd)
  * [Objects](#obj)
    * [The player, the confused and greedy hero](#player)
    * [The walls, cruel and impenetrable](#wall)
    * [The key, to open a door that pretends to be a wall](#key)
    * [The goal, the only way to success and exit](#goal)
    * [Points, tempting and cunning](#points)
    * [Riddles, challenges that are strong obstacles](#riddles)
  * [info command](#info_cmd)
  
* [Making maze](#mkmaze)
  * [Maze map](#maze_map)
  * [Maze data](#maze_data)
  * [make command](#make_cmd)

* [Proof of play](#proof)
  * [Replay file](#replay_file)
  * [Saving The Replay file](#save_replay_file)
  * [replay command](#replay_cmd)
  * [Working in a replay environment](#replay_env)

* [Contribute](#cont)
* [Resources](#res)


## What is mazex? <a class="anchor" id="what_is"></a>
mazex is a simple cooperative game whose goal is to reach the goal after getting the key and facing the obstacles and challenges! You have to choose the most optimal path to reach the goal and also collect as many points as possible. But be aware that sometimes the points will take you away from the goal and of course it depends on the designer of the maze!

Also, you can easily design the mazes you like for your friends and send them to challenge them and see how they play!

## How to install? <a class="anchor" id="install"></a>
mazex is a terminal game that must be run in a shell environment. This game uses the Python interpreter to run, and you can use pip to install and use it:
```
python3 -m pip install mazex
```

After installation, type the following command in the shell environment and follow the instructions:
```
mazex --help
```


## Gameplay <a class="anchor" id="gameplay"></a>
Mazex has a simple gameplay. You only use your keyboard and use the `up`, `down`, `left` and `right` arrow keys to move in the direction you want, and if you want to `exit` the game, you can use the `control+c` key.

## run command <a class="anchor" id="run_cmd"></a>
To run the game, you must use the run command.
The run command asks you for an argument that is the path of the Maze file you want to play and the extension of this file must be `.mzx`.

```
mazex run maze_file.mzx
```

## Objects <a class="anchor" id="obj"></a>
When you start the game, you will see symbols on the screen that are part of your maze and adventure. Knowing these signs will help you get closer to winning the game.

### The player, the confused and greedy hero <a class="anchor" id="player"></a>
The player is the only sign in the game that you can move. Actually, the player is you in the 2D space of the maze in which you are stuck and you have to reach the goal to win the game. Pay attention to the number of remaining moves that are shown at the top of the screen. If you can't reach your goal before you run out of moves, you lose the game!

### The walls, cruel and impenetrable <a class="anchor" id="wall"></a>
Walls are signs in different corners and places of the maze that do not allow you to pass. Watch out for the walls and cross the right paths to win the game.

### The key, to open a door that pretends to be a wall <a class="anchor" id="key"></a>
The key is the only way to reach your goal.
There is only one key in the maze, and when you reach it, a door will open for you that you thought was a wall before!

Hint: doors are usually located near the goal and open the way to reach the goal.

### The goal, the only way to success and exit <a class="anchor" id="goal"></a>
Goal! What is the meaning of life without it? Even if you are stuck in a confusing maze!
The goal is not so easy to reach and it is the last thing you will reach in the maze. Of course, if you haven't lost the game before! Move carefully and always think about your goal and move forward. But don't forget not to lose yourself!

### Points, tempting and cunning <a class="anchor" id="points"></a>
Points increase your position after winning.
But be careful that if you lose, they won't have any value! Be happy with the points you get, but don't be greedy and think about reaching the goal! Unless you're in a ridiculous game like this!

### Riddles, challenges that are strong obstacles <a class="anchor" id="riddles"></a>
When is a door no longer a door?

When it's ajar!

There may be many such riddles on your way and they will be your obstacle until you have answered them correctly.
Think carefully and enjoy reading them and solve them to get closer to victory!

## info command <a class="anchor" id="info_cmd"></a>
The info command will help you get ready for the game! This command will show you information about any maze you select. Like signs and the number of riddles and allowed moves.
Before starting the game, it is recommended to know more about the game you want to play with the help of the info command.

```
mazex info maze_file.mzx
```

An example of the output:
```
Player sign: X
Wall sign: #
Key sign: K
Goal sign: *
Point sign: $
Number of moves: 329
Number of riddles: 2
Number of points: 7
```


## Making maze <a class="anchor" id="mkmaze"></a>
The exciting and interesting part of mazex is right here!
You can make your own mazes. Just as you like and send it to your friends to challenge them and enjoy together. Or if you are a forgetful person like me, you can design mazes for yourself and get involved with them every once in a while. Just follow some simple rules and then easily make your own maze.

## Maze map <a class="anchor" id="maze_map"></a>
The first step to making a maze is to map it.
It's very simple! Just create a file in .txt format and then design your maze as you want in the file.

Essential rules to follow:
 - All around your maze must be walled.
 - Use only one symbol for each object in the maze.
 - You must use all the objects in your maze except the riddles.
 - Never use tab instead of space!

My suggestion to you is to spend enough time on your maze and design it fair and attractive so that your friends will trust you and enjoy playing your mazes.

An example of a maze map in a text file:
```
oooooooooooooooooooooooooooooooooooooo
o     ooooo  o$       o   o o        o
o  o         o            o o    o   o
o  o ooooooo o   oooooo   o o   ooo  o
o  o o   o o o    oKo       o   o*o  o
o  o o o o o o oooo o     o o   ooo  o
o  o o o o o o?o    o     o o    o   o
o$$o o o o o o      ooooooo ooooooo?oo
oooo o o o o oooooooo            o   o
o$     o o o         o ooooooooo ooo o
oooooooo oooooooooo  o         o  $o o
o                 o  o ooooooo o ooo o
oooooooooooooooo  o  o o$    o o o o o
o                 o  o       o o o o o
o ooooooooooooooooo  ooooooooo o ooo o
o                 o            o     o
ooooooooooooooooo oooooooooooooooooooo
oX                                  $o
oooooooooooooooooooooooooooooooooooooo
```

## Maze data <a class="anchor" id="maze_data"></a>
The next step is to create a json file containing your maze information. (You can do this before designing the maze map)

If you are not familiar with Jason files, see this link:

Create a json format file and enter your maze information in the following pattern:

- Create a key named `player` that contains a single character sign.
- Do this for `wall`, `key`, `goal` and `point` keys as well.
- Create a key named `moves` and write the number of allowed moves you want to choose for your maze. (To consider the number of movements in a fair way, you can first set its value to a large number and calculate the number of movements after playing the maze yourself)
- Create a key named `door` and write a list containing the position of the door you want to open after receiving the key. The first element of this list is the position of the y vector and the next is the position of the x vector. (To get this position, you can use conventional editors. Just note that the index of lists in programming languages starts from zero, so you must reduce the y and x positions by one of them)
- If you want to use a riddle in your maze, you must define a key named `riddles`.
The value of this key is equal to a two-dimensional list that contains lists containing riddle information. The first index of each riddle is equal to the question or the riddle itself. The second index is equal to the correct answer of the riddle, which is case-sensitive. And finally, the third index of each riddle contains the position of the riddle, which is defined exactly like the position of the door key mentioned above. (The mark of each riddle is equal to the question mark `?` and cannot be changed. Be sure to note that you must place the question mark as a riddle mark in the selected position)

An example of a json file that contains maze information:
```json
{
  "player": "X",
  "key": "K",
  "goal": "*",
  "wall": "o",
  "point": "$",
  "moves": 329,
  "door": [4, 32],
  "riddles": [["What building has the most stories?", "a library", [6, 14]],
             ["What can you put in a bucket to make it weigh less? ", "a hole", [7, 35]]]
}
```

## make command <a class="anchor" id="make_cmd"></a>
After completing these two steps, it's time to create your maze file with the help of the make command.
This command requires three arguments from you. The first argument is the path of the text file that contains the map of the maze. The second argument is the path of the json file that contains the maze information. And the third argument is related to the path of the output file or the final file of your maze that is supposed to be created by this command, which must be in .mzx format.

```
mazex make maze_map.txt maze_data.json maze_file.mzx
```

If a problem occurs, you can use the --help option for this command to get guidance. (This option can be used for any command)

```
mazex make --help
```

`Important note:` The final file created by the make command, which is in .mzx format, is an encrypted file so that your friends cannot easily cheat and get more information from the maze or change it. But this encryption is very simple and if your friends are programmers, they can easily decode it. Please do not be strict. This is a completely free project that I started and wrote when I was bored at my mom's house :)
So if you want to develop this project and use a stronger encryption, roll up your sleeves and get to work. I will also be very happy.

## Proof of play <a class="anchor" id="proof"></a>
An interesting system built into mazex is a `proof-of-play system`. Through this system, you can send a file executable by the `replay` command, which records your movements, to the person who designed the maze, to prove that you finished the maze and won the game. Or if the designed maze is not fair and has defects, you can prove it.

## Replay file <a class="anchor" id="replay_file"></a>
The replay file is an encrypted file that contains information about how to play and the moves you have made. When you win or lose the game, you can choose whether or not to create this file.

## Saving the replay file <a class="anchor" id="save_replay_file"></a>
To save the replay file of the game you played, you need to specify at the end of the game that you want this file to be created and then write the path where you want this file to be created. Note that replay files must be saved in .rmzx format!

Request to save the replay file at the end of the game:
![img1](https://raw.githubusercontent.com/mimseyedi/mazex/master/docs/images/mazex_game_over.png)

Save the replay file in the selected path:
![img1](https://raw.githubusercontent.com/mimseyedi/mazex/master/docs/images/mazex_saving_replay.png)

## replay command <a class="anchor" id="replay_cmd"></a>
With the help of the replay command, you can run replay files in .rmzx format. This command accepts only one argument from you, which is the path of the replay file that you want to view.

```
mazex replay replay_file.rmzx
```

## Working in a replay environment <a class="anchor" id="replay_env"></a>
The execution environment of the replay file is exactly similar to the game environment. With the difference that you can only watch the recorded movements of the player by using the `left` and `right` arrow keys.

The next move of the player is displayed by the `right` arrow key and the previous move of the player is displayed by the `left` arrow key. You can also exit the replay environment by pressing `control+c`.

At the bottom of the screen, information about each move will be displayed to you and you can follow the moves in detail.

## Contribute <a class="anchor" id="cont"></a>
I welcome your participation in this fun and free project and I have ideas for Mazex development in the future:
- Creating an easier system for making maze files
- Improving the encryption system for executable files by commands
- Writing tests for project functions. (I tested the program manually and very stupidly because I was bored)
- Writing a validator function for replay files in order to prevent fraud.
- Adding a portal to the maze to move and jump to another point.

## Resources <a class="anchor" id="res"></a>
Sources I used to make this project:
- click module
```
python3 -m pip install click
```
- prompt_toolkit module
```
python3 -m pip install prompt-toolkit==3.0.16
```
- canva website for poster design README file: https://www.canva.com/

Thank you for reading.