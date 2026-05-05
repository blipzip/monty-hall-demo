import random
from time import sleep

def __rand() -> int:
    return random.randrange(1,4)


def __host(msg: str, silent: bool, whisper: bool = False):
    if silent:
        return
    if whisper:
        msg = f"\033[249;3m{msg}\033[0m"
    print(f"🤵 {msg}")
    sleep(2)

def __robot(msg: str, silent:bool = False):
    if silent:
        return
    print(f"🤖 {msg}")
    sleep(2)

def __show_score(win: int, loss: int, silent: bool = False):
    total_games = win + loss
    if win == 0:
        pc = 0
    elif loss == 0:
        pc = 100
    else:
        pc = int(win / total_games * 100)
    __host(f"The tally is currently {win} wins and {loss} losses for the robot. That's a {pc}% win rate over {total_games} games.", silent=silent)

def __play(silent: bool = False) -> bool:
    options = [1,2,3]

    answer = __rand()
    __host(f"Between me and you, the winning door for this round is number {answer}", silent=silent, whisper=True)
    robot_first_guess = __rand()
    __robot(f"My first guess is {robot_first_guess}", silent=silent)
    remaining_options = options.copy()
    remaining_options.remove(answer)
    if robot_first_guess in remaining_options:
        remaining_options.remove(robot_first_guess)
    remove = -1
    if len(remaining_options) > 1:
        if random.random() > 0.5:
            remove = remaining_options[0]
        else:
            remove = remaining_options[1]
        __host("Since they chose the correct door on the first guess, I've chosen one of the remaining doors at random to reveal", silent=silent, whisper=True)

    else:
        remove = remaining_options[0]
        __host(f"Since they picked a wrong door on their first guess, the only door for me to reveal without giving away the answer is door number {remove}, so I'll tell them it's not that one", silent=silent, whisper=True)
    
    __host(f"OK, robot. You guessed {robot_first_guess}, but I can now reveal that door number {remove} is not a winning door.", silent=silent)
    robot_second_guesses = options.copy()
    robot_second_guesses.remove(robot_first_guess)
    robot_second_guesses.remove(remove)
    robot_second_guess = robot_second_guesses[0]

    __robot(f"Alright then. I'll switch my choice over. I choose {robot_second_guess} instead", silent=silent)

    if robot_second_guess == answer:
        __host("Robot, you won this round. Congratulations!", silent=silent)
        return True
    else:
        __host("No luck this time, Robot - you lost this round", silent=silent)
        return False
    
def __game(simulation_count: int | None = None):
    silent = simulation_count is not None
    
    __host("OK! Let's get started! It's me and you vs. the robot.", silent=silent)
    win = 0
    loss = 0
    i = 0
    while(True):
        i += 1
        if simulation_count and i > simulation_count:
            break
        
        result = __play(silent=silent)
        if result:
            win += 1
        else:
            loss += 1
        
        hide_score = silent
        if silent and i % (simulation_count / 10) == 0:
            hide_score = False
        
        __show_score(win=win, loss=loss, silent=hide_score)
        
        if not simulation_count:
            __host("Press enter to play again, or type 'exit' to end the game.", silent=False)
            action = input()
            if action.casefold() == "exit":
                break

print("👋 Starting up!")

__host("Hi! Welcome to the game show game theory demonstrator! Let's get started. Do you want the game explained, or do you want to simulate games?",silent=False)
print("  1 - Walk through rounds of the game step-by-step to understand the mechanics")
print("  2 - Simulate loads of games and show the results at the end")

res = 0
while(True):
    __host("Please enter 1 or 2 to continue", silent=False)
    res = input().strip()
    if res in ("1","2"):
        break
    __host("Sorry, but I didn't understand that.", silent=False)


match res:
    case "1": 
        __game()
    case "2":
        iterations = 0
        while True:
            __host("How many rounds to do you want to play?", silent=False)
            iterations = input().strip()
            if iterations.isdigit() and int(iterations) > 0 and int(iterations) <= 10000000:
                __host(f"Great! I'll run {iterations} rounds and tell you the results at the end.", silent=False)
                break
            __host("Sorry, but I didn't understand that. Please enter a number between 1 and 10000000.", silent=False)
        __game(int(iterations))

__host("That concludes today's game. I hope you enjoyed playing!", silent=False)