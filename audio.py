import pyaudio
import numpy as np
import librosa
import obswebsocket
from obswebsocket import obsws, requests
import os
import sys

# OBS WebSocket configuration
obs_host = "localhost"
obs_port = 4444
obs_password = "your_obs_password"

# Connect to OBS WebSocket
obs_ws = obsws(obs_host, obs_port, obs_password)
obs_ws.connect()

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Threshold for music detection
threshold = 0.02

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the audio stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Monitoring audio input...")

try:
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)

        # Convert audio data to numpy array for analysis
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Calculate the Root Mean Square (RMS) of the audio signal
        rms = np.sqrt(np.mean(np.square(audio_data)))

        # If the RMS exceeds the threshold, consider it as music
        if rms > threshold:
            print("Music detected!")
            # Send command to OBS to play the specific audio file
            obs_ws.call(requests.PlayPauseMedia(source="your_specific_audio_file_source"))

        # Prompt for user input
        user_input = input("Enter command ('reset' to restart, 'exit' to quit): ")

        # Process user input
        if user_input == 'reset':
            # Close current ports and restart the program
            stream.stop_stream()
            stream.close()
            audio.terminate()
            obs_ws.disconnect()
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif user_input == 'exit':
            # Close current ports and exit the program
            stream.stop_stream()
            stream.close()
            audio.terminate()
            obs_ws.disconnect()
            sys.exit()

finally:
    # Close the audio stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # Disconnect from OBS WebSocket
    obs_ws.disconnect()

# Make sure you have installed the required libraries using:
# Enter in macOS Terminal: 'pip install pyaudio librosa obs-websocket-py'

# Replace "your_obs_password" with the password you set for your OBS WebSocket server.
# Make sure your OBS is running and the WebSocket plug-in is enabled and the password is set correctly.

# Also, replace "your_specific_audio_file_source" with the name of the audio file source
# you want to play in OBS when music is detected.

# In addition, please confirm the numerical size of the ‘threshold’ parameter through debugging.
# This number will affect the sensitivity of the program to cut off the live audio.
