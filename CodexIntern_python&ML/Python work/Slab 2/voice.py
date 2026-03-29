import speech_recognition as sr
import pyttsx3
import datetime
import requests
import json
import time
import threading
import schedule
import os
from datetime import datetime, timedelta
import webbrowser
import random

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS engine
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)  # Female voice
        self.tts_engine.setProperty('rate', 150)
        
        # Store reminders and tasks
        self.reminders = []
        self.news_sources = ['bbc-news', 'cnn', 'the-verge', 'techcrunch']
        
        # API Keys (You'll need to get these from the respective services)
        self.weather_api_key = "YOUR_OPENWEATHER_API_KEY"  # Get from openweathermap.org
        self.news_api_key = "YOUR_NEWSAPI_KEY"  # Get from newsapi.org
        
        # Assistant state
        self.is_listening = False
        self.assistant_name = "Athena"
        
        print(f"🎯 {self.assistant_name} Voice Assistant Initialized!")
        print("Commands: 'reminder', 'weather', 'news', 'time', 'date', 'joke', 'stop'")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 {self.assistant_name}: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("⚡ Processing...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return ""
        except sr.RequestError as e:
            self.speak("There seems to be a problem with the speech recognition service.")
            print(f"Speech recognition error: {e}")
            return ""
    
    def set_reminder(self, command):
        """Set a reminder based on voice command"""
        try:
            # Parse time from command
            time_keywords = ['in', 'at', 'for']
            time_index = -1
            time_unit = None
            
            for word in time_keywords:
                if word in command:
                    time_index = command.find(word)
                    break
            
            if time_index == -1:
                self.speak("Please specify when you want the reminder. For example: 'set reminder in 10 minutes to call mom'")
                return
            
            # Extract time and message
            parts = command[time_index:].split()
            time_value = None
            time_type = None
            
            # Look for time patterns
            for i, part in enumerate(parts):
                if part.isdigit():
                    time_value = int(part)
                    if i + 1 < len(parts):
                        time_type = parts[i + 1]
                        reminder_text = ' '.join(parts[i + 2:])
                        break
            
            if not time_value or not time_type:
                self.speak("I couldn't understand the time. Please try again.")
                return
            
            # Calculate reminder time
            now = datetime.now()
            if 'minute' in time_type:
                reminder_time = now + timedelta(minutes=time_value)
            elif 'hour' in time_type:
                reminder_time = now + timedelta(hours=time_value)
            elif 'day' in time_type:
                reminder_time = now + timedelta(days=time_value)
            else:
                self.speak("Please specify minutes, hours, or days for the reminder.")
                return
            
            # Store reminder
            reminder = {
                'time': reminder_time,
                'message': reminder_text,
                'active': True
            }
            self.reminders.append(reminder)
            
            self.speak(f"Reminder set! I'll remind you to {reminder_text} at {reminder_time.strftime('%I:%M %p')}")
            
        except Exception as e:
            self.speak("Sorry, I had trouble setting that reminder. Please try again.")
            print(f"Reminder error: {e}")
    
    def check_reminders(self):
        """Check and notify about due reminders"""
        now = datetime.now()
        for reminder in self.reminders[:]:
            if reminder['active'] and now >= reminder['time']:
                self.speak(f"Reminder: {reminder['message']}")
                reminder['active'] = False
                self.reminders.remove(reminder)
    
    def get_weather(self, location=None):
        """Get weather information for a location"""
        try:
            if not location:
                self.speak("Which city would you like the weather for?")
                location_command = self.listen()
                if location_command:
                    # Extract city name from command
                    location = location_command.replace('weather', '').replace('in', '').strip()
            
            if not location:
                location = "London"  # Default location
            
            # Use OpenWeatherMap API
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=metric"
            
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                
                weather_report = f"The weather in {location} is {description}. Temperature is {temp}°C with {humidity}% humidity."
                self.speak(weather_report)
            else:
                self.speak(f"Sorry, I couldn't get the weather for {location}. Please check the city name.")
                
        except Exception as e:
            self.speak("I'm having trouble accessing weather information right now.")
            print(f"Weather error: {e}")
    
    def get_news(self, category='general'):
        """Get latest news headlines"""
        try:
            if not self.news_api_key or self.news_api_key == "YOUR_NEWSAPI_KEY":
                self.speak("News feature requires a News API key. Please set it up in the code.")
                return
            
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.news_api_key}"
            
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data['articles']:
                articles = data['articles'][:5]  # Get top 5 headlines
                
                self.speak("Here are the latest news headlines:")
                for i, article in enumerate(articles, 1):
                    title = article['title'].split(' - ')[0]  # Remove source from title
                    self.speak(f"Headline {i}: {title}")
                    time.sleep(1)
                
                self.speak("That's all for now.")
            else:
                self.speak("Sorry, I couldn't fetch the news right now.")
                
        except Exception as e:
            self.speak("I'm having trouble accessing news updates.")
            print(f"News error: {e}")
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why couldn't the bicycle stand up by itself? It was two tired!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why did the coffee file a police report? It got mugged!",
            "Why don't skeletons fight each other? They don't have the guts!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {current_date}")
    
    def open_website(self, site_name):
        """Open commonly used websites"""
        sites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'gmail': 'https://mail.google.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'github': 'https://www.github.com'
        }
        
        if site_name in sites:
            webbrowser.open(sites[site_name])
            self.speak(f"Opening {site_name}")
        else:
            self.speak(f"I don't know how to open {site_name}")
    
    def calculate(self, expression):
        """Perform basic calculations"""
        try:
            # Simple calculation parsing
            expression = expression.replace('plus', '+').replace('minus', '-')
            expression = expression.replace('times', '*').replace('divided by', '/')
            expression = expression.replace('x', '*').replace('X', '*')
            
            # Remove non-math characters
            clean_expression = ''.join(c for c in expression if c in '0123456789+-*/.() ')
            result = eval(clean_expression)
            self.speak(f"The answer is {result}")
        except:
            self.speak("Sorry, I couldn't calculate that.")
    
    def system_info(self):
        """Provide system information"""
        import psutil
        import platform
        
        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Battery (if available)
        try:
            battery = psutil.sensors_battery()
            battery_percent = battery.percent if battery else "Unknown"
        except:
            battery_percent = "Unknown"
        
        info = f"System status: CPU usage is {cpu_usage}%, Memory usage is {memory_usage}%, Battery is at {battery_percent}%"
        self.speak(info)
    
    def process_command(self, command):
        """Process voice commands and execute appropriate functions"""
        command = command.lower()
        
        # Greetings
        if any(word in command for word in ['hello', 'hi', 'hey']):
            self.speak(f"Hello! I'm {self.assistant_name}, your voice assistant. How can I help you today?")
        
        # Reminders
        elif 'reminder' in command:
            self.set_reminder(command)
        
        # Weather
        elif 'weather' in command:
            self.get_weather(command)
        
        # News
        elif 'news' in command:
            self.get_news()
        
        # Time
        elif 'time' in command:
            self.get_time()
        
        # Date
        elif 'date' in command:
            self.get_date()
        
        # Jokes
        elif 'joke' in command:
            self.tell_joke()
        
        # Calculations
        elif any(word in command for word in ['calculate', 'what is', 'how much is']):
            self.calculate(command)
        
        # Open websites
        elif 'open' in command:
            site = command.replace('open', '').strip()
            self.open_website(site)
        
        # System info
        elif any(word in command for word in ['system', 'battery', 'cpu', 'memory']):
            self.system_info()
        
        # Help
        elif 'help' in command or 'what can you do' in command:
            self.show_help()
        
        # Stop/Escort
        elif any(word in command for word in ['stop', 'exit', 'quit', 'goodbye']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        else:
            self.speak("I'm not sure how to help with that. Say 'help' to see what I can do.")
        
        return True
    
    def show_help(self):
        """Show available commands"""
        help_text = """
        I can help you with:
        • Setting reminders (say 'set reminder in 10 minutes to call mom')
        • Weather updates (say 'weather in London')
        • News headlines (say 'news')
        • Current time and date (say 'time' or 'date')
        • Telling jokes (say 'tell me a joke')
        • Calculations (say 'calculate 15 plus 27')
        • Opening websites (say 'open google')
        • System information (say 'system status')
        • Or just say 'stop' to exit
        """
        self.speak("Here's what I can do for you:")
        print(help_text)
    
    def reminder_checker(self):
        """Background thread to check reminders"""
        while self.is_listening:
            self.check_reminders()
            time.sleep(30)  # Check every 30 seconds
    
    def run(self):
        """Main assistant loop"""
        self.speak(f"Hello! I'm {self.assistant_name}, your voice assistant. Say 'help' to see what I can do.")
        
        self.is_listening = True
        
        # Start reminder checker in background
        reminder_thread = threading.Thread(target=self.reminder_checker, daemon=True)
        reminder_thread.start()
        
        try:
            while self.is_listening:
                command = self.listen()
                if command:
                    if not self.process_command(command):
                        break
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.speak("Assistant shutting down. Goodbye!")
        finally:
            self.is_listening = False

# Alternative simple version without API dependencies
class SimpleVoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.assistant_name = "Alexa"
        
        # Configure TTS
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)
        self.tts_engine.setProperty('rate', 150)
        
        self.reminders = []
        
        print(f"🎯 {self.assistant_name} Simple Voice Assistant Ready!")
    
    def speak(self, text):
        print(f"🤖 {self.assistant_name}: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=5)
            
            command = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {command}")
            return command
        except:
            return ""
    
    def run_simple(self):
        """Simplified version without API dependencies"""
        self.speak("Simple voice assistant activated. Say hello to start!")
        
        while True:
            try:
                command = self.listen()
                
                if not command:
                    continue
                
                if 'hello' in command:
                    self.speak("Hello! How can I help you today?")
                
                elif 'time' in command:
                    current_time = datetime.now().strftime("%I:%M %p")
                    self.speak(f"The time is {current_time}")
                
                elif 'date' in command:
                    current_date = datetime.now().strftime("%A, %B %d")
                    self.speak(f"Today is {current_date}")
                
                elif 'joke' in command:
                    jokes = [
                        "Why did the computer go to the doctor? It had a virus!",
                        "Why do programmers prefer dark mode? Because light attracts bugs!",
                        "What do you call a computer that sings? A Dell!"
                    ]
                    self.speak(random.choice(jokes))
                
                elif 'stop' in command or 'exit' in command:
                    self.speak("Goodbye!")
                    break
                
                else:
                    self.speak("I can tell time, date, or jokes. Try saying 'what time is it'")
            
            except KeyboardInterrupt:
                self.speak("Assistant shutting down.")
                break

def main():
    """Main function to run the voice assistant"""
    print("=" * 60)
    print("🎯 VOICE-ACTIVATED PERSONAL ASSISTANT")
    print("=" * 60)
    print("Choose mode:")
    print("1. Full Assistant (requires API keys)")
    print("2. Simple Assistant (no API keys needed)")
    print("3. Test Mode (text input only)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        assistant = VoiceAssistant()
        assistant.run()
    elif choice == "2":
        assistant = SimpleVoiceAssistant()
        assistant.run_simple()
    elif choice == "3":
        test_mode()
    else:
        print("Invalid choice. Running simple mode...")
        assistant = SimpleVoiceAssistant()
        assistant.run_simple()

def test_mode():
    """Test the assistant with text input instead of voice"""
    assistant = VoiceAssistant()
    
    print("\n🔧 TEST MODE - Type commands instead of speaking")
    print("Type 'stop' to exit\n")
    
    while True:
        command = input("You: ").strip().lower()
        if command == 'stop':
            break
        if command:
            assistant.process_command(command)

if __name__ == "__main__":
    # Install required packages first:
    # pip install speechrecognition pyttsx3 requests schedule psutil
    
    main()