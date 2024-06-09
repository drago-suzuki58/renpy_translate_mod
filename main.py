from modules.commands import commands
import modules.run_logs as logs

def main():
    commands()
    logs.logs("INFO", "Program started")

if __name__ == "__main__":
    main()