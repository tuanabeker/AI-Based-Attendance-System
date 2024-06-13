import mysql.connector
from tkinter import *
from PIL import Image, ImageTk
import cv2
from datetime import datetime, timedelta


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=(
            "Times New Roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"college_images/facedetector.jpg")
        img_top = img_top.resize((650, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=700)

        img_bottom = Image.open(
            r"college_images/face_recognition_identification.jpg")
        img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=650, y=55, width=950, height=700)

        b1_1 = Button(f_lbl, text="Face Recognition", command=self.face_recog, cursor="hand2", font=(
            "Times New Roman", 18, "bold"), bg="darkblue", fg="white")
        b1_1.place(x=375, y=625, width=200, height=40)

        self.last_recognized_time = {}

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(
            gray_image, scaleFactor, minNeighbors)

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))

            if confidence > 77:
                student_info = self.get_student_info_from_database(id)
                cv2.putText(img, f"ID: {student_info['id']} ({confidence}% confident)", (
                    x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                cv2.putText(img, f"Roll: {student_info['roll']}", (
                    x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                cv2.putText(img, f"Name: {student_info['name']}", (
                    x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                cv2.putText(img, f"Department: {student_info['department']}", (
                    x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)

                self.mark_attendance(student_info)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(img, f"Unknown Face ({confidence}% confident)", (
                    x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 3)

        return img

    def get_student_info_from_database(self, student_id):
        conn = mysql.connector.connect(
            host="localhost", user="root", password="4656", database="face_recognizer")
        cursor = conn.cursor()
        query = "select Student_id as id, Roll as roll, Name as name, Dep as department from student where Student_id=%s"
        cursor.execute(query, (student_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row is None:
            return {
                'id': student_id,
                'roll': 'Unknown',
                'name': 'Unknown',
                'department': 'Unknown',
            }
        assert not isinstance(row, dict)
        return {
            'id': row[0],
            'roll': row[1],
            'name': row[2],
            'department': row[3],
        }

    def face_recog(self):
        faceCascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            if not ret:
                break
            img = self.draw_boundary(
                img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) == 13:  # Press Enter to exit
                break

        video_cap.release()
        cv2.destroyAllWindows()

    def mark_attendance(self, student_info):
        now = datetime.now()
        if student_info['id'] not in self.last_recognized_time or (now - self.last_recognized_time[student_info['id']]).seconds >= 3600:
            with open("oyku.csv", "a") as f:
                dtString = now.strftime("%H:%M:%S")
                d1 = now.strftime("%d/%m/%Y")
                f.write(
                    f"\n{student_info['id']},{student_info['roll']},{student_info['name']},{student_info['department']},{dtString},{d1},Present")
            self.last_recognized_time[student_info['id']] = now


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
