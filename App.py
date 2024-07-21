from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, SelectField
from flask_uploads import UploadSet, configure_uploads
import os
import moviepy.editor as mp
from pydub import AudioSegment
import openai
import googletrans
from gtts import gTTS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOADED_VIDEOS_DEST'] = 'uploads/videos'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # Set maximum file size to 1GB

# Configure file upload
videos = UploadSet('videos', ('mp4', 'avi', 'mov'))
configure_uploads(app, videos)

# Form for uploading video and selecting target language
class UploadForm(FlaskForm):
    video = FileField('Video', validators=[FileRequired()])
    language = SelectField('Target Language', choices=[
        ('hi', 'Hindi'),
        ('en', 'English'),
        ('bn', 'Bengali'),
        ('zh-CN', 'Mandarin'),
        ('es', 'Spanish'),
        ('id', 'Indonesian'),
        ('ur', 'Urdu'),
        ('pt', 'Portuguese'),
        ('ru', 'Russian'),
        ('ja', 'Japanese'),
        ('tl', 'Tagalog'),
        ('ar', 'Arabic')
    ])
    submit = SubmitField('Translate')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = videos.save(form.video.data)
        language = form.language.data
        return redirect(url_for('translate', filename=filename, language=language))
    return render_template('index.html', form=form)

@app.route('/translate/<filename>/<language>')
def translate(filename, language):
    video_path = os.path.join(app.config['UPLOADED_VIDEOS_DEST'], filename)
    original_text, translated_text, translated_back_text, similarity_score = translate_video(video_path, language)
    
    # Save texts to files dynamically
    with open('Original_Language.txt', 'w', encoding='utf-8') as f:
        f.write(original_text)
    
    target_language_file = f'Target_Language_{language}.txt'
    with open(target_language_file, 'w', encoding='utf-8') as f:
        f.write(translated_text)
    
    return render_template('result.html', original_text=original_text, translated_text=translated_text, translated_back_text=translated_back_text, similarity_score=similarity_score, language=language)

def translate_video(video_path, target_language):
    def extract_audio(video_path, audio_path):
        clip = mp.VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)

    def chunk_audio(audio_path, chunk_length=15*60*1000):
        audio = AudioSegment.from_file(audio_path)
        if len(audio) <= chunk_length:
            return [audio]
        chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
        return chunks

    def transcribe_audio_whisper(audio_chunk):
        openai.api_key = 'insert key here'
        response = openai.Audio.transcribe("whisper-1", audio_chunk)
        return response['text']

    def translate_text(text, target_language):
        translator = googletrans.Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text

    def compute_similarity(text1, text2):
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors)
        return cosine_sim[0, 1]

    audio_path = "uploads/videos/extracted_audio.mp3"
    extract_audio(video_path, audio_path)

    chunks = chunk_audio(audio_path)
    full_transcription = ""

    for chunk in chunks:
        chunk.export("uploads/videos/temp_chunk.mp3", format="mp3")
        transcription = transcribe_audio_whisper(open("uploads/videos/temp_chunk.mp3", "rb"))
        #transcription = transcribe_audio_whisper("uploads/videos/temp_chunk.mp3")
        full_transcription += transcription + " "

    corrected_transcription = full_transcription

    translated_text = translate_text(corrected_transcription, target_language)
    translated_back_to_english = translate_text(translated_text, 'en')
    similarity_score = compute_similarity(corrected_transcription, translated_back_to_english) * 100  # Convert to percentage

    return corrected_transcription, translated_text, translated_back_to_english, similarity_score

if __name__ == '__main__':
    app.run(debug=True)
