from tkinter import *
import socket


def send(data):
    sc = socket.socket()
    try:
        sc.connect(('127.0.0.1', 5000))
    except IOError:
        return [False, ""]
    else:
        sc.send(data.encode())
        re = sc.recv(2048).decode()
        return [bool(int(re.split(",")[0])), re]


class mainapp(Tk):
    def __init__(self):
        #Create framework

        Tk.__init__(self)
        self._frame = None
        self.cFrame(login)
        self.title("BlockBreaker")

    def startg(self, username):
        self._frame.destroy()
        game(self, username)

    def cFrame(self, frame_class):
        #frame change func

        newframe = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = newframe
        self._frame.grid()


master =""


class login(Frame):
    def __init__(self, parent):
        #Login frame
        Frame.__init__(self, parent)
        #todo add title
        Label(self, text="username:").grid(sticky=E)
        Label(self, text="Password:").grid(row=1, sticky=E)

        self.userv = StringVar()
        user = Entry(self, textvariable=self.userv).grid(row=0, column=1, columnspan=2)
        self.passv = StringVar()
        Entry(self, textvariable=self.passv, show="*").grid(row=1, column=1, columnspan=2)

        Button(self, text="New Account", command=lambda: parent.cFrame(ca)).grid(row=2, column=0, sticky="ew")
        Button(self, text="Forgot Pass", command=lambda: parent.cFrame(fp)).grid(row=2, column=1, sticky="ew")
        Button(self, text="Login", command=self.login).grid(row=2, column=2, sticky="ew")
        self.bind("<Enter>", self.elogin)

    def login(self):
        #login func
        global master
        info = send("login," + self.userv.get() + "." + self.passv.get())
        if info[0]:
            master.startg(self.userv.get())

    def elogin(self, Event):
        global master
        info = send("login," + self.userv.get() + "." + self.passv.get())
        if info[0]:
            master.startg(self.userv.get())


class ca(Frame):
    def __init__(self, parent):
        #Create account frame
        Frame.__init__(self, parent)
        Label(self, text="Username:").grid(row=0, column=0, sticky=E)
        Label(self, text="Password:").grid(row=1, column=0, sticky=E)
        Label(self, text="Security question:").grid(row=2, column=0, sticky=E)
        Label(self, text="Security answer:").grid(row=3, column=0, sticky=E)

        self.userv = StringVar()
        self.passv = StringVar()
        self.sqv = StringVar()
        self.sav = StringVar()
        Entry(self, textvariable=self.userv).grid(row=0, column=1, columnspan=2)
        Entry(self, textvariable=self.passv, show="*").grid(row=1, column=1, columnspan=2)
        Entry(self, textvariable=self.sqv).grid(row=2, column=1, columnspan=2)
        Entry(self, textvariable=self.sav).grid(row=3, column=1, columnspan=2)

        self.loginR = Button(self, text="Return to login", command=lambda: parent.cFrame(login)).grid(row=4, column=0, sticky="ew")
        self.cra = Button(self, text="Create", command=self.createA)
        self.cra.grid(row=4, column=1,columnspan=2, sticky="ew")

    def createA(self):
        #create account function
        data = "ca," + self.userv.get() + "." + self.passv.get() + "." + self.sqv.get() + "." + self.sav.get()
        if send(data)[0]:
            self.cra.config(state=DISABLED, text="Completed")
        else:
            self.cra.config(state=DISABLED, text="Error")


class fp(Frame):
    def __init__(self, parent):
        #forgot password frame
        Frame.__init__(self, parent)
        Label(self, text="Username:").grid(row=0, column=0, sticky=E)
        self.sq = StringVar()
        Label(self, textvariable=self.sq).grid(row=1, column=0, rowspan=2, sticky=E)
        self.sq.set("Security question:")

        self.userv = StringVar()
        self.userv.trace("w", self.updateSq)
        Entry(self, textvariable=self.userv).grid(row=0, column=1, columnspan=2)

        self.sav = StringVar()
        self.sa = Entry(self, textvariable=self.sav).grid(row=1, column=1, columnspan=2)
        Button(self, text="Return to login", command=lambda: parent.cFrame(login)).grid(row=3,column=0, sticky="ew")
        self.checkpv = StringVar()
        self.checkpv.set("Check")
        self.checksa = Button(self, textvariable=self.checkpv, command=self.checkp, state=DISABLED)
        self.checksa.grid(row=3, column=1, columnspan=2, sticky="ew")

    def checkp(self):
        data = "fp," + self.userv.get() + "." + self.sav.get()
        re = send(data)
        re[1] =re[1].split(",")
        if re[0]:
            self.checkpv.set(re[1][1])
            self.checksa.config(state=DISABLED)

    def updateSq(self, *args, event=None):
        #updateing the sq
        data = "sq," + self.userv.get()
        re = send(data)
        re[1] = re[1].split(",")
        if re[0]:
            self.sq.set(re[1][1] + ":")
            self.checksa.config(state=ACTIVE)
        else:
            self.sq.set("Invalid user")
            self.checksa.config(state=DISABLED)


