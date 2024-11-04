from swarm import Agent


def generate_story(context=None):
    """
    Genererar nästa del av storyn baserat på kontext
    """
    initial_story = {
        "text": """Du vaknar upp i en mörk grotta. Det enda ljuset kommer från en fackla 
        som brinner svagt på väggen. Du hör droppande vatten i fjärran.""",
        "choices": [
            "Ta facklan och utforska grottan djupare",
            "Leta efter en väg ut",
            "Ropa efter hjälp",
        ],
    }
    return initial_story


StoryAgent = Agent(
    name="Story Agent",
    instructions="""Du är en storytelling agent som genererar fantasy-äventyr.
    Du skapar engagerande berättelser och ger spelaren meningsfulla val.""",
    functions=[generate_story],
)


"""
Denna agent ansvarar för att generera story baserat på användarens val.
Den ger även användaren nya val att göra.
Eventuellt delar vi upp detta i två klasser?
"""
