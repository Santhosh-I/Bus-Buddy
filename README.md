# 🚌 Bus Buddy – Smart Bus Tracking System  

A **web-based live bus tracking & student wait request platform** designed for schools, colleges, and organizations.  
Drivers can update **live location** and respond to student requests, while students/parents can track buses in real-time, view routes, and send **“Please Wait”** notifications.  

![GitHub repo size](https://img.shields.io/github/repo-size/Santhosh-I/Bus-Buddy?color=blue&style=flat)  
![GitHub last commit](https://img.shields.io/github/last-commit/Santhosh-I/Bus-Buddy?color=green&style=flat)  
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)  

---

## ✨ Features  

- 📍 **Live Bus Tracking** – Real-time positions of active buses & your own location.  
- 🙋 **Wait Requests** – Students can send “Please wait” requests to drivers.  
- 🗺️ **Route Visualization** – Interactive maps with routes & stops.  
- 🔔 **Notifications** – Sound + browser alerts for drivers on new requests.  
- ⏱️ **Time Consistency** – UTC storage, auto-converted to IST.  
- 📱 **Mobile Friendly** – Works smoothly on both desktop & mobile.  
- ⚙️ **Admin Panel (optional)** – Manage buses, routes, stops, and users.  

---

## 🛠️ Tech Stack  

**Backend:** Python, Flask, SQLAlchemy  
**Frontend:** HTML5, Bootstrap 5, JavaScript (ES6+), Leaflet.js, FontAwesome  
**Database:** SQLite / MySQL / PostgreSQL (via SQLAlchemy ORM)  
**APIs:** RESTful (JSON)  
**Time Zone:** UTC storage → IST display (Asia/Kolkata)  

---

## 📂 Project Structure  

bus-tracking/
├── app.py
├── models.py
├── static/
│ ├── js/
│ │ ├── main.js
│ │ └── timeUtils.js
│ └── sounds/
│ └── notification.mp3
├── templates/
│ ├── base.html
│ ├── driver.html
│ ├── bus_tracking.html
│ └── ...
├── requirements.txt
├── README.md
└── ...

yaml
Copy
Edit

---

## ⏳ Time Zone Standardization  

- **Storage:** UTC (`datetime.now(timezone.utc)`)  
- **API Responses:** UTC in ISO 8601 (e.g., `2025-08-17T22:30:45Z`)  
- **Frontend Display:** Converted to IST using `TimeUtils.js`  
- **Server-Side Templates:** Jinja2 filters for IST formatting  

---

## 🚀 Setup & Installation  

```bash
# Clone the repo
git clone https://github.com/Santhosh-I/Bus-Buddy.git
cd Bus-Buddy

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env   # Update settings

# Run database migrations
flask db upgrade

# Start the app
flask run
👉 Visit: http://localhost:5000

📌 Usage
👨‍✈️ Drivers

Log in, start tracking location

Manage wait requests (acknowledge/decline)

Allow location + notification permissions

👨‍🎓 Students/Parents

View live bus map

Track location + select route

Send “Please wait” requests

🔑 Key Endpoints
Endpoint	Description
/driver	Driver dashboard (maps, requests)
/bus-tracking	Student live bus tracking
/api/update_location	Update driver’s location
/api/bus_locations	Get all active bus locations
/api/driver/wait_requests	Poll for new wait requests

🌍 Browser Support
✔️ Chrome (latest)
✔️ Firefox (latest)
✔️ Edge (latest)
✔️ Safari (latest)

🔒 Requires HTTPS for geolocation + notifications

🐞 Troubleshooting
⏱️ Time errors → Ensure server time = UTC

📍 Location not detected → Enable browser geolocation & HTTPS

🔔 Notifications not working → Check browser notification permissions

📜 License
This project is licensed under the MIT License.
See LICENSE for more details.

👥 Contributors
Santhosh (@Santhosh-I)

Project contributors...

🙏 Acknowledgements
Leaflet.js

Bootstrap

FontAwesome

OpenStreetMap