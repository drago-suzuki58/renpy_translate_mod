import datetime

def initialaise_logfile(log_file):
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("")

def logs(log, log_file, description, text=""):
    if log:
        print(description, ":\t", text)
        with open(log_file, 'a', encoding='utf-8') as f:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            f.write(f"{current_time}:\t{description}:\t{text}\n")