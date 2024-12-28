from gtts import gTTS
import io

class Accessibility:
    def __init__(self):
        self.dyslexia_friendly = False
        self.high_contrast = False

    def text_to_speech(self, text):
        tts = gTTS(text=text, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)  # Write directly to the BytesIO buffer
        audio_buffer.seek(0)  # Move to the beginning of the BytesIO buffer
        return audio_buffer  # Return the audio buffer

    def toggle_dyslexia_friendly(self):
        self.dyslexia_friendly = not self.dyslexia_friendly
        # Implement font and color changes here

    def toggle_high_contrast(self):
        self.high_contrast = not self.high_contrast
        # Implement high contrast color changes here
