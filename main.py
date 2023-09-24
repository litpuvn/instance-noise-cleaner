import tkinter as tk
from tkinter import Menu, Label, Scrollbar, HORIZONTAL, BOTTOM, VERTICAL, X, Y, RIGHT
from tkinter import filedialog
from PIL import Image, ImageTk


class SubFrame():

    def __init__(self, master, borderSize, width, height, row, column, bg):
        self.borderFrame = tk.Frame(master)
        self.borderFrame.grid(row=row, column=column)

        self.cWidth = width
        self.cHeight = height
        self.canvas = tk.Canvas(self.borderFrame, width=self.cWidth, height=self.cHeight,
                                borderwidth=0, highlightthickness=0, bg=bg)

        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, width, height)

    def display_img(self, load):
        # self.clear()

        wpercent = (self.cWidth / float(load.size[0]))
        hpercent = (self.cHeight / float(load.size[1]))

        percent = None
        if wpercent < hpercent:
            percent = wpercent
            hsize = int((float(load.size[1]) * float(percent)))
            load = load.resize((self.cWidth, hsize), Image.Resampling.LANCZOS)
        else:
            percent = hpercent
            wsize = int((float(load.size[0]) * float(percent)))
            load = load.resize((wsize, self.cHeight), Image.Resampling.LANCZOS)

        render_img = ImageTk.PhotoImage(load)

        self.canvas.create_image(0, 0, image=render_img, anchor="nw")
        self.canvas.image = render_img


    def clear(self):
        self.canvas.delete("all")

    def set_title(self, title):
        widget = Label(self.canvas, text=title, fg='white', bg='black')
        widget.pack()
        self.canvas.create_window(40, 10, window=widget)
        # self.label_text.config(text = title)


class Frame():

    def __init__(self, master):
        self.borderSize = 8
        # self.bigFrame = self
        # self.bigFrame.grid(row=0, column=0)
        self.master = master


        ## create menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Open", command=self.onOpenFile)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)

        ## create canvas
        self.top_left = self.canvas_panel(900, 600, 0, 0, 'yellow')
        self.top_left.set_title("Original")

        self.bottom_left = self.canvas_panel(900, 600, 1, 0, 'red')
        self.bottom_left.set_title("Red")


        self.top_right = self.canvas_panel(900, 600, 0, 1, 'green')
        self.top_right.set_title("green")

        self.bottom_right = self.canvas_panel(900, 600, 1, 1, 'blue')
        self.bottom_right.set_title("blue")


    def canvas_panel(self, width, height, row, column, bg=None):
        my_sub_frame = SubFrame(self.master, self.borderSize, width, height, row, column, bg)
        return my_sub_frame


    def onOpenFile(self):
        ftypes = [('Image files', ('*.jpg', '*.png')), ('All files', '*')]
        dlg = filedialog.Open(self.master, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            load = Image.open(fl)
            rgb_im = load.convert('RGB')

            self.top_left.display_img(load)
            # Split into 3 channels
            r, g, b = rgb_im.split()

            self.bottom_left.display_img(r)
            self.top_right.display_img(g)
            self.bottom_right.display_img(b)


    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text


    def exitProgram(self):
        exit()


root = tk.Tk()
root.title("Fluorescent Image Explorer")
root.geometry("1900x1300")


frame = Frame(root)
root.mainloop()
