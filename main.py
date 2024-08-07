import modules.run_logs as logs
import modules.settings as settings
from modules.commands import commands


def main():
    settings.load_settings_from_ini()
    logs.initialize_logfile()
    commands()
    logs.logs("INFO", "Main", "End of main function")


if __name__ == "__main__":
    main()
