
import math
import cv2
import mediapipe as mp
import math
from touch_emulation import move_cursor, make_touch
from touch_manager import TouchManager

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

input_state_holding = False 
mouse_down = False
mouse_up = False 
draging = False
touch_manager = 0

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=1, # 0
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
      
      # Check distance between  [4: THUMB_TIP] and [8: INDEX_FINGER_TIP]
      
      # if less than x fire touch event 
      
      # a hand, a thumb, x position
      #hand_landmarks.landmark[4].x 
      #print("x: " + hand_landmarks.landmark[4].x + "\n" + "y: ",  hand_landmarks.landmark[4].y) 
      #print("y: ",  hand_landmarks.landmark[4].y ) 
      x=int(1920 - (hand_landmarks.landmark[4].x * 1920))
      y=int(hand_landmarks.landmark[4].y * 1080)

      
      



      # Truth value must be relative to palm size and distance to camera 
      dist = math.hypot(
        hand_landmarks.landmark[8].x - hand_landmarks.landmark[4].x,
        hand_landmarks.landmark[8].y - hand_landmarks.landmark[4].y
      )


      if (mouse_down):
        if dist > 0.1:
          mouse_down = False
          # fire a mouse up event 
          touch_manager.release_touch()
        else:
          draging = True
          # fire a drag event 
          touch_manager.drag_update(x,y)
      else:
        move_cursor(x=x, y=y)
        if dist < 0.1:
          mouse_down = True
          # Fire a mouse down event 
          touch_manager = TouchManager(x,y)


        # make_touch(
        #   x=int(1920 - (hand_landmarks.landmark[4].x * 1920)), 
        #   y=int(hand_landmarks.landmark[4].y * 1080),
        #   fingerRadius=4
        # )



      # To improve accuracy 
      # - take confidence into account 
      # - smooth over time
      # - account for missing frames 
      # - account for momentary glitches 

      #image = cv2.flip(image, 1)
      image = cv2.putText(
        image, "state: " + str(dist), 
        (50,50), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (255, 0, 0) if dist > 0.1 else (0, 255, 0), 
        2, 
        cv2.LINE_AA
      )


    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()