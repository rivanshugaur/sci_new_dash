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

### 
Firebase Firestore Setup & User Approval Process
1. Setting Up Firebase Firestore Database
Go to Firebase Console:

Navigate to Firebase Console

Create a new project or select an existing one

Enable Firestore Database:

In the left sidebar, click "Firestore Database"

Click "Create database" button

Start in production mode (we'll update rules later)

Select your preferred location and click "Enable"

2. Configuring Firestore Security Rules
Update Security Rules:

Go to "Rules" tab in Firestore section

Replace the default rules with:

javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only allow reading the approved_users collection if authenticated
    match /approved_users/{userId} {
      allow read: if request.auth != null;
      allow write: if false;  // No write access from frontend
    }
    
    // Deny all other reads/writes from clients
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
Click "Publish"

3. Creating Approved Users Collection
Add approved_users collection:

Go to "Data" tab in Firestore

Click "Start collection"

Enter collection ID: approved_users

Click "Next"

Add first approved user document:

Document ID: (auto-generate or use user's email)

Add these fields:

email (string): user@example.com

approved (boolean): true

timestamp (timestamp): current time

Click "Save"

4. Managing Approved Users (Admin Process)
Adding New Approved Users:
Via Firebase Console:

Go to Firestore "Data" tab

Select "approved_users" collection

Click "Add document"

Add fields:

email (string): new user's email

approved (boolean): true

timestamp (timestamp): current time

Via Admin Script (Alternative):

javascript
const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

async function addApprovedUser(email) {
  await db.collection('approved_users').add({
    email: email,
    approved: true,
    timestamp: admin.firestore.FieldValue.serverTimestamp()
  });
  console.log(`Added ${email} to approved users`);
}

// Example usage:
addApprovedUser('newuser@example.com');
Removing Users:
Simply delete the corresponding document from the approved_users collection

5. Important Notes
Admin Access Only:

All user management should be done through Firebase Console or admin scripts

Regular users cannot modify the approved_users collection

Email Matching:

Ensure the emails in approved_users exactly match the login emails (case-sensitive)

Backup:

Regularly export your Firestore data as backup

Go to Firestore > Data > Export

Monitoring:

Set up alerts in Firebase for suspicious activities

Review access logs regularly in Firebase Console > Project Settings > Monitoring

This guide provides a complete workflow for setting up the authentication system with approved users. You may want to adjust the field names or add additional fields based on your specific requirements.

give me the comple file to copy and paste and if possible make it concise
Here's a concise, ready-to-copy version for your README file:

Firebase Setup Guide
1. Firestore Configuration
Security Rules
javascript
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
2. User Approval Process
Create Collection:

Collection ID: approved_users

Fields: email (string), approved (boolean), timestamp (timestamp)

Add Users:

javascript
// Admin script (Node.js)
const admin = require('firebase-admin');
admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });

async function approveUser(email) {
  await admin.firestore().collection('approved_users').add({
    email: email,
    approved: true,
    timestamp: admin.firestore.FieldValue.serverTimestamp()
  });
}
3. Console Method
Go to Firestore > Data

Add document to approved_users

Set fields:

email: user@example.com

approved: true

timestamp: [use clock icon]

Key Notes
Only admins can modify approvals via console or scripts

Emails must match exactly (case-sensitive)

Regularly backup your Firestore data

This version:

Is more concise while keeping all critical info

Has ready-to-use code blocks

Maintains clear section separation

Includes both manual and programmatic methods

Highlights important considerations

Would you like me to adjust any part of this or add specific details for your project?

can you give me complete text together
Here's the complete, concise version you can directly copy and paste into your README file:

Firebase Authentication Setup
1. Firestore Security Rules
Update your Firestore rules to restrict access only to approved users:

javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /approved_users/{userId} {
      allow read: if request.auth != null;
      allow write: if false;  // Admin-only access
    }
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
2. Setting Up Approved Users
Via Firebase Console:
Go to Firestore > Data

Create collection: approved_users

Add documents with fields:

email (string): user@example.com

approved (boolean): true

timestamp (timestamp): [use clock icon]

Programmatic Method (Node.js):
javascript
const admin = require('firebase-admin');
const serviceAccount = require('./service-account-key.json');

admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });

async function addApprovedUser(email) {
  await admin.firestore().collection('approved_users').add({
    email: email,
    approved: true,
    timestamp: admin.firestore.FieldValue.serverTimestamp()
  });
}

// Usage:
addApprovedUser('user@example.com');
3. Important Notes
🔒 Only add emails that exactly match user login emails

⚠️ Never share your service account key

🔄 Regularly backup your Firestore data

👨💻 All user management should be done through admin tools

4. Troubleshooting
If login fails: verify email is in approved_users collection

Check Firebase console logs for authentication errors

Ensure timestamp field exists for proper sorting
### Step 6: Replace Firebase Config in Code
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