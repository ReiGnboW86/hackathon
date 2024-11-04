"""
Main Module
----------
Startpunkt för applikationen.
"""

# Ta bort
from agents.GameEngine import GameEngine


def main():
    game = GameEngine()
    game.run()


if __name__ == "__main__":
    main()
