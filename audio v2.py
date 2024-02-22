import time
import os
import sys
from datetime import datetime
import pyaudio
import numpy as np
from obswebsocket import obsws, requests
from threading import Thread

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
THRESHOLD = 0.02  # Threshold for music detection

# Flag to control audio monitoring
stop_audio_flag = False


# Function to create a log file
def create_log(log_path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_filename = os.path.join(log_path, f"OBS_audio_control_log_{timestamp}.txt")
    with open(log_filename, "w") as log_file:
        log_file.write("Log file created.\n")
    return log_filename


# Function to write to the log file
def write_to_log(log_filename, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_filename, "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")


# Function to switch audio source and play music in OBS
def switch_and_play_music():
    obs_ws.call(requests.SetCurrentScene(sceneName="Your Scene Name"))
    obs_ws.call(requests.SetMute(mute=True, source="Your Source Name"))  # Mute original audio source
    obs_ws.call(requests.SetSourceRender(source="Your Source Name", render=False))  # Disable original audio source
    obs_ws.call(requests.SetSourceRender(source="Your New Source Name", render=True))  # Enable new audio source
    obs_ws.call(requests.PlayPauseMedia(source="Your Music File"))  # Play music file


# Function to switch back audio source in OBS
def switch_back_audio():
    obs_ws.call(requests.SetCurrentScene(sceneName="Your Scene Name"))
    obs_ws.call(requests.SetMute(mute=False, source="Your Source Name"))  # Unmute original audio source
    obs_ws.call(requests.SetSourceRender(source="Your Source Name", render=True))  # Enable original audio source
    obs_ws.call(requests.SetSourceRender(source="Your New Source Name", render=False))  # Disable new audio source


# Function to stop audio monitoring
def stop_audio_monitoring(p, stream):
    global stop_audio_flag
    stop_audio_flag = True
    if stream:
        stream.stop_stream()
        stream.close()
    if p:
        p.terminate()


# Monitoring 1: Ambient microphone monitoring
def monitoring_1(log_filename):
    status_display("Ambient microphone monitoring")
    write_to_log(log_filename, "Ambient microphone monitoring")
    time.sleep(5)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    global stop_audio_flag
    stop_audio_flag = False

    while not stop_audio_flag:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(np.square(audio_data)))

        if rms > THRESHOLD:
            status_display("Music detected!")
            write_to_log(log_filename, "Music detected!")
            switch_and_play_music()
            break

    stop_audio_monitoring(p, stream)
    monitoring_2(log_filename)


# Monitoring 2: Waiting for music to stop
def monitoring_2(log_filename):
    status_display("Waiting for the music in the Ambient microphone to stop")
    write_to_log(log_filename, "Waiting for the music in the Ambient microphone to stop")
    time.sleep(5)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    global stop_audio_flag
    stop_audio_flag = False

    while not stop_audio_flag:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(np.square(audio_data)))

        if rms < THRESHOLD:
            status_display("Music stopped")
            write_to_log(log_filename, "Music stopped")
            switch_back_audio()
            break

    stop_audio_monitoring(p, stream)
    monitoring_1(log_filename)


# Function to display specific information in a status box
def status_display(message):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Enter 'start' to start monitoring, enter 'stop' to stop monitoring, enter 'exit' to exit.")
    print(message)


# System module
def system_module():
    print("Enter 'start' to start monitoring, enter 'stop' to stop monitoring, enter 'exit' to exit.")
    time.sleep(5)  # Wait for 5 seconds before starting monitoring

    log_path = "/path/to/log/directory"  # Specify the log file path here
    log_filename = create_log(log_path)
    status_display("On standby...")

    while True:
        command = input("Enter command: ")

        if command == "start":
            status_display("Starting monitoring...")
            stop_audio_flag = True
            time.sleep(1)
            monitoring_thread = Thread(target=monitoring_1, args=(log_filename,))
            monitoring_thread.start()
        elif command == "stop":
            status_display("Stopping monitoring...")
            write_to_log(log_filename, "Monitoring stopped.")
            time.sleep(1)
            stop_audio_flag = True
            time.sleep(1)
            status_display("On standby...")
            break
        elif command == "exit":
            status_display("Exiting program...")
            write_to_log(log_filename, "Program exited.")
            time.sleep(1)
            stop_audio_flag = True
            time.sleep(1)
            obs_ws.disconnect()
            time.sleep(1)
            sys.exit()


# Entry point of the program
if __name__ == "__main__":
    system_module()
