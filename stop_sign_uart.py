import cv2
import time
import threading
import os
import serial

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

stop_cascade = cv2.CascadeClassifier('stop_sign_classifier.xml')

if not os.path.exists("data"):
    os.makedirs("data")

sending_stop_signal = False
image_counter = 0

last_zero_print_time = 0
zero_print_interval = 0.5  # seconds

# To keep track of when stop signal started
stop_signal_end_time = 0

def send_stop_signal(frame):
    global sending_stop_signal, image_counter, stop_signal_end_time
    sending_stop_signal = True
    stop_signal_end_time = time.time() + 3  # Mark end time for 3 seconds

    print("🚦 Stop sign detected! Simulating sending '1' to Arduino...")

    filename = f"data/stop_frame_{int(time.time())}_{image_counter}.jpg"
    cv2.imwrite(filename, frame)
    print(f"🖼️  Image saved: {filename}")
    image_counter += 1

    # Simulate sending '1' for 3 seconds
    while time.time() < stop_signal_end_time:
        arduino.write(b'1')
        time.sleep(0.1)

    sending_stop_signal = False
    print("✅ Done simulating sending '1'. Resuming sending '0' to Arduino...")

def send_zero_signal():
    global last_zero_print_time
    now = time.time()
    if now - last_zero_print_time > zero_print_interval:
        print("Sending '0' to Arduino (keep moving)")
        last_zero_print_time = now

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stops = stop_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        current_time = time.time()

        # Show rectangle if detected
        if len(stops) > 0 and not sending_stop_signal:
            for (x, y, w, h) in stops:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            # Start stop signal thread with saved frame copy
            frame_copy = frame.copy()
            threading.Thread(target=send_stop_signal, args=(frame_copy,)).start()

        # Overlay text if within stop signal duration
        if current_time < stop_signal_end_time:
            cv2.putText(frame, "Stop Sign Detected", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            # If not sending stop, send zero signal periodically
            if not sending_stop_signal:
                send_zero_signal()
                arduino.write(b'0')

        cv2.imshow("Stop Sign Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("🛑 Interrupted by user.")

finally:
    cap.release()
    arduino.close()
    cv2.destroyAllWindows()
    print("Program ended. Released camera and closed all windows.")
