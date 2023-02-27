"""
mazex version 1.0.0
Author: mimseyedi
Github repo: https://github.com/mimseyedi/mazex
"""


import os
import sys
import json
import click
import pickle
import subprocess
from pathlib import Path
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog
from prompt_toolkit.key_binding.bindings.basic import load_basic_bindings


@click.group()
def main() -> None:
    """
    mazex is a simple terminal game in which you have to find the right way to reach the key and after opening the door,
    get to the goal with the least possible movement.\n
    You can also easily create your desired maze under the specified rules and protocols and send it to your friends and challenge them!\n
    For more information and contribution: https://github.com/mimseyedi/mazex
    """
    pass


@main.command('make')
@click.argument('args', nargs=3, type=str)
def make(args: list) -> None:
    """
    Creating a maze file with a text file containing the map of the maze and a json file containing the information of the maze.

    Usage pattern: mazex make [txt file path] [json file path] [output maze file path with .mzx suffix]
    """

    make_maze_file(txt_maze_path=args[0], json_maze_path=args[1], maze_file_path=args[2])


@main.command('run')
@click.argument('maze_file_path', nargs=1, type=str)
def run(maze_file_path: str) -> None:
    """
    Running a valid maze file and starting the game and challenge.

    Usage pattern: mazex run [maze file path]
    """

    run_game(maze_file_path=maze_file_path)


@main.command('replay')
@click.argument('replay_file_path', nargs=1, type=str)
def replay(replay_file_path: str) -> None:
    """
    Running the replay file to watch and check the movements of the recorded game.

    Usage pattern: mazex replay [replay file path]
    """

    run_replay(replay_file_path=replay_file_path)


@main.command('info')
@click.argument('maze_file_path', nargs=1, type=str)
def info(maze_file_path: str) -> None:
    """
    Display complete information of a maze file.

    Usage pattern: mazex info [maze file path]
    """

    get_maze_info(maze_file_path=maze_file_path)


@main.command('version')
def version() -> None:
    """
    Display the current version of mazex.
    """

    click.echo('1.0.0')


def run_game(maze_file_path: str) -> None:
    """
    This function checks the maze file and runs the game after confirmation.

    :param maze_file_path: Path of maze file in string.
    :return: None
    """

    if path_validator(path=maze_file_path, suffix='.mzx'):
        maze_data = load_maze(maze_file_path=maze_file_path)
        validated_result = maze_validator(maze_data=maze_data)

        if validated_result:
            logs = {}
            player_location, key_location, goal_location, total_point = validated_result
            session = PromptSession()
            moves_counter, is_key, point = maze_data['moves'], True, 0

            logs[maze_data['moves'] - moves_counter] = add_log(log_type='empty_loc',
                                                               log=[[player_location[0], player_location[1]]])
            while True:
                if moves_counter == 0:
                    logs[maze_data['moves'] - moves_counter] = add_log(log_type='lose',
                                                                         log=[[player_location[0], player_location[1]]])
                    maze_data = load_maze(maze_file_path)
                    logs.update(maze_data)
                    game_over(mode='lose', logs=logs)
                    clear_screen()
                    break

                clear_screen()
                draw_maze('game', maze_data['maze'], moves_counter, point, total_point, 0)

                prompt = session.prompt(key_bindings=game_bindings, bottom_toolbar=game_toolbar())

                if prompt == 'up':
                    player_location, moves_counter, current_point, logs = move(maze_data, player_location, moves_counter, [1, 0, 0, 0], logs)
                    point += current_point
                elif prompt == 'down':
                    player_location, moves_counter, current_point, logs = move(maze_data, player_location, moves_counter, [0, 1, 0, 0], logs)
                    point += current_point
                elif prompt == 'left':
                    player_location, moves_counter, current_point, logs = move(maze_data, player_location, moves_counter, [0, 0, 1, 0], logs)
                    point += current_point
                elif prompt == 'right':
                    player_location, moves_counter, current_point, logs = move(maze_data, player_location, moves_counter, [0, 0, 0, 1], logs)
                    point += current_point
                elif prompt == 'exit':
                    exit_code = exit_the_game()
                    if exit_code:
                        clear_screen()
                        break

                if player_location == goal_location:
                    logs[maze_data['moves'] - moves_counter] = add_log(log_type='win',
                                                                         log=[[player_location[0], player_location[1]]])
                    maze_data = load_maze(maze_file_path)
                    logs.update(maze_data)

                    game_over(mode='win', logs=logs, details=[moves_counter, point, total_point])
                    clear_screen()
                    break

                if player_location == key_location and is_key:
                    is_key = False
                    door_location = maze_data['door']
                    maze_data['maze'][door_location[0]].pop(door_location[1])
                    maze_data['maze'][door_location[0]].insert(door_location[1], ' ')

                    logs[maze_data['moves'] - moves_counter] = add_log(log_type='key',
                                                                         log=[[player_location[0], player_location[1]]])

    else:
        print(f"Error: '{maze_file_path}' is not valid!")


