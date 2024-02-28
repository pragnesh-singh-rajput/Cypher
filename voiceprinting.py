# Import the libraries
import speech_recognition as sr
import pyttsx3
import pyaudio
import wave
import numpy as np
import librosa
import scipy
import os

# Create a recognizer and a microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Create a text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150) # Set the speech rate

# Define a function to record and save voice samples
def record_voice(file_name, duration):
    # Create a pyaudio object
    p = pyaudio.PyAudio()
    # Open a stream with the default parameters
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    # Start recording
    print("Recording...")
    frames = []
    # Loop until the duration is reached
    for i in range(0, int(44100 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    # Stop recording
    print("Done.")
    # Close the stream and the pyaudio object
    stream.stop_stream()
    stream.close()
    p.terminate()
    # Save the voice sample as a WAV file
    wf = wave.open(file_name, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b"".join(frames))
    wf.close()

# Define a function to extract voice features
def extract_voice_features(file_name):
    # Load the voice sample
    y, sr = librosa.load(file_name)
    # Extract the pitch, tone, and intensity features
    pitch = librosa.feature.chroma_stft(y=y, sr=sr)
    tone = librosa.feature.tonnetz(y=y, sr=sr)
    intensity = librosa.feature.rms(y=y)
    # Concatenate the features into a single vector
    features = np.concatenate((pitch.mean(axis=1), tone.mean(axis=1), intensity.mean(axis=1)))
    # Return the features
    return features

# Define a function to compare voice features
def compare_voice_features(features1, features2):
    # Calculate the cosine similarity between the features
    similarity = scipy.spatial.distance.cosine(features1, features2)
    # Return the similarity
    return similarity

# Define a function to perform voice authentication
def voice_authentication():
    # Prompt the user to say something
    engine.say("Please say something to authenticate yourself.")
    engine.runAndWait()
    print("Please say something to authenticate yourself.")
    # Capture the voice input from the microphone
    with microphone as source:
        audio = recognizer.listen(source)
    # Convert the voice input to text using Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio)
        print("You said: {}".format(text))
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return
    except sr.RequestError as e:
        print("Sorry, I could not connect to Google Speech Recognition. {}".format(e))
        return
    # Record and save the voice input as a WAV file
    record_voice("voice_input.wav", 3)
    # Extract the voice features from the voice input
    input_features = extract_voice_features("voice_input.wav")
    # Compare the voice features with the voice database
    min_similarity = 1 # Initialize the minimum similarity
    user_name = None # Initialize the user name
    user_access = None # Initialize the user access
    for name, access, features in voice_database:
        # Calculate the similarity between the input features and the database features
        similarity = compare_voice_features(input_features, features)
        # Update the minimum similarity and the user name and access if the similarity is lower
        if similarity < min_similarity:
            min_similarity = similarity
            user_name = name
            user_access = access
    # Set a threshold for the similarity
    threshold = 0.1
    # Check if the similarity is below the threshold
    if min_similarity < threshold:
        # Greet the user and tell their access level
        engine.say("Hello, {}. You have {} access.".format(user_name, user_access))
        engine.runAndWait()
        print("Hello, {}. You have {} access.".format(user_name, user_access))
    else:
        # Reject the user and tell them to try again
        engine.say("Sorry, I could not authenticate you. Please try again.")
        engine.runAndWait()
        print("Sorry, I could not authenticate you. Please try again.")
    # Remove the voice input file
    os.remove("voice_input.wav")

# Create a voice database with some sample users and their voice features and access levels
voice_database = [
    ("Max", "admin", extract_voice_features("VoiceDB/max.wav")),
    #("Radar", "moderator", extract_voice_features("VoiceDB/radar.wav")),
    #("Hero", "user", extract_voice_features("VoiceDB/hero.wav")),
    #("Annu"' "guest"' extract_voice_features("VoiceDB/annu.wav"))
]

# Call the voice authentication function
voice_authentication()
