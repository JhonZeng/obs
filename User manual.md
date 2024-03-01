User manual

### Setting Up OBSWebSocket Plugin:
1. **Introduction to OBSWebSocket Plugin:**
   - OBSWebSocket is a plugin that allows external applications to communicate with OBS Studio through a WebSocket connection.
   - It enables controlling OBS Studio programmatically, which is useful for automating tasks or integrating OBS with other software.

2. **Installing OBSWebSocket Plugin:**
   - Go to the OBSWebSocket GitHub repository: [obs-websocket](https://github.com/Palakis/obs-websocket).
   - Follow the installation instructions provided in the repository's README file.
   - Typically, you need to download the appropriate release for your operating system and install it by following the installation instructions.

### Setting Up OBS for Use with the Code:
1. **Configuring OBS with OBSWebSocket:**
   - Open OBS Studio and navigate to `Tools > WebSocket Server Settings`.
   - Enable the WebSocket server by checking the box labeled "Enable WebSocket server".
   - Take note of the server settings, including the server IP address, port number, and password.
   - By default, the server IP address is `localhost` and the port is `4444`. You may need to adjust these settings if you're connecting to OBS from a different device or network.

2. **Setting Scene and Source Names:**
   - In OBS Studio, set up your scenes and sources as needed for your live stream or recording.
   - Each scene and source has a name associated with it, which you will use in the code to control OBS.
   - Make sure to use descriptive names for scenes and sources to easily identify them in the code.

### Modifying the Python Script:
1. **Configuring OBS Connection in the Script:**
   - In the Python script, locate the OBS WebSocket configuration section.
   - Update the `obs_host`, `obs_port`, and `obs_password` variables with the appropriate values.
   - For example:
     ```python
     obs_host = "localhost"
     obs_port = 4444
     obs_password = "your_obs_password"
     ```

2. **Setting Scene and Source Names in the Script:**
   - Within the code, you'll find functions that interact with OBS scenes and sources.
   - Update the function calls with the names of your scenes and sources in OBS.
   - For example:
     ```python
     obs_ws.call(requests.SetCurrentScene(sceneName="Your Scene Name"))
     obs_ws.call(requests.SetMute(mute=True, source="Your Source Name"))
     ```

### Running the Script:
1. **Executing the Python Script:**
   - After making the necessary modifications to the script, run it using a Python interpreter.
   - Follow the command line prompts to set up the monitoring device, start and stop monitoring, or exit the program.
   - Ensure that the audio input device you want to monitor is selected correctly during the setup phase.

By following these instructions, you should be able to use the provided Python script to control OBS Studio and monitor audio input on macOS. If you encounter any issues, refer to the OBSWebSocket documentation or seek assistance from the OBS community.