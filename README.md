# morning-bot
Morning Briefing Script

## Pre-requisites
- Python 3.8+

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/morning-bot.git
   cd morning-bot
   ```

2. Create a virtual environment
   ```bash
   python3 -m venv venv
   ```

3. Activate venv
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables
   - Create a `.env` file in the root directory
   - Add your API keys and configurations, e.g.:
     ```
     WEATHER_API_KEY=your_weather_api_key
     ```

6. Run the script
   ```bash
   python src/main.py
   ```