import datetime

import modules.settings as settings

def initialize_logfile():
    with open(settings.LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("")
        logs("INFO", "Log", f"Log file initialized: {settings.LOG_FILE}")

def logs(level, description, text=""):
    # ログレベルの設定(追加も可能)
    level_mapping = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
    valid_levels = level_mapping.keys()
    if settings.LOG_ENABLED:
        # ログレベルで、そのレベル以上のログのみ出力する
        if level in valid_levels and level_mapping[level] >= level_mapping[settings.LOG_LEVEL]:
            print(f"{level}:\t{description}:\t{text}")
            with open(settings.LOG_FILE, 'a', encoding='utf-8') as f:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                f.write(f"{current_time}:{level}:\t{description}:\t{text}\n")

        elif level not in valid_levels:
            logs("ERROR", "Logs", f"Invalid log level '{level}'")