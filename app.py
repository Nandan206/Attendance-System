from flask import Flask, render_template
from pymongo import MongoClient
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://nand:321nandan@cluster0.cfdbh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['attendance']
collection = db['students']

# Your route and logic here...
@app.route('/admin')
def admin():
    try:
        # Fetch all student data from the 'students' collection
        students = collection.find()

        # Initialize counts
        total_students = 0
        present_today = 0
        absent_today = 0

        # Get today's date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Process the student data
        students_list = []
        for student in students:
            total_students += 1
            attendance = student.get('attendance', [])

            if attendance:
                last_record = attendance[-1]
                if last_record.get('date') == current_date and last_record.get('status') == 'present':
                    present_today += 1
                else:
                    absent_today += 1
            else:
                absent_today += 1

            student_data = {
                'id': student['_id'],
                'name': student.get('name', 'Unknown'),
                'attendance': attendance
            }
            students_list.append(student_data)

        return render_template(
            'login.html',
            students=students_list,
            total_students=total_students,
            present_today=present_today,
            absent_today=absent_today
        )
    except Exception as e:
        return f"Error fetching data: {e}"

if __name__ == '__main__':
    app.run(debug=True)
