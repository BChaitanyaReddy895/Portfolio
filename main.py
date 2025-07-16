from flask import Flask, jsonify, request
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import os
import shutil

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Email configuration (replace with your Gmail credentials)
EMAIL_ADDRESS = "chaituchaithanyareddy895@gmail.com"
EMAIL_PASSWORD = "einf clqk oyds ucuj"
RECIPIENT_EMAIL = "chaituchaithanyareddy895@gmail.com"

# Admin password for delete functionality (replace with a secure password)
ADMIN_PASSWORD = "Chaitu895@"  # Change this to a strong password

# SQLite database paths
PROJECT_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "portfolio.db")
PERSISTENT_DB_PATH = "/data/portfolio.db"
FALLBACK_DB_PATH = "/tmp/portfolio.db"

def init_db():
    conn = None
    db_path = PERSISTENT_DB_PATH

    try:
        # Check if /data/ exists; if not, fall back to /tmp/
        if not os.path.exists("/data"):
            logging.warning("Persistent storage directory '/data' not found. Falling back to /tmp (non-persistent).")
            db_path = FALLBACK_DB_PATH
            # Ensure /tmp/ exists (it should, but just in case)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Check if the database exists at the target path; if not, copy from project directory
        if not os.path.exists(db_path):
            if os.path.exists(PROJECT_DB_PATH):
                shutil.copy(PROJECT_DB_PATH, db_path)
                logging.info(f"Copied portfolio.db from {PROJECT_DB_PATH} to {db_path}")
            else:
                logging.warning(f"Initial portfolio.db not found at {PROJECT_DB_PATH}. Creating a new database.")

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create reviews table if it doesn't exist, with position column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                description TEXT NOT NULL,
                position INTEGER DEFAULT 0
            )
        ''')

        # Check if position column exists; if not, add it
        cursor.execute("PRAGMA table_info(reviews)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'position' not in columns:
            cursor.execute("ALTER TABLE reviews ADD COLUMN position INTEGER DEFAULT 0")
            logging.info("Added 'position' column to reviews table.")

        # Optional: Clean up test entries (IDs 9-12) if they exist (run once, then comment out)
        cursor.execute("DELETE FROM reviews WHERE id IN (9, 10, 11, 12)")
        logging.info("Cleaned up test entries from reviews table.")

        conn.commit()
        logging.info(f"SQLite database initialized successfully at {db_path}.")
    except Exception as e:
        logging.error(f"Error initializing SQLite database: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

    return db_path

# Initialize the database and set the DB_PATH for the app to use
DB_PATH = init_db()

# Data for API endpoints
skills_data = [
    {"title": "Machine Learning", "icon": "brain", "skills": [
        {"name": "Numpy", "proficiency": 85},
        {"name": "Pandas", "proficiency": 90},
        {"name": "NLP", "proficiency": 80}
    ]},
    {"title": "Backend Development", "icon": "server", "skills": [
        {"name": "PHP", "proficiency": 70},
        {"name": "Python", "proficiency": 95},
        {"name": "Java", "proficiency": 75},
        {"name": "Flask", "proficiency": 85}
    ]},
    {"title": "Database", "icon": "database", "skills": [
        {"name": "MySQL", "proficiency": 80}
    ]},
    {"title": "Deep Learning", "icon": "network-wired", "skills": [
        {"name": "TensorFlow", "proficiency": 75}
    ]}
]

achievements_data = [
    {
        "icon": "trophy",
        "title": "Screen Smart Ideathon Winner",
        "organization": "IEEE Student Branch, REVA University",
        "description": "Proposed an innovative solution for reducing screen time among students, utilizing that time for upskilling."
    },
    {
        "icon": "award",
        "title": "Finalist in AI Hackathon",
        "organization": "Entellika Sparc AI Hackathon",
        "description": "Developed a Python Tkinter app for matching top 5 internships based on resume skills using binary classification and Naive Bayes."
    },
    {
        "icon": "star",
        "title": "Winner at UI/UX Design Challenge",
        "organization": "IIT Jammu",
        "description": "Designed an e-commerce platform showcasing Indian state-specific handicrafts, promoting cultural heritage."
    },
    {
        "icon": "microphone",
        "title": "Vexa Chatbot Launch Presentation",
        "organization": "REVA University",
        "description": "Delivered an 8-minute talk on the Vexa Chatbot launch, showcasing technical details and project impact to peers and faculty."
    }
]

hobbies_data = [
    {
        "icon": "code",
        "title": "Coding",
        "description": "Building side projects and exploring new technologies to fuel my passion for software development."
    },
    {
        "icon": "chalkboard-teacher",
        "title": "Educating Others",
        "description": "Sharing knowledge in Python and tech concepts, driven by a passion for teaching."
    },
    {
        "icon": "book",
        "title": "Reading",
        "description": "Keeping up with tech trends through blogs and articles."
    },
    {
        "icon": "palette",
        "title": "Digital Art",
        "description": "Creating digital artwork and experimenting with UI/UX design."
    }
]

projects_data = [
    {
        "title": "Vexa Chatbot",
        "description": "An AI-powered chatbot for Sahayak Organization, assisting users with queries about underprivileged children's development.",
        "technologies": ["Python", "Deep Learning", "PyTorch", "Flask", "HTML", "CSS"],
        "githubLink": "https://github.com/BChaitanyaReddy895/vexa_chatbot",
        "liveLink": "https://chaitanya895-sahayak.hf.space",
        "image": "/static/images/Vexa Chatbot.png",
        "video": "https://drive.google.com/file/d/1zNCedqcqOxuD4WvIqn47wZLqG-jG5Qkf/view?usp=sharing",  # Placeholder for video link
        "role": "Lead Developer and Presenter",
        "contributions": [
            "Designed and implemented the chatbot's NLP pipeline using PyTorch",
            "Developed the Flask backend for seamless user interaction",
            "Presented the project in an 8-minute talk at 1 year anniversary of sahayak organization, explaining its functioning, impact and it's future goals"
        ]
    },
    {
        "title": "Bangla to English Translator",
        "description": "A machine learning model translating Bangla text, images, PDFs, and websites to English using NLP and web crawling techniques with advanced search mechanisms.",
        "technologies": ["Python", "NLP", "HTML", "CSS", "JavaScript"],
        "githubLink": "https://github.com/BChaitanyaReddy895/Bengali_English_translator",
        "liveLink": "https://chaitanya895-bangla-translator.hf.space",
        "image": "/static/images/translator.jpg",
        "role": "Lead Developer and Machine Learning Engineer",
        "contributions": [
            "Built the NLP model for accurate Bangla-to-English translation",
            "Integrated web crawling for real-time website translation and advance search mechanisms",
            "Designed the user interface for accessibility and ease of use"
        ]
    },
     {
        "title": "Multi Agentic AI For Sustainable Farming",
        "description": "It is an AI-powered platform designed to assist farmers with smart crop recommendations, weather insights, market trends, and sustainability tracking. Built by a team of four, it supports multiple languages and promotes eco-friendly practices—empowering farmers through technology, data, and informed decision-making for a better tomorrow.",
        "technologies": ["AI","Machine Learning","Python","Streamlit","PLotly","Agentic AI"],
        "githubLink": "https://github.com/BChaitanyaReddy895/Agentic-AI-for-Sustainable-Farming",
        "liveLink": "https://chaitanya895-multiagenticai.hf.space",
        "image": "/static/images/agenticAI.png",
        "role": "Lead Developer and Team Contributor",
        "contributions": [
            "Designed the Architecture of each agent, describing what each agent does",
            "Designed modern and user friendly interface that supports the farmers in using it in a better way for getting the smart recommendations and enhancing their prodcutivity",
            "Worked on the features includes the soil analysis where i had provided the option to the users to upload the soil images for analysis, Crop Rotation Planner for suggesting the crops to maintain the fertility of the soil",
            "implemented the features include Fertilizer Optimization Calculator that suggests the farmers for optimum use of fertilizers per hectare and Sustainability Score Tracker for tracking the sustainability score"
        ]
    }
]

education_data = [
    {
        "degree": "B.Tech in Computer Science and Engineering",
        "institution": "REVA University",
        "period": "2023-2027",
        "description": "Specializing in Python, C, Java, Machine Learning, and NLP.",
        "achievements": [
            "Won IEEE Ideathon at REVA University",
            "Developed Bangla to English translation model for industrial use",
            "Participated in Entellika Sparc AI Hackathon and IIT Jammu UI/UX Challenge",
            "Delivered an 8-minute talk on Vexa Chatbot launch to peers and faculty"
        ]
    }
]

certifications_data = [
    {
        "title": "MeViTechnologies LLP certificate of appreciation for outstanding performance and exceptional dedication through out the SDP on NLP",
        "platform": "MeViTechnlogies",
        "year": "November 2024",
        "description": "Completed a comprehensive course on NLP from the skill development program conducted at REVA University",
        "certificateLink": "https://drive.google.com/file/d/18feyqzNhxoHeFcpjUGtwYECxhJTGlneI/view?usp=sharing",  # Replace with actual link
        "badge": "static/images/certifications/sdpnlp.jpg"  # Placeholder for badge image
    },
    {
        "title": "Art of C Programming",
        "platform": "Swayam",
        "year": "June 2024",
        "description": "Art of C Programming Course Completion with a consolidate score of 89%.",
        "certificateLink": "https://drive.google.com/file/d/1p4lkzUMqFGtBKJk8ppuSgiyCrR9MrYvS/view?usp=drive_link",  # Replace with actual link
        "badge": "static/images/certifications/Screenshot 2025-07-14 203706.png"  # Placeholder for badge image
    }
]

volunteer_experience_data = [
   
    {
        "role": "Core Team Member",
        "organization": "Sahayak Organization(NGO)",
        "period": "2025",
        "description": "Developed the Vexa Chatbot to support queries about underprivileged children's development.",
        "contributions": [
            "Led the development of the chatbot’s AI backend",
            "Presented the project to stakeholders in an 8-minute talk"
        ]
    }
]

talks_data = [
    {
        "title": "Vexa Chatbot Launch – Speaker Session",
        "event": "REVA University Tech Talk",
        "date": "July 2025",  # Update with actual date
        "description": "Delivered an 8-minute presentation on the Vexa Chatbot, covering its technical architecture, impact, and deployment for the Sahayak Organization.",
        "videoLink": "https://drive.google.com/file/d/1zNCedqcqOxuD4WvIqn47wZLqG-jG5Qkf/view?usp=sharing"
        
    }
]

@app.route('/')
def serve_index():
    try:
        return app.send_static_file('index.html'), 200
    except Exception as e:
        logging.error(f"Error serving index.html: {str(e)}")
        return jsonify({"error": "File not found"}), 404

@app.route('/static/<path:path>')
def serve_static(path):
    logging.info(f"Serving static file: {path}")
    try:
        return app.send_static_file(path)
    except Exception as e:
        logging.error(f"Error serving static file {path}: {str(e)}")
        return jsonify({"error": "File not found"}), 404

@app.route('/api/skills')
def get_skills():
    try:
        return jsonify(skills_data)
    except Exception as e:
        logging.error(f"Error in /api/skills: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/achievements')
def get_achievements():
    try:
        return jsonify(achievements_data)
    except Exception as e:
        logging.error(f"Error in /api/achievements: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/hobbies')
def get_hobbies():
    try:
        return jsonify(hobbies_data)
    except Exception as e:
        logging.error(f"Error in /api/hobbies: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/reviews', methods=['GET', 'POST'])
def handle_reviews():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if request.method == 'POST':
            try:
                data = request.get_json()
                if not data or 'rating' not in data or 'description' not in data or 'name' not in data:
                    return jsonify({"error": "Invalid request data"}), 400
                rating = int(data['rating'])
                if rating < 1 or rating > 5:
                    return jsonify({"error": "Rating must be between 1 and 5"}), 400
                description = data['description']
                name = data['name']
                position = int(data.get('position', 0))
                
                cursor.execute(
                    "INSERT INTO reviews (name, rating, description, position) VALUES (?, ?, ?, ?)",
                    (name, rating, description, position)
                )
                conn.commit()
                logging.info(f"New review added: {name}, {rating}, {description}, position: {position}")
                return jsonify({"message": "Review submitted successfully!"})
            except Exception as e:
                conn.rollback()
                logging.error(f"Error in /api/reviews POST: {str(e)}")
                return jsonify({"error": "Internal server error"}), 500
        else:
            try:
                cursor.execute("SELECT id, name, rating, description, position FROM reviews ORDER BY position ASC, id ASC")
                reviews = [{"id": row[0], "name": row[1], "rating": row[2], "description": row[3], "position": row[4]} for row in cursor.fetchall()]
                return jsonify(reviews)
            except Exception as e:
                logging.error(f"Error in /api/reviews GET: {str(e)}")
                return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        logging.error(f"Error connecting to SQLite database in /api/reviews: {str(e)}")
        return jsonify({"error": f"Database connection error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/reviews/update_position/<int:id>', methods=['PATCH'])
def update_review_position(id):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({"error": "Password is required"}), 400

        password = data['password']
        if password != ADMIN_PASSWORD:
            return jsonify({"error": "Invalid password"}), 403

        if 'position' not in data:
            return jsonify({"error": "Position is required"}), 400

        position = int(data['position'])
        cursor.execute("SELECT name FROM reviews WHERE id = ?", (id,))
        review = cursor.fetchone()
        if not review:
            return jsonify({"error": "Review not found"}), 404
        
        cursor.execute("UPDATE reviews SET position = ? WHERE id = ?", (position, id))
        conn.commit()
        logging.info(f"Review position updated for id {id}: {review[0]}, new position: {position}")
        return jsonify({"message": f"Position updated for review by {review[0]}"})
    except Exception as e:
        logging.error(f"Error in /api/reviews/update_position/{id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/reviews/delete/<int:id>', methods=['DELETE'])
def delete_review(id):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({"error": "Password is required"}), 400

        password = data['password']
        if password != ADMIN_PASSWORD:
            return jsonify({"error": "Invalid password"}), 403

        cursor.execute("SELECT name FROM reviews WHERE id = ?", (id,))
        review = cursor.fetchone()
        if not review:
            return jsonify({"error": "Review not found"}), 404
        
        cursor.execute("DELETE FROM reviews WHERE id = ?", (id,))
        conn.commit()
        logging.info(f"Review deleted with id {id}: {review[0]}")
        return jsonify({"message": f"Review by {review[0]} deleted successfully!"})
    except Exception as e:
        logging.error(f"Error in /api/reviews/delete/{id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/projects')
def get_projects():
    try:
        return jsonify(projects_data)
    except Exception as e:
        logging.error(f"Error in /api/projects: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/education')
def get_education():
    try:
        return jsonify(education_data)
    except Exception as e:
        logging.error(f"Error in /api/education: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/certifications')
def get_certifications():
    try:
        return jsonify(certifications_data)
    except Exception as e:
        logging.error(f"Error in /api/certifications: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/volunteer')
def get_volunteer_experience():
    try:
        return jsonify(volunteer_experience_data)
    except Exception as e:
        logging.error(f"Error in /api/volunteer: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/talks')
def get_talks():
    try:
        return jsonify(talks_data)
    except Exception as e:
        logging.error(f"Error in /api/talks: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'message' not in data:
            return jsonify({"error": "Invalid request data"}), 400
        email = data['email']
        message = data['message']
        logging.info(f"Contact form submission - Email: {email}, Message: {message}")

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "New Contact Form Submission"
        
        body = f"New message from your portfolio website:\n\nFrom: {email}\nMessage: {message}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
            logging.info(f"Email sent to {RECIPIENT_EMAIL}")

        return jsonify({"message": "Message sent successfully!"})
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"SMTP Authentication Error: {str(e)}")
        return jsonify({"error": "Failed to authenticate with email server. Please try again later."}), 500
    except smtplib.SMTPException as e:
        logging.error(f"SMTP Error: {str(e)}")
        return jsonify({"error": "Failed to send email. Please try again later."}), 500
    except Exception as e:
        logging.error(f"Error in /api/contact: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
