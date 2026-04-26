import curses
import random
import time

CYRILLIC = list('АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯабвгдежзийклмнопрстуфхцчшщъьюя')

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(50)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_BLACK, -1)

    height, width = stdscr.getmaxyx()

    drops  = [random.randint(-height, 0) for _ in range(width)]
    trails = [random.randint(8, 20)       for _ in range(width)]
    chars  = [
        [random.choice(CYRILLIC) for _ in range(height + 22)]
        for _ in range(width)
    ]

    speed  = 0.05
    paused = False
    HELP   = " [q]quit  [p]pause  [+/-]speed "

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = not paused
        elif key in (ord('+'), ord('=')):
            speed = max(0.01, speed - 0.01)
        elif key == ord('-'):
            speed = min(0.2,  speed + 0.01)
        elif key == ord('r'):
            drops  = [random.randint(-height, 0) for _ in range(width)]
            trails = [random.randint(8, 20)       for _ in range(width)]

        if paused:
            try:
                stdscr.addstr(0, 0, " ПАУЗА — натисни [p] ",
                              curses.color_pair(1) | curses.A_BOLD)
            except curses.error:
                pass
            time.sleep(0.1)
            continue

        new_h, new_w = stdscr.getmaxyx()
        if new_h != height or new_w != width:
            height, width = new_h, new_w
            drops  = [random.randint(-height, 0) for _ in range(width)]
            trails = [random.randint(8, 20)       for _ in range(width)]
            chars  = [
                [random.choice(CYRILLIC) for _ in range(height + 22)]
                for _ in range(width)
            ]
            stdscr.clear()

        for i in range(width):
            head = drops[i]
            tail = head - trails[i]

            for row in range(height - 1):
                dist = head - row
                ch = chars[i][row % len(chars[i])]

                if row == head:
                    attr = curses.color_pair(1) | curses.A_BOLD
                elif 0 < dist <= 3:
                    attr = curses.color_pair(2) | curses.A_BOLD
                elif 3 < dist <= trails[i]:
                    attr = curses.color_pair(3)
                elif row == tail - 1:
                    attr = curses.color_pair(4) | curses.A_BOLD
                else:
                    continue

                try:
                    stdscr.addstr(row, i, ch, attr)
                except curses.error:
                    pass

            erase_row = tail - 1
            if 0 <= erase_row < height - 1:
                try:
                    stdscr.addstr(erase_row, i, ' ')
                except curses.error:
                    pass

            if random.random() < 0.1:
                r = random.randint(0, len(chars[i]) - 1)
                chars[i][r] = random.choice(CYRILLIC)

            drops[i] += 1
            if drops[i] - trails[i] > height:
                drops[i]  = random.randint(-10, 0)
                trails[i] = random.randint(8, 20)

        try:
            stdscr.addstr(height - 1, 0,
                          HELP + ' ' * (width - len(HELP) - 1),
                          curses.color_pair(2))
        except curses.error:
            pass

        stdscr.refresh()
        time.sleep(speed)

if __name__ == '__main__':
    curses.wrapper(main)
