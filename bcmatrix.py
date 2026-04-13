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
    curses.init_pair(1, curses.COLOR_WHITE,   -1)  # head
    curses.init_pair(2, curses.COLOR_GREEN,   -1)  # bright
    curses.init_pair(3, curses.COLOR_GREEN,   -1)  # mid (dim applied)
    curses.init_pair(4, curses.COLOR_BLACK,   -1)  # dim (bold=dark green trick)

    height, width = stdscr.getmaxyx()
    cols = width

    drops  = [random.randint(-height, 0) for _ in range(cols)]
    trails = [random.randint(8, 20)       for _ in range(cols)]
    chars  = [
        [random.choice(CYRILLIC) for _ in range(height + 22)]
        for _ in range(cols)
    ]

    speed  = 0.05   # seconds per frame
    paused = False

    HELP = " [q]quit  [p]pause  [+/-]speed  [r]reset "

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = not paused
        elif key == ord('+') or key == ord('='):
            speed = max(0.01, speed - 0.01)
        elif key == ord('-'):
            speed = min(0.2, speed + 0.01)
        elif key == ord('r'):
            drops  = [random.randint(-height, 0) for _ in range(cols)]
            trails = [random.randint(8, 20)       for _ in range(cols)]

        if paused:
            try:
                stdscr.addstr(0, 0, " ПАУЗА — натисни [p] за продължаване ",
                              curses.color_pair(1) | curses.A_BOLD)
            except curses.error:
                pass
            time.sleep(0.1)
            continue

        new_h, new_w = stdscr.getmaxyx()
        if new_h != height or new_w != width:
            height, width = new_h, new_w
            cols   = width
            drops  = [random.randint(-height, 0) for _ in range(cols)]
            trails = [random.randint(8, 20)       for _ in range(cols)]
            chars  = [
                [random.choice(CYRILLIC) for _ in range(height + 22)]
                for _ in range(cols)
            ]
            stdscr.clear()

        for i in range(cols):
            head = drops[i]
            tail = head - trails[i]

            for row in range(height):
                if row >= height - 1:
                    continue
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
                    stdscr.addch(row, i, ch, attr)
                except curses.error:
                    pass

            # erase the cell just behind the tail
            erase_row = tail - 1
            if 0 <= erase_row < height - 1:
                try:
                    stdscr.addch(erase_row, i, ' ')
                except curses.error:
                    pass

            # randomly mutate a char in the trail
            if random.random() < 0.1:
                r = random.randint(0, len(chars[i]) - 1)
                chars[i][r] = random.choice(CYRILLIC)

            drops[i] += 1
            if drops[i] - trails[i] > height:
                drops[i]  = random.randint(-10, 0)
                trails[i] = random.randint(8, 20)

        # help bar at the bottom
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
