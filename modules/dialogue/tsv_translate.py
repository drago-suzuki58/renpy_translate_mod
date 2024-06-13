from typing import List
from googletrans import Translator
import re
import requests

import modules.run_logs as logs
import modules.base16 as base16

def main(input: str, output: str, fromlang: str, tolang: str, target: List[str]):
    logs.logs("DEBUG", "Translate_dialogue", f"{input}, {output}, {fromlang}, {tolang}, {target}")

    progress = 1

    if fromlang == tolang:
        logs.logs("ERROR", "Translate_dialogue", "The source and target languages are the same.")
        return

    g_translator = Translator()
    logs.logs("INFO", "Translate_dialogue", f"Translor initialized")

    with open(input, "r", encoding="utf-8") as f:
        with open(output, "w", encoding="utf-8") as output_f:
            lines = f.readlines()
            total_lines = len(lines) - 1
            output_f.write("filename\tlinenumber\tidentifier\tcontents\n") # ヘッダー行を追加
            logs.logs("INFO", "Translate_dialogue", f"Read {len(lines)} lines from {input}")

            for line in lines:
                if line == "filename\tlinenumber\tidentifier\tcontents\n":
                    continue # ヘッダー行をスキップ

                filename, linenumber, identifier, contents = line.strip().split('\t')

                if target and filename not in target:
                    continue

                match_str = re.match(r'^([^"]*)"((?:[^"\\]|\\.)*)"', contents) # エスケープされていないダブルクォーテーションのみを対象にする(つまりセリフと人物を分ける)

                if match_str == None:
                    output_f.write(f"{filename}\t{linenumber}\t{identifier}\t{contents}\n")

                    logs.logs("DEBUG", "Translate_dialogue", f"Append:\t{filename}, {linenumber}, {identifier}, {contents}")
                    logs.logs("INFO", "Translate_dialogue", f"Line {progress}/{total_lines}:\t{contents}")

                    progress += 1

                else:
                    person = match_str.group(1)
                    dialogue = match_str.group(2)
                    original_dialogue = dialogue
                    logs.logs("DEBUG", "Translate_dialogue", f"Extracted:\t{person},{dialogue}")

                    dialogue = base16.encode_matches(r'\{.*?\}', dialogue)
                    dialogue = base16.encode_matches(r'\[.*?\]', dialogue)
                    dialogue = base16.encode_matches(r'\\.', dialogue)

                    for _ in range(5): # 翻訳のタイムアウト時に最大5回再試行
                        try:
                            translated_text = g_translator.translate(dialogue, src=fromlang, dest=tolang).text
                            logs.logs("INFO", "Translate_dialogue", f"Translated:\t{original_dialogue} -> {translated_text}")
                            break
                        except requests.exceptions.Timeout:
                            logs.logs("WARNING", "Translate_dialogue", f"Google Translate API timed out. Retrying...:\t{_}/5 time:\tLine: {progress}")
                            continue
                    else:
                        logs.logs("ERROR", "Translate_dialogue", f"Google Translate API timed out 5 times. Skipping this line.\nLine: {progress}")
                        continue

                    translated_text = base16.decode_matches(translated_text)

                    contents = f'{person}"{translated_text}"'
                    output_f.write(f"{filename}\t{linenumber}\t{identifier}\t{contents}\n")
                    logs.logs("DEBUG", "Translate_dialogue", f"Append:\t{filename}, {linenumber}, {identifier}, {contents}")

                    logs.logs("INFO", "Translate_dialogue", f"Line {progress}/{total_lines}:\t{contents}")
                    progress += 1