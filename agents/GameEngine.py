"""
GameEngine Module
---------------
Huvudmodul som koordinerar alla spelagenter och spelflödet.

Detta modul innehåller:
- GameEngine: Huvudspelmotor som koordinerar alla komponenter
"""

from .StoryAgent import StoryManager
from .RenderAgent import SceneRenderer
from rich.console import Console
from rich.panel import Panel


class GameEngine:
    """
    Huvudspelmotor som koordinerar story och rendering.

    Attributes:
        console: Rich console för formaterad output
        story_manager: Hanterar story-generering
        renderer: Hanterar visuell presentation
        game_active: Kontrollerar om spelet är aktivt
    """

    def __init__(self):
        self.console = Console()
        self.story_manager = StoryManager()
        self.renderer = SceneRenderer()
        self.game_active = True

    def run(self):
        """
        Huvudspelloop som koordinerar story och rendering.
        """
        self._show_welcome()

        player_choice = None
        while self.game_active:
            try:
                # Generera nästa scen direkt från StoryManager istället för StoryAgent
                scene = self.story_manager.get_next_scene(player_choice)

                # Använd bara RenderAgent för att visa scenen
                player_choice = self.renderer.render_scene(scene)

                if player_choice == "exit":
                    self._handle_game_exit()
                    break

            except Exception as e:
                self._handle_error(e)

    def _show_welcome(self):
        """Visar välkomstskärm"""
        self.console.print(
            "\n[bold magenta]Välkommen till AI Dungeon Master![/bold magenta]"
        )
        self.console.print(
            Panel.fit(
                "Ett oändligt fantasy-äventyr genererat av AI\n"
                "Dina val formar historien...",
                title="Äventyr väntar",
            )
        )
        input("\nTryck Enter för att börja ditt äventyr...")

    def _handle_game_exit(self):
        """Hanterar avslutning av spelet"""
        self.console.print(
            Panel.fit(
                "[yellow]Tack för att du spelade![/yellow]\n"
                "Ditt äventyr har nått sitt slut...",
                title="Spelet Avslutat",
                border_style="yellow",
            )
        )

    def _handle_error(self, error: Exception):
        """
        Hanterar fel som uppstår under spelet.

        Args:
            error: Det fel som uppstått
        """
        self.console.print(
            Panel(
                f"[red]Ett fel uppstod:[/red]\n{str(error)}",
                title="Fel",
                border_style="red",
            )
        )
        if input("\nVill du fortsätta? (j/n): ").lower() != "j":
            self.game_active = False
