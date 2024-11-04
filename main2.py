from swarm import Swarm, Agent
import time
import random
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get and set API key directly
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

print(api_key)

# Set it once at the start
# api_key = os.environ["OPENAI_API_KEY"]

# Quick verification
# if not api_key.startswith("sk-"):
#     raise ValueError(
#         "Invalid API key format. OpenAI API keys should start with 'sk-'"
#     )

print(f"API key starts with: {api_key[:7]}")  # Verification print


# Define Result class for handling returns
@dataclass
class Result:
    value: str
    agent: Optional[Agent] = None
    context_variables: Optional[Dict[str, Any]] = None


def clear_screen():
    print("\033[H\033[J", end="")


def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


# For now, we'll just print the narrative and choices directly
def transfer_to_render(context_variables, narrative, choices):
    print("\n" + "=" * 50)
    print(narrative)
    print("\nChoices:")
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    print("=" * 50)
    return Result(value="Story displayed", context_variables=context_variables)


# Story Agent Definition
story_agent = Agent(
    name="Story Agent",
    model="gpt-4",  # Specifying model explicitly for better storytelling
    instructions="""You are a creative storyteller for a text adventure game. Your role is to:
1. Generate engaging narrative content
2. Provide 2-3 choices for the player at each story beat
3. Pass the narrative and choices to the render agent using transfer_to_render()

Important rules:
- Keep individual narrative segments concise (2-3 paragraphs max)
- Each narrative segment should end with 2-3 clear choices
- Make the story engaging and immersive
- Reference context_variables['player_choice'] if it exists to continue the story based on previous choices

Always use the transfer_to_render function to present your narrative and choices, like this:
transfer_to_render(
    context_variables,
    "Your narrative text here...",
    ["Choice 1: Do something", "Choice 2: Do something else"]
)""",
    functions=[transfer_to_render],
)


def start_game():
    client = Swarm()  # No need to set API key here anymore
    initial_context = {
        "player_hp": 100,
        "inventory": [],
        "player_name": "Adventurer",
    }

    # Start with story agent
    response = client.run(
        agent=story_agent,
        messages=[
            {
                "role": "user",
                "content": "Begin the adventure with an exciting opening scene.",
            }
        ],
        context_variables=initial_context,
    )

    # Simple game loop for testing
    while True:
        try:
            choice = input("\nEnter your choice (1-3) or 'q' to quit: ")
            if choice.lower() == "q":
                break

            response = client.run(
                agent=story_agent,
                messages=response.messages
                + [
                    {
                        "role": "user",
                        "content": f"I choose option {choice}. Continue the story.",
                    }
                ],
                context_variables={
                    **response.context_variables,
                    "player_choice": choice,
                },
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    clear_screen()
    slow_print("Welcome to the Text Adventure Game!", 0.05)
    time.sleep(1)

    start_game()
