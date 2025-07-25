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

### 4. Add your Firebase credentials
 - Place your `serviceAccountKey.json` in the root directory.
 - Ensure the Firebase config in `login_page.py` is correct.

### 5. Run the app
```bash
streamlit run login_page.py
```


## Folder Structure

sci_dashboard_local/
├── login_page.py             # for logging into the page and calling the sci_dashboard
├── sci_dashboard.py          # manages and maintains the functionalities of the dashboard
├── serviceAccountKey.json    # Firebase credentials
├── requirements.txt          # all requirements that need to be installed before running the dashboard
└── README.md                 # all instructions to set up the dashboard

## 🔐 Firebase Setup (Required for Login & Access Control)

To use this dashboard with your own Firebase backend, follow these steps:

### Step 1: Create Firebase Project
- Go to [https://console.firebase.google.com](https://console.firebase.google.com)
- Create a new project (e.g., `sci-kpi-dashboard`)
- Disable Google Analytics if not needed

### Step 2: Enable Authentication
- In Firebase Console → Authentication → Sign-in method
- Enable **Email/Password**

### Step 3: Set Up Firestore
- Go to Firestore Database → Create database (start in production or test mode)
- Add a collection: `approved_users`
- Add documents using user emails as IDs (e.g., `user@example.com`)

### Step 4: Generate Firebase Admin Credentials
- Go to Project Settings → Service Accounts
- Click "Generate new private key"
- Download and place `serviceAccountKey.json` in your project root

### Step 5: Replace Firebase Config in Code
- In Project Settings → General → Add Web App → Copy config
- Replace the `firebaseConfig` dictionary in `login_page.py` with your copied values

```python
firebaseConfig = {
  "apiKey": "...",
  "authDomain": "...",
  "projectId": "...",
  "storageBucket": "...",
  "messagingSenderId": "...",
  "appId": "...",
  "databaseURL": "..."
}
```

Once complete, you can log in, sign up, and control access based on the `approved_users` collection.


### Sample Data Format
- The file format should remain the same as the sample file provided initially.

### Access Control
Only emails listed in the Firestore `approved_users` collection are allowed to log in.


### Future Scope

- For any feature enhancements or visualization improvements, you can update `sci_dashboard.py`, which controls the main web app layout and charts.
- To apply changes in data cleaning or preprocessing logic, update `cleaner.py`.
- For authentication or login flow changes, modify `login_page.py` to update the Firebase config, layout, or validation rules.


## 👤 Support
- **Rivanshu Gaur**
- Email: rivanshugaur@gmail.com
- LinkedIn: [Rivanshu Gaur](https://www.linkedin.com/in/rivanshu-gaur-a3468628b)