import cv2
from pyzbar import pyzbar
from pymongo import MongoClient
from datetime import datetime
import warnings
import os
import sys

# Suppress all pyzbar warnings globally
warnings.filterwarnings('ignore')

# Redirect stderr (where pyzbar warnings go) to os.devnull to suppress output
sys.stderr = open(os.devnull, 'w')

# MongoDB setup
client = MongoClient('mongodb+srv://nand:321nandan@cluster0.cfdbh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['attendance']
collection = db['students']

def mark_as_present_mongodb(barcode_data: str) -> None:
    """Mark a barcode as present in the MongoDB collection."""
    try:
        # Find the student based on barcode (ID)
        barcode_document = collection.find_one({'_id': barcode_data})
        if not barcode_document:
            print(f"Barcode {barcode_data} not found in MongoDB.")
            return
        
        # Ensure 'attendance' field is an array, initialize if not
        if 'attendance' not in barcode_document or not isinstance(barcode_document['attendance'], list):
            collection.update_one(
                {'_id': barcode_data},
                {'$set': {'attendance': []}}
            )
            print(f"Initialized 'attendance' field as an array for {barcode_data}.")

        # Get the current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Check if there's already an attendance entry for today
        attendance_exists = collection.find_one({
            '_id': barcode_data,
            'attendance.date': current_date
        })

        if attendance_exists:
            print(f"Attendance for {barcode_data} already marked today.")
        else:
            # Insert a new attendance entry with date and time
            collection.update_one(
                {'_id': barcode_data},
                {
                    '$push': {
                        'attendance': {
                            'date': current_date,
                            'status': 'present',
                            'time': datetime.now().strftime('%H:%M:%S')
                        }
                    }
                }
            )
            print(f"Attendance for {barcode_data} marked as present.")
    except Exception as e:
        print(f"Error updating barcode in MongoDB: {e}")

def decode_barcode(frame):
    """Decode barcodes from the video frame."""
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        (x, y, w, h) = barcode.rect
        
        # Draw a rectangle around the barcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Mark attendance in MongoDB
        mark_as_present_mongodb(barcode_data)

    return frame

def main():
    """Main function for video capture and barcode scanning."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return
    
    print("Video capture started successfully. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Decode barcodes from the frame
        frame = decode_barcode(frame)

        # Show the processed video frame
        cv2.imshow('Barcode Scanner', frame)

        # Quit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting barcode scanner.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

# Reset stderr to default after the program finishes
sys.stderr = sys.stderr