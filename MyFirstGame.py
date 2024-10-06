import os
import random

#Import the Turtle module
import turtle
turtle.fd(0)
#Set the animations speed to the maximum
turtle.speed(0)
#Background color
turtle.bgcolor("black")
#Hide the default turtle
turtle.ht()
#This saves memory
turtle.setundobuffer(1)
#This speeds up drawing
turtle.tracer(1)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, start_x, start_y):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(start_x, start_y)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #bondary detection
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
        else:
            return False    


class Player(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
        Sprite.__init__(self, spriteshape, color, start_x, start_y)        
        self.speed = 4
        self.lives = 3

    def turn_left(self):
        self.lt(45)    

    def turn_right(self):
        self.rt(45) 

    def accelerate(self):
        self.speed += 1  

    def decelerate(self):
        self.speed -= 1   


class Enemy(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
       Sprite.__init__(self, spriteshape, color, start_x, start_y) 
       self.speed = 6
       self.setheading(random.randint(0, 360))


class Missile(Sprite):
    def __init__(self, spriteshape, color, start_x, start_y):
        Sprite.__init__(self, spriteshape, color, start_x, start_y)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        # self.goto(-1000, 1000)
        
    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):

        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed)  

    #Border check
        if self.xcor() < -290 or self.xcor() > 290 or \
        self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

    

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()    


#create game object
game = Game()

#Draw the border
game.draw_border()

#create my sprites        
player = Player("triangle", "white", 0, 0)
enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)


#Keyboard bindings
turtle.listen()
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")



#Main game loop
while True:
    player.move()
    enemy.move()
    missile.move()

    #check for collision
    if player.is_collision(enemy):
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        enemy.goto(x, y)
       
    #check for a collision between the enemy and the missile   
    if missile.is_collision(enemy):
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        enemy.goto(x, y)
        missile.status = "ready"

delay = input("Press enter to finish. >")

