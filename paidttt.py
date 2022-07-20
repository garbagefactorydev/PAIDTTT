import turtle
from random import randrange, choice
from functools import partial
from time import sleep


class Game:
    def __init__(self, display_object):
        self.display = display_object
        self.players = ("human", "ai")
        self.board = {value: str(count) for count, value in enumerate(self.display.empty_fields)}

        self.player_positions = []
        self.ai_positions = []
        self.game_over = False

    def start(self):
        first_player = self.choose_first_player()
        if first_player == "ai":
            self.ai_turn()

    def choose_first_player(self):
        return choice(self.players)

    def player_turn(self, position):
        player_move = self.board[position]
        self.player_positions.append(player_move)
        self.check_winner('human')
        self.ai_turn()

    def ai_turn(self):
        if not self.game_over:
            ai_move = self.board[self.display.jump(self.display.random_free_position())]
            self.display.draw_o()
            self.ai_positions.append(ai_move)
            self.check_winner('ai')

    def check_winner(self, player):
        win_combinations = ('012', '345', '678',
                            '036', '147', '258',
                            '048', '246')
        positions = self.player_positions if player == 'human' else self.ai_positions
        for win_combination in win_combinations:
            if all(position in positions for position in list(win_combination)):
                decoded_win_combination = self.decode_win_combination(win_combination)
                self.declare_winner(player, decoded_win_combination)

    def declare_winner(self, winner, combination):
        self.game_over = True
        self.display.draw_cross_out(combination)
        self.display.game_over_screen(winner)

    def decode_win_combination(self, combination):
        decoder = {key: value for value, key in self.board.items()}
        cross_start = decoder[combination[0]]
        cross_stop = decoder[combination[2]]
        return cross_start, cross_stop


class Drawing:
    X = """
self.pen.color("yellow")
p.goto(x-size, y+size)
p.pendown()
p.goto(x+size, y-size)
p.penup()
p.goto(x+size, y+size)
p.pendown()
p.goto(x-size, y-size)
"""
    O = """
self.pen.color("blue")
p.goto(x, y-size)
p.pendown()
p.circle(size)
"""
    BOARD = """
self.pen.color("black")
p.goto(x-240, y-80)
p.pendown()
p.goto(x+240, y-80)
p.penup()

p.goto(x-240, y+80)
p.pendown()
p.goto(x+240, y+80)
p.penup()

p.goto(x-80, y+240)
p.pendown()
p.goto(x-80, y-240)
p.penup()

p.goto(x+80, y+240)
p.pendown()
p.goto(x+80, y-240)
p.penup()
"""
    CROSS = """
self.pen.color("red")
p.goto(x)
p.pendown()
p.goto(y)
p.penup()
"""
    GAME_OVER = """
self.pen.color("yellow")
winner = self.kwargs["game_over"]
p.hideturtle()
p.color("yellow")
p.write("Game Over", align='center', font=('Arial', 60, 'bold'))
p.penup()
p.goto(0, -40)
p.pendown()
p.write(f"{winner.upper()} WON", align='center', font=('Arial', 30, 'bold'))
p.penup()
p.goto(0, -80)
p.pendown()
p.write(f"Press [R]estart or [C]lose", align='center', font=('Arial', 20, 'bold'))
"""
    DRAWINGS = {
        "x": X,
        "o": O,
        "board": BOARD,
        "cross": CROSS,
        "game_over": GAME_OVER,
    }

    def __init__(self, position, symbol="o", **kwargs):
        self.kwargs = kwargs
        self.position = position
        self.symbol = symbol
        self.pen = turtle.Turtle(visible=False)
        self.draw()

    def draw(self):
        x, y = self.position
        p = self.pen
        size = 40
        p.pensize(10)
        p.penup()

        exec(Drawing.DRAWINGS[self.symbol])


class Display:
    def __init__(self):
        self.screen = None
        self.cursor = None
        self.cursor_position = None

        self.navigation = ["Up", "Down", "Left", "Right"]
        self.empty_fields = None

        self.game = None

    def initialize_graphics(self):
        self.screen = turtle.Screen()
        self.cursor = turtle.Turtle(visible=False)
        self.cursor.shape("circle")

        self.get_cursor_position()
        turtle.bgcolor("green")

        self.empty_fields = [
            (-160, 160),    (0, 160),   (160, 160),
            (-160, 0),      (0, 0),     (160, 0),
            (-160, -160),   (0, -160),  (160, -160)
        ]

    def initialize_game(self):
        turtle.clearscreen()
        self.initialize_graphics()
        self.game = Game(self)

    def get_cursor_position(self):
        self.cursor_position = tuple(map(int, self.cursor.position()))

    def draw_board(self):
        Drawing(self.cursor_position, "board")

    def draw_x(self):
        cp = self.cursor_position
        if cp in self.empty_fields:
            Drawing(cp, "x")
            self.empty_fields.remove(cp)
            self.game.player_turn(cp)

    def draw_o(self):
        Drawing(self.cursor_position, "o")
        self.empty_fields.remove(self.cursor_position)

    @staticmethod
    def draw_cross_out(pattern):
        Drawing(pattern, "cross")
        sleep(3)

    def draw_game_over(self, winner):
        Drawing(self.cursor_position, "game_over", game_over=winner)

    def random_free_position(self):
        if ef := len(self.empty_fields):
            random_index = randrange(0, ef)
            return self.empty_fields[random_index]

    def jump(self, position):
        p = self.cursor
        p.penup()
        p.goto(position)
        self.get_cursor_position()
        return position

    def move(self, key):
        p = self.cursor
        p.penup()
        x, y = self.cursor_position
        shift = None
        if key == "Up": shift = ((x, y+160), (x, y+320))
        if key == "Down": shift = ((x, y-160), (x, y-320))
        if key == "Left": shift = ((x-160, y), (x-320, y))
        if key == "Right": shift = ((x+160, y), (x+320, y))

        if shift[0] in self.empty_fields:
            p.goto(shift[0])
        elif shift[1] in self.empty_fields:
            p.goto(shift[1])
        elif len(self.empty_fields) <= 3:
            p.goto(self.random_free_position())
        self.get_cursor_position()

    def game_screen(self):
        self.initialize_game()
        self.cursor.showturtle()
        self.draw_board()
        s = self.screen

        s.onkey(self.end, "c")
        for key in self.navigation:
            s.onkey(partial(self.move, key), key=key)
        s.onkey(self.draw_x, "space")
        s.onkey(self.draw_o, "o")
        s.onkey(self.game_over_screen, "g")

        self.game.start()

        s.listen()
        s.mainloop()

    def game_over_screen(self, winner):
        self.initialize_game()
        self.draw_game_over(winner)
        s = self.screen

        s.onkey(self.end, "c")
        s.onkey(self.game_screen, "r")

        s.listen()

    def end(self):
        self.screen.bye()


if __name__ == "__main__":
    display = Display()
    display.game_screen()
