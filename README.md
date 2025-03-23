# 📖 CramQuest - Study Habit Tracker 🎮📚

A **Flask-based** study habit tracking application that **gamifies learning** through an RPG-inspired system.

---

## 🚀 Features

- **RPG-Style Learning**: Turn study sessions into epic battles.
- **Quest-Based System**: Organize study tasks as quests.
- **Battle Arena**: Complete tasks to defeat enemies.
- **Real-Time Updates**: Track progress dynamically via WebSockets.
- **Leveling System**: Earn XP and badges for completing study sessions.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (via SQLAlchemy)
- **Real-Time Features**: Flask-SocketIO for WebSockets
- **API Documentation**: Swagger UI (planned)
- **Security**: CSRF protection, password hashing via `werkzeug.security`
- **Deployment**: Gunicorn + Nginx

---

## 🎯 Software Engineering Principles Applied

### **📌 Architectural Pattern (MVC)**
- **Models**: Organized in `/models` with manager classes (`PlayerManager`, `QuestManager`).
- **Views**: HTML templates with Jinja2 in `/templates`.
- **Controllers**: API request handling in `/routes`.

### **📌 SOLID Principles**
- **Single Responsibility**: Each class and function has a single, clear purpose.
- **Dependency Inversion**: Database access is abstracted through manager classes.

### **📌 Security Best Practices**
- **Session-based authentication**
- **Password hashing** using `werkzeug.security`
- **CSRF protection** in forms

### **📌 Database Design**
- **Relational Schema**: `users`, `quests`, `flashcards`, `player_badges`
- **Indexed queries** for performance
- **Foreign Key Constraints** ensuring data integrity

### **📌 Design Patterns Used**
- **Manager Pattern**: Database operations (`PlayerManager`, `FlashcardManager`).
- **Factory Pattern**: Enemy creation logic.
- **Observer Pattern**: WebSocket-based live updates.

### **📌 RESTful API Design**
- **Proper HTTP method usage** (GET, POST, PUT, DELETE)
- **API versioning** for maintainability
- **Structured endpoint naming** (e.g., `/api/quest/get_by_subject_id`)

---

## 📄 Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/study-quest.git
   cd study-quest