def make_maze_file(txt_maze_path: str, json_maze_path, maze_file_path: str) -> None:
    """
    This function takes the text file that contains the map of the maze and
    the json file that keeps the information of the maze along with a name for the output file of the maze, and
    makes a file executable by the run command in .mzx format.

    :param txt_maze_path: Path of text file in string.
    :param json_maze_path: Path of json file in string.
    :param maze_file_path: Path of output file with .mzx suffix in string.
    :return: None
    """

    if path_validator(path=txt_maze_path, suffix='.txt'):
        with open(txt_maze_path, 'r') as txt_maze_file:
            maze = [list(line.strip()) for line in txt_maze_file.readlines()]
    else:
        print(f"Error: '{txt_maze_path}' is not valid!")
        return

    if path_validator(path=json_maze_path, suffix='.json'):
        with open(json_maze_path, 'r') as json_maze_file:
            maze_data = json.load(json_maze_file)

        maze_data['maze'] = maze
    else:
        print(f"Error: '{json_maze_path}' is not valid!")
        return

    if maze_validator(maze_data=maze_data):
        if maze_file_path.endswith('.mzx'):
            if not Path(maze_file_path).exists():
                with open(maze_file_path, 'wb') as maze_file:
                    pickle.dump(maze_data, maze_file)

                print(f"The maze file was created successfully!")
            else:
                print(f"Error: '{maze_file_path}' already exists!")
        else:
            print("Error: The output file must have the .mzx suffix!")


def load_maze(maze_file_path: str) -> dict:
    """
    This function loads the maze file and returns its information.

    :param maze_file_path: Path of maze file in string.
    :return: dict
    """

    with open(maze_file_path, 'rb') as maze_file:
        maze_data = pickle.load(maze_file)

    return maze_data


