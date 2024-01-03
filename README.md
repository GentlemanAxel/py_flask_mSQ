# py_flask_mSQ (mathSymbolsQuiz)

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
## In dev project 🏗️
## mathSymbolsQuiz use python with a flask interface.

---

## Overview

"py_flask_mSQ" is a Flask-based web application designed for enhancing users' mathematical symbol comprehension through an interactive quiz format. 
The application incorporates user authentication, an administrative panel, and statistical tracking features. 
Users can register, log in, and explore a variety of mathematical symbols through a testing module, gaining or losing points based on their accuracy. 
The application also includes an admin panel to manage user bans, a complaint submission feature, and a statistics page to showcase user scores and ranks.

---

## Main Features (not all are implemented yet)

- User Authentication: Users can register, log in, and log out securely. Passwords are hashed for security using the SHA-256 algorithm.

- Symbol Quiz: The application offers an interactive quiz to test users' knowledge of mathematical symbols. Users receive points based on their correct answers, and their progress is tracked.

- Admin Panel: Administrators can access a dedicated panel for user management. This includes the ability to ban and unban users, view user scores, and access statistical information.

- User Bans: Administrators can impose temporary bans on users, specifying the reason for the ban and its duration. Banned users are redirected to a personalized page.

- Complaint Submission: Users can submit complaints through the application. Administrators can review and address these complaints through a designated section.

- Statistics Page: Users can view their own scores and ranks in comparison to other users. The statistics page provides insights into the overall performance of users.

- Secure Database Storage: User data, including usernames, hashed passwords, scores, and ban statuses, is stored securely in an SQLite database.

- Flask Extensions: The application utilizes Flask extensions such as Flask-SQLAlchemy for efficient database management, Flask-Login for user session management, and Flask-WTF for form handling.

- Web-based Interface: The user interface is implemented using HTML templates, providing a clean and intuitive design.

- Interactive Testing Feedback: Users receive immediate feedback during the symbol quiz, informing them whether their answers are correct and providing the correct symbol if needed.

---

## Usage

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/GentlemanAxel/py_flask_mSQ.git
    ```

2. Navigate to the project directory:

    ```bash
    cd py_flask_mSQ
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    
### Run the Application

```bash
python quiz.py
```
Access the application in your web browser at http://127.0.0.1:5000/.

---


### Example Usage
1. Open the web browser and go to http://127.0.0.1:5000/.
2. Create an account.
3. Return on the main menu.
4. Play !

### Credits

<a href='https://github.com/GentlemanAxel' target="_blank"><img alt='GitHub' src='https://img.shields.io/badge/GentlemanAxel-100000?style=for-the-badge&logo=GitHub&logoColor=white&labelColor=black&color=CA2C2C'/></a>
