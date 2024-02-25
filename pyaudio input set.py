# display
import pyaudio

p = pyaudio.PyAudio()
# print(p)
device_index = 0

for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info.get('name', '').find('i2s') != -1:
        print(device_info)
        device_index = device_info.get('index')

print('Selected device index: {}'.format(device_index))

# output exp：
# {'index': 1, 'structVersion': 2,
# 'name': 'snd_rpi_i2s_card: simple-card_codec_link snd-soc-dummy-dai-0 (hw:1,0)',
# 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 2,
# 'defaultLowInputLatency': 0.005804988662131519,
# 'defaultLowOutputLatency': 0.005804988662131519,
# 'defaultHighInputLatency': 0.034829931972789115,
# 'defaultHighOutputLatency': 0.034829931972789115,
# 'defaultSampleRate': 44100.0}
# Selected device index: {device_index}

# set
import pyaudio

p = pyaudio.PyAudio()


def record_wav(duration):
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=10,  # 指定设备的index值
                    frames_per_buffer=CHUNK)