def maze_validator(maze_data: dict) -> bool:
    """
    This function evaluates the maze information and approves it if there is no problem and rejects it otherwise.

    :param maze_data: maze information in dict format.
    :return: bool
    """

    def keys_validator() -> bool:
        """
        The task of this function is to check the dictionary keys containing the information of the maze.

        :return: bool
        """

        signs = set()
        for key in ['maze', 'player', 'wall', 'goal', 'moves', 'key', 'door', 'point']:
            if key not in maze_data.keys():
                print(f"Error: The {key} key is one of the essential keys and must be there!")
                return False

            if key in ['player', 'wall', 'key', 'goal', 'point']:
                if not isinstance(maze_data[key], str):
                    print(f"Error: The sign of the {key} key must be of the string type!")
                    return False

                if len(maze_data[key]) != 1:
                    print(f"Error: The sign of the {key} key must be a character!")
                    return False

                signs.add(maze_data[key])

        if len(signs) != 5:
            print(f"Error: One sign is used for two keys and this is unacceptable!")
            return False

        return True


    def wall_validator(wall_sign: str) -> bool:
        """
        The task of this function is to check the walls to make sure of their correct location.

        :param wall_sign: A sign assigned to the 'wall' in one char.
        :return: bool
        """

        for y in [0, len(maze_data['maze']) - 1]:
            for x in range(len(maze_data['maze'][y])):
                if maze_data['maze'][y][x] != wall_sign:
                    print(f'Error: Lack of proper covering of the wall at [{y}, {x}]')
                    return False

        for y in range(1, len(maze_data['maze']) - 1):
            if maze_data['maze'][y][0] != wall_sign or maze_data['maze'][y][-1] != wall_sign:
                print(f'Error: Lack of proper covering of the wall in line {y}')
                return False

        return True


    def pkg_validator(player_sign: str, key_sign: str, goal_sign: str) -> bool:
        """
        The task of this function is to check player, key and goal keys to make sure that they are correct according to the rules.

        :param player_sign: A sign assigned to the 'player' in one char.
        :param key_sign: A sign assigned to the 'key' in one char.
        :param goal_sign: A sign assigned to the 'goal' in one char.
        :return: bool
        """

        player_counter, key_counter, goal_counter = 0, 0, 0
        for y in range(len(maze_data['maze'])):
            player_counter += maze_data['maze'][y].count(player_sign)
            key_counter += maze_data['maze'][y].count(key_sign)
            goal_counter += maze_data['maze'][y].count(goal_sign)

        for sign, number in {'player': player_counter, 'key': key_counter, 'goal': goal_counter}.items():
            if number != 1:
                print(f'Error: The valid number of {sign} in each maze is equal to one!')
                return False

        return True


    def door_validator(door_location: list) -> bool:
        """
        The task of this function is to check the 'door' key to make sure that the correct place is considered for this key.

        :param door_location: The location of 'door' key in [y, x] format.
        :return: bool
        """

        if not isinstance(door_location, list) or len(door_location) != 2:
            print(f"Error: The value provided for the door is not valid!")
            return False

        try:
            if maze_data['maze'][door_location[0]][door_location[1]] != maze_data['wall']:
                print(f"Error: The location intended for the door must be the location of a wall!")
                return False
        except IndexError:
            print(f"Error: The door location was not found in the maze!")
            return False
        except TypeError:
            print(f"Error: The door location must be integers!")

        if door_location[0] in [0, len(maze_data['maze']) - 1] or \
                door_location[1] in [0, len(maze_data['maze'][door_location[0]])]:
            print(f"Error: Really? do you like to run away? The door location cannot be one of the border walls!")
            return False

        return True


    def moves_validator(moves: int) -> bool:
        """
        The task of this function is to check the number of movements assigned to the maze and validate it.

        :param moves: A positive integer indicating the number of allowed moves in a maze.
        :return: bool
        """

        if not isinstance(moves, int):
            print(f"Error: The value of moves must be of integer type!")
            return False

        if moves < 0:
            print(f"Error: The value of moves must be a positive integer!")
            return False

        return True


    def riddle_validator(riddles: list) -> bool:
        """
        The task of this function is to check the 'riddles' and their locations in order to manage them correctly in the maze.

        :param riddles: A 2D list containing the information of puzzles in the form of separate lists.
                        Pattern: [[question, answer, location in [y, x]], ...]
        :return: bool
        """

        for index, riddle in enumerate(riddles):
            try:
                question, answer, loc = riddle
            except ValueError:
                print(f"Error: Riddle number {index} is not properly packaged!")
                return False

            if not isinstance(question, str) or not isinstance(answer, str):
                print(f"Error: The question and answer values of each riddle must be of string type!")
                return False

            if not isinstance(loc, list):
                print(f"Error: The location of riddle number {index} is not valid!")
                return False

            try:
                if maze_data['maze'][loc[0]][loc[1]] != "?":
                    print(f"Error: The mismatch of riddle number {index} with its address!")
                    return False
            except IndexError:
                print(f"Error: The riddle location was not found in the maze!")
                return False
            except TypeError:
                print(f"Error: The location of riddle number {index} must be of integer type!")
                return False

        return True


    def point_counter(point_sign: str) -> int:
        """
        A function to count the number of points or bonuses in each maze.

        :param point_sign: A sign assigned to the 'point' in one char.
        :return: int
        """

        points = 0
        for y in range(len(maze_data['maze'])):
            points += maze_data['maze'][y].count(point_sign)

        return points


    def find_location(sign: str) -> list:
        """
        A function to find the location of a sign in the maze that accepts as an argument.

        :param sign: Any sign in one char.
        :return: list [y, x]
        """

        for y in range(len(maze_data['maze'])):
            for x in range(len(maze_data['maze'][y])):
                if maze_data['maze'][y][x] == sign:
                    location = [y, x]

        return location


    if keys_validator() and wall_validator(maze_data['wall']) and \
        pkg_validator(maze_data['player'], maze_data['key'], maze_data['goal']) and \
        door_validator(maze_data['door']) and moves_validator(maze_data['moves']) and \
        riddle_validator(maze_data['riddles']):

        total_point = point_counter(maze_data['point'])
        player, key, goal = find_location(maze_data['player']), find_location(maze_data['key']), find_location(maze_data['goal'])

        return player, key, goal, total_point

    return False


