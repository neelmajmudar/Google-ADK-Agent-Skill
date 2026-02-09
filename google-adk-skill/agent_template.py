"""
Google ADK Agent Template — Multi-Tool Agent with Session State

Usage:
  1. Copy this folder as your agent project
  2. Update .env with your API key
  3. Customize tools and agent instruction
  4. Run: adk web <folder_name>
"""

import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import ToolContext


# --- Tool Definitions ---
# Tips:
#   - Use descriptive verb-noun names
#   - Always include full docstrings with Args and Returns
#   - Return dicts for structured data
#   - Include tool_context param (not in docstring) if you need state access


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city: The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict with 'status' and 'report' or 'error_message'.
    """
    timezone_map = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
    }

    tz_id = timezone_map.get(city.lower())
    if not tz_id:
        return {"status": "error", "error_message": f"Timezone not found for '{city}'."}

    now = datetime.datetime.now(ZoneInfo(tz_id))
    return {"status": "success", "report": f"Current time in {city}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"}


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city: The name of the city to get weather for.

    Returns:
        dict with 'status' and 'report' or 'error_message'.
    """
    # Replace with real API call in production
    mock_weather = {
        "new york": "Sunny, 25°C (77°F)",
        "london": "Cloudy, 15°C (59°F)",
        "tokyo": "Partly cloudy, 28°C (82°F)",
    }

    report = mock_weather.get(city.lower())
    if not report:
        return {"status": "error", "error_message": f"Weather data unavailable for '{city}'."}

    return {"status": "success", "report": f"Weather in {city}: {report}"}


def save_user_preference(key: str, value: str, tool_context: ToolContext) -> dict:
    """Saves a user preference that persists across sessions.

    Args:
        key: The preference name (e.g., "favorite_city", "units").
        value: The preference value.

    Returns:
        dict confirming the save.
    """
    tool_context.state[f"user:{key}"] = value
    return {"status": "saved", "key": key, "value": value}


# --- Agent Definition ---
# The variable MUST be named root_agent for `adk web` / `adk run` to find it.

root_agent = Agent(
    model="gemini-2.5-flash",
    name="assistant",
    description="A helpful assistant that provides time, weather, and remembers user preferences.",
    instruction="""You are a friendly and helpful assistant.

You can:
1. Tell the current time in various cities using 'get_current_time'
2. Provide weather reports using 'get_weather'
3. Save user preferences using 'save_user_preference'

When the user asks about time or weather, use the appropriate tool.
If the user expresses a preference (e.g., "my favorite city is Paris"),
save it using save_user_preference.

Always be concise and friendly in your responses.""",
    tools=[get_current_time, get_weather, save_user_preference],
)
