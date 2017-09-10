# sirtet 1.0 - a tetris clone typish game
# help    : if there's a clear bug please send a patch to github. i'll give credits to you. 
#           new features like "next block" are not needed for this kind of a niche game.
#           i developed this game mainly to test my new laptop.
# license : GNU General Public License v3.0
# author  : mystikkogames
# email   : mystikkogames@protonmail.com
# date    : 10.9.2017
# credits : https://gist.github.com/sanchitgangwar/2158089

import curses, random, sys
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN 

NAME = 'sirtet 1.0'
WIDTH = 15
HEIGHT = 22
BLOCKS = [[[0,0],[0,1],[0,2],[0,-1]], [[0,0],[1,0],[2,0],[2,1]], [[0,0],[1,0],[2,0],[2,-1]], [[0,0],[0,1],[1,0],[1,1]], [[0,0],[1,0],[-1,0],[0,1]], [[0,0],[1,0],[1,1], [2,1]], [[0,0],[1,0],[1,-1],[2,-1]]]

class Sirtet:
    score = 0
    
    def __init__(self):
        self.print_id()

    def play(self):
        self.init_me()
        self.game_on()
        curses.endwin()
        self.print_game_over()

    def init_me(self):
        curses.initscr()
        self.new_block()
        self.blocks = []
        self.win = curses.newwin(HEIGHT, WIDTH, 0, 0)
        self.win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.win.border(0)
        self.win.nodelay(1)
        self.key = 0 
        self.prev_key = 0

    def print_help(self):
        print 'help'
        print '<-  : left'
        print '->  : right'
        print 'v   : drop'
        print '^   : rotate'
        print 'esc : exit'
        
    def print_id(self):
        print NAME
        print 'by mystikkogames'
        print '---'

    def print_game_over(self):
        print 'game over'
        print 'score : %i' % self.score

    def remove_full_rows(self):
        for y in range(1, HEIGHT - 1):
            all_in, p = 1, []
            for x in range(1, WIDTH - 1):
                t = [x, y]
                p.append(t)
                if not t in self.blocks:
                    all_in = 0
            if all_in:
                for x in range(1, WIDTH - 1):
                    self.blocks.remove(p.pop())
                for b in self.blocks:
                    if b[1] < y:
                        b[1] += 1
                s = self.remove_full_rows()
                return 2 + 2 * s
        return 0

    def is_block_inside(self):
        for i in range(4):
            if not self.is_inside(self.cur_block[i]):
                return 0
        return 1

    def is_inside(self, b):
        if b[0] < 1 or b[0] > WIDTH - 2 or b[1] + 2 < 0 or b[1] > HEIGHT - 2:
            return 0
        return 1

    def is_too_high(self):
        for b in self.blocks:
            if b[1] < 4:
                return 1
        return 0

    def draw_block(self, c = '#'):
        for i in range(4):
            if self.is_inside(self.cur_block[i]):
                self.win.addch(self.cur_block[i][1], self.cur_block[i][0], c)

    # I'm using [-y, x] formula for rotation
    def rotate_block(self):
        a, b = self.cur_block[0][0], self.cur_block[0][1]
        for i in range(4):
            x, y = self.cur_block[i][0], self.cur_block[i][1]
            dx, dy = x - a, y - b
            self.cur_block[i][0], self.cur_block[i][1] = a + -dy, b + dx

    def move_x_block(self, dx = 1):
        for i in range(4):
            self.cur_block[i][0] += dx

    def move_block_y(self, dy = 1):
        for i in range(4):
            self.cur_block[i][1] += dy

    def draw_blocks(self, c = '#'):
        for b in self.blocks:
            if self.is_inside(b):
                self.win.addch(b[1], b[0], c)

    def new_block(self):
        self.cur_block = [[0,0] for i in range(4)]
        j = random.randint(0, len(BLOCKS) - 1)
        for i in range(4):
            self.cur_block[i][0] = BLOCKS[j][i][0] + int(WIDTH / 2)
            self.cur_block[i][1] = BLOCKS[j][i][1] + 1   

    def clone_block(self):
        b = [[0,0],[0,0],[0,0],[0,0]]
        for i in range(4):
            b[i][0], b[i][1] = self.cur_block[i][0], self.cur_block[i][1]
        return b

    def copy_block(self, b):
        for i in range(4):
            self.cur_block[i][0], self.cur_block[i][1] = b[i][0], b[i][1]

    def hit(self):
        for i in range(4):  
            if self.cur_block[i] in self.blocks:
                return 1
        return 0

    def is_out_y(self):
        for i in range(4):  
            if self.cur_block[i][1] + 2 > HEIGHT:
                return 1
        return 0

    def clean_screen(self):
        for y in range(1, HEIGHT - 1):
            for x in range(1, WIDTH - 1):
                self.win.addch(y, x, '.')  

    def input(self):
        event = self.win.getch()
        self.key = 0
        if event != -1:
            if event != self.prev_key:
                self.key = event
        self.prev_key = self.key
        self.clean_screen()
        if self.key == KEY_UP:
            bl = self.clone_block()
            self.rotate_block()
            self.move_block_y(-1)
            if self.hit() or not self.is_block_inside():                    
                self.copy_block(bl)
        elif self.key == KEY_LEFT:
            self.move_x_block(-1)
            if self.hit() or not self.is_block_inside():
                self.move_x_block(1)
            self.move_block_y(-1)
        elif self.key == KEY_RIGHT:
            self.move_x_block()
            if self.hit() or not self.is_block_inside():
                self.move_x_block(-1)
            self.move_block_y(-1)

    def game_on(self):
        while self.key != 27:
            self.win.border(0)
            self.win.addstr(0, 2, 'sirtet (%i)' % self.score) 
            self.win.timeout(200 - min(100, int(self.score / 5)))   
            self.input()
            self.move_block_y()
            if self.hit() or self.is_out_y():
                self.move_block_y(-1)
                self.blocks += self.cur_block
                self.new_block()
            self.draw_block()
            self.draw_blocks()
            if self.is_too_high():
                break
            self.score += self.remove_full_rows()

def main():    
    s = Sirtet()
    if len(sys.argv) > 1:
        s.print_help()
    else:
        s.play()

if __name__ == '__main__':
    main()