def move(maze_data: dict, player_location: list, remaining_moves: int, direction: list, logs: dict) -> tuple:
    """
    The task of this function is to manage the movement of the player in the maze and the events that occur.

    :param maze_data: Information of maze in dict format.
    :param player_location: Location of player sign in [y, x] format.
    :param remaining_moves: Number of moves left.
    :param direction: To move with binary values in a list like this: [up, down, left, right]
                      Example: [1, 0, 0, 0] >>> up
                               [0, 1, 0, 0] >>> down
                               [0, 0, 1, 0] >>> left
                               [0, 0, 0, 1] >>> right
    :param logs: Movement logs in dict format.
    :return: tuple
    """

    def get_riddle(riddle_location: list):
        for index in range(len(maze_data['riddles'])):
            if maze_data['riddles'][index][2][0] == riddle_location[0] and \
                maze_data['riddles'][index][2][1] == riddle_location[1]:
                question = maze_data['riddles'][index][0]
                answer = maze_data['riddles'][index][1]
                return question, answer

    def riddle_form(question: str, answer: str):
        user_answer = input_dialog(title='Riddle?', text=question).run()
        return user_answer

    maze = maze_data['maze']
    last_player_location = player_location[0], player_location[1]
    point, last_remaining_moves = 0, remaining_moves

    if maze[last_player_location[0]][last_player_location[1]] != '?':
        maze[last_player_location[0]].pop(last_player_location[1])
        maze[last_player_location[0]].insert(last_player_location[1], " ")

    if direction[0] == 1:
        player_location[0] -= 1
    elif direction[1] == 1:
        player_location[0] += 1
    elif direction[2] == 1:
        player_location[1] -= 1
    elif direction[3] == 1:
        player_location[1] += 1

    if maze[player_location[0]][player_location[1]] == '$':
        point = 1
        maze[player_location[0]].pop(player_location[1])
        maze[player_location[0]].insert(player_location[1], maze_data['player'])
        remaining_moves -= 1

        logs[maze_data['moves'] - remaining_moves] = add_log(log_type='point',
                                                             log=[[player_location[0], player_location[1]]])

    elif maze[player_location[0]][player_location[1]] == '?':
        question, answer = get_riddle([player_location[0], player_location[1]])

        user_answer = riddle_form(question, answer)

        if user_answer != answer:
            maze[player_location[0]].pop(player_location[1])
            maze[player_location[0]].insert(player_location[1], '?')

            player_location = [last_player_location[0], last_player_location[1]]
            remaining_moves = last_remaining_moves

            maze[player_location[0]].pop(player_location[1])
            maze[player_location[0]].insert(player_location[1], maze_data['player'])

            remaining_moves -= 1

            logs[maze_data['moves'] - remaining_moves] = add_log(log_type='riddle',
                                                                 log=[[player_location[0], player_location[1]],
                                                                      question, user_answer])
        else:
            remaining_moves -= 1

            maze[player_location[0]].pop(player_location[1])
            maze[player_location[0]].insert(player_location[1], maze_data['player'])

            logs[maze_data['moves'] - remaining_moves] = add_log(log_type='riddle',
                                                                 log=[[player_location[0], player_location[1]],
                                                                      question, user_answer])

    elif maze[player_location[0]][player_location[1]] == maze_data['wall']:
        player_location = [last_player_location[0], last_player_location[1]]
        remaining_moves = last_remaining_moves

        maze[player_location[0]].pop(player_location[1])
        maze[player_location[0]].insert(player_location[1], maze_data['player'])

    else:
        maze[player_location[0]].pop(player_location[1])
        maze[player_location[0]].insert(player_location[1], maze_data['player'])

        remaining_moves -= 1

        logs[maze_data['moves'] - remaining_moves] = add_log(log_type='empty_loc', log=[[player_location[0], player_location[1]]])

    return player_location, remaining_moves, point, logs


