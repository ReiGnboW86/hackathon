from agents.StoryAgent import StoryAgent, generate_story
from agents.RenderAgent import display_and_get_choice
from agents.CombatAgent import CombatAgent


def run_game():
    print("\nVälkommen till AI Dungeon Master!")
    print("=" * 50)

    # Initiera spelet
    game_active = True
    context = {}

    while game_active:
        # Generera story och val
        current_scene = generate_story(context)

        # Visa story och få spelarens val
        player_choice = display_and_get_choice(
            current_scene["text"], current_scene["choices"]
        )

        # Uppdatera kontext med spelarens val
        context["last_choice"] = player_choice

        # Avsluta spelet om spelaren väljer att avsluta
        if player_choice.lower() == "avsluta":
            game_active = False


if __name__ == "__main__":
    run_game()