class game():

    def __init__(self, root, username):
        self.username = username
        # the canvas where the game is
        self.root = root
        self.root.title('Blockity Breakity')

        self.canvas = Canvas(self.root, width=1000, height=800)
        self.canvas.configure(background="black")

        #start screen

        self.thisthing = self.canvas.create_text(50, 100, anchor=W, font=('Gotham', 43),
                                                 text='Use arrow keys press start to begin!', fill='purple')
        self.startButton = self.canvas.create_rectangle(300, 250, 700, 350, fill='purple', outline='purple')
        self.thatthing = self.canvas.create_text(500, 300, font=('Gotham', 44), text='START', fill='black')
        self.localscore = self.canvas.create_text(150,300,font=('Gotham',20), text='Your High Scores:', fill='white')
        self.globalscore = self.canvas.create_text(850,300,font=('Gotham',20),text='All High Scores:', fill='white')
        loc =str(send("rloc," + self.username)).lstrip("[True, '1,[]']").rstrip(']"]').lstrip('[True, "1,[').replace("',", " -", 5).replace(",", "\n", 4).replace(" (", "",4).replace("(", "").replace(")", "").replace("'","")
        glob = str(send("rglob," + self.username)).lstrip("[True, '1,[]']").rstrip(']"]').lstrip('[True, "1,[').replace("',", " -", 5).replace(",", "\n", 4).replace(" (", "",4).replace("(", "").replace(")", "").replace("'","")

        self.localscorelist = self.canvas.create_text(150,400,font=('Gatham',15),text=loc,fill='white')
        self.globalscorelist = self.canvas.create_text(850, 400, font=('Gatham',15), text=glob, fill='white')
        self.errorexceptbitchfuck = 0

        def beginB(event):
            e = event.x
            f = event.y
            a, b, c, d = 100000, 0, 0, 0
            if self.errorexceptbitchfuck == 0:
                a, b, c, d = self.canvas.coords(self.startButton)
            if e < c and e > a and f < d and f > b:
                self.canvas.delete(self.thisthing)
                self.canvas.delete(self.thatthing)
                self.canvas.delete(self.startButton)
                self.canvas.delete(self.localscore)
                self.canvas.delete(self.globalscore)
                self.canvas.delete(self.localscorelist)
                self.canvas.delete(self.globalscorelist)
                self.errorexceptbitchfuck = 1
                self.startgame()

        self.root.bind('<Button-1>', beginB)

        # initial ball speed
        self.ballspeed = -5

        # The canvas and root boiler plate things that you may want to put somewhere else.
        self.canvas.pack()

    def startgame(self):

        # game variables
        self.level = 1
        self.nomove = 0
        self.mlr = 0
        self.mud = self.ballspeed
        self.lives = 3
        self.score = 0

        # Paddle, Ball, Blocks, and score n' shit at begining of game
        self.lineinButt = self.canvas.create_rectangle(-1, 701, 1001, 705, fill='white')
        self.ball = self.canvas.create_oval(475, 550, 500, 575, fill='white')
        self.paddle = self.canvas.create_rectangle(425, 680, 575, 695, fill='white')
        self.blocks = []
        inc = 0
        for i in range(50):  # ask about bug here
            if (i % 5) == 0:
                self.blocks.append(
                    self.canvas.create_rectangle(0 + (100 * inc), 200, 100 + (100 * inc), 230, fill='blue'))
            if (i % 5) == 1:
                self.blocks.append(
                    self.canvas.create_rectangle(0 + (100 * inc), 230, 100 + (100 * inc), 260, fill='blue'))
            if (i % 5) == 2:
                self.blocks.append(
                    self.canvas.create_rectangle(0 + (100 * inc), 260, 100 + (100 * inc), 290, fill='blue'))
            if (i % 5) == 3:
                self.blocks.append(
                    self.canvas.create_rectangle(0 + (100 * inc), 170, 100 + (100 * inc), 200, fill='blue'))
            if (i % 5) == 3:
                self.blocks.append(
                    self.canvas.create_rectangle(0 + (100 * inc), 290, 100 + (100 * inc), 320, fill='blue'))
            if (i % 5) == 4:
                inc += 1
        self.scoreTrack = self.canvas.create_text(50, 750, anchor=W, font=('Gotham', 25), text='SCORE: ', fill='green')
        self.lifeTrack = self.canvas.create_text(800, 750, anchor=W, font=('Gotham', 25), text='LIVES: ', fill='green')
        self.scoreDisp = self.canvas.create_text(227, 750, anchor=W, font=('Gotham', 25), text=str(self.score),
                                                 fill='green')
        self.lifeDisp = self.canvas.create_text(923, 750, anchor=W, font=('Gotham', 25), text=str(self.lives),
                                                fill='green')

        # moving the ball go fucking figure
        def moveball():
            # the function that resets the game at end
            def beginagain():
                self.errorexceptbitchfuck = 0
                self.canvas.delete(self.gg)
                self.canvas.delete(self.ys)
                self.canvas.delete(self.scoreDisp)
                self.canvas.delete(self.scoreTrack)
                self.canvas.delete(self.lifeTrack)
                self.canvas.delete(self.lifeDisp)
                self.canvas.delete(self.lineinButt)
                self.ballspeed = -5

                self.thisthing = self.canvas.create_text(50, 100, anchor=W, font=('Gotham', 43),
                                                         text='Use arrow keys press start to begin!', fill='purple')
                self.startButton = self.canvas.create_rectangle(300, 250, 700, 350, fill='purple', outline='purple')
                self.thatthing = self.canvas.create_text(500, 300, font=('Gotham', 44), text='START', fill='black')
                self.localscore = self.canvas.create_text(150, 300, font=('Gotham', 20), text='Your High Scores:',
                                                          fill='white')
                self.globalscore = self.canvas.create_text(850, 300, font=('Gotham', 20), text='All High Scores:',
                                                           fill='white')

                loc = str(send("rloc," + self.username)).rstrip(']"]').lstrip('[True, "1,[').replace("',", " -",
                                                                                                     5).replace(",",
                                                                                                                "\n",
                                                                                                                4).replace(
                    " (", "", 4).replace("(", "").replace(")", "").replace("'", "")
                glob = str(send("rglob," + self.username)).rstrip(']"]').lstrip('[True, "1,[').replace("',", " -",
                                                                                                       5).replace(",",
                                                                                                                  "\n",
                                                                                                                  4).replace(
                    " (", "", 4).replace("(", "").replace(")", "").replace("'", "")

                self.localscorelist = self.canvas.create_text(150, 400, font=('Gatham',15), text=loc, fill='white')
                self.globalscorelist = self.canvas.create_text(850, 400, font=('Gatham',15), text=glob, fill='white')
                self.errorexceptbitchfuck = 0

                def beginB(event):
                    e = event.x
                    f = event.y
                    a, b, c, d = 100000, 0, 0, 0
                    if self.errorexceptbitchfuck == 0:
                        a, b, c, d = self.canvas.coords(self.startButton)
                    if e < c and e > a and f < d and f > b:
                        self.canvas.delete(self.thisthing)
                        self.canvas.delete(self.thatthing)
                        self.canvas.delete(self.startButton)
                        self.canvas.delete(self.localscore)
                        self.canvas.delete(self.globalscore)
                        self.canvas.delete(self.localscorelist)
                        self.canvas.delete(self.globalscorelist)
                        self.errorexceptbitchfuck = 1
                        self.startgame()

                self.root.bind('<Button-1>', beginB)

            x0, y0, x1, y1 = self.canvas.coords(self.ball)

            # checks if ball has hit any of the blocks and deals with that
            for block in self.blocks:
                doubleHitCheckLR = 0
                doubleHitCheckUD = 0
                a0, b0, a1, b1 = self.canvas.coords(block)
                if ((x0 > a0) and (x0 < a1) and (y0 < b1) and (y0 > b0)) or (
                        (x1 > a0) and (x1 < a1) and (y0 < b1) and (y0 > b0)) or (
                        (x0 > a0) and (x0 < a1) and (y1 < b1) and (y1 > b0)) or (
                        (x1 > a0) and (x1 < a1) and (y1 < b1) and (y1 > b0)):
                    if ((((x0 + x1) / 2) < a0) or (((x0 + x1) / 2) > a1)) and (
                            (((y0 + y1) / 2) < b0) or (((y0 + y1) / 2) > b1)):
                        if doubleHitCheckUD < 1:
                            self.mud = self.mud * (-1)
                        doubleHitCheckUD += 1
                        doubleHitCheckLR += 1
                    elif (((x0 + x1) / 2) < a0) or (((x0 + x1) / 2) > a1):
                        if doubleHitCheckLR < 1:
                            self.mlr = self.mlr * (-1)
                        doubleHitCheckLR += 1
                    elif (((y0 + y1) / 2) < b0) or (((y0 + y1) / 2) > b1):
                        if doubleHitCheckUD < 1:
                            self.mud = self.mud * (-1)
                        doubleHitCheckUD += 1
                    self.canvas.delete(block)
                    self.blocks.remove(block)
                    self.score += 1
                    self.canvas.delete(self.scoreDisp)
                    self.scoreDisp = self.canvas.create_text(227, 750, anchor=W, font=('Gotham', 25),
                                                             text=str(self.score), fill='green')

            # when the ball hits the paddle
            i0, j0, i1, j1 = self.canvas.coords(self.paddle)
            if ((x0 > i0) and (x0 < i1) and (y0 < j1) and (y0 > j0)) or (
                    (x1 > i0) and (x1 < i1) and (y0 < j1) and (y0 > j0)) or (
                    (x0 > i0) and (x0 < i1) and (y1 < j1) and (y1 > j0)) or (
                    (x1 > i0) and (x1 < i1) and (y1 < j1) and (y1 > j0)):
                if (((x0 + x1) / 2) < (((i0 + i1) / 2) + 10)) and (((x0 + x1) / 2) > (((i0 + i1) / 2) - 10)):
                    self.mud = self.mud * (-1)
                elif (((x0 + x1) / 2) < (((i0 + i1) / 2) + 23)) and ((x0 + x1) / 2) > ((i0 + i1) / 2):
                    self.mud = self.mud * (-1)
                    self.mlr = 2
                elif ((x0 + x1) / 2) < ((i0 + i1) / 2) and (((x0 + x1) / 2) > (((i0 + i1) / 2) - 23)):
                    self.mud = self.mud * (-1)
                    self.mlr = -2
                elif (((x0 + x1) / 2) < (((i0 + i1) / 2) + 36)) and ((x0 + x1) / 2) > ((i0 + i1) / 2):
                    self.mud = self.mud * (-1)
                    self.mlr = 4
                elif ((x0 + x1) / 2) < ((i0 + i1) / 2) and (((x0 + x1) / 2) > (((i0 + i1) / 2) - 36)):
                    self.mud = self.mud * (-1)
                    self.mlr = -4
                elif (((x0 + x1) / 2) < (((i0 + i1) / 2) + 49)) and ((x0 + x1) / 2) > ((i0 + i1) / 2):
                    self.mud = self.mud * (-1)
                    self.mlr = 6
                elif ((x0 + x1) / 2) < ((i0 + i1) / 2) and (((x0 + x1) / 2) > (((i0 + i1) / 2) - 49)):
                    self.mud = self.mud * (-1)
                    self.mlr = -6
                elif (((x0 + x1) / 2) < (((i0 + i1) / 2) + 62)) and ((x0 + x1) / 2) > ((i0 + i1) / 2):
                    self.mud = self.mud * (-1)
                    self.mlr = 8
                elif ((x0 + x1) / 2) < ((i0 + i1) / 2) and (((x0 + x1) / 2) > (((i0 + i1) / 2) - 62)):
                    self.mud = self.mud * (-1)
                    self.mlr = -8
                elif ((x0 + x1) / 2) > ((i0 + i1) / 2):
                    self.mud = self.mud * (-1)
                    self.mlr = 10
                else:
                    self.mud = self.mud * (-1)
                    self.mlr = -10

            # recreates blocks and makes up and down speed increase. if you win it does a thing
            if len(self.blocks) == 0:
                if abs(self.ballspeed) < 10:
                    self.ballspeed -= 1
                self.mud = self.ballspeed
                self.blocks = []
                inc = 0
                for i in range(50):  # ask about bug here
                    if (i % 5) == 0:
                        self.blocks.append(
                            self.canvas.create_rectangle(0 + (100 * inc), 200, 100 + (100 * inc), 230, fill='blue'))
                    if (i % 5) == 1:
                        self.blocks.append(
                            self.canvas.create_rectangle(0 + (100 * inc), 230, 100 + (100 * inc), 260, fill='blue'))
                    if (i % 5) == 2:
                        self.blocks.append(
                            self.canvas.create_rectangle(0 + (100 * inc), 260, 100 + (100 * inc), 290, fill='blue'))
                    if (i % 5) == 3:
                        self.blocks.append(
                            self.canvas.create_rectangle(0 + (100 * inc), 170, 100 + (100 * inc), 200, fill='blue'))
                    if (i % 5) == 4:
                        self.blocks.append(
                            self.canvas.create_rectangle(0 + (100 * inc), 290, 100 + (100 * inc), 320, fill='blue'))
                    if (i % 5) == 4:
                        inc += 1

                self.canvas.delete(self.ball)
                self.ball = self.canvas.create_oval(475, 550, 500, 575, fill='white')
                self.mud = self.ballspeed
                self.mlr = 0
                if abs(self.ballspeed) >= 10:
                    self.nomove = 1
                    self.canvas.delete(self.ball)
                    self.canvas.delete(self.paddle)
                    for block in self.blocks:
                        self.canvas.delete(block)
                    self.gg = self.canvas.create_text(500, 350, font=('Gotham', 75), text='YOU WON!!!', fill='green')
                    self.ys = self.canvas.create_text(500, 450, font=('Gotham', 45), text='good job', fill='green')
                    send("reg," + str(self.username) + "." + str(self.score))
                    self.root.after(1000, beginagain)

            # checks if ball has hit any of the walls or bottom also voids loop if you win

            if abs(self.ballspeed) >= 10:
                self.WooHooVictory = True
            elif self.lives != 0:  # will restart if lives hit zero
                if x1 == 1000 or x1 > 1000:
                    self.mlr = -1 * self.mlr
                if x0 == 0 or x0 < 0:
                    self.mlr = -1 * self.mlr

                if y1 == 700 or y1 > 700:
                    self.canvas.delete(self.ball)
                    self.lives -= 1
                    self.canvas.delete(self.lifeDisp)
                    self.lifeDisp = self.canvas.create_text(923, 750, anchor=W, font=('Gotham', 25),
                                                            text=str(self.lives), fill='green')
                    self.ball = self.canvas.create_oval(475, 550, 500, 575, fill='white')
                    self.mud = self.ballspeed
                    self.mlr = 0
                if y0 == 0 or y0 < 0:
                    self.mud = -1 * self.mud

                self.canvas.move(self.ball, self.mlr, self.mud)
                self.root.after(23, moveball)
            else:
                self.nomove = 1
                self.canvas.delete(self.ball)
                self.canvas.delete(self.paddle)
                for block in self.blocks:
                    self.canvas.delete(block)
                self.gg = self.canvas.create_text(500, 350, font=('Gotham', 75), text='GAME OVER', fill='red')
                self.ys = self.canvas.create_text(500, 450, font=('Gotham', 45), text='you suck', fill='red')
                send("reg," + str(self.username) + "." + str(self.score))
                self.root.after(1000, beginagain)

        # moves the paddle
        self.leftcheck = 0
        self.rightcheck = 0

        def moveL(event):
            self.leftcheck = 1
            movepaddleL()

        def moveR(event):
            self.rightcheck = 1
            movepaddleR()

        def dontmove(event):
            self.rightcheck = 0
            self.leftcheck = 0

        def movepaddleL():
            if (self.leftcheck == 1) and (self.nomove != 1):
                i0, j0, i1, j1 = self.canvas.coords(self.paddle)
                if i0 > 0:
                    self.canvas.move(self.paddle, -5, 0)
                    self.canvas.after(15, movepaddleL)

        def movepaddleR():
            if (self.rightcheck == 1) and (self.nomove != 1):
                i0, j0, i1, j1 = self.canvas.coords(self.paddle)
                if i1 < 1000:
                    self.canvas.move(self.paddle, 5, 0)
                    self.canvas.after(15, movepaddleR)

        self.surprise = 1

        def b(event):
            if self.surprise == 1:
                self.surprise += 1
            else:
                self.surprise = 1

        def i(event):
            if self.surprise == 2:
                self.surprise += 1
            else:
                self.surprise = 1

        def g(event):
            if self.surprise == 3:
                self.canvas.delete(self.ball)
                self.ball = self.canvas.create_oval(450, 525, 525, 600, fill='white')
                self.surprise = 1
            else:
                self.surprise = 1

        self.root.bind('<Left>', moveL)
        self.root.bind('<Right>', moveR)
        self.root.bind('<KeyRelease>', dontmove)
        self.root.bind('<b>', b)
        self.root.bind('<i>', i)
        self.root.bind('<g>', g)

        # starts the shit
        self.root.after(1, moveball)


master = mainapp()
mainloop()
