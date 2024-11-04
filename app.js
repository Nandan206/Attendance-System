const express = require('express');
const mongoose = require('mongoose');
const path = require('path');

// Initialize Express app
const app = express();

// Set the view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files (CSS)
app.use(express.static(path.join(__dirname, 'public')));

// MongoDB connection string
const uri = 'mongodb+srv://nand:321nandan@cluster0.cfdbh.mongodb.net/attendance?retryWrites=true&w=majority&appName=Cluster0';

// Connect to MongoDB Atlas
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error('MongoDB connection error:', err));

// Define a Student model
const studentSchema = new mongoose.Schema({
    _id: String,
    name: String,
    attendance: [
        {
            date: String,
            status: String,
            time: String,
        }
    ]
});
const Student = mongoose.model('Student', studentSchema);

// Main route to fetch attendance data and render HTML
app.get('/admin', async (req, res) => {
    try {
        const students = await Student.find();

        let total_students = students.length;
        let present_today = 0;
        let absent_today = 0;

        const current_date = new Date().toISOString().split('T')[0]; // Get current date in 'YYYY-MM-DD' format

        // Process students attendance data
        students.forEach(student => {
            const attendance = student.attendance || [];
            const last_record = attendance[attendance.length - 1] || {};
            if (last_record.date === current_date && last_record.status === 'present') {
                present_today++;
            } else {
                absent_today++;
            }
        });

        // Render the 'admin.ejs' template and pass the data to it
        res.render('admin', { total_students, present_today, absent_today, students });
    } catch (err) {
        res.status(500).send('Error fetching data: ' + err.message);
    }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
