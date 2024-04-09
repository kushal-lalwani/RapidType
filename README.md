# RapidType

RapidType is a web application designed to improve your typing speed and accuracy. It provides various typing tests and visualizations to track your progress.

## Features

- **Multiple Text Types**: Choose from different types of text prompts such as normal words, punctuation, and rows of keys.
- **Real-time Feedback**: Receive immediate feedback on your typing accuracy as you type.
- **Graphical Representation**: Visualize your typing speed over time with interactive graphs.
- **User Authentication**: Secure user authentication system for signing up, logging in, and managing user profiles.
- **Leaderboard**: View the leaderboard to see top performers based on typing speed and accuracy.
- **Profile Page**: Track your typing test history and monitor your progress over time.

## Usage

1. **Signup/Login**: Optionally Create an account or login to access the typing tests and other features.
2. **Start Typing Test**: Select a text type and test time, then start typing the provided text prompt to automatically start the test.
3. **Receive Feedback**: Get real-time feedback on your typing accuracy and speed as you type.
4. **View Results**: After completing the test, view your typing speed (WPM) and accuracy.
5. **Track Progress**: Monitor your typing test history and track your progress on the profile page.
6. **Explore Leaderboard**: Check the leaderboard to see top performers and compare your results.

## Technologies Used

- **Django**: Backend framework for handling server-side logic and database management.
- **JavaScript**: Used for client-side scripting to create interactive features and handle user interactions.
- **Plotly**: Library for generating interactive graphs and visualizations.
- **HTML/CSS/Bootstrap**: Frontend technologies for designing and styling the user interface.

## Setup

To set up RapidType locally, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Run the development server: `python manage.py runserver`
5. Access RapidType in your web browser at your localhost
