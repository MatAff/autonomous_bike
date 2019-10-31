#!/usr/bin/env python3

import curses # https://docs.python.org/3/howto/curses.html
import time
import random

class SimpleDisplay():
    def __init__(self, quitkey="q", show_fps=(20,-1), show_time=(40, -1), show_keypresses=(0, -2)):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.start_color()
        self.stdscr.nodelay(True)
        self.quitkey = quitkey

        self.running = True
        self.show_fps = show_fps
        if show_fps:
            self.frame_count = 0
            self.last_measure = 0
            self.fps_frequency = 1
        self.show_time = show_time
        if show_time:
            self.t0 = time.time()
        if show_keypresses:
            self.show_keypresses = show_keypresses

        self.components = []

    def add(self, component):
        self.components.append(component)

    def update(self, vars):
        try:
            for component in self.components:
                component.update(**vars.get(component.name, {}))
                component.print(self.stdscr)

            self.rows, self.cols = self.stdscr.getmaxyx()

            c = self.stdscr.getch()

            if c == ord(self.quitkey):
                self.running = False

            if self.show_keypresses and c > -1:
                x, y = self.show_keypresses
                if x < 0: x = self.cols + x
                if y < 0: y = self.rows + y
                self.stdscr.addstr(y, x, chr(c) + "  ")

            if self.show_time:
                x, y = self.show_time
                if x < 0: x = self.cols + x
                if y < 0: y = self.rows + y
                now = time.time()
                self.stdscr.addstr(y, x, "t = " + str(round(now - self.t0, 2)))

            if self.show_fps:
                self.frame_count += 1
                x, y = self.show_fps
                if x < 0: x = self.cols + x
                if y < 0: y = self.rows + y
                now = time.time()
                if now > self.last_measure + self.fps_frequency:
                    self.fps = self.frame_count / self.fps_frequency
                    self.last_measure = now
                    self.stdscr.addstr(y, x, "FPS: " + str(self.fps))
                    self.frame_count = 0

            self.stdscr.addstr(self.rows-1, 0, "Press " + self.quitkey +" to quit")
            self.stdscr.move(self.rows-1, self.cols-1)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.stdscr.addstr(0, 0, str(e))
        finally:
            self.stdscr.refresh()
            return self.running

    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


class DisplayComponent():
    def __init__(self, **kwargs):
        self.value = 0
        self.x = 0
        self.y = 0
        self.attribute = curses.A_NORMAL
        self.name = "".join([chr(random.randint(ord('a'), ord('z'))) for i in range(8)])

    def update(self, **kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k ,v)

    def print(self, screen):
        screen.addstr(self.y, self.x, self.format_value(), self.attribute)

    def format_value(self):
        return str(self.value)


class Text(DisplayComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k,v in kwargs.items():
            self.__setattr__(k ,v)

    def update(self, **kwargs):
        super().update(**kwargs)

    def print(self, screen):
        super().print(screen)

    def format_value(self):
        return str(self.value)


class VarNumber(DisplayComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k,v in kwargs.items():
            self.__setattr__(k ,v)

    def update(self, **kwargs):
        super().update(**kwargs)

    def print(self, screen):
        super().print(screen)

    def format_value(self):
        val = self.value
        if self.round is not None:
            val = round(val, self.round)

        val = str(val)
        if self.prefix == True:
            val = self.name + " = " + val
        elif self.prefix:
            val = self.prefix + val
        return val


class VarBar(DisplayComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 0
        self.var_min = 0
        self.var_max = 1
        self.space = " "
        self.left = "["
        self.right = "]"
        self.marker = "x"
        self.length = 20
        for k,v in kwargs.items():
            self.__setattr__(k ,v)

    def update(self, **kwargs):
        super().update(**kwargs)

    def print(self, screen):
        super().print(screen)

    def format_value(self):
        ll = len(self.left)
        lr = len(self.right)
        bs = ll
        be = self.length - lr

        s = [self.left] + [self.space] * (self.length - ll - lr) + [self.right]

        pos = round(LERP(self.value, self.var_min, self.var_max, bs, be - 1))
        pos = min_max(pos, bs, be - 1)
        s[pos] = self.marker
        return "".join(s)


def LERP(x, x1, x2, y1, y2):
	return (x - x1) * (y2 - y1) / (x2 - x1) + y1


def min_max(x, x_min, x_max):
	return max((min((x, x_max)), x_min))


if __name__ == "__main__":

    # Extend scope for cleanup
    disp = None

    try:
        # Setup
        s = 0
        t0 = time.time()

        disp = SimpleDisplay()
        disp.add(Text(value="Title", y=0, attribute=curses.A_UNDERLINE))

        disp.add(VarNumber(name="s", prefix=True, y=2, round=2))
        disp.add(VarBar(name="s", var_min=-30, var_max=30, value=s, length=31, y=3))
        disp.add(Text(value="|    " * 6 + "|", x=0, y=4))
        disp.add(Text(value="-30 -20  -10   0    10   20   30", x=0, y=5))

        # next_time = 0
        # step = 0
        # for i in range(1,9):
        #     disp.add(Text(value=" abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ .!?☺", x=0, y=8+i, attribute=curses.color_pair(i)))

        # Loop
        running = True
        while running:
            t = time.time() - t0
            ds = random.random() - 0.5 - (s / 10000)
            s += ds

            # if time.time() > next_time:
            #     step += 1
            #     for i in range(1,9):
            #         curses.init_pair(i, ((i-step)%8)+1, i)
            #     next_time = time.time() + 0.01

            running = disp.update({
                's':{"value":s}
            })
    finally:
        disp.cleanup()
