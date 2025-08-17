🚌 Bus Tracking System
A web-based live bus tracking and student wait request platform for schools, colleges, and organizations. Drivers can update live location and respond to student wait requests; students/parents can track buses in real time, view routes, and send "Please wait" notifications.

Features
Live Bus Tracking: View real-time positions of all active buses and your own location on a map.

Wait Requests: Students can send a "Please wait" request for their stop; drivers receive instant notifications and can acknowledge/decline.

Route Visualization: Each bus route and all stops are visualized on an interactive map.

Notification System: Sound and browser notifications for drivers when new student wait requests arrive.

Time Consistency: All timestamps are stored in UTC and displayed in India Standard Time (IST) for end users.

Mobile Friendly: Designed for both desktop and mobile browsers.

Admin Panel: (optional) For managing buses, routes, stops, and users.

Stack
Backend: Python, Flask, SQLAlchemy

Frontend: HTML5, Bootstrap 5, JavaScript (ES6+), Leaflet.js, FontAwesome

Database: SQLite/MySQL/PostgreSQL (via SQLAlchemy ORM)

APIs: RESTful endpoints (JSON)

Time Zone Handling: UTC storage, IST display (Asia/Kolkata)

Project Structure
text
bus-tracking/
├── app.py
├── models.py
├── static/
│   ├── js/
│   │   ├── main.js
│   │   └── timeUtils.js
│   └── sounds/
│       └── notification.mp3
├── templates/
│   ├── base.html
│   ├── driver.html
│   ├── bus_tracking.html
│   └── ...
├── requirements.txt
├── README.md
└── ...
Time Zone Standardization
Storage: All timestamps (e.g., timestamp, last_updated) are stored in the database in UTC (datetime.now(timezone.utc)).

APIs: All API responses return UTC ISO 8601 formatted timestamps (e.g., "2025-08-17T22:30:45Z").

Frontend Display: All times are converted and displayed in IST using a centralized TimeUtils class in JavaScript.

Templates: When rendering server-side, use a Jinja2 filter to format times in IST.

Migration: Legacy data is migrated from IST to UTC if necessary.

Setup & Installation
Clone the repo

text
git clone https://github.com/yourusername/bus-tracking
cd bus-tracking
Install dependencies

text
pip install -r requirements.txt
Configure environment variables
(Copy .env.example to .env and update settings.)

Run the database migrations

text
flask db upgrade
Run the app

text
flask run
Visit http://localhost:5000

Usage
Drivers:
Log in, start tracking your location, and manage wait requests. Grant location permissions for accurate updates and browser notification permissions for instant alerts.

Students/Parents:
View the live map, see your location alongside all active buses, select a route, and send a "Please wait" request if needed.

Key Endpoints
/driver — Driver dashboard (maps, status, wait requests)

/bus-tracking — Live bus tracking for students

/api/driver/wait_requests — Poll for new wait requests (JSON)

/api/update_location — Post driver's current location

/api/bus_locations — Get all active bus locations (JSON)

Browser Support
Latest releases of Chrome, Firefox, Edge, Safari

Requires geolocation and (optionally) notification permissions

Customization
Add or edit buses/routes/stops using the admin panel or scripts.

Adjust map home coordinates in the JS as needed.

Replace notification.mp3 in static/sounds/ with your custom sound (optional).

Troubleshooting
Time errors / misaligned clocks:

Ensure server time is set to UTC.

All browser displayed times are converted to IST using the JS TimeUtils class.

Location not detected:

Check browser settings and permissions.

Use HTTPS for production deployments (browsers block geolocation on HTTP).

Notifications not working:

Ensure permissions for notifications are granted in browser settings.

License
MIT License.
See LICENSE for more information.

Contributors
Your Name (@yourusername)

Project contributors...

Acknowledgements
Leaflet.js

Bootstrap

FontAwesome

OpenStreetMap

This project is designed with standard time handling and robust event-driven notifications for educational institution bus fleets.