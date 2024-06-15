import argparse

import modules.settings as settings
import modules.run_logs as logs

def commands():
    logs.logs("INFO", "Start", "")

    parser = argparse.ArgumentParser(description='This script allows for the handling of RenPy dialogues and choices as TSV data, enabling automatic translation and the ability to play the game in a different language.')
    parser.add_argument('--log', '-l', default=settings.LOG_ENABLED, action='store_true', help='Print log to console and log file')
    parser.add_argument('--log_file', '-lf', default=settings.LOG_FILE, help='The log file to write to')
    parser.add_argument('--log_level', '-lv', default=settings.LOG_LEVEL, help='Print debug information')

    subparsers = parser.add_subparsers(dest='mode', help='Mode to run the program in')

    # modules.dialogue.tsv_translate
    tsv_translate_parser = subparsers.add_parser('tsv_translate', help='Translate a TSV file to a different language')
    tsv_translate_parser.add_argument('--input', '-i', default=settings.TSV_TRANSLATE_INPUT, help='The TSV file to translate')
    tsv_translate_parser.add_argument('--output', '-o', default=settings.TSV_TRANSLATE_OUTPUT, help='The output TSV file')
    tsv_translate_parser.add_argument('--fromlang', '-fr', default=settings.FROM_LANG, help='The language to translate from')
    tsv_translate_parser.add_argument('--tolang', '-to', default=settings.TO_LANG, help='The language to translate to')
    tsv_translate_parser.add_argument('--target', '-t', nargs='+', default=settings.L_TARGET, help='The target files to translate(If the list is empty, all files will be targeted)')
    tsv_translate_parser.add_argument('--start_line', '-sl', type=int, default=settings.START_LINE, help='The line to start translating from')

    # modules.dialogue.tsv2rpy
    tsv2rpy_parser = subparsers.add_parser('tsv2rpy', help='Convert a TSV file to RenPy script')
    tsv2rpy_parser.add_argument('--input', '-i', default=settings.TSV2RPY_INPUT, help='The TSV file to convert')
    tsv2rpy_parser.add_argument('--output', '-o', default=settings.TSV2RPY_OUTPUT, help='The output RenPy script')
    tsv2rpy_parser.add_argument('--tl_lang', '-tl', default=settings.TL_LANG, help='The target language to translate to')
    tsv2rpy_parser.add_argument('--comment', '-c', default=settings.COMMENT, action='store_true', help='Add comments to the RenPy script')
    tsv2rpy_parser.add_argument('--split_file', '-sf', default=settings.SPLIT_FILE, action='store_true', help='Split the output file into multiple files')
    tsv2rpy_parser.add_argument('--split_prefix', '-sp', default=settings.SPLIT_PREFIX, help='The prefix for the split files')

    # modules.menu.extract
    extract_menu_parser = subparsers.add_parser('extract_menu', help='Extract menu options from a RenPy script')
    extract_menu_parser.add_argument('--input', '-i', nargs='+', default=settings.L_EXTRACT_MENU_INPUT, help='The RenPy script to extract menu options from')
    extract_menu_parser.add_argument('--output', '-o', default=settings.EXTRACT_MENU_OUTPUT, help='The output TSV file')

    # modules.menu.tsv_translate
    tsv_translate_menu_parser = subparsers.add_parser('tsv_translate_menu', help='Translate menu options in a RenPy script')
    tsv_translate_menu_parser.add_argument('--input', '-i', default=settings.MENU_TSV_TRANSLATE_INPUT, help='The TSV file to translate')
    tsv_translate_menu_parser.add_argument('--output', '-o', default=settings.MENU_TSV_TRANSLATE_OUTPUT, help='The output TSV file')
    tsv_translate_menu_parser.add_argument('--fromlang', '-fr', default=settings.FROM_LANG, help='The language to translate from')
    tsv_translate_menu_parser.add_argument('--tolang', '-to', default=settings.TO_LANG, help='The language to translate to')
    tsv_translate_menu_parser.add_argument('--target', '-t', nargs='+', default=settings.L_TARGET, help='The target files to translate(If the list is empty, all files will be targeted)')
    tsv_translate_menu_parser.add_argument('--start_line', '-sl', type=int, default=settings.START_LINE, help='The line to start translating from')

    # modules.menu.tsv2rpy
    tsv2rpy_menu_parser = subparsers.add_parser('tsv2rpy_menu', help='Convert menu options in a RenPy script to RenPy script')
    tsv2rpy_menu_parser.add_argument('--input', '-i', default=settings.MENU_TSV2RPY_INPUT, help='The TSV file to convert')
    tsv2rpy_menu_parser.add_argument('--output', '-o', default=settings.MENU_TSV2RPY_OUTPUT, help='The output RenPy script')
    tsv2rpy_menu_parser.add_argument('--tl_lang', '-tl', default=settings.TL_LANG, help='The target language to translate to')
    tsv2rpy_menu_parser.add_argument('--comment', '-c', default=settings.COMMENT, action='store_true', help='Add comments to the RenPy script')
    tsv2rpy_menu_parser.add_argument('--split_file', '-sf', default=settings.SPLIT_FILE, action='store_true', help='Split the output file into multiple files')
    tsv2rpy_menu_parser.add_argument('--split_prefix', '-sp', default=settings.MENU_SPLIT_PREFIX, help='The prefix for the split files')

    args = parser.parse_args()
    handle_command(args)

def handle_command(args):

    # ログ設定をグローバルに
    settings.LOG_ENABLED = args.log
    settings.LOG_FILE = args.log_file
    settings.LOG_LEVEL = args.log_level
    logs.logs("DEBUG", "Logs", f"{settings.LOG_ENABLED}")
    logs.logs("DEBUG", "Logs", f"Current log level '{settings.LOG_LEVEL}'")

    logs.logs("DEBUG", "Mode", f"{args.mode}")
    # モードによって対応するモジュールを呼び出す
    if args.mode == 'tsv_translate':
        import modules.dialogue.tsv_translate
        modules.dialogue.tsv_translate.main(args.input, args.output, args.fromlang, args.tolang, args.target, args.start_line)
    elif args.mode == 'tsv2rpy':
        import modules.dialogue.tsv2rpy
        modules.dialogue.tsv2rpy.main(args.input, args.output, args.tl_lang, args.comment, args.split_file, args.split_prefix)
    elif args.mode == 'extract_menu':
        import modules.menu.extract
        modules.menu.extract.main(args.input, args.output)
    elif args.mode == 'tsv_translate_menu':
        import modules.menu.tsv_translate
        modules.menu.tsv_translate.main(args.input, args.output, args.fromlang, args.tolang, args.target, args.start_line)
    elif args.mode == 'tsv2rpy_menu':
        import modules.menu.tsv2rpy
        modules.menu.tsv2rpy.main(args.input, args.output, args.tl_lang, args.comment, args.split_file, args.split_prefix)
    else:
        logs.logs("ERROR", "Mode", "Invalid mode")