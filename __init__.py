# Config
WORK = True
EXTRACT_DIALOGUE_OUTPUT = 'untranslated.tsv'
EXTRACT_DIALOGUE_TO_LANG = 'japanese'

def extract():
    import renpy
    from renpy import ast
    import io

    def get_untranslated_info_line(tobj):
        contents = ""
        if tobj.block and (tobj.block[0].translatable or isinstance(tobj.block[0], ast.Say)):
            contents = tobj.block[0].get_code()

        return u'{}\t{}\t{}\t{}\n'.format(tobj.filename, tobj.linenumber, tobj.identifier, contents) # TSV形式で出力

    def make_untranslated_txt(language):

        translator = renpy.game.script.translator # 現在の翻訳情報を取得(\renpy\translation\__init__.py)

        missing_translates = set()

        for tlblockid, translate in translator.default_translates.items():
            if (tlblockid, language) not in translator.language_translates: # 翻訳が存在しない場合
                missing_translates.add(translate)

        with io.open(EXTRACT_DIALOGUE_OUTPUT,'w',encoding='utf-8') as f:
            f.write(u"filename\tlinenumber\tidentifier\tcontents\n") # TSVのヘッダー
            for line in sorted(map(get_untranslated_info_line, missing_translates), key=lambda x: (x.split('\t')[0], int(x.split('\t')[1]) if x else 0)):
                f.write(line)

    if WORK:
        make_untranslated_txt(EXTRACT_DIALOGUE_TO_LANG)
