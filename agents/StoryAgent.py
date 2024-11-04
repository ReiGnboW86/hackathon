"""
StoryAgent Module
----------------
Ansvarar för att generera och hantera spelberättelsen genom AI.

Detta modul innehåller:
- StoryGenerator: Genererar AI-baserade scener och val
- StoryManager: Hanterar story-flödet och kontexten
- StoryAgent: Swarm Agent som koordinerar story-genereringen
"""

from swarm import Agent
from typing import Dict, Any, List
import openai
from dotenv import load_dotenv
import os
from rich.console import Console

# Ladda .env fil
load_dotenv()

# Konfigurera OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class StoryGenerator:
    """
    Genererar story-innehåll genom OpenAI's API.

    Attributes:
        story_context (List): Lista med tidigare scener och val
    """

    def __init__(self):
        self.console = Console()
        if not openai.api_key:
            # Använd en dummy-generator istället för att kasta ett fel
            self.use_dummy_data = True
            self.console.print(
                "[yellow]Varning: OPENAI_API_KEY saknas. Använder dummy-data istället.[/yellow]"
            )
        else:
            self.use_dummy_data = False
        self.story_context = []

    def generate_next_scene(self, last_choice: str = None) -> Dict[str, Any]:
        """
        Genererar nästa scen baserat på tidigare val.

        Args:
            last_choice: Spelarens senaste val

        Returns:
            Dict med scene_text och choices
        """
        prompt = self._build_story_prompt(last_choice)
        response = self._get_ai_response(prompt)
        scene_data = self._parse_ai_response(response)
        self._update_context(scene_data, last_choice)

        # Lägg alltid till ett avslutningsalternativ
        scene_data["choices"].append("Avsluta äventyret")
        return scene_data

    def _build_story_prompt(self, last_choice: str = None) -> str:
        if not self.story_context:
            return """Som en fantasy story generator, skapa en inledande scen för ett äventyr.
            Beskriv scenen och ge exakt tre valmöjligheter för spelaren.
            Format: Scenbeskrivning | Val 1 | Val 2 | Val 3"""

        # Använd de två senaste scenerna för kontext
        recent_context = (
            self.story_context[-2:]
            if len(self.story_context) > 1
            else self.story_context
        )
        context_str = "\n".join(
            [
                f"Tidigare scen: {scene['scene']}\nSpelaren valde: {scene['choice']}"
                for scene in recent_context
            ]
        )

        return f"""Baserat på denna kontext:
        {context_str}
        Spelaren valde: {last_choice}
        
        Skapa nästa scen i äventyret med exakt tre nya val.
        Format: Scenbeskrivning | Val 1 | Val 2 | Val 3"""

    def _get_ai_response(self, prompt: str) -> str:
        if self.use_dummy_data:
            # Returnera dummy-data om API-nyckel saknas
            return """Du står framför en mystisk grotta. Månen lyser svagt genom träden och du hör konstiga ljud inifrån.|
                     Gå in i grottan|Undersök området utanför|Leta efter en annan väg"""

        try:
            client = openai.OpenAI()  # Skapa en klient-instans
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Du är en kreativ fantasy story generator.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            self.console.print(f"[red]Fel vid API-anrop: {str(e)}[/red]")
            return "En ny utmaning väntar...|Utforska vidare|Vila|Återvänd"

    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        try:
            parts = response.split("|")
            return {
                "scene_text": parts[0].strip(),
                "choices": [choice.strip() for choice in parts[1:4]],  # Exakt 3 val
            }
        except:
            return {
                "scene_text": "Din resa fortsätter...",
                "choices": ["Gå vidare", "Vila", "Vänd tillbaka"],
            }

    def _update_context(self, scene_data: Dict[str, Any], choice: str = None):
        self.story_context.append({"scene": scene_data["scene_text"], "choice": choice})
        # Behåll bara de senaste 5 scenerna för att begränsa kontextens storlek
        if len(self.story_context) > 5:
            self.story_context = self.story_context[-5:]


class StoryManager:
    def __init__(self):
        self.generator = StoryGenerator()

    def get_next_scene(self, player_choice: str = None) -> Dict[str, Any]:
        return self.generator.generate_next_scene(player_choice)


# Skapa StoryAgent med den nya strukturen
StoryAgent = Agent(
    name="StoryAgent",
    instructions="""Du är en storytelling agent som genererar dynamiska och
    sammanhängande fantasy-äventyr. Du skapar engagerande scener och
    ger spelaren exakt tre meningsfulla val i varje situation.""",
    functions=[StoryManager().get_next_scene],
)


"""
Denna agent ansvarar för att generera story baserat på användarens val.
Den ger även användaren nya val att göra.
Eventuellt delar vi upp detta i två klasser?
"""
"""
Denna agent ansvarar för att generera story baserat på användarens val.
Den ger även användaren nya val att göra.
Eventuellt delar vi upp detta i två klasser?
"""
