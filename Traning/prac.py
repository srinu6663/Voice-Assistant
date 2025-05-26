import librosa
import soundfile as sf
import os

mp3_folder = "C:/Users/srinu/Downloads/Whatsapp-downlode/dataset"
wav_folder = "C:/Users/srinu/Downloads/Whatsapp-downlode/dataset/hey_eon"
os.makedirs(wav_folder, exist_ok=True)

for filename in os.listdir(mp3_folder):
    if filename.endswith(".mp3"):
        mp3_path = os.path.join(mp3_folder, filename)
        wav_filename = os.path.splitext(filename)[0] + ".wav"
        wav_path = os.path.join(wav_folder, wav_filename)

        y, sr = librosa.load(mp3_path, sr=16000, mono=True)
        sf.write(wav_path, y, sr)

        print(f"✅ Converted (librosa): {filename} → {wav_filename}")
