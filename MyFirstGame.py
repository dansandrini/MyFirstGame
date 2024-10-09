import os
import random
import turtle
import time

# Set the animations speed to the maximum
turtle.speed(0)
# Background color
turtle.bgcolor("black")
# Hide the default turtle
turtle.ht()
# This saves memory
turtle.setundobuffer(1)
# This speeds up drawing
turtle.tracer(0)
turtle.title("Space War")

turtle.setup(width=800, height=700)

def start_screen():
    turtle.clear()
    turtle.bgcolor("black")
    turtle.penup()
    turtle.color("white")
    turtle.goto(0, 50)
    turtle.write("Space War", align="center", font=("Arial", 24, "bold"))
    turtle.goto(0, -50)
    turtle.write("Press 'S' to Start", align="center", font=("Arial", 18, "normal"))
    turtle.hideturtle()
    turtle.listen()
    turtle.onkey(main_game, "s")
    turtle.mainloop()

def game_over():
    turtle.clear()
    turtle.bgcolor("black")
    turtle.penup()
    turtle.color("red")
    turtle.goto(0, 50)
    turtle.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
    turtle.goto(0, -50)
    turtle.write("Press 'R' to Restart or 'Q' to Quit", align="center", font=("Arial", 18, "normal"))
    turtle.hideturtle()
    turtle.listen()
    turtle.onkey(main_game, "r")
    turtle.onkey(turtle.bye, "q")
    turtle.mainloop()

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, start_x, start_y):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed = 0
        self.penup()
        self.color(color)
        self.goto(start_x, start_y)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
           (self.xcor() <= (other.xcor() + 20)) and \
           (self.ycor() >= (other.ycor() - 20)) and \
           (self.ycor() <= (other.ycor() + 20)):
            return True
        return False

class Player(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
        Sprite.__init__(self, spriteshape, color, start_x, start_y)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        if self.speed > 1:
            self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
        Sprite.__init__(self, spriteshape, color, start_x, start_y)
        self.speed = 6
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
        Sprite.__init__(self, spriteshape, color, start_x, start_y)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)

        # Boundary detection
        if self.xcor() > 250:
            self.setx(250)
            self.lt(60)

        if self.xcor() < -250:
            self.setx(-250)
            self.lt(60)

        if self.ycor() > 250:
            self.sety(250)
            self.lt(60)

        if self.ycor() < -250:
            self.sety(-250)
            self.lt(60)

class Missile(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
        Sprite.__init__(self, spriteshape, color, start_x, start_y)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "firing":
            self.fd(self.speed)

        # Border check
        if self.xcor() < -290 or self.xcor() > 290 or \
           self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
        Sprite.__init__(self, spriteshape, color, start_x, start_y)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, 1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 0

    def move(self):
        if self.frame < 15:  # Duração da explosão
            self.fd(10)
            self.frame += 1
        else:
            self.goto(-1000, 1000)  # Remove da tela

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
        self.pen.ht()  # Hide the status pen
        self.pen.speed(0)
        self.pen.color("white")

    def draw_border(self):
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
            self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s Lives: %s " % (self.score, self.lives)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

def main_game():
    turtle.clear()
    game = Game()
    game.draw_border()
    game.show_status()

    global player  # Declare player as a global variable
    player = Player("triangle", "white", 0, 0)
    missile = Missile("triangle", "yellow", 0, 0)

    enemies = [Enemy("circle", "red", random.randint(-250, 250), random.randint(-250, 250)) for _ in range(6)]
    allies = [Ally("square", "blue", random.randint(-250, 250), random.randint(-250, 250)) for _ in range(6)]
    particles = [Particle("circle", "orange", 0, 0) for _ in range(20)]

    # Keyboard bindings
    turtle.listen()
    turtle.onkey(player.turn_left, "Left")
    turtle.onkey(player.turn_right, "Right")
    turtle.onkey(player.accelerate, "Up")
    turtle.onkey(player.decelerate, "Down")
    turtle.onkey(missile.fire, "space")

    while game.lives > 0:
        turtle.update()
        time.sleep(0.02)

        player.move()
        missile.move()

        for enemy in enemies:
            enemy.move()
            if player.is_collision(enemy):
                game.lives -= 1
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                enemy.goto(x, y)
                game.score -= 100
                game.show_status()

            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

        for ally in allies:
            ally.move()
            if missile.is_collision(ally):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                ally.goto(x, y)
                missile.status = "ready"
                game.score -= 50
                game.show_status()

            if player.is_collision(ally):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                ally.goto(x, y)
                game.score += 50
                game.show_status()

        for particle in particles:
            particle.move()

    game_over()

# Tela inicial
start_screen()
