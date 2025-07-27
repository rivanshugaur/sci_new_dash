# SCI KPI Dashboard
A secure, interactive dashboard built with Streamlit and Firebase for the Shipping Corporation of India. It allows approved users to upload KPI data and view sector-wise, monthly, and vessel-wise performance metrics.

---

## 🧰 Features
- Firebase Authentication (login, signup, reset password)
- Admin-approved access using Firestore
- Upload weekly/monthly KPI data (CSV)
- Real-time KPI visualization: monthly, sector-wise, and vessel-wise (stacked charts)
- Data stored in a SQL database
- Smart caching for performance using Streamlit's cache


---

## Technologies Used
- Python 3.13 (language used)
- Streamlit (library used to create the frontend dashboard interface)
- Firebase Authentication (used in the login page for login management)
- Firestore (acts as a database to store and check admin-approved users)
- Pyrebase4 (Firebase SDKs are meant for JavaScript, so Pyrebase lets Python connect to Firebase Authentication and Firestore)
- Firebase Admin SDK (for accessing Firestore securely as an admin, reading/writing approved user data)
- Plotly (for interactive charts)
- Pandas (used for data manipulation and analysis)
- SQLAlchemy (acts as the bridge between Python and the SQL database)

## How to run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/sci-kpi-dashboard.git
# This command copies the entire repository (all code, folders, README, etc.) from GitHub to your local computer.

cd sci-kpi-dashboard
# This command moves your terminal into the newly downloaded folder so you can run or edit the project from there.
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv  # create the virtual environment
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Firebase Setup (Login & Access Control)

To use the login feature with your own Firebase backend:

1. Firebase Project & Auth Setup
	•	Go to Firebase Console
	•	Create a project (e.g., sci-kpi-dashboard)
	•	In Authentication > Sign-in method, enable Email/Password
	•	In Firestore, create a database in production mode

2. Create approved_users Collection
	•	Go to Firestore > Data
	•	Create collection: approved_users
	•	Add documents with fields:
	•	email (string): user@example.com
	•	approved (boolean): true
	•	timestamp (timestamp): [use clock icon]

3. Firestore Security Rules:
    rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /approved_users/{userId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    match /{document=**} {
      allow read, write: if false;
    }
  }
}

4. Firebase Admin Credentials
	•	Go to Project Settings > Service Accounts
	•	Click Generate New Private Key
	•	Save it as serviceAccountKey.json in your project root

5. Replace Firebase Config in Code
	•	Go to Project Settings > General > Add Web App
	•	Copy the config and replace the one in login_page.py:
        firebaseConfig = {
  "apiKey": "...",
  "authDomain": "...",
  "projectId": "...",
  "storageBucket": "...",
  "messagingSenderId": "...",
  "appId": "...",
  "databaseURL": "..."
}

### 5. MySQL Database Setup
Before uploading KPI data, a MySQL database must be set up and connected. Follow the steps below:

## Step 1: Create MySQL Database
Log into MySQL and create a database:

```sql
CREATE DATABASE sci_db;
```
Create the `kpi_table` where the data will be stored:

```sql

(this is optional as sqlalchemy will automatically create the table and columns)

CREATE TABLE kpi_table (
  vessel VARCHAR(100),
  vessel_code VARCHAR(50),
  sector VARCHAR(50),
  Total_Income FLOAT,
  DOE FLOAT,
  GOP FLOAT,
  IOE FLOAT,
  PBT FLOAT,
  year INT,
  month VARCHAR(20),
);
```
## Step 2: Update Database Connection in Code
In your Streamlit code change the DB_CONFIG according to your credentials:

```python
from sqlalchemy import create_engine
# Example (adjust user, password, host, and database name as needed)
change the :
DB_CONFIG = {
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Stcs@9978"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "3306"),
    "name": os.getenv("DB_NAME", "sci_db")
}
according to your database

```
Make sure `pymysql` is installed in your environment:
```bash
pip install pymysql
```
Ensure this engine is used in both:
- The data upload script
- The dashboard data loader

### 5. Run the app
```bash
streamlit run login_page.py
```

### 👤 Support
- **Rivanshu Gaur**
- Email: rivanshugaur@gmail.com
- LinkedIn: [Rivanshu Gaur](https://www.linkedin.com/in/rivanshu-gaur-a3468628b)
