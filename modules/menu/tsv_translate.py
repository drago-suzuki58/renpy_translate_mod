from typing import List
from googletrans import Translator
import re
import requests

import modules.run_logs as logs
import modules.base16 as base16

def main(input: str, output: str, fromlang: str, tolang: str, target: List[str], start_line: int, translated_dic: str):
    logs.logs("DEBUG", "Translate_menu", f"{input}, {output}, {fromlang}, {tolang}, {target}")

    progress = 1
    total_chars = 0
    tlist = translated_list(translated_dic)

    if fromlang == tolang:
        logs.logs("ERROR", "Translate_dialogue", "The source and target languages are the same.")
        return

    g_translator = Translator()
    logs.logs("INFO", "Translate_dialogue", f"Translor initialized")

    with open(input, "r", encoding="utf-8") as f:
        with open(output, "w", encoding="utf-8") as output_f:
            lines = f.readlines()
            total_lines = len(lines) - 1
            output_f.write("filename\tlinenumber\tchoice\ttranslated\n") # ヘッダー行を追加
            logs.logs("INFO", "Translate_dialogue", f"Read {len(lines)} lines from {input}")

            for line in lines:
                if line == "filename\tlinenumber\tchoice\ttranslated\n":
                    continue # ヘッダー行をスキップ
                elif line == "filename\tlinenumber\tidentifier\tcontents\n":
                    logs.logs("ERROR", "Translate_dialogue", "This is not a menu TSV file.")
                    return

                filename, linenumber, choice , translated_text= line.strip().split('\t')

                if choice in tlist:
                    logs.logs("DEBUG", "Translate_dialogue", f"Skip_3:\t{filename}, {linenumber}, {choice}, {translated_text}")
                    progress += 1
                    continue

                if target == [""]:
                    logs.logs("DEBUG", "Translate_dialogue", f"Pass:\t{filename}, {linenumber}, {choice}, {translated_text}")
                    pass
                elif filename not in target:
                    logs.logs("DEBUG", "Translate_dialogue", f"Skip_1:\t{filename}, {linenumber}, {choice}, {translated_text}")
                    progress += 1
                    continue

                if progress < start_line:
                    logs.logs("DEBUG", "Translate_dialogue", f"Skip_2:\t{filename}, {linenumber}, {choice}, {translated_text}")
                    progress += 1
                    continue

                if choice:
                    original_choice = choice
                    logs.logs("DEBUG", "Translate_dialogue", f"Extracted:\t{choice}")

                    choice = base16.encode_matches(r'\{.*?\}', choice)
                    choice = base16.encode_matches(r'\[.*?\]', choice)
                    choice = base16.encode_matches(r'\\.', choice) # \{encoded_text} の形式だと変換されてしまうと思うので|encoded_text|のように変換

                    for _ in range(5): # 翻訳のタイムアウト時に最大5回再試行
                        try:
                            total_chars += len(choice)
                            translated_text = g_translator.translate(choice, src=fromlang, dest=tolang).text
                            logs.logs("INFO", "Translate_dialogue", f"Translated:\t{original_choice} -> {translated_text}")
                            break
                        except requests.exceptions.Timeout:
                            logs.logs("WARNING", "Translate_dialogue", f"Google Translate API timed out. Retrying...:\t{_}/5 time:\tLine: {progress}")
                            continue
                    else:
                        logs.logs("ERROR", "Translate_dialogue", f"Google Translate API timed out 5 times. Skipping this line.\nLine: {progress}")
                        continue

                    translated_text = base16.decode_matches(translated_text)

                    output_f.write(f"{filename}\t{linenumber}\t{original_choice}\t{translated_text}\n")
                    logs.logs("DEBUG", "Translate_dialogue", f"Append:\t{filename}, {linenumber}, {original_choice}, {translated_text}")

                    logs.logs("INFO", "Translate_dialogue", f"Line {progress}/{total_lines}:\t{original_choice},\t{translated_text}")
                    progress += 1

    logs.logs("INFO", "Translate_dialogue", f"Total characters: {total_chars}")

def translated_list(translated_dic):
    translated = []
    try:
        with open(translated_dic, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line == "filename\tlinenumber\tchoice\ttranslated\n":
                    continue
                filename, linenumber, choice, translated_text = line.strip().split('\t')
                translated.append(choice)
    except FileNotFoundError:
        logs.logs("DEBUG", "Translate_dialogue", f"File not found: {translated_dic}")
        return []

    logs.logs("DEBUG", "Translate_dialogue", translated)
    return translated