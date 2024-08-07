from modules.commands import commands
import modules.settings as settings
import modules.run_logs as logs


def main():
    settings.load_settings_from_ini()
    logs.initialize_logfile()
    commands()
    logs.logs("INFO", "Main", "End of main function")


if __name__ == "__main__":
    main()
