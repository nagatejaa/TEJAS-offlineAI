
import sys
import time
import threading
import webbrowser
from wikipedia import wikipedia
from HEAD.mouth import speak
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QA_FILE_PATH = os.path.join(BASE_DIR, "..", "DATA", "Brain_DATA", "qna.txt")
QA_FILE_PATH = os.path.normpath(QA_FILE_PATH)


# Load Q&A Data
def load_qa_data(file_path):
    qa_dict = {}
    with open(file_path, 'r', encoding='utf-8', errors="replace") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            if ':' not in line:
                print(f"Skipping invalid line {line_number}: '{line}' (No colon found)")
                continue
            parts = line.split(':', 1)
            if len(parts) != 2:
                print(f"Skipping invalid line {line_number}: '{line}' (Invalid format after split)")
                continue
            q, a = parts
            qa_dict[q.strip()] = a.strip()
    return qa_dict


# Save new Q&A pair
def save_qa_data(file_path, qa_dict, new_q, new_a):
    if new_q not in qa_dict:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{new_q}:{new_a}\n")
        qa_dict[new_q] = new_a  # Update in-memory dictionary


# Display text with animation
def print_animated_message(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.075)
    print()






def ask_ollama(question):
    """Send text to Ollama and get response."""
    try:
        result = subprocess.run(
            ["ollama", "run", "dolphin-llama3:8b"],
            input=question,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "🤖 Ollama did not respond in time."
    except Exception as e:
        return f"Error communicating with Ollama: {e}"


# Define array for command keywords
COMMAND_KEYWORDS = ["show", "browse", "open in browser", "search"]

# Main Function to Handle Input and Call Appropriate Functions
def mind(prompt):
    # Load Q&A data into memory
    qa_dict = load_qa_data(QA_FILE_PATH)

    # Normalize the prompt and extract core query
    core_query = prompt.lower().strip()

    # Check if the prompt starts with any command keywords and remove it
    for command in COMMAND_KEYWORDS:
        if core_query.startswith(command):
            # Remove the command keyword and clean the remaining query
            core_query = core_query.replace(command, "").strip()
            # Directly trigger Google search for commands
            return  # Exit after triggering Google search

    # Check the dataset for a response
    response = qa_dict.get(core_query)
    if response:
        animate_thread = threading.Thread(target=print_animated_message, args=(response,))
        speak_thread = threading.Thread(target=speak, args=(response,))
        animate_thread.start()
        speak_thread.start()
        animate_thread.join()
        speak_thread.join()
        return

    # Try fetching from Wikipedia for the cleaned query
    # response = wiki_search(core_query, qa_dict)
    # if response:
    #     return  # If Wikipedia returns a result, stop further processing.

    # # As a fallback, direct the user to Google for the cleaned query
    print(f"Querying Ollama for: {core_query}")
    response = ask_ollama(core_query)
    print(f"Ollama response: {response}")
    speak(response)
    if response:
        return


