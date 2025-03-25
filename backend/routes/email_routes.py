from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np
from scipy.sparse import csr_matrix, hstack
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
from typing import Optional
from dotenv import load_dotenv
import requests
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path

# ✅ Initialize NLTK
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

router = APIRouter()

# ✅ Gemini AI Setup (Optional)
load_dotenv()
try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        GEMINI_ENABLED = True
        print("✅ Gemini AI is enabled.")
    else:
        GEMINI_ENABLED = False
        print("⚠️ GEMINI_API_KEY not found. Gemini AI disabled.")
except ImportError:
    GEMINI_ENABLED = False
    print("⚠️ google.generativeai module not installed. Gemini AI disabled.")

# ✅ Gmail Authentication
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    try:
        # Correct credential path
        credential_path = Path(__file__).resolve().parent.parent / 'credential.json'
        if not credential_path.exists():
            raise FileNotFoundError(f"❗ Credential file not found at {credential_path}")

        # Initialize the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credential_path),
            scopes=SCOPES,
            redirect_uri="http://localhost:51295/"
        )

        # Start the local server for authentication
        creds = flow.run_local_server(port=51295)
        service = build('gmail', 'v1', credentials=creds)
        print("✅ Authentication successful")
        return service
    except Exception as e:
        print(f"❗ Authentication failed: {e}")
        return None
    
# ✅ Fetch Top 5 Emails
def fetch_top_emails(service, max_results=5):
    try:
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        if not messages:
            print("📭 No emails found.")
            return []

        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

            # Extract Subject
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")

            # Extract Body
            body = "No Body Available"
            parts = msg_data.get('payload', {}).get('parts', [])
            for part in parts:
                if part.get('mimeType') == 'text/plain':
                    body_data = part.get('body', {}).get('data', '')
                    body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                    break

            emails.append({"subject": subject, "body": body})

        print("✅ Fetched Top 5 Emails.")
        return emails
    except HttpError as error:
        print(f"❗ Gmail API Error: {error}")
        return []

# ✅ Text Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

# ✅ Load Models
try:
    BASE_DIR = Path(__file__).resolve().parent.parent
    MODELS_DIR = BASE_DIR / "models"
    
    phishing_model = joblib.load(MODELS_DIR / "phishing_model.pkl")
    emotion_model = joblib.load(MODELS_DIR / "emotion_model.pkl")
    
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    print(f"✅ Phishing Model Classes: {phishing_model.classes_}")
    print(f"✅ Emotion Model Classes: {emotion_model.classes_}")
    
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Model loading failed: {str(e)}")

# ✅ Email Data Schema
class EmailData(BaseModel):
    subject: str
    body: str

# ✅ Get Top Emotions
def get_top_emotions(emotion_probs, top_n=2):
    sorted_indices = np.argsort(emotion_probs)[-top_n:][::-1]
    return [{"emotion": emotion_model.classes_[i], "score": float(emotion_probs[i])} 
            for i in sorted_indices]

# ✅ Analyze with Gemini
async def analyze_with_gemini(subject: str, body: str) -> Optional[str]:
    if not GEMINI_ENABLED:
        return None
    
    try:
        prompt = f"""
        Analyze this email for phishing attempts and emotional tone.
        Provide a concise analysis in this format:
        
        Phishing Likelihood: [Low/Medium/High]
        Emotional Tone: [Primary Emotion]
        Analysis: [2-3 sentence explanation]
        
        Email Subject: {subject}
        Email Body: {body}
        """
        response = gemini_model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else None
    except Exception as e:
        print(f"Gemini analysis failed: {e}")
        return None

# ✅ API Endpoint for Analysis
@router.post("/analyze_email")
async def analyze_email(data: EmailData):
    gemini_analysis = await analyze_with_gemini(data.subject, data.body)
    try:
        email_text = f"{data.subject} {data.body}"
        processed_text = preprocess_text(email_text)

        vectorized = vectorizer.fit_transform([processed_text])
        if vectorized.shape[1] < 5000:
            padding = csr_matrix((vectorized.shape[0], 5000 - vectorized.shape[1]))
            vectorized = hstack([vectorized, padding])

        features = vectorized.toarray()
        phishing_proba = phishing_model.predict_proba(features)[0]
        emotion_proba = emotion_model.predict_proba(features)[0]

        phishing_pred = np.argmax(phishing_proba)
        phishing_score = float(phishing_proba[phishing_pred])

        result = {
            "analysis": {
                "source": "Gemini AI" if gemini_analysis else "Local Models",
                "content": gemini_analysis if gemini_analysis else None
            },
            "phishing": {
                "result": "Phishing" if phishing_pred == 1 else "Not Phishing",
                "score": round(phishing_score, 4),
                "confidence": "High" if phishing_score > 0.75 
                             else "Medium" if phishing_score > 0.5 
                             else "Low"
            },
            "emotions": {
                "primary": get_top_emotions(emotion_proba, 1)[0],
                "top_emotions": get_top_emotions(emotion_proba, 3),
                "all_emotions": {emotion_model.classes_[i]: round(float(prob), 4) 
                               for i, prob in enumerate(emotion_proba)}
            }
        }

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# ✅ API to Fetch and Analyze
@router.get("/fetch_and_analyze")
async def fetch_and_analyze():
    service = authenticate_gmail()
    emails = fetch_top_emails(service)

    if not emails:
        return {"message": "No emails found."}

    analysis_results = []
    
    # Directly call the analyze_email function
    for email in emails:
        try:
            result = await analyze_email(EmailData(**email))
            analysis_results.append(result)
        except Exception as e:
            analysis_results.append({"error": str(e)})

    return {"results": analysis_results}
