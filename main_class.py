import face_recognition as fr
import cv2
import os
import pickle
import numpy as np

class FaceRecognition:
    def __init__(self, frames_dir, pickle_path):
        #self.filename = filename
        self.frames_dir = frames_dir
        self.pickle_path = pickle_path
        self.students = {
            'Dinesh': '213J1A4267',
            'Ritesh': '213J1A4280',
            'Vardhan': '213J1A4287',
            'Bhavani Shankar': '213J1A4288',
            'Shyam': '213J1A4297',
            'Hemant Srinivas': '213J1A4298',
            'Harsha Vardhan': '213J1A42A6',
            'Sadhik': '213J1A42B1',
            'Sadhiq Shaik': '213J1A42B2',
            'Manideep': '213J1A42B6',
            'Rohit': '213J1A42B9',
            'Purna': '213J1A42C2',
            'Dev': '213J1A42C3',
            'Murali': '213J1A42C6',
            'Vivek': '213J1A42C9',
            'Deepak': '213J1A42D2',
            'Naveen': '223J5A4208',
            'Praveen Kumar': '223J5A4209',
            'Tharun': '223J5A4211',
        }

        #self.csm_students = csm_students
        with open(self.pickle_path, 'rb') as file:
            self.known_face_encodings = pickle.load(file)

    def load_new_student(path):
        x_image = fr.load_image_file(path)
        x_face_encoding = fr.face_encodings(x_image)[0]
        return x_face_encoding

    def load_image_paths(self):
        image_paths = [os.path.join(self.frames_dir, filename) for filename in os.listdir(self.frames_dir) if filename.lower().endswith('.jpg')]
        return image_paths

    def find_faces(self, image_paths):
        face_locations = []
        face_encodings = []

        for path in image_paths:
            frame = fr.load_image_file(path)
            rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

            face_locations = fr.face_locations(rgb_frame, number_of_times_to_upsample=1, model='hog')
            face_encodings_for_frame = fr.face_encodings(frame, face_locations)

            face_encodings.extend(face_encodings_for_frame)

        with open('video_face_encodings.pkl', 'wb') as file:
            pickle.dump(face_encodings, file)

        print(f"Extracted {len(face_encodings)} faces and encoded to video_face_encodings.pkl")

    def cosine_similarity(self, vector_a, vector_b):
        vector_a = np.array(vector_a, dtype=float)
        vector_b = np.array(vector_b, dtype=float)
        dot_product = np.dot(vector_a, vector_b)
        magnitude_a = np.linalg.norm(vector_a)
        magnitude_b = np.linalg.norm(vector_b)

        if magnitude_a == 0 or magnitude_b == 0:
            return 0

        cosine_similarity_value = dot_product / (magnitude_a * magnitude_b)
        return cosine_similarity_value

    def compare_faces(self, video_face_encodings):
        similarities = []
        student_names = []
        csm_students = list(self.students.keys())

        for y in video_face_encodings:
            nec = [self.cosine_similarity(y, x) for x in self.known_face_encodings]
            similarities.append(nec)

        for x in similarities:
            student_names.append(csm_students[np.argmax(x)])

        return list(set(student_names))


#sample usage
'''fc = FaceRecognition('/content/Frames','/content/original_encodings.pkl')
paths = fc.load_image_paths()
fc.find_faces(paths)
with open('/content/video_face_encodings.pkl', 'rb') as file:
  video_face_encodings = pickle.load(file)
fc.compare_faces(video_face_encodings)'''