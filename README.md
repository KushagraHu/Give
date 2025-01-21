# Give
# College Feedback System

## Overview

The **College Feedback System** is a user-friendly application built with Python using SQLite and Tkinter. It enables students to submit feedback about various aspects of their college and allows admins to view and manage the feedback. Additionally, the app fetches inspirational quotes for motivation. This project is designed as a "mini-project" to showcase skills in Python, GUI development, and database management.

---

## Features

### 1. User Roles:

- **Student**: Can create an account, log in, and submit feedback.
- **Admin**: Has access to view and clear all submitted feedback.

### 2. Feedback Categories:

- Environment
- Infrastructure
- Faculty
- Hostel
- Library
- Playground
- Fest

### 3. Additional Functionalities:

- **Inspirational Quotes**: Fetch random motivational quotes via API.
- **Data Management**: Admin can clear all feedback data from the dashboard.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/college-feedback-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd college-feedback-system
   ```
3. Install required dependencies:
   ```bash
   pip install requests
   ```
4. Run the application:
   ```bash
   python app.py
   ```

---

## Usage

### Initial Setup

- On the first run, the database will initialize automatically with a default admin account:
  - **Username**: `admin`
  - **Password**: `admin123`

### Functionality

#### For Students:

1. Create an account with the "student" role.
2. Log in to submit feedback across various categories.
3. Explore motivational quotes in the "Inspirational Quotes" section.

#### For Admins:

1. Log in with the "admin" role.
2. View all feedback in the admin dashboard.
3. Use the **Clear All Feedback** button to delete all feedback records.

---

## Code Structure

- **app.py**: Main application file.
- **college\_feedback.db**: SQLite database file (auto-created on first run).

---

## Video Demonstration

### Description for LinkedIn Post:

"🚀 Excited to share my mini-project: **College Feedback System**! Built using Python, SQLite, and Tkinter, this project allows students to provide feedback and admins to manage it seamlessly. Additionally, the app fetches inspirational quotes for some extra motivation. Watch the demo to see it in action! 💻✨

✅ User Roles (Student/Admin)
✅ Feedback Management
✅ Inspirational Quotes API Integration
✅ Admin Dashboard with Clear Data Button

\#Python #SQLite #Tkinter #Programming #CollegeProjects #MiniProject"

---

## License

This project is licensed under the MIT License.

---

## Screenshots

Include screenshots showing:

1. Login Page
2. Feedback Submission Page
3. Admin Dashboard
4. Inspirational Quotes Section

                                                                :) Kushagra
