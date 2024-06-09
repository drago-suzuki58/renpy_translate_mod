from modules.commands import commands
import modules.run_logs as logs

def main():
    commands()
    logs.logs("INFO", "Main", "End of main function")

if __name__ == "__main__":
    main()