import modules.run_logs as logs

def main(input: str, output: str, tl_lang: str, comment: bool):
    logs.logs("DEBUG", "TSV2RPY_menu", f"{input}, {output}, {tl_lang}, {comment}")
    previous_filename = ''
    ourput_lines = ''

    with open(input, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line == "filename\tlinenumber\tchoice\ttranslated\n":
                continue
            filename, linenumber, choice, translated = line.strip().split('\t')

            if comment:
                if not filename == previous_filename: # 前のファイル名と違うときだけファイル名を出力
                    ourput_lines += f"# {filename}\n"
                ourput_lines += f"# line:{linenumber}\n"
                previous_filename = filename

            ourput_lines += f"    old \"{choice}\"\n    new \"{translated}\"\n\n"

    with open(output, 'w', encoding='utf-8') as f:
        f.write(f"translate {tl_lang} strings:\n\n")
        f.write(ourput_lines)