import curses
from curses import wrapper
import time
import random
import winsound

fr = open("highscore.txt", "r")
highscore = int(fr.read())

WIN_WIDTH = 40
WIN_HEIGHT = 40

ROWS = []
COLMS =[]

for i in range(0, WIN_WIDTH+1):
    ROWS.append(i)

for i in range(0, WIN_HEIGHT+1):
    COLMS.append(i)



def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.curs_set(0)

    position_s = {"x": 1, "y": 1}
    position_a = {"x": random.randrange(0, WIN_WIDTH), "y": random.randrange(0, WIN_HEIGHT)}

    size = 5
    score = 0
    rev = 0
    l = 0

    run = False
    game_over = False
    start_screen = True

    direction = "right"

    snake = []
    d = ["right", "left", "up", "down"]
       
    stdscr.clear()

    while start_screen:
        try:
            l += 1

            if l%2 == 0:
                stdscr.addstr(20, 16, "SNAKE!", curses.A_REVERSE)
                stdscr.addstr(23, 11, "press 'p' to play", curses.A_REVERSE)
                winsound.Beep(600, 600)
            else:  
                stdscr.addstr(20, 16, "SNAKE!")
                stdscr.addstr(23, 11, "press 'p' to play")
                winsound.Beep(400, 600)

            stdscr.nodelay(1)
            c = stdscr.getch()
            if c == 112:
                raise KeyboardInterrupt
            else:
                curses.flushinp()

        except KeyboardInterrupt:
            start_screen = False
            run = True
            stdscr.clear()
            break

    stdscr.addstr(position_a["y"], position_a["x"], " ", curses.color_pair(1))

    while run: 
        try:            
            for i in snake:
                if i == position_s:
                    for z in snake:
                        stdscr.addstr(z["y"], z["x"], " ")

                    stdscr.addstr(position_a["y"], position_a["x"], " ")
                    game_over = True

                    raise KeyboardInterrupt
                else:
                    pass
            #direction = random.choice(d)
            snake.append(position_s.copy())

            stdscr.addstr(position_s["y"], position_s["x"], " ", curses.color_pair(1))
            stdscr.addstr(1, 45, f"SCORE: {score}")
            stdscr.addstr(4, 45, f"SIZE: {size}")
            stdscr.addstr(7, 45, f"HIGHSCORE: {highscore}")

            for i in range(0, 43):
                stdscr.addstr(i, 0, " ", curses.A_REVERSE)
                stdscr.addstr(i, 42, " ", curses.A_REVERSE)
                stdscr.addstr(0, i, " ", curses.A_REVERSE)
                stdscr.addstr(42, i, " ", curses.A_REVERSE)

            if position_s["x"] == position_a["x"] and position_s["y"] == position_a["y"]:
                position_a = {"x": random.randrange(1, WIN_WIDTH-1), "y": random.randrange(1, WIN_HEIGHT-1)}
                stdscr.addstr(position_a["y"], position_a["x"], " ", curses.color_pair(1))
                size += 1
                score += 50
                winsound.Beep(400, 100)

            if direction == "right":
                if position_s["x"] > WIN_WIDTH:
                    position_s["x"] = 1
                else:
                    position_s["x"] += 1
            elif direction == "left":
                if position_s["x"] <= 1:
                    position_s["x"] = WIN_WIDTH+1
                else:
                    position_s["x"] -= 1
            elif direction == "up":
                if position_s["y"] <= 1:
                    position_s["y"] = WIN_HEIGHT+1
                else:
                    position_s["y"] -= 1
            elif direction == "down":
                if position_s["y"] > WIN_HEIGHT:
                    position_s["y"] = 1
                else:    
                    position_s["y"] += 1
                       
            time.sleep(0.05)              

            if len(snake) > size:
                stdscr.addstr(snake[0]["y"], snake[0]["x"], " ")
                snake.pop(0)


           
            stdscr.refresh()            
            
            stdscr.nodelay(1)
            c = stdscr.getch()
            if c == 3:
                raise KeyboardInterrupt
            elif c == 100:
                if direction == "left":
                    pass
                else:
                    direction = "right"
            elif c == 97:
                if direction == "right":
                    pass
                else:
                    direction = "left"
            elif c == 119:
                if direction == "down":
                    pass
                else: 
                    direction = "up"
            elif c == 115:
                if direction == "up":
                    pass
                else:
                    direction = "down"
            else:
                curses.flushinp()

        except KeyboardInterrupt:
            if score > highscore:
                fw = open("highscore.txt", "w")
                fw.write(str(score))    
                fw.close()
            else:
                pass 
            
            run = False
            break
        
    while game_over:
        try:
            rev += 1

            if rev%2 == 0:
                winsound.Beep(300, 600)
                stdscr.addstr(20, 16, "GAME OVER!", curses.A_REVERSE)
            else:
                winsound.Beep(100, 600)
                stdscr.addstr(20, 16, "GAME OVER!")          

            stdscr.nodelay(1)
            c = stdscr.getch()
            if c == 3:
                raise KeyboardInterrupt
            else:
                curses.flushinp()

        except KeyboardInterrupt:
            game_over = False
            break

    fr.close()

wrapper(main)