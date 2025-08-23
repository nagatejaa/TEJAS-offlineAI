# Offline AI Setup Guide

## Installation Steps

1. **Install TTS Library**  
  ```bash
  pip install TTS
  ```

2. **Update and Install Dependencies**  
  ```bash
  sudo apt update
  sudo apt install espeak ffmpeg libsndfile1
  ```

3. **Test Installations**  
  Run the following script to verify the setup:  
  ```bash
  python3 test_installations.py
  ```

## Setting Up Dolphin-Llama3

### Download the Model
- Visit the [Dolphin-Llama3 Library](https://ollama.com/library/dolphin-llama3).
- Click on **Download** (top-right corner) for Windows or Mac.

### Installation for Linux
Run the following command to install Dolphin-Llama3:  
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Running the Model
1. In a terminal, execute one of the following commands to download and run the model:
  - For the 8B model (~5GB):  
    ```bash
    ollama run dolphin-llama3:8b
    ```
  - For the 70B model (~40GB):  
    ```bash
    ollama run dolphin-llama3:70b
    ```

  > **Note:** The download may take some time. Once prompted, enter the required input to proceed.

2. The server will continue running in the background. Use the following commands to manage the service:
  - **Stop the service:**  
    ```bash
    sudo systemctl stop --now ollama
    ```
  - **Restart the service:**  
    ```bash
    sudo systemctl start --now ollama
    ```

## Setting Up `ear.py`

### Install Dependencies
Run the following command to install the required Python libraries:  
```bash
pip install torch sounddevice numpy openai-whisper noisereduce
```

### Expected Output
When running the script, you should see:  
```
Loading Whisper (small) on cpu...
Speak... (Ctrl+C to stop)
```

### Example Conversation
```
You said: hello how are you
Say another sentence...
You said: open the window
Say another sentence...
```

Stop the application with `Ctrl+C`.

---

## Configuration

### Model Size
You can adjust the model size in the code:  
```python
MODEL_SIZE = "small"   # tiny / base / small / medium / large
```
- `tiny`: Fastest, least accurate  
- `large`: Slowest, most accurate  

### Noise Reduction Strength
Modify the noise reduction parameters in the code:  
```python
reduced = nr.reduce_noise(y=audio_np, sr=SAMPLE_RATE)
```
For stronger noise removal, add parameters like:  
```python
reduced = nr.reduce_noise(y=audio_np, sr=SAMPLE_RATE, prop_decrease=0.9)
```
Higher `prop_decrease` values result in stronger noise reduction.

### Energy VAD Threshold
Adjust the energy-based voice activity detection (VAD) threshold:  
```python
def energy_vad(audio, threshold=0.01):
  return np.sqrt(np.mean(audio**2)) > threshold
```
- Increase `threshold` (e.g., `0.02` or `0.03`) to make it less sensitive to background noise.  
- Decrease `threshold` (e.g., `0.005`) to make it more sensitive to quieter speech.

### Silence Duration Before Processing
Modify the silence duration in the code:  
```python
if silence_frames > 15:
```
Each `frame` is approximately 0.07 seconds. A value of `15` corresponds to ~1 second of silence before finalizing a sentence. Adjust this value for longer or shorter pauses.

---

## Tips
- Use headphones and an external microphone for better accuracy.  
- In noisy environments, increase the VAD threshold and enable stronger noise reduction.  
- For faster processing, use smaller models like `tiny` or `base`.

## Running the Application
After completing the setup, start the application by running:  
```bash
python3 main.py
```

This will launch the **TEJAS** application.

## Additional Resources
- For Dolphin-Llama3-related queries, refer to this [YouTube video](https://youtu.be/eiMSapoeyaU?si=lrEJrb3Vq_QolxHs).
- Follow this [YouTube tutorial](https://www.youtube.com/watch?v=eiMSapoeyaU&t=698s) for detailed installation steps.