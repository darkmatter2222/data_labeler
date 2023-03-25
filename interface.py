from tkinter import Frame, Canvas, Tk, BOTH, N, W, E,NW, Label, RIGHT, CENTER, Button, Listbox
from PIL import Image, ImageTk


class bbox_label():
    def __init__(self):
        self.width = int(1920 * 1.1)
        self.height = int(1080 * 1.1)
        self.temp = ''
        self.title = "darkmatter's data labeling tool"
        self.root = Tk()
        #self.root.columnconfigure(1, weight=1)  # confiugures column 0 to stretch with a scaler of 1.
        self.box = {}

        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(width=True, height=True)

        self.img = ImageTk.PhotoImage(file=r"O:\source\repos\data_labeler\test_data\test_image.png")
        self.image_canvas = Canvas(self.root, cursor='tcross', bg='blue', width=1920, height=1080)
        self.image_canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.image_canvas.grid(row=0, column=0, sticky=N)
        self.image_canvas.bind("<Motion>", self.mouseMove)
        self.image_canvas.bind("<ButtonPress-1>", self.mouseDown)
        self.image_canvas.bind("<ButtonRelease-1>", self.mouseUp)

        self.list_box = Listbox(self.root, bg='green', height=33, width=30)
        self.list_box.grid(row=0, column=1, sticky=N)

        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=2, column=0, sticky=N + W)
        self.load_button = Button(self.button_frame, text="Load", width=10)
        self.load_button.grid(row=0, column=0, sticky=W)
        self.save_button = Button(self.button_frame, text="Save", width=10)
        self.save_button.grid(row=0, column=1, sticky=W)
        self.save_button = Button(self.button_frame, text="Prev", width=10)
        self.save_button.grid(row=0, column=2, sticky=W)
        self.save_button = Button(self.button_frame, text="Next", width=10)
        self.save_button.grid(row=0, column=3, sticky=W)

        self.cords_frame = Frame(self.root)
        self.cords_frame.grid(row=1, column=0, sticky=N + W)

        self.cords_label = Label(self.cords_frame, text='')
        self.cords_label.grid(row=0, column=0, sticky=W)

        self.select_cords_label = Label(self.cords_frame, text='')
        self.select_cords_label.grid(row=0, column=1, sticky=E)

    def mouseMove(self, event):
        self.cords_label.config(text='x: %d, y: %d' % (event.x, event.y))

    def mouseDown(self, event):
        self.select_cords_label.config(text='x: %d, y: %d' % (event.x, event.y))
        self.box['start'] = (event.x, event.y)

    def mouseUp(self, event):
        self.box['end'] = (event.x, event.y)
        self.image_canvas.create_rectangle(self.box['start'][0],
                                           self.box['start'][1],
                                           self.box['end'][0],
                                           self.box['end'][1],
                                           outline="#ff6600")

    def start(self):
        self.root.title(self.title)

        self.root.mainloop()
