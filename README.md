# Luna - Voice-Activated AI Personal Assistant

Luna is a conversational, voice-controlled AI assistant built in Python. Powered by the Google Gemini API, Luna can listen to your voice commands, maintain context across an entire conversation, respond with a synthesized vocal personality, and execute local automation tools on your computer.

## Features

*   **Voice Interface**: True hands-free interaction using low-level microphone capturing and offline text-to-speech engine execution.
*   **Contextual Memory**: Built using stateful chat tracking, allowing for natural, multi-turn conversations where the assistant remembers previous prompts.
*   **Function Calling (Tools)**: Seamless integration with local Python functions, allowing the AI to check the system time, date, or open websites in your browser dynamically based on raw speech.
*   **Sanitized Output**: Automatic scrubbing of markdown syntax to ensure spoken audio flows naturally without reading technical formatting out loud.

## Installation & Setup

*   **Clone the Repository**
*  ***Install Dependencies***
```bash
pip install sounddevice speech_recognition pyttsx3 google-genai python-dotenv
```
* ***Configure Your API Key***
1. Obtain an API Key and create a file named .env in the root directory of your project
2. Add your key to the file exactly like this
```bash
GEMINI_API_KEY="your_actual_api_key_here")
```

* ***Usage***
```bash
py luna.py
```
* ***Some Interactions to Try***
1. Conversational Memory: Ask "What is the capital of India?" followed immediately by "What is the population of that city?" Luna will preserve the context.
2. System Tools: Say "Luna, what time is it?" or "Luna, check the date."
3. Web Automation: Say "Luna, open a popular E-commerce website."
To close down the assistant gracefully, simply say "shut down" or "exit" during a listening prompt.

## Technical Architecture
1. Brain: ```google-gen-ai``` SDK utilizing the ```gemini-3.5-flash``` model.
2. Ears (Speech-to-Text): Raw audio byte streams captured via ```sounddevice``` and transcribed using Google Speech Recognition Cloud API wrapper.
3. Voice (Text-to-Speech): powered by ```pyttsx3```, to ensure thread stability alongside open microphone streams.
4. Agentic Execution: Automated tool parsing using native Gemini tool definitions and docstring declarations.
