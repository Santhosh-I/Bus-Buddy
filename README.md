
# 🚌 Bus Buddy

*A real-time bus tracking and student wait request platform for schools, colleges, and organizations.*

---

## 🚀 Features

* **Live Bus Tracking**: View real-time positions of all active buses and your own location on a map.
* **Wait Requests**: Students can send a *"Please wait"* request for their stop; drivers receive instant notifications and can acknowledge/decline.
* **Route Visualization**: Each bus route and all stops are shown on an interactive map.
* **Notification System**: Sound + browser notifications for drivers when new student wait requests arrive.
* **Time Consistency**: All timestamps are stored in UTC and displayed in IST.
* **Mobile Friendly**: Works seamlessly on both desktop and mobile.
* **Admin Panel (optional)**: Manage buses, routes, stops, and users.

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask, SQLAlchemy
* **Frontend**: HTML5, Bootstrap 5, JavaScript (ES6+), Leaflet.js, FontAwesome
* **Database**: SQLite/MySQL/PostgreSQL (via SQLAlchemy ORM)
* **APIs**: RESTful endpoints (JSON)
* **Time Zone**: UTC storage, IST display (Asia/Kolkata)

---

## 📂 Project Structure

```
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
```

---

## ⏰ Time Zone Handling

* **Database Storage**: All timestamps stored in UTC.
* **APIs**: Return UTC ISO 8601 format.
* **Frontend**: Converted & displayed in IST with `TimeUtils.js`.
* **Server Templates**: Jinja2 filter for IST formatting.

---

## ⚙️ Setup & Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/bus-tracking
cd bus-tracking

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env  # and update settings

# Run DB migrations
flask db upgrade

# Start the app
flask run
```

👉 Visit: [http://localhost:5000](http://localhost:5000)

---

## 👨‍💻 Usage

### 🎧 Drivers

* Log in and start location tracking.
* Respond to student *"Please wait"* requests.
* Allow browser notifications.

### 🎓 Students/Parents

* View buses & routes live.
* Send *"Please wait"* requests for their stop.

---

## 🔑 API Endpoints

* `/driver` — Driver dashboard
* `/bus-tracking` — Live student tracking
* `/api/driver/wait_requests` — Poll for wait requests
* `/api/update_location` — Post driver location
* `/api/bus_locations` — Get all active bus locations

---

## 🌍 Browser Support

* Chrome ✅
* Firefox ✅
* Edge ✅
* Safari ✅

⚠️ Requires **geolocation** and (optional) **notifications**.

---

## 🎨 Customization

* Add/edit buses & routes in the admin panel.
* Change map home coordinates in JS.
* Replace `notification.mp3` with a custom sound.

---

## 🐛 Troubleshooting

* **Time errors** → Ensure server is set to UTC.
* **Location not detected** → Use HTTPS & check permissions.
* **Notifications not working** → Enable notification permissions in browser.


---

## 🤝 Contributors

* SANTHOSH-I
* Developed By "Tech-Knox"

---
## 🙏 Acknowledgements

* [Leaflet.js](https://leafletjs.com)
* [Bootstrap](https://getbootstrap.com)
* [FontAwesome](https://fontawesome.com)
* [OpenStreetMap](https://www.openstreetmap.org)

---
