import cv2
from pyzbar import pyzbar
from pymongo import MongoClient

# MongoDB setup
try:
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB connection string if different
    db = client['qr_database']
    collection = db['qr_codes']
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Dictionary to store QR code data and their "present" status
qr_code_status = {}

def decode_qr(frame):
    # Find QR codes in the frame
    qr_codes = pyzbar.decode(frame)
    
    # List to store decoded QR code data
    qr_data_list = []

    # Loop over the detected QR codes
    for qr_code in qr_codes:
        # Extract the bounding box location of the QR code and draw a rectangle around it
        (x, y, w, h) = qr_code.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Decode the QR code data and draw it on the frame
        qr_data = qr_code.data.decode('utf-8')
        qr_type = qr_code.type
        text = f'{qr_data} ({qr_type})'
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Add the QR code data to the list
        qr_data_list.append(qr_data)

        # Check if the QR code exists in the database
        qr_document = collection.find_one({'qr_data': qr_data})
        if qr_document:
            # If present in database, update the status to "marked as present"
            collection.update_one({'qr_data': qr_data}, {'$set': {'status': 'present'}})
            qr_code_status[qr_data] = True
            print(f"QR Code {qr_data} marked as present.")
        else:
            qr_code_status[qr_data] = False
            print(f"QR Code {qr_data} is not recognized.")

    return frame, qr_data_list

def main():
    # Initialize the video stream
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Decode QR codes in the frame
        frame, qr_data_list = decode_qr(frame)

        # Print the QR code data
        if qr_data_list:
            for qr_data in qr_data_list:
                print(f"QR Code Data: {qr_data} - Status: {'Present' if qr_code_status[qr_data] else 'Not Recognized'}")

        # Display the frame
        cv2.imshow('QR Code Scanner', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
