"""
RenderAgent Module
----------------
Hanterar all visuell presentation och användarinteraktion.
"""

# Ta bort
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
import os


class SceneRenderer:
    """
    Hanterar rendering av spelscener och användarinteraktion.

    Attributes:
        console: Rich console för formaterad output
    """

    def __init__(self):
        self.console = Console()

    def _clear_screen(self):
        """Rensar terminalfönstret"""
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def render_scene(self, scene_data: Dict[str, Any]) -> str:
        """
        Renderar en scen och hanterar spelarens val.
        """
        try:
            self._clear_screen()

            # Formatera texten utan "Scen:" prefix och extra whitespace
            scene_text = scene_data["scene_text"].replace("Scen:", "").strip()
            choices = [
                f"Val {i+1}: {choice}"
                for i, choice in enumerate(scene_data["choices"])
                if choice != "Avsluta äventyret"
            ]

            # Kombinera scen och val i samma text
            full_text = f"{scene_text}\n\n" + "\n".join(choices)

            # Visa endast en panel med all information
            panel = Panel(
                full_text, title="Nuvarande Scen", border_style="magenta", width=80
            )
            self.console.print(panel)

            # Visa bara Q-alternativet under panelen
            self.console.print("\n[red]Tryck 'Q' för att avsluta spelet[/red]")

            return self._handle_player_choice(scene_data["choices"])
        except KeyError as e:
            self.console.print(f"[red]Felaktig scendata: {e}[/red]")
            return "exit"

    def _handle_player_choice(self, choices: List[str]) -> str:
        """
        Hanterar spelarval.
        """
        while True:
            choice_input = (
                self.console.input("\nVälj ett alternativ (1-3 eller Q): ")
                .strip()
                .upper()
            )

            if choice_input == "Q":
                if self._confirm_exit():
                    return "exit"
                continue

            try:
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(choices):
                    return choices[choice_num - 1]
                self.console.print("[red]Ogiltigt val, välj mellan 1-3 eller Q[/red]")
            except ValueError:
                self.console.print(
                    "[red]Vänligen ange ett nummer mellan 1-3 eller Q för att avsluta[/red]"
                )

    def _confirm_exit(self) -> bool:
        """
        Bekräftar att spelaren vill avsluta.

        Returns:
            bool: True om spelaren bekräftar, False annars
        """
        response = self.console.input(
            "\n[yellow]Är du säker på att du vill avsluta? (j/n): [/yellow]"
        )
        return response.lower() == "j"


# Ta bort eller kommentera ut denna del
# RenderAgent = Agent(
#     name="RenderAgent",
#     instructions="""Du är en rendering agent...""",
#     functions=[SceneRenderer().render_scene],
# )
