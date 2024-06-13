from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2


class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="HELP DESK", font=(
            "Times New Roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"C:\Users\oztur\PycharmProjects\pythonProject2\college_images\help.jpg")
        img_top = img_top.resize((1530, 720), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=720)

        dev_label = Label(f_lbl, text="Email: helpdesk@gmail.com", font=(
            "Times new roman", 20, "bold"), fg="blue")
        dev_label.place(x=600, y=150)


if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()
