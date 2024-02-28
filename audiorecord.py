# Import the libraries
import pyaudio
import wave

# Set the parameters
filename = "VoiceDB/annu.wav" # The file name to save the audio
chunk = 1024 # The number of samples per buffer
format = pyaudio.paInt16 # The sample format
channels = 1 # The number of channels
rate = 44100 # The sample rate
duration = 5 # The duration of recording in seconds

# Create a pyaudio object
p = pyaudio.PyAudio()

# Open a stream with the specified parameters
stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

# Start recording
print("Recording...")
frames = [] # A list to store the audio data
# Loop until the duration is reached
for i in range(0, int(rate / chunk * duration)):
    # Read data from the stream
    data = stream.read(chunk)
    # Append the data to the frames list
    frames.append(data)

# Stop recording
print("Done.")
# Close the stream and the pyaudio object
stream.stop_stream()
stream.close()
p.terminate()

# Save the audio data as a WAV file
wf = wave.open(filename, "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(format))
wf.setframerate(rate)
wf.writeframes(b"".join(frames))
wf.close()
