import cv2
import time
import numpy as np
import gc
import serial
import threading

# Initialize serial communication with Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
arduino.flush()

# Parameters
num_cols = 3
num_rows = 2
resolution = (80, 60)
motion_threshold = 500
threshold_calm = 1.5    # Motion intensity for calm
threshold_erratic = 4.0 # Motion intensity for erratic
cache_clear_interval = 10
frame_skip = 15         # Skip more frames to reduce load
observe_duration = np.random.randint(10, 20)   # Random duration in OBSERVE state
movement_duration = np.random.randint(15, 30)  # Random duration in movement states
transition_duration = 2 # Time in TRANSITION state

# State Variables
states = ["SILENT", "OBSERVE", "ERRATIC", "CALM", "BREATHING", "TRANSITION"]
current_state = "SILENT"
last_state_change = time.time()
motion_history = []
max_history = 10
frame_count = 0
last_cache_clear_time = time.time()
state_changed = False
smoothed_intensity = 0.0  # Default value for motion intensity

# Shared frame variable for threading
frame = None
frame_lock = threading.Lock()

# Capture frames in a separate thread
def capture_frames():
    global frame
    cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    cap.set(cv2.CAP_PROP_FPS, 15)

    while True:
        ret, temp_frame = cap.read()
        if ret:
            with frame_lock:
                frame = cv2.cvtColor(cv2.resize(temp_frame, resolution), cv2.COLOR_BGR2GRAY)
        else:
            print("Error: Unable to read frame!")
            break
    cap.release()

capture_thread = threading.Thread(target=capture_frames, daemon=True)
capture_thread.start()

# Helper function for state transition
def change_state(new_state):
    global current_state, last_state_change, state_changed
    if current_state != new_state:
        print(f"State Change: {current_state} → {new_state}")
        current_state = new_state
        last_state_change = time.time()
        state_changed = True

# Apply a noise filter to ignore minor changes
def apply_noise_filter(thresh):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

try:
    prev_gray = None
    while True:
        with frame_lock:
            if frame is None:
                continue
            gray = frame.copy()

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        diff = None
        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(cv2.GaussianBlur(diff, (5, 5), 0), 20, 255, cv2.THRESH_BINARY)

            # Apply noise filter
            thresh = apply_noise_filter(thresh)

            # Motion intensity calculation
            total_pixels = gray.size
            motion_intensity = np.sum(thresh) / 255 / total_pixels * 100
            motion_history.append(motion_intensity)
            if len(motion_history) > max_history:
                motion_history.pop(0)
            smoothed_intensity = sum(motion_history) / len(motion_history)

            # Debugging motion intensity
            print(f"Smoothed Motion Intensity: {smoothed_intensity:.2f}, Current State: {current_state}")

            # State machine logic
            if current_state == "SILENT" and smoothed_intensity > 0:
                change_state("OBSERVE")

            elif current_state == "OBSERVE":
                if time.time() - last_state_change >= observe_duration:
                    if smoothed_intensity > threshold_erratic:
                        change_state("ERRATIC")
                    elif smoothed_intensity > threshold_calm:
                        change_state("CALM")
                    else:
                        change_state("BREATHING")

            elif current_state in ["ERRATIC", "CALM", "BREATHING"]:
                if time.time() - last_state_change >= movement_duration:
                    change_state("TRANSITION")

            elif current_state == "TRANSITION":
                if time.time() - last_state_change >= transition_duration:
                    arduino.write(("IDLE\n").encode())  # Stop the servo
                    change_state("SILENT")

            # Send current state to Arduino only when it changes
            if state_changed:
                arduino.write((current_state + '\n').encode())
                state_changed = False

        prev_gray = gray.copy()

        # Cache clearing
        if time.time() - last_cache_clear_time > cache_clear_interval:
            gc.collect()
            last_cache_clear_time = time.time()

        # Visualize motion detection
        display_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for col in range(num_cols):
            for row in range(num_rows):
                x_start = col * (resolution[0] // num_cols)
                y_start = row * (resolution[1] // num_rows)
                x_end = x_start + (resolution[0] // num_cols)
                y_end = y_start + (resolution[1] // num_rows)

                # Check motion detection
                color = (0, 255, 0) if smoothed_intensity > threshold_calm else (0, 0, 255)

                cv2.rectangle(display_frame, (x_start, y_start), (x_end, y_end), color, 1)

        cv2.imshow("Motion Detection", display_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nMotion detection stopped manually.")

cv2.destroyAllWindows()
arduino.close()
