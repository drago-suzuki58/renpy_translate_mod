import os

import modules.run_logs as logs


def main(
    input: str,
    output: str,
    tl_lang: str,
    comment: bool,
    split_file: bool,
    split_prefix: str,
):
    logs.logs("DEBUG", "TSV2RPY_dialogue", f"{input}, {output}, {tl_lang}, {comment}")

    output_lines = {}

    with open(input, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if (
                line == "filename\tlinenumber\tidentifier\tcontents\n"
            ):  # ヘッダー行をスキップ
                continue
            elif line == "filename\tlinenumber\tchoice\ttranslated\n":
                logs.logs(
                    "ERROR", "TSV2RPY_dialogue", "This is not a dialogue TSV file."
                )
                return
            filename, linenumber, identifier, contents = line.strip().split("\t")

            if filename not in output_lines:
                output_lines[filename] = []
                logs.logs("DEBUG", "TSV2RPY_menu", f"Output filename: {filename}")
                if comment:
                    output_lines[filename].append(f"# {filename}\n")

            if comment:
                output_lines[filename].append(f"# line:{linenumber}\n")

            output_lines[filename].append(
                f"translate {tl_lang} {identifier}:\n\n    {contents}\n\n"
            )

    if split_file:
        for filename, lines in output_lines.items():
            safe_filename = os.path.basename(filename)  # ファイル名のみ取得
            with open(f"{split_prefix}{safe_filename}", "w", encoding="utf-8") as f:
                f.writelines(lines)
                logs.logs(
                    "INFO",
                    "TSV2RPY_menu",
                    f"Write {len(lines)} lines to {split_prefix}_{filename}",
                )
    else:
        with open(output, "w", encoding="utf-8") as f:
            for filename, lines in output_lines.items():
                f.writelines(lines)
                logs.logs(
                    "INFO", "TSV2RPY_menu", f"Write {len(lines)} lines to {output}"
                )
