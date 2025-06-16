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
        "title": "VEXA Chatbot",
        "description": "An AI-powered chatbot for Sahayak Organization, assisting users with queries about underprivileged children's development.",
        "image": "/static/images/Vexa Chatbot.png",
        "technologies": ["Python", "Deep Learning", "PyTorch", "Flask", "HTML", "CSS"],
        "githubLink": "https://github.com/BChaitanyaReddy895/vexa_chatbot",
        "liveLink": "https://chaitanya895-sahayak.hf.space"
    },
    {
        "title": "Bangla to English Translator",
        "description": "A machine learning model translating Bangla text, images, PDFs, and websites to English using NLP and web crawling techniques.",
        "image": "/static/images/translator.png",
        "technologies": ["Python", "NLP", "HTML", "CSS", "JavaScript"],
        "githubLink": "https://github.com/BChaitanyaReddy895/Bengali_English_translator",
        "liveLink": "https://chaitanya895-bangla-translator.hf.space"
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
            "Participated in Entellika Sparc AI Hackathon and IIT Jammu UI/UX Challenge"
        ]
    }
]

certifications_data = [
    {
        "title": "Certified AI Practitioner",
        "organization": "Hugging Face",
        "date": "June 2025",
        "description": "Completed a comprehensive course on AI fundamentals, including LLMs and AI agents.",
        "certificateLink": "https://huggingface.co/certificates/your-certificate-id"  # Replace with actual link if available
    },
    {
        "title": "Python for Data Science",
        "organization": "Coursera",
        "date": "March 2024",
        "description": "Learned advanced Python techniques for data analysis and visualization.",
        "certificateLink": "https://coursera.org/certificates/your-certificate-id"  # Replace with actual link
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
                # Optional: Allow position to be specified in the request, default to 0
                position = int(data.get('position', 0))
                
                # Insert the review into the database with the position
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
        else:  # GET request
            try:
                # Sort by position (ascending), then by id (ascending) as a tiebreaker
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
        # Check for admin password in the request body
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({"error": "Password is required"}), 400

        password = data['password']
        if password != ADMIN_PASSWORD:
            return jsonify({"error": "Invalid password"}), 403

        if 'position' not in data:
            return jsonify({"error": "Position is required"}), 400

        position = int(data['position'])

        # Check if the review exists
        cursor.execute("SELECT name FROM reviews WHERE id = ?", (id,))
        review = cursor.fetchone()
        if not review:
            return jsonify({"error": "Review not found"}), 404
        
        # Update the position of the review
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
        # Check for admin password in the request body
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({"error": "Password is required"}), 400

        password = data['password']
        if password != ADMIN_PASSWORD:
            return jsonify({"error": "Invalid password"}), 403

        # Check if the review exists
        cursor.execute("SELECT name FROM reviews WHERE id = ?", (id,))
        review = cursor.fetchone()
        if not review:
            return jsonify({"error": "Review not found"}), 404
        
        # Delete the review
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

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'message' not in data:
            return jsonify({"error": "Invalid request data"}), 400
        email = data['email']
        message = data['message']
        logging.info(f"Contact form submission - Email: {email}, Message: {message}")

        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "New Contact Form Submission"
        
        body = f"New message from your portfolio website:\n\nFrom: {email}\nMessage: {message}"
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable TLS
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
