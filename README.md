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

## Running the Application
After completing the setup, start the application by running:  
```bash
python3 main.py
```

This will launch the **TEJAS** application.

## Additional Resources
- For Dolphin-Llama3-related queries, refer to this [YouTube video](https://youtu.be/eiMSapoeyaU?si=lrEJrb3Vq_QolxHs).
- Follow this [YouTube tutorial](https://www.youtube.com/watch?v=eiMSapoeyaU&t=698s) for detailed installation steps.