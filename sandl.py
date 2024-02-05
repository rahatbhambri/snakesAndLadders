import random, sys, json
from typing import List, Dict
from queue import Queue

class Snake:
    def __init__(self, str_, end):
        self.str = str_
        self.end = end

class Ladder:
    def __init__(self, str_, end):
        self.str = str_
        self.end = end

class Dice:
    def __init__(self, num, size, movement_strategy='SUM'):
        self.num = num
        self.size = size
        self.movement_strategy = movement_strategy
        self.rand = random.Random()

    def get_moves(self):
        rolls = [self.rand.randint(1, self.size) for _ in range(self.num)]

        if self.movement_strategy == 'SUM':
            steps = sum(rolls)
        elif self.movement_strategy == 'MAX':
            steps = max(rolls)
        elif self.movement_strategy == 'MIN':
            steps = min(rolls)
        else:
            raise ValueError("Invalid movement strategy. Use SUM, MAX, or MIN.")

        return steps
    

class Player:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.blocked = 0 

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def decrement_blocked(self):
        self.blocked -= 1
        if self.blocked < 0:
            self.blocked = 0

    def set_blocked(self, turns):
        self.blocked = turns

    def is_blocked(self):
        return self.blocked > 0


class SnakeAndLadderGame:
    def __init__(self, dice, snake, ladder, n, m, special, overr):
        self.win_pos = n * m
        self.dice = dice
        #print(snake, "here")
        self.snake_map = {s.str: s.end for s in snake}
        self.ladder_map = {l.str: l.end for l in ladder}
        self.players = Queue() 
        self.specials = special 
        self.overr = overr

        if self.specials:
            self.add_splObjects()
    
    def add_splObjects(self): 
        croc_h = random.randint(5, 99)
        croc_t = croc_h - 5
        self.snake_map[croc_h] = croc_t 

        for _ in range(5) :
            mine_pos = random.randint(5, 99) 
            self.snake_map[mine_pos] = -1

    def add_player(self, player):
        self.players.put(player)

    def move(self, player):
        if player.is_blocked():
            player.decrement_blocked()
            print(f"{player.name} encountered a Mine and is blocked for {player.blocked} turns")
        else:
            steps = self.dice.get_moves() if self.overr != 1 else int(input(f"Enter dice roll for {player.name} "))
            n_pos = player.get_pos() + steps

            print(f"{player.name} rolled a {steps} and moved from {player.get_pos()} to {min(self.win_pos, n_pos)}")

            if n_pos >= self.win_pos:
                print(f"{player.name} -> winner")
                return False
            else:
                if n_pos in self.snake_map:
                    if self.snake_map[n_pos] != -1:
                        if self.snake_map[n_pos] == n_pos - 5:
                            print(f"{player.name} encountered a Crocodile and moved 5 steps back")
                            player.set_pos(self.snake_map[n_pos])
                        else:
                            print(f"{player.name} encountered a snake and moved from {n_pos} to {self.snake_map[n_pos]}")
                            player.set_pos(self.snake_map[n_pos])
                    else:
                        player.set_blocked(2)
                        print(f"{player.name} encountered a Mine and is blocked for {player.blocked} turns")
                elif n_pos in self.ladder_map:
                    print(f"{player.name} climbed a ladder and moved from {n_pos} to {self.ladder_map[n_pos]}")
                    player.set_pos(self.ladder_map[n_pos])
                    if player.get_pos() == self.win_pos:
                        print(f"{player.name} -> winner")
                        return False
                else:
                    player.set_pos(n_pos)

        return True


    def start(self):
        while True:
            if self.players.qsize() <= 1:
                print("Required more than two people to play")
                return

            player = self.players.get()

            if self.move(player):
                self.players.put(player)
            else:
                return
            
def main():
    # An override to manually enter the board configurations like dice strategy, number of snakes and number of ladders etc. 
    # Pass 1 to args to begin override else pass 0 to read from conf.json

    overr = int(sys.argv[1:][0])
    if overr != 1:
        try:
            with open('conf.json', 'r') as json_file:
                config = json.load(json_file)

            number_of_players = config.get('number_of_players', 2)
            board_size = config.get('board_size', 10)
            number_of_snakes = config.get('number_of_snakes', 3)
            number_of_ladders = config.get('number_of_ladders', 2)
            number_of_dice = config.get('number_of_dice', 1) 
            dice_strategy = config.get('dice_strategy', 'MIN')

        except FileNotFoundError:
            print(f"Error: Configuration file not found.")
            return

    t = int(input("Enter the number of test cases: "))
    
    for _ in range(t):

        if overr == 1:
            print("Enter number of snakes")
        s = int(input()) if overr == 1 else number_of_snakes
        print("Enter snake configurations")
        snakes = [list(map(int, input().split())) for _ in range(s)]

        l1 = []
        for s in snakes:
            l1.append(Snake(s[0], s[1]))
        snakes = l1

        if overr == 1:
            print("Enter number of ladders")
        l = int(input()) if overr == 1 else number_of_ladders
        print("Enter ladder configurations")
        ladders = [list(map(int, input().split())) for _ in range(l)]

        l2 = []
        for l in ladders:
            l2.append(Ladder(l[0], l[1]))
        ladders = l2

        if overr == 1:
            print("Enter number of players")
        n = int(input()) if overr == 1 else number_of_players
        print("Enter player names")
        players = [input().split() for _ in range(n)]
        players = [Player(name, int(pos)) for name, pos in players]

       
        print("Special Objects? y/N")
        ip = str(input())
        spl = False
        if ip == "y":
            spl = True
        

    num_dices = number_of_dice if overr != 1 else 2
    boardrows = board_size if overr != 1 else 10
    boardcols = board_size if overr != 1 else 10
    dice_strat = dice_strategy if overr != 1 else "MIN"

    overr = overr if overr in [0, 1] else 0

    snake_and_ladder_game = SnakeAndLadderGame(Dice(num_dices, 6, dice_strat), snakes, ladders, boardrows, boardcols, spl, overr)

    for player in players:
        snake_and_ladder_game.add_player(player)

    snake_and_ladder_game.start()
        

if __name__ == "__main__":
    main()

