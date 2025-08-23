# Offline AI Setup Guide

## Installation Steps

1. **Install TTS Library**  
  Install the TTS library using the following command:  
  ```bash
  pip install TTS
  ```

2. **Update and Install Dependencies**  
  Update your system and install the required dependencies:  
  ```bash
  sudo apt update
  sudo apt install espeak ffmpeg libsndfile1
  ```

3. **Verify Installations**  
  Run the script below to ensure the setup is correct:  
  ```bash
  python3 test_installations.py
  ```

## Setting Up Dolphin-Llama3

### Download the Model
- Visit the [Dolphin-Llama3 Library](https://ollama.com/library/dolphin-llama3).
- Select **Download** (top-right corner) for your operating system (Windows or Mac).

### Installation for Linux
Install Dolphin-Llama3 on Linux using the following command:  
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Running the Model
1. Use one of the commands below to download and run the model:
  - **8B Model (~5GB):**  
    ```bash
    ollama run dolphin-llama3:8b
    ```
  - **70B Model (~40GB):**  
    ```bash
    ollama run dolphin-llama3:70b
    ```

  > **Note:** The download process may take some time. Follow the prompts to proceed.

2. Manage the server using the following commands:
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
Install the required Python libraries:  
```bash
pip install torch sounddevice numpy openai-whisper noisereduce
```

### Noise Reduction Parameters
Adjust the noise reduction settings in the code:  
```python
audio_np = nr.reduce_noise(
   y=audio_np,
   sr=SAMPLE_RATE,
   n_std_thresh_stationary=1.5,  # Lower → less aggressive, higher → stronger
   prop_decrease=1.0,            # 1.0 = full suppression, 0.5 = partial
   stationary=True               # Use for constant background noise (e.g., fan/AC)
)
```
- **`n_std_thresh_stationary`:** Controls suppression strength. Default is `1.5`. Use `2.0–3.0` for noisy environments.  
- **`prop_decrease`:** Determines the amount of noise removed. `1.0` = full removal, `0.8` = partial removal.  
- **`stationary`:** Set to `True` for steady noise (e.g., fan, AC) or `False` for non-stationary noise (e.g., music, conversations).

### Voice Activity Detection (VAD)
Define VAD sensitivity in the code:  
```python
def is_speech(audio: np.ndarray, threshold: float = 0.03) -> bool:
   return np.sqrt(np.mean(audio**2)) > threshold
```
- **`threshold`:** Adjust sensitivity.  
  - Lower values (e.g., `0.02`) increase sensitivity but may trigger on background noise.  
  - Higher values (e.g., `0.05`) reduce false positives but may miss faint speech.

### Whisper Model Selection
Choose the appropriate Whisper model based on your requirements:  
- **`tiny` / `base`:** Fast, less accurate in noisy environments.  
- **`small` / `medium`:** Balanced accuracy and speed.  
- **`large`:** Best accuracy for noisy environments, requires more GPU memory.

## Configuration

### Model Size
Specify the model size in the code:  
```python
MODEL_SIZE = "small"   # Options: tiny, base, small, medium, large
```

### Noise Reduction Strength
Modify the noise reduction parameters for stronger suppression:  
```python
reduced = nr.reduce_noise(y=audio_np, sr=SAMPLE_RATE, prop_decrease=0.9)
```

### Energy-Based VAD Threshold
Adjust the energy threshold for VAD:  
```python
def energy_vad(audio, threshold=0.01):
   return np.sqrt(np.mean(audio**2)) > threshold
```
- Increase `threshold` (e.g., `0.02` or `0.03`) to reduce sensitivity to background noise.  
- Decrease `threshold` (e.g., `0.005`) to detect quieter speech.

### Silence Duration Before Processing
Set the silence duration in the code:  
```python
if silence_frames > 15:
```
- Each `frame` is ~0.07 seconds. A value of `15` corresponds to ~1 second of silence. Adjust as needed.

## Tips
- Use headphones and an external microphone for improved accuracy.  
- In noisy environments, increase the VAD threshold and enable stronger noise reduction.  
- For faster processing, use smaller models like `tiny` or `base`.

## Running the Application
Start the application by executing:  
```bash
python3 main.py
```

This will launch the **TEJAS** application.

## Additional Resources
- For Dolphin-Llama3-related queries, refer to this [YouTube video](https://youtu.be/eiMSapoeyaU?si=lrEJrb3Vq_QolxHs).  
- Follow this [YouTube tutorial](https://www.youtube.com/watch?v=eiMSapoeyaU&t=698s) for detailed installation steps.
