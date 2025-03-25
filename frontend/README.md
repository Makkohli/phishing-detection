Here's a detailed README for your project:  

---

# **AI for Emotional Manipulation Detection in Cyber Attacks**  

This project detects **phishing attempts** and analyzes the **emotional tone** of emails using AI models. It uses a combination of **FastAPI** for the backend, **Next.js** for the frontend, and **machine learning models** for phishing and emotion detection. The system also supports optional **Gemini AI integration** for advanced analysis.  

---

## 🚀 **Features**  

- **Phishing Detection:** Predicts whether an email is a phishing attempt using a trained model.  
- **Emotion Analysis:** Detects emotional tones using an emotion classification model.  
- **Gemini AI Integration (Optional):** Provides detailed insights using Google's Gemini API.  
- **Email Authentication:** Authenticate and fetch emails using Gmail API.  
- **Interactive Dashboard:** Visualize and analyze results on the frontend.  

---

## 🛠️ **Tech Stack**  

| Component        | Technology                                  |
|-------------------|--------------------------------------------|
| **Frontend**      | Next.js, Tailwind CSS                      |
| **Backend**       | FastAPI, Python                            |
| **Database**      | PostgreSQL or MongoDB                      |
| **AI Models**     | DistilBERT, Random Forest, XGBoost         |
| **APIs**          | Gmail API, Gemini API (Optional)           |
| **ML Libraries**  | Scikit-Learn, NumPy, Pandas, Joblib        |
| **Authentication**| OAuth2 (Google Authentication)             |

---

## 🏗️ **Project Structure**  

```bash
phishing-detection/
├── backend/
│   ├── models/                      # Pretrained ML models
│   ├── routes/                      # API routes
│   ├── utils/                       # Utility functions
│   ├── main.py                      # FastAPI entry point
│   ├── email_routes.py              # Email analysis APIs
│   └── credential.json              # Gmail API credentials (ignored in Git)
├── frontend/
│   ├── public/                      # Static assets
│   ├── src/                         # Frontend source code
│   │   ├── components/              # Reusable UI components
│   │   ├── pages/                   # Pages like Home, Dashboard
│   │   ├── hooks/                   # API Hooks
│   │   └── App.js                   # Main App component
│   └── tailwind.config.js           # Tailwind CSS config
├── .gitignore                       # Ignoring unnecessary files
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## ⚙️ **Prerequisites**  

Ensure you have the following installed:  
- Python 3.10+  
- Node.js 18+  
- npm or yarn  
- Git  
- FastAPI  
- Gmail API access  
- (Optional) Gemini API access  

---

## 🔎 **Environment Variables**  

Create a `.env` file in the backend directory:  
```env
GEMINI_API_KEY=your_gemini_api_key
```

---

## 🛠️ **Setup Instructions**  

### 1. Clone the Repository  
```bash
git clone https://github.com/Makkohli/phishing-detection.git
cd phishing-detection
```

### 2. Backend Setup  
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows
# source venv/bin/activate    # On Mac/Linux
pip install -r requirements.txt
```

### 3. Frontend Setup  
```bash
cd ../frontend
npm install
```

---

## 🚦 **Running the Project**  

### Start Backend:  
```bash
cd backend
uvicorn main:app --reload
```
- API will be available at `http://localhost:8000`

### Start Frontend:  
```bash
cd ../frontend
npm run dev
```
- Frontend will be available at `http://localhost:3000`

---

## 🧪 **API Endpoints**  

| Method | Endpoint                  | Description                       |
|---------|---------------------------|----------------------------------|
| GET     | `/`                        | Test API                         |
| POST    | `/analyze_email`           | Analyze phishing & emotions      |
| GET     | `/fetch_and_analyze`       | Fetch top 5 emails & analyze     |

---

## ⚡ **Usage**  

1. **Authenticate with Gmail**:  
   - Authenticate using OAuth2 to fetch emails.  
2. **Analyze Emails**:  
   - Emails will be analyzed for phishing attempts and emotional manipulation.  
3. **View Results**:  
   - Results will be displayed on the dashboard.  

---

## 🧑‍💻 **Contributing**  

Contributions are welcome! Feel free to fork the repository and submit a pull request.  

1. Fork the repo.  
2. Create a new branch:  
```bash
git checkout -b feature-branch
```
3. Commit your changes:  
```bash
git commit -m "Add your feature"
```
4. Push the branch:  
```bash
git push origin feature-branch
```
5. Open a pull request.  

---

## 🛡️ **License**  

This project is licensed under the MIT License.  

---

## 📞 **Contact**  

- **Author:** Manish Kohli  
- **GitHub:** [Makkohli](https://github.com/Makkohli)  
- **Email:** manish@example.com  

---

This README provides detailed documentation for your project. If you'd like further customization, let me know! 😊