def path_validator(path: str, suffix: str) -> bool:
    """
    The task of this function is to validate file paths.

    :param path: Path of file in string format.
    :param suffix: Suffix of the file.
    :return: bool
    """

    return True if Path(path).exists() and Path(path).is_file() and path.endswith(suffix) else False


def draw_maze(maze_mode: str, maze: list, remaining_moves: int, point: int, total_point: int, moves: int) -> None:
    """
    A function to draw and display the maze.

    :param maze_mode: Binary value, 'game' or 'replay'
    :param maze: Maze in list format.
    :param remaining_moves: Number of moves left.
    :param point: Total points earned.
    :param total_point: The total number of points in the maze that can be achieved.
    :param moves: Number of total moves in positive integer.
    :return: None
    """

    if maze_mode == 'game':
        print(f"Remaining Moves: {remaining_moves} - Point: {point}/{total_point}")
    else:
        print(f'Move: {remaining_moves}/{moves} - Point: {point}/{total_point}')

    for line in maze:
        print(''.join(line))


def game_over(mode: str, logs: dict, details: list=[]) -> None:
    """
    This function will be called at the end of the game and is responsible for the end state and
    the end message depending on the end mode of the game.

    :param mode: In two situations, lose or win.
    :param logs: Movement logs in dict format.
    :param details: Details containing information necessary for display in 'win' mode.
    :return: None
    """

    lose_style = Style.from_dict({
        'dialog': 'bg:#cb4335',
        'dialog frame.label': 'bg:#2c3e50 #cb4335',
        'dialog.body': 'bg:#2c3e50 #cb4335',
        'dialog shadow': 'bg:#17202a'})

    win_style = Style.from_dict({
        'dialog': 'bg:#229954',
        'dialog frame.label': 'bg:#2c3e50 #229954',
        'dialog.body': 'bg:#2c3e50 #229954',
        'dialog shadow': 'bg:#17202a'})

    if mode == 'lose':
        user_answer = yes_no_dialog(title='GAME OVER', text='Unfortunately, you lost the game!\nDo you want to save the replay file?', style=lose_style).run()
        if user_answer:
            save_replay(logs=logs)

    else:
        user_answer = yes_no_dialog(title='GAME OVER', text=f'Congratulations, you won!\nRemaining moves: {details[0]}\nPoint: {details[1]}/{details[2]}\nDo you want to save the replay file?',
                       style=win_style).run()
        if user_answer:
            save_replay(logs=logs)


def exit_the_game() -> bool:
    """
    The task of this function is to exit the game after user confirmation.

    :return: bool
    """

    exit_style = Style.from_dict({
        'dialog': 'bg:#cb4335',
        'dialog frame.label': 'bg:#2c3e50 #cb4335',
        'dialog.body': 'bg:#2c3e50 #cb4335',
        'dialog shadow': 'bg:#17202a'})

    exit_code = yes_no_dialog(title='EXIT', text='Are you sure?', style=exit_style).run()
    return True if exit_code else False


