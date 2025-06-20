import cv2
import time
import threading
import os
# import serial


# arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Load Haar Cascade Classifier
stop_cascade = cv2.CascadeClassifier('stop_sign_classifier.xml')

if not os.path.exists("data"):
    os.makedirs("data")

# Flag for sending signal
sending_stop_signal = False
image_counter = 0  # To save images uniquely

# Sending a stop signal to the Arduino
def send_stop_signal(frame):
    global sending_stop_signal, image_counter
    sending_stop_signal = True

    print("🚦 Stop sign detected! Simulating '1' signal...")

    # Save detected frame as an image
    filename = f"data/stop_frame_{int(time.time())}_{image_counter}.jpg"
    cv2.imwrite(filename, frame)
    print(f"🖼️  Image saved: {filename}")
    image_counter += 1

    # Simulate signal for 3 seconds
    end_time = time.time() + 3
    while time.time() < end_time:
        # arduino.write(b'1')
        time.sleep(0.1)

    sending_stop_signal = False
    print("✅ Done simulating stop. Resume '0'.")

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stops = stop_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(stops) > 0 and not sending_stop_signal:
            for (x, y, w, h) in stops:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            # Start stop-signal simulation and image save
            frame_copy = frame.copy() 
            threading.Thread(target=send_stop_signal, args=(frame_copy,)).start()

        # if not sending_stop_signal:
        #     arduino.write(b'0')

        cv2.imshow("Stop Sign Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("🛑 Interrupted by user.")

finally:
    cap.release()
    # arduino.close()
    cv2.destroyAllWindows()
