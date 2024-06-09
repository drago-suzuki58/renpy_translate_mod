from typing import List
from googletrans import Translator
import re
import requests

import modules.run_logs as logs
import modules.base16 as base16

def main(input: str, output: str, fromlang: str, tolang: str, target: List[str]):
    logs.logs("DEBUG", "Translate_menu", f"{input}, {output}, {fromlang}, {tolang}, {target}")

    lines_to_write = []
    progress = 2

    if fromlang == tolang:
        logs.logs("ERROR", "Translate_dialogue", "The source and target languages are the same.")
        return

    g_translator = Translator()
    logs.logs("INFO", "Translate_dialogue", f"Translor initialized")

    with open(input, "r", encoding="utf-8") as f:
        lines = f.readlines()
        total_lines = len(lines)
        logs.logs("INFO", "Translate_dialogue", f"Read {len(lines)} lines from {input}")

        for line in lines:
            if line == "filename\tlinenumber\tchoice\ttranslated\n":
                continue # ヘッダー行をスキップ

            filename, linenumber, choice , translated_text= line.strip().split('\t')

            if target and filename not in target:
                continue

            if choice:
                original_choice = choice
                logs.logs("DEBUG", "Translate_dialogue", f"Extracted:\t{choice}")

                choice = base16.encode_matches(r'\{.*?\}', choice)
                choice = base16.encode_matches(r'\[.*?\]', choice)
                choice = base16.encode_matches(r'\\.', choice) # \{encoded_text} の形式だと変換されてしまうと思うので|encoded_text|のように変換

                for _ in range(5): # 翻訳のタイムアウト時に最大5回再試行
                    try:
                        translated_text = g_translator.translate(choice, src=fromlang, dest=tolang).text
                        logs.logs("INFO", "Translate_dialogue", f"Translated:\t{original_choice} -> {translated_text}")
                        break
                    except requests.exceptions.Timeout:
                        continue
                else:
                    logs.logs("ERROR", "Translate_dialogue", f"Google Translate API timed out 5 times. Skipping this line.\nLine: {progress}")
                    continue

                translated_text = base16.decode_matches(translated_text)

                lines_to_write.append(f"{filename}\t{linenumber}\t{original_choice}\t{translated_text}\n")
                logs.logs("DEBUG", "Translate_dialogue", f"Append:\t{filename}, {linenumber}, {original_choice}, {translated_text}")

                logs.logs("INFO", "Translate_dialogue", f"Line {progress}/{total_lines}:\t{original_choice},\t{translated_text}")
                progress += 1

    with open(output, "w", encoding="utf-8") as f:
        f.write("filename\tlinenumber\tchoice\ttranslated\n") # ヘッダー行を追加
        for line in lines_to_write:
            f.write(line)
        logs.logs("INFO", "Translate_dialogue", f"Wrote {len(lines_to_write)} lines to {output}")