def clear_screen() -> None:
    """
    The task of this function is to clear the screen in order to update the information of the maze.

    :return: None
    """

    subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)


def game_toolbar() -> HTML:
    """
    This function returns an html string containing a simple game guide that can be seen at the bottom of the screen.

    :return: HTML
    """

    return HTML('control+c to exit and moving with &#x2191; &#x2193; &#x2190; &#x2192;')


game_bindings = load_basic_bindings()

@game_bindings.add('up')
def _(event):
    """
    Read the up arrow key to move the player up.

    :param event:
    :return:
    """

    event.current_buffer.insert_text('up')
    event.app.exit(result=event.app.current_buffer.text)


@game_bindings.add('down')
def _(event):
    """
    Read the down arrow key to move the player down.

    :param event: The event that is automatically passed to this binder.
    :return: str
    """

    event.current_buffer.insert_text('down')
    event.app.exit(result=event.app.current_buffer.text)


@game_bindings.add('left')
def _(event):
    """
    Read the left arrow key to move the player left.

    :param event: The event that is automatically passed to this binder.
    :return: str
    """

    event.current_buffer.insert_text('left')
    event.app.exit(result=event.app.current_buffer.text)


@game_bindings.add('right')
def _(event):
    """
    Read the right arrow key to move the player right.

    :param event: The event that is automatically passed to this binder.
    :return: str
    """

    event.current_buffer.insert_text('right')
    event.app.exit(result=event.app.current_buffer.text)


@game_bindings.add('c-c')
def _(event):
    """
    Reading Control+C (^C) to create a command to quit the game.

    :param event: The event that is automatically passed to this binder.
    :return: str
    """

    event.current_buffer.insert_text('exit')
    event.app.exit(result=event.app.current_buffer.text)


def get_maze_info(maze_file_path: str) -> None:
    """
    This function Displaying complete information of the maze file.

    :param maze_file_path: Path of maze file in string format.
    :return: None
    """

    if path_validator(path=maze_file_path, suffix='.mzx'):
        maze_data = load_maze(maze_file_path)
        validated_result = maze_validator(maze_data=maze_data)

        if validated_result:
            print(f"Player sign: {maze_data['player']}")
            print(f"Wall sign: {maze_data['wall']}")
            print(f"Key sign: {maze_data['key']}")
            print(f"Goal sign: {maze_data['goal']}")
            print(f"Point sign: {maze_data['point']}")
            print(f"Number of moves: {maze_data['moves']}")
            print(f"Number of riddles: {len(maze_data['riddles'])}")
            print(f"Number of points: {validated_result[-1]}")
    else:
        print(f"Error: '{maze_file_path}' is not valid!")


