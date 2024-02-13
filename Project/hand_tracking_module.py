import cv2
import mediapipe as mp
import numpy as np
import time     # check framerate

from typing import Union


webcam_image = np.ndarray
confidence = float
coords_vector = Union[int, list[int]]
rgb_tuple = tuple[int, int, int]
# =========================


# Class ===================
class VanzeDetector():
    def __init__(self, 
                    mode: bool = False, 
                    number_hands: int = 2, 
                    model_complexity: int = 1,
                    min_detec_confidence: confidence = 0.5, 
                    min_tracking_confidence: confidence = 0.5
                ):
        
        # Parametros necessário para inicializar o hands -> solução do mediapipe
        self.mode = mode
        self.max_num_hands = number_hands
        self.complexity = model_complexity
        self.detection_con = min_detec_confidence
        self.tracking_con = min_tracking_confidence

        # Inicializando o hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,
                                        self.max_num_hands,
                                        self.complexity,
                                        self.detection_con,
                                        self.tracking_con)    
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, 
                    img: webcam_image, 
                    draw_hands: bool = True):
        # Correção de cor
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Coletando resultados do processo das hands e analisando-os
        self.results = self.hands.process(img_RGB)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw_hands:
                    self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)  

        return img

    def find_position(self, 
                        img: webcam_image, 
                        hand_number: int = 0, 
                        draw_hands: bool = True):
        self.required_landmark_list = []
        
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(my_hand.landmark):
                height, width, channels = img.shape
                center_x, center_y = int(lm.x*width), int(lm.y*height)

                self.required_landmark_list.append([id, center_x, center_y])  

                # if draw_hands:
                #     # if id==8:
                #     cv2.circle(img, (center_x, center_y), 10, (255, 0, 0), cv2.FILLED)

        return self.required_landmark_list

    def fingers_up(self):
      
        fingers = []

        # dedão - analisado diferente por que o dedão se comporta de maneira diferente. Não desce no eixo y que nem os outros dedos
        if self.required_landmark_list[self.tip_ids[0]][1] > self.required_landmark_list[self.tip_ids[0] - 1][1]: fingers.append(1)
        else: fingers.append(0)

        # Para os outros 4 dedos
        for id in range(1, 5):
            if self.required_landmark_list[self.tip_ids[id]][2] < self.required_landmark_list[self.tip_ids[id] - 2][2]: fingers.append(1)
            else: fingers.append(0)

        return fingers

    def draw_in_position(self,
                            img: webcam_image,
                            x_vector: coords_vector, 
                            y_vector: coords_vector,
                            rgb_selection: rgb_tuple = (255, 0, 0),
                            thickness: int = 10):
        x_vector = x_vector if type(x_vector) == list else [x_vector]
        y_vector = y_vector if type(y_vector) == list else [y_vector]

        for x, y in zip(x_vector, y_vector):
            cv2.circle(img, (x, y), thickness, rgb_selection, cv2.FILLED)

        return img
        
# Main ==================== para teste de classe
def main():
    # coletando o framerate e capturando o vídeo
    previous_time = 0
    current_time = 0
    capture = cv2.VideoCapture(0)

    Vanze = VanzeDetector()

    while True:
        success, img = capture.read()
        
        img = Vanze.find_hands(img) #, draw_hands=False)
        landmark_list = Vanze.find_position(img) #, draw_hands=False)
        if landmark_list:
            print(landmark_list[8])

        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,255), 3)
        # cv2.putText(material, texto, localização, fonte, fontScale, cor, thickness)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
