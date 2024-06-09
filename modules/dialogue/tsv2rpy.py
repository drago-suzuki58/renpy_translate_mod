import modules.run_logs as logs

def main(input: str, output: str, tl_lang: str, comment: bool):
    logs.logs("DEBUG", "TSV2RPY_dialogue", f"{input}, {output}, {tl_lang}, {comment}")

    previous_filename = ''
    ourput_lines = ''

    with open(input, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line == u"filename\tlinenumber\tidentifier\tcontents\n":
                continue
            filename, linenumber, identifier, contents = line.strip().split('\t')

            if comment:
                if not filename == previous_filename: # 前のファイル名と違うときだけファイル名を出力
                    ourput_lines += f"# {filename}\n"
                    logs.logs("DEBUG", "TSV2RPY_dialogue", f"Output filename: {filename}")
                ourput_lines += f"# line:{linenumber}\n"
                previous_filename = filename

                ourput_lines += f"translate {tl_lang} {identifier}:\n\n    {contents}\n\n"


    with open(output, 'w', encoding='utf-8') as f:
        f.write(ourput_lines)
        logs.logs("INFO", "TSV2RPY_dialogue", f"Write {len(ourput_lines)} chars to {output}")