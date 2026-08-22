from flask import Flask, render_template, request, jsonify
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
DATA_FILE = 'data.json'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Default data – extended for all pages
    default = {
        "logo_url": "logo.png",
        "hero": [
            {"image": "hero1.jpg", "title": "Building Dreams", "subtitle": "Excellence in Civil Engineering & Construction"},
            {"image": "hero2.jpg", "title": "Sustainable Future", "subtitle": "Innovative Green Construction Solutions"},
            {"image": "hero3.jpg", "title": "Precision & Quality", "subtitle": "Delivering Excellence Every Time"}
        ],
        "what_we_do": [
            {"icon": "fa-building", "title": "Residential Building", "description": "Quality homes designed for comfort and longevity."},
            {"icon": "fa-house-chimney", "title": "Duplex House", "description": "Modern duplex designs with premium finishes."},
            {"icon": "fa-tree", "title": "Villa & Farmhouse", "description": "Luxury villas and farmhouses in serene locations."},
            {"icon": "fa-paint-roller", "title": "Interiors", "description": "Aesthetic interiors with sustainable materials."}
        ],
        "specialized_in": [
            {"icon": "fa-droplet", "title": "Rain Water Harvesting", "description": "Sustainable water management solutions."},
            {"icon": "fa-microchip", "title": "IOT Integration", "description": "Smart building automation and IOT solutions."},
            {"icon": "fa-leaf", "title": "Green Interiors", "description": "Eco-friendly materials and sustainable design."},
            {"icon": "fa-solar-panel", "title": "Solar Solutions", "description": "Renewable energy integration for buildings."}
        ],
        "testimonials": [
            {"name": "Ramesh Kumar", "feedback": "Amruthadhara Infra delivered our dream home with exceptional quality and on time. Highly recommended!", "project": "Residential Villa"},
            {"name": "Priya Reddy", "feedback": "Their attention to detail and sustainable approach made our farmhouse truly special. Amazing team!", "project": "Farmhouse Project"},
            {"name": "Suresh Patel", "feedback": "Professional, reliable, and innovative. They transformed our commercial space beyond expectations.", "project": "Commercial Building"}
        ],
        "vision": {
            "title": "Young minds big vision",
            "text": "We are a team of passionate engineers and designers committed to building a sustainable future through innovative construction practices. Our vision is to create structures that stand the test of time while respecting the environment."
        },
        "contact": {
            "phone": "9347051097",
            "whatsapp": "9347051097",
            "email": "info@amruthadharainfra.com",
            "address": "Hyderabad, Telangana, India"
        },
        "social": {
            "youtube": "https://youtube.com",
            "twitter": "https://x.com",
            "facebook": "#",
            "instagram": "#",
            "linkedin": "#"
        },
        "pricing": [
            {"label": "Basic", "price": "₹1,899", "note": "per sq.ft"},
            {"label": "Premium", "price": "₹2,399", "note": "per sq.ft"},
            {"label": "Luxury", "price": "₹3,299", "note": "per sq.ft"},
            {"label": "Ultra Luxury", "price": "₹4,999", "note": "per sq.ft"}
        ],
        "parallax_image": "parallax.jpg",
        # NEW SECTIONS FOR OTHER PAGES
        "about": {
            "what_we_do_text": "We are a civil-engineering-led Private Limited Company delivering integrated solutions across construction, interiors, water infrastructure and development.",
            "mission": "To deliver integrated construction, interior, water, and real estate solutions through site-first understanding, practical design, quality execution, and a strong commitment to safety, sustainability, and client trust.",
            "vision": "To create safe, sustainable, and high-performing built environments by combining thoughtful planning, engineering discipline, and responsible execution.",
            "team": [
                {"name": "Arun Kumar", "role": "CEO & Founder", "image": "team1.jpg"},
                {"name": "Sneha Reddy", "role": "Lead Architect", "image": "team2.jpg"},
                {"name": "Vikram Singh", "role": "Project Manager", "image": "team3.jpg"},
                {"name": "Priya Sharma", "role": "Interior Designer", "image": "team4.jpg"}
            ],
            "achievements": [
                {"title": "Best Construction Company 2024", "image": "ach1.jpg"},
                {"title": "Green Building Award 2023", "image": "ach2.jpg"},
                {"title": "ISO 9001:2020 Certified", "image": "ach3.jpg"}
            ]
        },
        "careers": {
            "jobs": [
                {"title": "Senior Site Engineer", "experience": "5+ Years", "type": "Full Time"},
                {"title": "Architect", "experience": "3+ Years", "type": "Full Time"},
                {"title": "Project Manager", "experience": "7+ Years", "type": "Full Time"}
            ],
            "internships": [
                {"title": "Site Engineer Intern", "location": "Hyderabad", "duration": "6 Months"},
                {"title": "CAD/CAM Intern", "location": "Hyderabad", "duration": "3 Months"},
                {"title": "2D and 3D Designer Intern", "location": "Remote", "duration": "3 Months"},
                {"title": "Video Editing Intern", "location": "Remote", "duration": "3 Months"}
            ]
        },
        "gallery": [
            "https://images.unsplash.com/photo-1541888081622-c20536443c51?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1541888081622-c20536443c51?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80"
        ],
        "projects": {
            "past": [
                {"title": "Sunrise Villas", "description": "Luxury villa project completed in 2023", "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80"},
                {"title": "Green Valley Township", "description": "Completed in 2022", "image": "https://images.unsplash.com/photo-1541888081622-c20536443c51?auto=format&fit=crop&w=600&q=80"}
            ],
            "present": [
                {"title": "Downtown Commercial Tower", "description": "Expected completion 2026", "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80"},
                {"title": "Riverside Residences", "description": "Ongoing project", "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80"}
            ],
            "upcoming": [
                {"title": "Eco-Friendly Tech Park", "description": "Starting Q3 2027", "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80"},
                {"title": "Smart City Housing", "description": "Planned for 2028", "image": "https://images.unsplash.com/photo-1541888081622-c20536443c51?auto=format&fit=crop&w=600&q=80"}
            ]
        }
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(default, f, indent=2)
    return default

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

# Routes for all pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')

# API endpoints
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def update_data():
    new_data = request.get_json()
    if new_data:
        save_data(new_data)
        return jsonify({"status": "success", "message": "Data updated successfully"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'filename': filename}), 200
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
