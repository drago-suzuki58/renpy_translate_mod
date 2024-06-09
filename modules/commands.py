import argparse

import modules.settings as settings
import modules.run_logs as logs

def commands():
    parser = argparse.ArgumentParser(description='WIP')
    parser.add_argument('--log', '-l', default=False, action='store_true', help='Print log to console and log file')
    parser.add_argument('--log_file', '-lf', default='log.txt', help='The log file to write to')

    subparsers = parser.add_subparsers(dest='mode', help='Mode to run the program in')

    tsv_translate_parser = subparsers.add_parser('tsv_translate', help='Translate a TSV file to a different language')
    tsv_translate_parser.add_argument('--input', '-i', default='untranslated.tsv', help='The TSV file to translate')
    tsv_translate_parser.add_argument('--output', '-o', default='translated.tsv', help='The output TSV file')
    tsv_translate_parser.add_argument('--fromlang', '-fr', default='en', help='The language to translate from')
    tsv_translate_parser.add_argument('--tolang', '-to', default='ja', help='The language to translate to')
    tsv_translate_parser.add_argument('--target', '-t', nargs='+', default=[], help='The target files to translate(If the list is empty, all files will be targeted)')

    tsv2rpy_parser = subparsers.add_parser('tsv2rpy', help='Convert a TSV file to RenPy script')
    tsv2rpy_parser.add_argument('--input', '-i', default='translated.tsv', help='The TSV file to convert')
    tsv2rpy_parser.add_argument('--output', '-o', default='converted.rpy', help='The output RenPy script')
    tsv2rpy_parser.add_argument('--tl_lang', '-tl', default='japanese', help='The target language to translate to')
    tsv2rpy_parser.add_argument('--comment', '-c', default=True, action='store_true', help='Add comments to the RenPy script')

    extract_menu_parser = subparsers.add_parser('extract_menu', help='Extract menu options from a RenPy script')
    extract_menu_parser.add_argument('--input', '-i', default='script.rpy', help='The RenPy script to extract menu options from')
    extract_menu_parser.add_argument('--output', '-o', default='menu_untranslated.tsv', help='The output TSV file')

    tsv_translate_menu_parser = subparsers.add_parser('tsv_translate_menu', help='Translate menu options in a RenPy script')
    tsv_translate_menu_parser.add_argument('--input', '-i', default='menu_untranslated.tsv', help='The TSV file to translate')
    tsv_translate_menu_parser.add_argument('--output', '-o', default='menu_translated.tsv', help='The output TSV file')
    tsv_translate_menu_parser.add_argument('--fromlang', '-fr', default='en', help='The language to translate from')
    tsv_translate_menu_parser.add_argument('--tolang', '-to', default='ja', help='The language to translate to')
    tsv_translate_menu_parser.add_argument('--target', '-t', nargs='+', default=[], help='The target files to translate(If the list is empty, all files will be targeted)')

    tsv2rpy_menu_parser = subparsers.add_parser('tsv2rpy_menu', help='Convert menu options in a RenPy script to RenPy script')
    tsv2rpy_menu_parser.add_argument('--input', '-i', default='menu_translated.tsv', help='The TSV file to convert')
    tsv2rpy_menu_parser.add_argument('--output', '-o', default='menu_converted.rpy', help='The output RenPy script')
    tsv2rpy_menu_parser.add_argument('--tl_lang', '-tl', default='japanese', help='The target language to translate to')
    tsv2rpy_menu_parser.add_argument('--comment', '-c', default=True, action='store_true', help='Add comments to the RenPy script')

    args = parser.parse_args()
    handle_command(args)

def handle_command(args):

    # ログ設定をグローバルに
    settings.LOG_ENABLED = args.log
    settings.LOG_FILE = args.log_file

    if settings.LOG_ENABLED:
        logs.initialize_logfile() # ログファイルの初期化
        logs.logs('INFO', f'Logging enabled. Log file:{settings.LOG_FILE}')

    if args.mode == 'tsv_translate':
        pass
    elif args.mode == 'tsv2rpy':
        pass
    elif args.mode == 'extract_menu':
        pass
    elif args.mode == 'tsv_translate_menu':
        pass
    elif args.mode == 'tsv2rpy_menu':
        pass
    else:
        print('Invalid mode. Exiting...')