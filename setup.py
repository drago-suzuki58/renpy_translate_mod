from cx_Freeze import setup, Executable

# Python script to executable file
setup(
    name = "RenPy Translate Tools",
    version = "1.2.0",
    description = "This script allows for the handling of RenPy dialogues and choices as TSV data, enabling automatic translation and the ability to play the game in a different language.",
    executables = [Executable("main.py")]
)