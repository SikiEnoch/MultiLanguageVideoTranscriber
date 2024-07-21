# MultiLanguageVideoTranscriber

Overview
VideoTranslatorApp is a Flask-based web application that allows users to upload video files, extract audio, transcribe the audio to text, and translate the text into various target languages. The app provides a similarity score between the original transcription and the back-translated text to ensure translation accuracy.

Features
Upload Video: Users can upload video files in formats such as MP4, AVI, and MOV.
Audio Extraction: The app extracts audio from uploaded video files.
Audio Transcription: The audio is transcribed to text using OpenAI's Whisper API.
Text Translation: The transcribed text is translated into a user-selected target language.
Similarity Scoring: The app calculates a similarity score between the original transcription and the back-translated text to measure accuracy.
Text Files: Save original and translated texts to files.

Target Languages

The application supports translation to the following languages:
Hindi
English
Bengali
Mandarin
Spanish
Indonesian
Urdu
Portuguese
Russian
Japanese
Tagalog
Arabic
Prerequisites
Before running the application, ensure you have the following installed:

Python 3.6 or higher
Flask
Flask-WTF
Flask-Uploads
MoviePy
Pydub
OpenAI API Client
Googletrans
gTTS (Google Text-to-Speech)
Scikit-learn

Installation
Clone the repository:
python -m venv venv


pip install -r requirements.txt
Configure OpenAI API key:

Replace the placeholder 'sk-None-9xxxxxxxxx' with your actual OpenAI API key in translate_video().

Run the application
app.py

Access the application:
Open your web browser and navigate to http://localhost:5000.

Usage
On the homepage, upload a video file.
Select the target language for translation.
Click the "Translate" button.
View the original, translated, and back-translated texts, along with the similarity score.
File Structure

VideoTranslatorApp/
│
├── app.py                # Main application file
├── requirements.txt      # List of required Python packages
├── static/               # Static files (e.g., CSS, JavaScript)
├── templates/            # HTML templates
├── uploads/
│   └── videos/           # Directory for uploaded videos and processed audio
│
└── README.md             # Project documentation

License
This project is licensed under the MIT License. See the LICENSE file for details.
