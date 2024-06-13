from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="TRAIN DATA SET", font=(
            "Times New Roman", 35, "bold"), bg="white", fg="black")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(
            r"C:\Users\Pc\source\repos\pythonProject2\college_images\facial-recognition.jpg")
        img_top = img_top.resize((1530, 325), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)

        # button
        b1_1 = Button(self.root, text="TRAIN DATA", command=self.train_classifier,
                      cursor="hand2", font=("Times New Roman", 30, "bold"), bg="red", fg="white")
        b1_1.place(x=0, y=380, width=1530, height=60)

        img_bottom = Image.open(
            r"C:\Users\Pc\source\repos\pythonProject2\college_images\opencv_face_reco_more_data.jpg")
        img_bottom = img_bottom.resize((1530, 325), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=0, y=440, width=1530, height=325)

    def train_classifier(self):
        print("Training classifier...")

        data_dir = "data"
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", f"Data directory {
                                 data_dir} not found.")
            return

        path = [os.path.join(data_dir, file) for file in os.listdir(
            data_dir) if file.endswith('.jpg')]

        faces = []
        ids = []

        for image_path in path:
            try:
                img = Image.open(image_path).convert('L')  # Gray scale image
                imgNp = np.array(img, 'uint8')
                id_str = os.path.basename(image_path)[len('user'):].split('.')[
                    0]  # Get the ID part of the filename
                try:
                    # Try converting the extracted ID string to an integer
                    id = int(id_str)
                except ValueError:
                    print(f"Skipping file {
                          image_path} due to invalid ID format: {id_str}")
                else:
                    faces.append(imgNp)
                    ids.append(id)
                    print('Adding', image_path, 'ID', id)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing image {
                                     image_path}: {str(e)}")

        if not faces:
            messagebox.showerror(
                "Error", "No valid images found for training.")
            return

        ids = np.array(ids)

        print("Number of valid faces:", len(faces))
        print("Number of valid IDs:", len(ids))

        # ====== Train the classifier and save ======
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.save("classifier.xml")
            print("Classifier saved successfully.")
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training datasets completed!!")
        except Exception as e:
            messagebox.showerror("Error", f"Error during training: {str(e)}")
            cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
