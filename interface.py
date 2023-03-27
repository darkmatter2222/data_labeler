from tkinter import Frame, Canvas, Tk, BOTH, N, W, E, NW, Label, END, RIGHT, CENTER, Button, Listbox
from PIL import Image, ImageTk
import glob
import json


class bbox_label():
    def __init__(self):
        self.data_root = r'O:\source\repos\data_labeler\training_data\inventory'
        self.image_names = []
        self.image_data = []

        self.width = int(1920 * 1.2)
        self.height = int(1080 * 1.1)
        self.temp = ''
        self.title = "darkmatter's data labeling tool"
        self.root = Tk()
        # self.root.columnconfigure(1, weight=1)  # confiugures column 0 to stretch with a scaler of 1.
        self.box = {}

        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(width=True, height=True)

        #self.img = ImageTk.PhotoImage(file=r"O:\source\repos\data_labeler\test_data\test_image.png")
        self.image_canvas = Canvas(self.root, cursor='tcross', bg='white', width=1920, height=1080)
        #self.image_canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.image_canvas.grid(row=0, column=0, sticky=N)
        self.image_canvas.bind("<Motion>", self.mouseMove)
        self.image_canvas.bind("<ButtonPress-1>", self.mouseDown)
        self.image_canvas.bind("<ButtonRelease-1>", self.mouseUp)

        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=2, column=0, sticky=N + W)
        self.load_button = Button(self.button_frame, text="Reset", width=10, command=self.reset)
        self.load_button.grid(row=0, column=0, sticky=W)
        self.commit_button = Button(self.button_frame, text="Commit", width=10, command=self.commit)
        self.commit_button.grid(row=0, column=2, sticky=W)
        self.root.bind("<space>", self.commit)
        self.root.bind("<BackSpace>", self.reset)

        self.cords_frame = Frame(self.root)
        self.cords_frame.grid(row=1, column=0, sticky=N + W)

        self.cords_label = Label(self.cords_frame, text='')
        self.cords_label.grid(row=0, column=0, sticky=W)

        self.count_label1 = Label(self.cords_frame, text='')
        self.count_label1.grid(row=1, column=0, sticky=W)
        self.count_label2 = Label(self.cords_frame, text='')
        self.count_label2.grid(row=2, column=0, sticky=W)

        self.select_cords_label = Label(self.cords_frame, text='')
        self.select_cords_label.grid(row=0, column=1, sticky=E)
        self.unlabeled = []
        self.labeled = {}
        self.loadData()

        self.image_name_on_screen = None

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

    def reset(self, event=None):
        self.loadData()
        self.load_next_image()

    def readData(self):
        self.image_data = []
        self.image_names = []
        for file in glob.glob(f"{self.data_root}\*.png"):
            self.image_names.append(file)
        try:
            f = open(f"{self.data_root}\\boxes.json")
            self.image_data = json.load(f)
            f.close()
        except:
            self.image_data = []

    def saveData(self):
        with open(f"{self.data_root}\\boxes.json", "w") as outfile:
            outfile.write(json.dumps(self.image_data, indent=1))

    def loadData(self):
        self.image_canvas.delete('all')
        self.image_name_on_screen = None
        self.unlabeled = []
        self.labeled = {}
        self.box = {}
        self.readData()
        for data in self.image_data:
            self.labeled[data['image_name']] = data['bbox']

        for image_name in self.image_names:
            if image_name.split('\\')[-1:][0] not in self.labeled:
                self.unlabeled.append(image_name)

        self.count_label1.config(text=f'Labeled:{len(self.labeled)}')
        self.count_label2.config(text=f'Labeled:{len(self.unlabeled)}')

    def load_next_image(self):
        try:

            if len(self.unlabeled) > 0:
                self.img = ImageTk.PhotoImage(
                    file=f"{self.data_root}\\" + self.unlabeled[0].split('\\')[-1:][0])
                self.image_canvas.create_image(0, 0, anchor=NW, image=self.img)
                self.image_name_on_screen = self.unlabeled[0]
            else:
                self.image_canvas.delete('all')
                self.image_name_on_screen = None
        except:
            print(self.unlabeled[0])

    def commit(self, event=None):
        self.image_data.append(
            {"image_name": self.image_name_on_screen.split('\\')[-1:][0],
             'bbox': [self.box['start'][0],
                      self.box['start'][1],
                      self.box['end'][0],
                      self.box['end'][1]]})

        self.saveData()
        self.loadData()
        self.load_next_image()

    def start(self):
        self.root.title(self.title)
        self.loadData()
        self.load_next_image()
        self.root.mainloop()

