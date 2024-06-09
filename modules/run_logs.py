import datetime

import modules.settings as settings

def initialize_logfile():
    with open(settings.LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("")

def logs(description, text=""):
    if settings.LOG_ENABLED:
        print(description, ":\t", text)
        with open(settings.LOG_FILE, 'a', encoding='utf-8') as f:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            f.write(f"{current_time}:\t{description}:\t{text}\n")