def run_replay(replay_file_path: str) -> None:
    """
    This function is responsible for executing the replay file and manages the movements.

    :param replay_file: Path of replay file in string format.
    :return: None
    """

    if path_validator(path=replay_file_path, suffix='.rmzx'):
        replay_data = load_replay(replay_file_path)
        validated_result_with_total_point = replay_validator(replay_data)

        if validated_result_with_total_point:
            session = PromptSession()
            current_location, point = 0, 0
            base_maze = load_replay(replay_file_path)['maze']
            toolbar_message = 'control+c to exit - next move with &#x2192; and previous move with &#x2190;'

            while True:
                clear_screen()
                draw_maze('replay', replay_data['maze'], current_location, point, validated_result_with_total_point, replay_data['moves'])

                prompt = session.prompt(key_bindings=replay_bindings, bottom_toolbar=replay_toolbar(toolbar_message))

                if prompt == 'next':
                    try:
                        if current_location + 1 not in replay_data.keys():
                            raise KeyError

                        replay_data[current_location + 1]

                        player_location = [replay_data[current_location]['loc'][0], replay_data[current_location]['loc'][1]]
                        replay_data['maze'][player_location[0]].pop(player_location[1])
                        replay_data['maze'][player_location[0]].insert(player_location[1], ' ')
                        last_maze = replay_data['maze']

                        current_location += 1

                        player_location = [replay_data[current_location]['loc'][0], replay_data[current_location]['loc'][1]]
                        sign = base_maze[player_location[0]][player_location[1]]

                        if sign == replay_data['key']:
                            replay_data['maze'][replay_data['door'][0]].pop(replay_data['door'][1])
                            replay_data['maze'][replay_data['door'][0]].insert(replay_data['door'][1], ' ')

                        elif sign == replay_data['point']:
                            point += 1

                        replay_data['maze'][player_location[0]].pop(player_location[1])
                        replay_data['maze'][player_location[0]].insert(player_location[1], replay_data['player'])

                        if replay_data[current_location]['log_type'] in ['empty_loc', 'key', 'goal', 'win', 'lose']:
                            toolbar_message = f'{replay_data[current_location]["log_type"]} {replay_data[current_location]["loc"]}'
                        elif replay_data[current_location]['log_type'] == 'point':
                            toolbar_message = f'{replay_data[current_location]["log_type"]} {replay_data[current_location]["loc"]} Point: {replay_data[current_location]["point"]}'
                        elif replay_data[current_location]['log_type'] == 'riddle':
                            toolbar_message = f'{replay_data[current_location]["log_type"]} {replay_data[current_location]["loc"]} q:{replay_data[current_location]["question"]} a:{replay_data[current_location]["answer"]}'

                    except KeyError:
                        toolbar_message = 'This is the last move!'

                elif prompt == 'previous':
                    try:
                        if current_location - 1 not in replay_data.keys():
                            raise KeyError

                        player_location = [replay_data[current_location]['loc'][0], replay_data[current_location]['loc'][1]]
                        replay_data['maze'][player_location[0]].pop(player_location[1])

                        sign = base_maze[player_location[0]][player_location[1]]

                        if sign in [replay_data['point'], replay_data['goal']]:
                            replay_data['maze'][player_location[0]].insert(player_location[1], sign)
                            if sign == replay_data['point']:
                                point -= 1

                        elif sign == '?' and replay_data[current_location]['log_type'] == 'riddle':
                            replay_data['maze'][player_location[0]].insert(player_location[1], sign)
                        elif sign == replay_data['key']:
                            replay_data['maze'][player_location[0]].insert(player_location[1], sign)
                            replay_data['maze'][replay_data['door'][0]].pop(replay_data['door'][1])
                            replay_data['maze'][replay_data['door'][0]].insert(replay_data['door'][1], replay_data['wall'])
                        else:
                            replay_data['maze'][player_location[0]].insert(player_location[1], ' ')

                        current_location -= 1

                        player_location = [replay_data[current_location]['loc'][0], replay_data[current_location]['loc'][1]]
                        replay_data['maze'][player_location[0]].pop(player_location[1])
                        replay_data['maze'][player_location[0]].insert(player_location[1], replay_data['player'])
                        toolbar_message = f'{replay_data[current_location]["log_type"]} {replay_data[current_location]["loc"]}'

                        if replay_data[current_location]['log_type'] in ['empty_loc', 'key', 'goal', 'win', 'lose']:
                            toolbar_message = f'{replay_data[current_location]["log_type"]} {replay_data[current_location]["loc"]}'
                        elif replay_data[current_location]['log_type'] == 'point':
                            toolbar_message = f'{replay_data[current_location]["log_type"]} {replay_data[current_location]["loc"]} Point: {replay_data[current_location]["point"]}'
                        elif replay_data[current_location]['log_type'] == 'riddle':
                            toolbar_message = f'{replay_data[current_location]["log_type"]} {replay_data[current_location]["loc"]} q:{replay_data[current_location]["question"]} a:{replay_data[current_location]["answer"]}'

                    except KeyError:
                        toolbar_message = 'This is the first location!'

                elif prompt == 'exit':
                    exit_code = exit_the_replay()
                    if exit_code:
                        clear_screen()
                        break
    else:
        print(f"Error: '{replay_file_path}' is not valid!")


