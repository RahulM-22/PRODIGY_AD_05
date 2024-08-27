import cv2
from pyzbar import pyzbar
import webbrowser

# Function to decode QR codes
def decode_qr_code(frame):
    # Find and decode QR codes in the frame
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        # Extract the data from the QR code
        qr_data = obj.data.decode("utf-8")
        # Draw a rectangle around the QR code in the frame
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Put the QR code data as text on the frame
        cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Return the data
        return qr_data
    return None

# Function to handle the main QR code scanning process
def scan_qr_code():
    # Open the default camera
    cap = cv2.VideoCapture(0)
    scanned_data = None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Decode the QR code in the current frame
        scanned_data = decode_qr_code(frame)

        # Display the resulting frame
        cv2.imshow("QR Code Scanner", frame)

        # If data is scanned, display it and ask for further action
        if scanned_data:
            print(f"Scanned Data: {scanned_data}")
            cv2.destroyAllWindows()
            cap.release()
            
            # Ask the user for further action
            action = input(f"Scanned Data: {scanned_data}\nChoose an action:\n1. Open in browser\n2. Save to file\n3. Scan again\n4. Quit\n")
            if action == '1':
                webbrowser.open(scanned_data)
                break
            elif action == '2':
                with open("scanned_qr_code.txt", "a") as f:
                    f.write(scanned_data + "\n")
                print("Data saved to scanned_qr_code.txt")
                break
            elif action == '3':
                scanned_data = None
                cap = cv2.VideoCapture(0)
            elif action == '4':
                break

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# Run the QR code scanner
if __name__ == "__main__":
    scan_qr_code()
