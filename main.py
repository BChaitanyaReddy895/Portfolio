from flask import Flask, jsonify, request
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Email configuration (replace with your Gmail credentials)
EMAIL_ADDRESS = "chaituchaithanyareddy895@gmail.com"
EMAIL_PASSWORD = "einf clqk oyds ucuj"
RECIPIENT_EMAIL = "chaituchaithanyareddy895@gmail.com"

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

# In-memory storage for reviews (for "Educating Others" hobby)
reviews_data = []

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
    global reviews_data
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
            review = {"name": name, "rating": rating, "description": description}
            reviews_data.append(review)
            logging.info(f"New review added: {review}")
            return jsonify({"message": "Review submitted successfully!"})
        except Exception as e:
            logging.error(f"Error in /api/reviews POST: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    else:  # GET request
        try:
            return jsonify(reviews_data)
        except Exception as e:
            logging.error(f"Error in /api/reviews GET: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

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
