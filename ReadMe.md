

***

# TeamUp: Collaborative Project Matchmaker

## Overview

**TeamUp** is a web platform that helps people form teams, work together on projects, and organize tasks visually. Users can sign up, create profiles, start new projects, join projects that match their skills and interests, and collaborate with teammates using a Kanban-style dashboard. TeamUp is built primarily with Python and Streamlit for an intuitive, beautiful user experience.

***

## Features

- **User Authentication**: Register/login securely with session management.
- **Profile Management**: Create, view, and edit user profiles listing skills, bio, and contact.
- **Project Discovery**: Search and filter projects by title, description, required skills, and sort order.
- **Project Creation & Management**: Submit new projects, edit project details, and manage members.
- **Kanban Task Board**: Organize project tasks across 'To Do', 'In Progress', and 'Done' columns—assign tasks, move stages, and delete.
- **Team Collaboration**: Send join requests, invite participants, and control access.
- **Notifications**: Real-time alerts for join requests and project actions.
- **Responsive UI**: Custom styling, professional card-based layouts, dynamic navigation.
- **Secure Data Storage**: Lightweight JSON-based database for all user/project data.

***

## Installation

### Prerequisites

- Python 3.8+
- Streamlit

### Setup Instructions

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/teamup.git
   cd teamup
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run streamlit_app/Home.py
   ```
   *(or simply run the main Home.py for the full platform experience)*

***

## Usage

1. **Register an account.**
2. **Log in** to view the platform's main navigation.
3. **Explore Projects** to discover interesting projects and send join requests.
4. **Submit a new project** to start your own team.
5. **Open the Project Dashboard** to manage tasks visually using the Kanban system.
6. **Send and receive notifications** for collaboration events.

All user and project data is saved automatically and is accessible to team members and project owners through their dashboards.

***

## Project Structure

```
project-matchmaker/
│
├── core/                # Core backend logic (auth, user/project management)
│   ├── project_functions.py
│   ├── user_functions.py
│   └── utils.py
│
├── data/                # Lightweight database (JSON files)
│   ├── projects.json
│   └── users.json
│
├── streamlit_app/       # Main application interface (Streamlit pages)
│   ├── Home.py
│   ├── Login.py
│   ├── Register.py
│   ├── Profile.py
│   ├── ExploreProjects.py
│   ├── EditProject.py
│   ├── SubmitProject.py
│   ├── ProjectDashboard.py
│   ├── Notifications.py
│   └── images/
│        ├── hero_image.jpg
│        └── team_image.png
│
├── venv/                # (if using a virtualenv)
│
└── requirements.txt     # Dependencies list
```

***

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository and create a new branch.
2. Ensure all new features include clear documentation.
3. Open a pull request with a description of your changes.
4. Report bugs and suggest enhancements via GitHub Issues.

Please adhere to the code style and contribute respectfully to help TeamUp grow.

***

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

***

## Contact

Created by AADITYA JAISWAL 
Contact:  aadityajaiswalofficial@gmail.com
GitHub: https://github.com/aadityajxcodes

For project-related questions, open an issue on this repository.

***

*Enjoy collaborating with TeamUp: Where ideas meet teams!*

