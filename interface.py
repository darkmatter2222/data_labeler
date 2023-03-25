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

        self.list_box = Listbox(self.root, bg='white', height=33, width=60)
        self.list_box.grid(row=0, column=1, sticky=N)
        self.list_box.bind("<ButtonRelease-1>", self.lbMouseUp)

        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=2, column=0, sticky=N + W)
        self.load_button = Button(self.button_frame, text="Load", width=10, command=self.loadData)
        self.load_button.grid(row=0, column=0, sticky=W)
        self.save_button = Button(self.button_frame, text="Save", width=10, command=self.saveData)
        self.save_button.grid(row=0, column=1, sticky=W)
        self.commit_button = Button(self.button_frame, text="Commit", width=10, command=self.commit)
        self.commit_button.grid(row=0, column=2, sticky=W)

        self.cords_frame = Frame(self.root)
        self.cords_frame.grid(row=1, column=0, sticky=N + W)

        self.cords_label = Label(self.cords_frame, text='')
        self.cords_label.grid(row=0, column=0, sticky=W)

        self.select_cords_label = Label(self.cords_frame, text='')
        self.select_cords_label.grid(row=0, column=1, sticky=E)
        self.loadData()

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

    def lbMouseUp(self, event):
        sel = self.list_box.curselection()
        self.img = ImageTk.PhotoImage(
            file=f"{self.data_root}\\{' - '.join(self.list_box.get(sel[0]).split(' - ')[1:])}")
        self.image_canvas.create_image(0, 0, anchor=NW, image=self.img)

        sel = self.list_box.curselection()
        state = self.list_box.get(sel[0]).split(' - ')[0]
        file = ' - '.join(self.list_box.get(sel[0]).split(' - ')[1:])
        if state == 'Labeled':
            for i, data in enumerate(self.image_data):
                if data['image_name'] == file:
                    self.image_canvas.create_rectangle(*self.image_data[i]['bbox'],
                                                       outline="#ff6600")
                break

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
        self.list_box.delete(0, END)
        self.readData()
        labeled_image_names = []
        for i, data in enumerate(self.image_data):
            self.list_box.insert(i, str('Labeled - ') + data['image_name'])
            labeled_image_names.append(data['image_name'])
        for i, data in enumerate(self.image_names):
            file = data.split('\\')[-1:][0]
            if file not in labeled_image_names:
                self.list_box.insert(i, str('Not Labeled - ') + file)

    def commit(self):
        sel = self.list_box.curselection()
        state = self.list_box.get(sel[0]).split(' - ')[0]
        file = ' - '.join(self.list_box.get(sel[0]).split(' - ')[1:])
        if state == 'Labeled':
            for i, data in enumerate(self.image_data):
                if data[i]['image_name'] == file:
                    self.image_data[i]['bbox'] = [self.box['start'][0], self.box['start'][1], self.box['end'][0],
                                                  self.box['end'][1]]
                break
        else:
            self.image_data.append(
                {"image_name": file, 'bbox': [self.box['start'][0], self.box['start'][1], self.box['end'][0],
                                              self.box['end'][1]]})

        self.saveData()
        self.loadData()

    def start(self):
        self.root.title(self.title)

        self.root.mainloop()
