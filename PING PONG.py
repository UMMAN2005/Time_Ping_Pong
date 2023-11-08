from tkinter import *
from time import sleep
from tkinter import messagebox

WIDTH = 1500
HEIGHT = 600
xVelocity = 10
yVelocity = 5
score1 = 0
score2 = 0
SPEED = 30
speed = 30
speed_limit = 6
pong_speed = 20
winning = 3
acceleration = 3
pressed_keys = set()


def exiting():
    quit()


def show_score():
    global score1, score2
    score_entry = f"Player1:     {score1}      |      Player2:     {score2}"
    score.set(score_entry)


def move_up_label1():
    canvas.move(label1, 0, -pong_speed)


def move_down_label1():
    canvas.move(label1, 0, pong_speed)


def move_up_label2():
    canvas.move(label2, 0, -pong_speed)


def move_down_label2():
    canvas.move(label2, 0, pong_speed)


def handle_keypress(event):
    global pressed_keys

    # Add the key to the set of pressed keys
    pressed_keys.add(event.keysym)

    # Check for simultaneous key presses
    if 'w' in pressed_keys and 'Up' in pressed_keys:
        move_up_label1()
        move_up_label2()
    elif 's' in pressed_keys and 'Down' in pressed_keys:
        move_down_label1()
        move_down_label2()
    elif 's' in pressed_keys and 'Up' in pressed_keys:
        move_down_label1()
        move_up_label2()
    elif 'w' in pressed_keys and 'Down' in pressed_keys:
        move_up_label1()
        move_down_label2()
    elif 'w' in pressed_keys:
        move_up_label1()
    elif 'Up' in pressed_keys:
        move_up_label2()
    elif 's' in pressed_keys:
        move_down_label1()
    elif 'Down' in pressed_keys:
        move_down_label2()


def handle_keyrelease(event):
    global pressed_keys

    # Remove the released key from the set of pressed keys
    if event.keysym in pressed_keys:
        pressed_keys.remove(event.keysym)


def update_game():
    global xVelocity, yVelocity
    global score1, score2
    global speed
    show_score()
    coordinates = canvas.coords(ball)
    coordinates2 = canvas.coords(label1)
    coordinates3 = canvas.coords(label2)

    if coordinates[0] == (coordinates3[0]) and (
            (coordinates3[1] - 64) <= coordinates[1] <= (coordinates3[1] + 64)):
        xVelocity = -xVelocity  # Reverse the x-velocity when ball touches label2
        if speed >= speed_limit:
            speed -= acceleration

    elif coordinates[0] > WIDTH - image_width1:
        score1 += 1
        speed = SPEED
        sleep(1.5)
        canvas.moveto(ball, 0, 0)

    if coordinates2[0] <= coordinates[0] <= (coordinates2[0] + 50) and (
            (coordinates2[1] - 64) <= coordinates[1] <= (coordinates2[1] + 64)):
        xVelocity = -xVelocity  # Reverse the x-velocity when ball touches label1
        if speed >= speed_limit:
            speed -= acceleration

    elif coordinates[0] < 0:
        score2 += 1
        speed = SPEED
        sleep(1.5)
        canvas.moveto(ball, HEIGHT - 20, 0)

    if coordinates[1] >= (HEIGHT - image_height1) or coordinates[1] < 0:
        yVelocity = -yVelocity

    canvas.move(ball, xVelocity, yVelocity)
    window.after(speed, update_game)  # Update every 10 milliseconds
    if score1 == winning:
        score1 = 0
        score2 = 0
        window.destroy()
        messagebox.showinfo(title="WINNER", message="PLAYER1 won!")
    elif score2 == winning:
        score1 = 0
        score2 = 0
        window.destroy()
        messagebox.showinfo(title="WINNER", message="PLAYER1 won!")

    print(speed)


window = Tk()
window.title("PING PONG GAME")
window.attributes("-fullscreen", True)

score = StringVar()

score_board = Label(textvariable=score, bg='black', fg='white', height=2, font=("Comic Sans MS", 20))
score_board.pack()

button = Button(text='Exit', bg='#00FF00', font=("Arial", 30, 'bold'), fg='red', command=exiting)
button.pack(anchor=S)

canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg='blue')
canvas.pack()
canvas.focus_set()

photo_image1 = PhotoImage(file='icons8-alarm-clock-16.png')
ball = canvas.create_image(0, 0, image=photo_image1, anchor=NW)
image_width1 = photo_image1.width()
image_height1 = photo_image1.height()

photo_image2 = PhotoImage(file='rectangle.png')
label1 = canvas.create_image(0, HEIGHT / 2, image=photo_image2, anchor=NW)

photo_image3 = PhotoImage(file='rectangle.png')
label2 = canvas.create_image(WIDTH - 60, HEIGHT / 2, image=photo_image3, anchor=NW)

canvas.bind("<KeyPress>", handle_keypress)
canvas.bind("<KeyRelease>", handle_keyrelease)

update_game()  # Start the game loop
window.mainloop()
