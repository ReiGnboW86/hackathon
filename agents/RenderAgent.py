from swarm import Swarm, Agent
from typing import List, Dict
import time


# Function for RenderAgent to display text with a typewriter effect
def print_with_effect(text: str, delay: float = 0.03):
    """
    Print text with a typewriter effect

    Args:
        text: The text to print
        delay: Delay between each character
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def display_and_get_choice(story: str, choices: List[str]) -> str:
    """
    Display the story and choices, then get user input.

    Args:
        story: The story text to display
        choices: List of choices for the player

    Returns:
        The player's selected choice
    """
    # Clear some space and print story
    print("\n" + "=" * 50 + "\n")
    print_with_effect(story)
    print("\n" + "-" * 25 + " Choices " + "-" * 25 + "\n")

    # Display numbered choices
    for idx, choice in enumerate(choices, 1):
        print_with_effect(f"{idx}. {choice}")

    # Get and validate input
    while True:
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(choices):
                return choices[choice - 1]
            print("Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")


# Create the RenderAgent
render_agent = Agent(
    name="RenderAgent",
    instructions="""You are a rendering agent that displays story content to the player.
    Your primary function is to take story content and choices from the StoryAgent,
    display them appropriately, and return the player's choice.""",
    functions=[display_and_get_choice],
)

# Create the StoryAgent
story_agent = Agent(
    name="StoryAgent",
    instructions="""You are a storytelling agent that creates engaging D&D-style narratives.
    Present story segments with 2-4 choices for the player.
    Format your responses as a dictionary with 'story' and 'choices' keys.
    Keep stories concise (2-3 paragraphs) and choices clear.
    Adapt the story based on player choices.""",
    model="gpt-4",  # Using GPT-4 for better storytelling
)

# Create the Swarm client
client = Swarm()

# Initial story prompt
initial_messages = [
    {
        "role": "user",
        "content": "Start a new D&D style adventure story. The setting is a medieval fantasy world.",
    }
]


# Main game loop
def run_game():
    messages = initial_messages
    while True:
        # Get story and choices from StoryAgent
        response = client.run(agent=story_agent, messages=messages)

        # Extract last message content
        story_content = response.messages[-1]["content"]

        try:
            # Parse the story content into a proper format for RenderAgent
            # Assuming StoryAgent returns content in format:
            # {"story": "...", "choices": ["...", "..."]}
            story_data = eval(story_content)

            # Pass to RenderAgent for display and choice selection
            render_response = client.run(
                agent=render_agent,
                messages=[
                    {
                        "role": "user",
                        "content": f"Display this story segment and get player choice: {story_data}",
                    }
                ],
            )

            # Add player's choice back to messages for StoryAgent
            messages.append(
                {
                    "role": "user",
                    "content": f"Player chose: {render_response.messages[-1]['content']}",
                }
            )

        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
    run_game()
