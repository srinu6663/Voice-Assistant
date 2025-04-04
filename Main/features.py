import pywhatkit as kit

def play_youtube(song_name, speak):
    """Play a song on YouTube."""
    print(f"🎥 Playing {song_name} on YouTube...")
    speak(f"Playing {song_name} on YouTube.")
    kit.playonyt(song_name)
