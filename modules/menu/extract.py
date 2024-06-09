from typing import List
import re

import modules.run_logs as logs

def main(input: List[str], output: str):
    logs.logs("DEBUG", "Extract_menu", f"{input}, {output}")
    choices = []
    for input_file in input:
        if input_file.endswith('.rpy'):
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()
            choices.extend(extract_menu_choices(text, input_file))  # ここを変更
    if choices:
        write_choices_to_file(choices, output)


def extract_menu_choices(text, filename):
    # menuラベルを見つけて、その中のインデントされた選択肢を抽出する
    def extract_choices(lines, indent, start_line):
        choices = []
        while lines:
            line = lines.pop(0)
            line_indent = len(line) - len(line.lstrip())
            if line_indent < indent:
                lines.insert(0, line)
                return choices
            line = line.strip()
            if line_indent == indent + 2 and line.startswith('"'):
                choice = re.search(r'"(.*?)"', line).group(1)
                choices.append([filename, start_line, choice, "Untranslated"])  # 選択肢、行数、ファイル名をタプルとして追加
            elif line.startswith('menu:'):
                choices.extend(extract_choices(lines, line_indent + 2, start_line + len(choices) + 1))  # 行数を更新
            start_line += 1  # 行数を更新
        logs.logs("DEBUG", "Extract_menu", f"Extracted {len(choices)} choices from {filename}")
        return choices

    lines = text.split('\n')
    indent = len(lines[0]) - len(lines[0].lstrip()) if lines[0].startswith('menu:') else 0
    return extract_choices(lines, indent, 1)  # 初期行数を1として渡す

def write_choices_to_file(choices, output):
    with open(output, 'w', encoding='utf-8') as file:
        file.write('filename\tlinenumber\tchoice\ttranslated\n') # ヘッダー行を追加
        for choice in choices:
            file.write('\t'.join(map(str, choice)) + '\n') # タブ区切りで書き込み
        logs.logs("INFO", "Extract_menu", f"Write {len(choices)} choices to {output}")