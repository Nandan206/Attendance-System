# Smart Attendance System

## Project Overview
The Smart Attendance System is a barcode-based attendance tracking application that simplifies attendance management. Using a Python script for barcode scanning and a web-based admin dashboard, this project enables efficient attendance marking and monitoring for educational institutions. 

## Key Features
- **Barcode-based Attendance Tracking**: Scans barcodes with a camera and marks attendance automatically.
- **Admin Dashboard**: Provides a user-friendly interface to view, search, and manage attendance records in real-time.
- **Database Integration**: MongoDB Atlas database to store and manage attendance records securely in the cloud.
- **Automated Notifications**: AWS SES integration to send email notifications if required.

## Tools and Technologies Used
- **Languages**: Python (OpenCV, PyZbar), JavaScript (Node.js, Express.js)
- **Frontend**: EJS for templating, HTML, CSS for styling
- **Backend**: MongoDB Atlas for database, Mongoose for data handling, Node.js for server
- **Other**: AWS SES for email notifications (optional)

---

## System Architecture
1. **Barcode Scanning Module**: The `hack.py` script, written in Python, uses OpenCV and PyZbar to capture barcode data and sends it to MongoDB via the server.
2. **Admin Dashboard**: Built with Express.js and rendered with EJS, it allows the admin to view and manage attendance data, including marking students as "present" or "absent."
3. **Database**: MongoDB Atlas cloud database hosts attendance data, making it accessible from anywhere.
4. **Notification System**: AWS SES can be configured to send attendance notifications.

---

## Getting Started

### Prerequisites
Ensure the following are installed on your system:
- **Node.js and npm** (for server and frontend dependencies)
- **Python 3.x** (for barcode processing)
- **MongoDB Atlas** (cloud database)
- **AWS SES Account** (optional for email notifications)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nandan206/smart-attendance-system.git
   cd smart-attendance-system
2. **Install Node Dependencies**:
   ```bash
   npm install
3. **Install Python Dependencies**:
   ```bash
   pip install opencv-python pyzbar pymongo
   
## Set Up MongoDB:

1. Create a MongoDB Atlas account and set up a cluster.
2. Replace the MongoDB connection URI in app.js with your database URI.
   
## Environment Configuration:

Create a .env file (use .env.example as a template) and add your MongoDB URI, AWS SES credentials (if using), and other sensitive information.

## Running the Application
Run Barcode Scanner:
**Start the barcode scanning script to capture attendance using the camera**.

```bash
python hack.py

├── public                 # Contains CSS and client-side assets
│   └── styles
│       └── loginsty.css   # Styling for the login page
├── views                  # Contains EJS templates
│   └── admin.ejs          # Template for the admin dashboard
├── app.js                 # Main server file
├── hack.py                # Barcode scanning script
├── package.json           # Node dependencies
└── README.md              # Project documentation
