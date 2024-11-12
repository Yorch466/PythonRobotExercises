import cv2
import mediapipe as mp
import pyautogui
import math

# Inicialización de MediaPipe y detección de manos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Obtener el tamaño de la pantalla para el mapeo de coordenadas
screen_width, screen_height = pyautogui.size()

# Inicialización de la cámara
cap = cv2.VideoCapture(0)

# Variable para rastrear el estado del clic
clicked = False

try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Invertir la imagen horizontalmente para efecto espejo
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        # Obtener el tamaño del cuadro de la cámara
        frame_height, frame_width, _ = image.shape

        # Verificar si se detectan manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibuja las conexiones de la mano en la imagen
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Obtener la posición de la punta del dedo índice (landmark 8) y del pulgar (landmark 4)
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Convertir coordenadas normalizadas a píxeles en el marco de la cámara
                x = int(index_finger_tip.x * frame_width)
                y = int(index_finger_tip.y * frame_height)

                # Mapeo de la posición del dedo a la posición de la pantalla
                screen_x = int((index_finger_tip.x) * screen_width)
                screen_y = int((index_finger_tip.y) * screen_height)

                # Mover el puntero del ratón a la posición mapeada
                pyautogui.moveTo(screen_x, screen_y)

                # Visualización de la posición del dedo índice
                cv2.circle(image, (x, y), 10, (255, 0, 255), -1)

                # Calcular la distancia entre la punta del índice y la punta del pulgar
                thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
                distance = math.hypot(x - thumb_x, y - thumb_y)

                # Si la distancia es pequeña, realizar un clic
                if distance < 40:
                    if not clicked:
                        pyautogui.click()
                        clicked = True  # Cambiar estado a "clic realizado"
                        cv2.circle(image, (x, y), 15, (0, 255, 0), -1)  # Dibujar círculo verde en la punta del dedo índice
                else:
                    clicked = False  # Cambiar estado a "clic no realizado"

        # Mostrar la imagen en una ventana
        cv2.imshow('Control de Ratón con MediaPipe', image)

        # Presionar 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Liberar los recursos
    cap.release()
    cv2.destroyAllWindows()
    hands.close()