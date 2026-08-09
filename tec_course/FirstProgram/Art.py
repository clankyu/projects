import math
import turtle
import random

thickness = int(input("Line thickness > "))
t = turtle.Turtle()
t.speed(0)
turtle.bgcolor("black")


for i in range(36):
    r = abs(math.cos(random.random() * math.pi))  # 0..1
    g = abs(math.cos(random.random() * math.pi))
    b = abs(math.cos(random.random() * math.pi))
    t.pensize(thickness)
    t.color(r, g, b)
    t.backward(random.randint(100, 200))
    t.left(random.randint(20, 270))

turtle.done()

