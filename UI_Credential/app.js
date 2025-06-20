const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const cookieParser = require('cookie-parser');
const path = require('path');
const User = require('./models/User');
require('dotenv').config();

const app = express();
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

// Connect to MongoDB Atlas
mongoose
  .connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB Atlas'))
  .catch((err) => console.error('MongoDB connection error:', err));

// Routes
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'views', 'signup.html')));
app.get('/login', (req, res) => res.sendFile(path.join(__dirname, 'views', 'login.html')));
app.get('/welcome', (req, res) => {
    const username = req.cookies.username;
    if (!username) return res.redirect('/login');
    res.sendFile(path.join(__dirname, 'views', 'welcome.html'));
});

// Signup Route
app.post('/signup', async (req, res) => {
    const { username, email, password } = req.body;
    try {
        // Check if the username or email already exists
        const existingUser = await User.findOne({ $or: [{ username }, { email }] });
        if (existingUser) {
            return res.send('Username or email already exists. Please choose a different one.');
        }

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Save the user
        const user = new User({ username, email, password: hashedPassword });
        await user.save();

        res.redirect('/login');
    } catch (err) {
        console.error(err);
        res.send('Error signing up. Please try again.');
    }
});


// Login Route
app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    try {
        const user = await User.findOne({ email });
        if (!user || !(await bcrypt.compare(password, user.password))) {
            return res.send('Invalid email or password.');
        }
        res.cookie('username', user.username);
        res.redirect('/welcome');
    } catch (err) {
        console.error(err);
        res.send('Error logging in. Please try again.');
    }
});

app.listen(process.env.PORT, () => console.log(`Server running on port http://localhost:${process.env.PORT}`));
