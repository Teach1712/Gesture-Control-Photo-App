
# Import required libraries
import cv2  # OpenCV for video capture and image processing
import mediapipe as mp  # MediaPipe for hand tracking
import time  # For timing and debouncing
import numpy as np  # For image filter operations


# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils


# List of available filters
FILTERS = [None, 'GRAYSCALE', 'SEPIA', 'NEGATIVE', 'BLUR']
current_filter = 0  # Index of the current filter


# Open webcam for video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()


# Gesture timing and state variables
last_action_time = 0  # Last time a filter was changed
DEBOUNCE_TIME = 1    # Minimum seconds between filter changes
pinch_in_progress = False  # Tracks if pinch gesture is ongoing
capture_request = False    # Set to True when a photo should be captured


def apply_filter(frame, ftype):
    """
    Apply the specified filter to the frame.
    :param frame: Input image frame (BGR)
    :param ftype: Filter type as string or None
    :return: Filtered image
    """
    if ftype == 'GRAYSCALE':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif ftype == 'SEPIA':
        # Sepia filter matrix
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        return np.clip(cv2.transform(frame, sepia_filter), 0, 255).astype(np.uint8)
    elif ftype == 'NEGATIVE':
        return cv2.bitwise_not(frame)
    elif ftype == 'BLUR':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    return frame  # No filter


# Main loop: process webcam frames
while True:
    success, img = cap.read()  # Read a frame from the webcam
    if not success:
        print("Failed to read frame.")
        break
    img = cv2.flip(img, 1)  # Mirror the image for natural interaction
    h, w = img.shape[:2]
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
    results = hands.process(img_rgb)  # Detect hands
    capture_request = False  # Reset capture flag each frame

    # If hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)  # Draw hand skeleton
            lm = hand.landmark
            # Build a dictionary of finger tip pixel coordinates
            tips = {name: (int(lm[idx].x * w), int(lm[idx].y * h))
                    for name, idx in {
                        'thumb': mp_hands.HandLandmark.THUMB_TIP,
                        'index': mp_hands.HandLandmark.INDEX_FINGER_TIP,
                        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                        'ring': mp_hands.HandLandmark.RING_FINGER_TIP,
                        'pinky': mp_hands.HandLandmark.PINKY_TIP
                    }.items()}
            # Draw a colored circle at each fingertip
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
            for i, (name, (x, y)) in enumerate(tips.items()):
                cv2.circle(img, (x, y), 10, colors[i], cv2.FILLED)

            # Get coordinates for thumb and index fingertips
            thumb_x, thumb_y = tips['thumb']
            index_x, index_y = tips['index']
            current_time = time.time()

            # --- Gesture 1: Pinch (thumb + index) to capture photo ---
            pinch = abs(thumb_x - index_x) < 30 and abs(thumb_y - index_y) < 30
            if pinch and not pinch_in_progress:
                pinch_in_progress = True
                capture_request = True  # Trigger photo capture
            if not pinch and pinch_in_progress:
                pinch_in_progress = False  # Reset pinch state

            # --- Gesture 2: Thumb + middle/ring/pinky to change filter ---
            elif any(abs(thumb_x - tips[finger][0]) < 30 and abs(thumb_y - tips[finger][1]) < 30
                     for finger in ['middle', 'ring', 'pinky']):
                # Debounce to avoid rapid filter changes
                if current_time - last_action_time > DEBOUNCE_TIME:
                    current_filter = (current_filter + 1) % len(FILTERS)
                    last_action_time = current_time
                    print("Filter changed to:", FILTERS[current_filter] or "None")
            break  # Only process the first detected hand per frame

    # Apply the selected filter to the frame
    filtered_img = apply_filter(img, FILTERS[current_filter])
    # If grayscale, convert back to BGR for display
    display_img = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR) if FILTERS[current_filter]=='GRAYSCALE' else filtered_img

    # If a capture was requested, save the image and show feedback
    if capture_request:
        cv2.putText(display_img, "Picture Captured!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        ts = int(time.time())
        cv2.imwrite(f"picture_{ts}.jpg", display_img)
        print(f"Saved: picture_{ts}.jpg")

    # Show the webcam feed with overlays
    cv2.imshow("Gesture-Controlled Photo App", display_img)
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

