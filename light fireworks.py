import turtle
import random
import math
import time
import pygame
from pygame import mixer

# 初始化pygame混音器
pygame.mixer.init()

# 加载音乐（请确保音乐文件路径正确）
try:
    pygame.mixer.music.load("C://Users//ljsky//Desktop//Mariah Carey - All I Want For Christmas Is You.mp3")  # 把这里改成你的音乐文件路径
    pygame.mixer.music.set_volume(0.5)  # 设置音量，0.0 到 1.0
    pygame.mixer.music.play(-1)  # -1表示循环播放
except:
    print("音乐文件加载失败，请检查文件路径是否正确")

# 设置窗口
screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("圣诞烟花")
screen.tracer(0)

# 创建文字对象（初始时不显示）
text = turtle.Turtle()
text.hideturtle()
text.penup()
text.color("white")
text.goto(0, -220)

# 记录开始时间
start_time = time.time()
text_shown = False


# [之前的 Particle 和 Firework 类保持不变]
class Particle:
    def __init__(self, x, y, is_core=False):
        self.x = x
        self.y = y
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.size = random.randint(3, 5) if not is_core else random.randint(4, 6)

        if is_core:
            self.color = random.choice(["gold", "orange", "dark orange"])
        else:
            self.color = random.choice(["hot pink", "deep pink", "red", "royal blue",
                                        "cyan", "medium slate blue", "magenta", "spring green"])

        self.life = 150 if is_core else 100
        self.is_core = is_core

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.shapesize(0.1)
        self.t.color(self.color)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.is_core:
            self.dx *= 0.98
            self.dy *= 0.98
        else:
            self.dy -= 0.15

        self.life -= 2

        self.t.clear()
        if self.life > 0:
            self.t.goto(self.x, self.y)
            self.t.dot(self.size)

            if self.is_core:
                self.t.dot(self.size + 2, self.color)
                self.t.dot(self.size + 4, self.color)


class Firework:
    def __init__(self):
        self.x = random.randint(-300, 300)
        self.y = random.randint(-50, 200)
        self.particles = []
        self.create_particles()

    def create_particles(self):
        for angle in range(0, 360, 10):
            particle = Particle(self.x, self.y, True)
            speed = random.uniform(2, 4)
            rad = math.radians(angle + random.uniform(-2, 2))
            particle.dx = math.cos(rad) * speed
            particle.dy = math.sin(rad) * speed
            self.particles.append(particle)

        for angle in range(0, 360, 5):
            for _ in range(2):
                particle = Particle(self.x, self.y)
                speed = random.uniform(4, 8)
                rad = math.radians(angle + random.uniform(-2, 2))
                particle.dx = math.cos(rad) * speed
                particle.dy = math.sin(rad) * speed
                self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.move()
        return any(p.life > 0 for p in self.particles)


# 管理烟花
fireworks = []


def create_firework():
    if random.random() < 0.1:
        fireworks.append(Firework())


def show_text():
    for i in range(30):
        text.clear()
        text.write("祝大家圣诞快乐", align="center",
                   font=("Arial", 25 + i // 10, "bold"))
        screen.update()
        time.sleep(0.05)


def update():
    global text_shown
    current_time = time.time()

    if not text_shown and current_time - start_time > 5:
        show_text()
        text_shown = True

    create_firework()

    for firework in fireworks[:]:
        if not firework.update():
            fireworks.remove(firework)

    screen.update()
    screen.ontimer(update, 20)


# 清理函数
def cleanup():
    pygame.mixer.music.stop()
    pygame.mixer.quit()


# 设置窗口关闭时的清理
screen.onkey(cleanup, "q")  # 按 q 键退出
screen.listen()

# 启动动画
update()
screen.mainloop()

# 确保程序结束时正确关闭音乐
cleanup()