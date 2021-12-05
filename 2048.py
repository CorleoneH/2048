# coding=utf-8

import sys
import os
import platform
import random
import itertools

class Game:
    grid = []
    controls = ['w', 'a', 's', 'd']
    def __init__(self, win_goal):
        self.win_goal = win_goal
        self.cur_goal = 0

    @staticmethod
    def trim(seqs, direction=0):
        return ([0, 0, 0, 0] + [n for n in seqs if n])[-4:] if direction else ([n for n in seqs if n] + [0, 0, 0, 0])[:4]

    @staticmethod
    def sum_seqs(seqs, direction=0):
        if seqs[1] and seqs[2] and seqs[1] == seqs[2]:
            return Game.trim([seqs[0], seqs[1]*2, 0, seqs[3]], direction=direction)
        if seqs[0] and seqs[1] and seqs[0] == seqs[1]:
            seqs[0], seqs[1] = seqs[0]*2, 0
        if seqs[2] and seqs[3] and seqs[2] == seqs[3]:
            seqs[2], seqs[3] = seqs[2]*2, 0
        return Game.trim(seqs, direction=direction)
            
    @staticmethod
    def up(grid):
        for col in [0, 1, 2, 3]:
            for _idx, n in enumerate(Game.sum_seqs(Game.trim([row[col] for row in grid]))):
                grid[_idx][col] = n
        return grid    

    @staticmethod    
    def down(grid):
        for col in [0, 1, 2, 3]:
            for _idx, n in enumerate(Game.sum_seqs(Game.trim([row[col] for row in grid], direction=1), direction=1)):
                grid[_idx][col] = n
        return grid  

    @staticmethod
    def left(grid):
        return [Game.sum_seqs(Game.trim(row)) for row in grid]
    
    @staticmethod
    def right(grid):
        return [Game.sum_seqs(Game.trim(row, direction=1), direction=1) for row in grid]
    
    def set_win_goal(self):
        self.clean_screen()
        while True:
            win_goal = input("Input your win goal[Enter to default:32]: ")
            # Press enter to start the game directly with default
            if len(win_goal) == 0:
                break
            # Handing int exception if no valid number
            try:
                self.win_goal = int(win_goal)
                break
            except ValueError:
                print("Oops! That was no valid number. Try again...")

    def get_cur_goal(self):
        self.cur_goal = max(max(row) for row in self.grid)

    def rnd_field(self):
        number = random.choice([4, 2, 4, 2, 4, 2, 4, 2, 4, 2])
        x, y = random.choice([(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if self.grid[x][y] == 0])
        self.grid[x][y] = number

    # clean screen for display in same place
    def clean_screen(self):
        if "windows" in platform.system().lower():
            os.system("cls")
        elif "linux" in platform.system().lower():
            os.system("clear")

    def print_screen(self):
        self.clean_screen()
        
        # get CURRENT GOAL before displaying
        self.get_cur_goal()
        
        # print game info, including WIN GOAL and CURRENT GOAL
        print("WIN GOAL: {}\t\tCURRENT GOAL: {}\n\n".format(self.win_goal, self.cur_goal))

        # -------------- print game main zone [start]---------------------------
        print("-" * 21)

        for row in self.grid:
            print("|{}|".format('|'.join([str(col or ' ').center(4) for col in row])))
            print("-" * 21)
        # --------------- print game main zone [end]----------------------------

    def logic(self, control):
        grid = {'w' : Game.up, 's' : Game.down, 'a' : Game.left, 'd' : Game.right}[control]([[c for c in r] for r in self.grid])
        if grid != self.grid:
            del self.grid[:]
            self.grid.extend(grid)
            if [n for n in itertools.chain(*grid) if n >= self.win_goal]:
                return 1, "WIN!!!"
            self.rnd_field()
            self.print_screen()
        else:
            if not [1 for g in [f(grid) for f in [Game.up, Game.down, Game.left, Game.right]] if g != self.grid]:
                return -1, "Game Over!!!"

        return 0, ''    # return 0 if continue; return 1 if "Win", return -1 if "Game Over"

    def main_loop(self):
        del self.grid[:]
        self.grid.extend([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        
        # set WIN GOAL in every beginning of game
        self.set_win_goal()

        self.rnd_field()
        self.rnd_field()

        while True:
            self.print_screen()
            control = input("input w/a/s/d:")
            if control in self.controls:
                status, info = self.logic(control)
                # win or lose
                if status:
                    self. print_screen()
                    print(info)
                    if input("Start another game?[Y/y]").lower() == 'y':
                        break
                    else:
                        sys.exit(0)
            
        self.main_loop()


if __name__ == "__main__":
    Game(32).main_loop()