def replay_validator(replay_data: dict) -> bool:
    """
    The task of this function is to evaluate and confirm the replay file and the information inside it.

    :param replay_data: The replay file information in dict format.
    :return: bool
    """

    special_keys = ['maze', 'player', 'wall', 'key', 'goal', 'point', 'moves', 'door', 'riddles']
    validated_maze = maze_validator(replay_data)

    if validated_maze:
        player_location, key_location, goal_location, total_point = validated_maze

        for key in replay_data.keys():
            if key not in special_keys and not isinstance(key, int):
                print('Error: The replay file has a problem. This file is probably manipulated!')
                return False

        return total_point

    return False


def replay_toolbar(message: str) -> HTML:
    """
    This function manages the messages related to each location during
    the execution of the replay file and displays it at the bottom of the screen.

    :param message: The message to be displayed.
    :return: HTML
    """

    return HTML(message)


def add_log(log_type: str, log: list) -> dict:
    if log_type in ['empty_loc', 'key', 'goal', 'win', 'lose']:
        return {'log_type': log_type, 'loc': log[0]}

    elif log_type == 'point':
        return {'log_type': log_type,'loc': log[0], 'point': 1}

    elif log_type == 'riddle':
        return {'log_type': log_type, 'loc': log[0], 'question': log[1], 'answer': log[2]}


def save_replay(logs: dict) -> None:
    """
    The task of this function is to save game movements and logs in the replay file.

    :param logs: Movement logs in dict format.
    :return: None
    """

    error_message, success = '', False

    while not success:
        replay_path = input_dialog(title='Save replay', text=f'{error_message}Please Enter The Path of replay file:', completer=PathCompleter()).run()

        if replay_path is not None:
            if len(replay_path.strip()) > 0:
                if replay_path.endswith('.rmzx'):
                    if not Path(replay_path).exists():
                        try:
                            with open(replay_path, 'wb') as replay_file:
                                pickle.dump(logs, replay_file)

                            error_message, success = '', True

                        except FileNotFoundError:
                            error_message = 'Error: This path is not valid!\n'
                    else:
                        error_message = 'Error: This file already exists!\n'
                else:
                    error_message = 'Error: The replay file must be saved with the .rmzx suffix!\n'
            else:
                error_message = 'Error: Empty path is not valid!\n'
        else:
            break


def load_replay(replay_path: str) -> dict:
    """
    The task of this function is to load the information in the replay file.

    :param replay_path: Path of replay file in string format.
    :return: dict
    """

    with open(replay_path, 'rb') as replay_file:
        replay_data = pickle.load(replay_file)

    return replay_data


def exit_the_replay() -> bool:
    """
    The task of this function is to exit the replay after user confirmation.

    :return: bool
    """

    exit_style = Style.from_dict({
        'dialog': 'bg:#cb4335',
        'dialog frame.label': 'bg:#2c3e50 #cb4335',
        'dialog.body': 'bg:#2c3e50 #cb4335',
        'dialog shadow': 'bg:#17202a'})

    exit_code = yes_no_dialog(title='EXIT', text='Are you sure?', style=exit_style).run()
    return True if exit_code else False


replay_bindings = load_basic_bindings()

@replay_bindings.add('left')
def _(event):
    """
    Read the left arrow key to previous move.

    :param event: The event that is automatically passed to this binder.
    :return: str
    """

    event.current_buffer.insert_text('previous')
    event.app.exit(result=event.app.current_buffer.text)


@replay_bindings.add('right')
def _(event):
    """
    Read the right arrow key to next move.

    :param event: The event that is automatically passed to this binder.
    :return: str
    """

    event.current_buffer.insert_text('next')
    event.app.exit(result=event.app.current_buffer.text)


@replay_bindings.add('c-c')
def _(event):
    """
    Reading Control+C (^C) to create a command to quit the replay.

    :param event: The event that is automatically passed to this binder.
    :return: str
    """

    event.current_buffer.insert_text('exit')
    event.app.exit(result=event.app.current_buffer.text)


if __name__ == '__main__':
    main()
