import unittest
import sys

sys.path.insert(0, '../renpy_translate_mod')

import modules.settings as settings
import modules.run_logs as logs
import modules.base16 as base16
import modules.menu.tsv_translate as menu_tsv_translate
import modules.dialogue.tsv_translate as dialogue_tsv_translate
import modules.menu.tsv2rpy as menu_tsv2rpy
import modules.dialogue.tsv2rpy as dialogue_tsv2rpy
import modules.menu.extract as menu_extract

class TestModules(unittest.TestCase):
    def setUp(self):

        self.settings()
        settings.LOG_ENABLED = True
        settings.LOG_FILE = 'test/log.txt'
        settings.LOG_LEVEL = 'DEBUG'

    def settings(self):
        settings.load_settings_from_ini()

    def test_run_logs(self):
        logs.initialize_logfile()

        logs.logs("DEBUG", "Logs", f"Test")
        logs.logs("INFO", "Logs", f"Test")
        logs.logs("WARNING", "Logs", f"Test")
        logs.logs("ERROR", "Logs", f"Test")
        logs.logs("CRITICAL", "Logs", f"Test")

    def test_encode_decode_core(self):
        test_string = "This is a test string"
        encoded_string = base16.base16_encode(test_string)
        decoded_string = base16.base16_decode(encoded_string)

        self.assertEqual(test_string, decoded_string)

    def test_encode_decode_match_1(self):
        test_string = "Hello, {player_name}"
        encoded_string = base16.encode_matches(r'\{.*?\}', test_string)
        decoded_string = base16.decode_matches(encoded_string)

        self.assertEqual(test_string, decoded_string)

    def test_encode_decode_match_2(self):
        test_string = "Hello, [player_name]"
        encoded_string = base16.encode_matches(r'\[.*?\]', test_string)
        decoded_string = base16.decode_matches(encoded_string)

        self.assertEqual(test_string, decoded_string)

    def test_encode_decode_match_3(self):
        test_string = "Hello, \"player_name\""
        encoded_string = base16.encode_matches(r'\\.', test_string)
        decoded_string = base16.decode_matches(encoded_string)

        self.assertEqual(test_string, decoded_string)


    def test_dialogue_tsv_translate_1(self):
        dialogue_tsv_translate.main("test/input_sample/untranslated.tsv", "test/file/translated_1.tsv", "en", "ja", [""], 0)
        with open("test/file/translated_1.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/translated_1.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_dialogue_tsv_translate_2(self):
        dialogue_tsv_translate.main("test/input_sample/untranslated.tsv", "test/file/translated_2.tsv", "en", "ja", ["test1.rpy"], 0)
        with open("test/file/translated_2.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/translated_2.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_dialogue_tsv_translate_3(self):
        dialogue_tsv_translate.main("test/input_sample/untranslated.tsv", "test/file/translated_3.tsv", "en", "ja", [""], 9)
        with open("test/file/translated_3.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/translated_3.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_dialogue_tsv_translate_4(self):
        dialogue_tsv_translate.main("test/input_sample/untranslated.tsv", "test/file/translated_4.tsv", "en", "zh-CN", [""], 0)
        with open("test/file/translated_4.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/translated_4.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_dialogue_tsv_translate_5(self):
        dialogue_tsv_translate.main("test/input_sample/untranslated.tsv", "test/file/translated_5.tsv", "en", "ja", ["test1.rpy", "test3.rpy"], 0)
        with open("test/file/translated_5.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/translated_5.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)


    def test_menu_tsv_translate_1(self):
        menu_tsv_translate.main("test/input_sample/menu_untranslated.tsv", "test/file/menu_translated_1.tsv", "en", "ja", [""], 0, "")
        with open("test/file/menu_translated_1.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_translated_1.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_menu_tsv_translate_2(self):
        menu_tsv_translate.main("test/input_sample/menu_untranslated.tsv", "test/file/menu_translated_2.tsv", "en", "ja", ["test1.rpy"], 0, "")
        with open("test/file/menu_translated_2.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_translated_2.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_menu_tsv_translate_3(self):
        menu_tsv_translate.main("test/input_sample/menu_untranslated.tsv", "test/file/menu_translated_3.tsv", "en", "ja", [""], 9, "")
        with open("test/file/menu_translated_3.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_translated_3.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_menu_tsv_translate_4(self):
        menu_tsv_translate.main("test/input_sample/menu_untranslated.tsv", "test/file/menu_translated_4.tsv", "en", "zh-CN", [""], 0, "")
        with open("test/file/menu_translated_4.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_translated_4.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_menu_tsv_translate_5(self):
        menu_tsv_translate.main("test/input_sample/menu_untranslated.tsv", "test/file/menu_translated_5.tsv", "en", "ja", ["test1,rpy", "test3.rpy"], 0, "")
        with open("test/file/menu_translated_5.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_translated_5.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_menu_tsv_translate_6(self):
        menu_tsv_translate.main("test/input_sample/menu_untranslated.tsv", "test/file/menu_translated_6.tsv", "en", "ja", [""], 0, "test/input_sample/menu_translated_dic.tsv")
        with open("test/file/menu_translated_6.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_translated_6.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_dialogue_tsv2rpy_1(self):
        dialogue_tsv2rpy.main("test/input_sample/translated.tsv", "test/file/converted_1.rpy", "japanese", False, False, "")
        with open("test/file/converted_1.rpy", "r", encoding="utf-8") as output_f:
            with open("test/sample/converted_1.rpy", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_dialogue_tsv2rpy_2(self):
        dialogue_tsv2rpy.main("test/input_sample/translated.tsv", "test/file/converted_2.rpy", "japanese", True, True, "test/file/converted_2_")
        for filename in ["test1", "test2", "test3"]:
            with open(f"test/file/converted_2_{filename}.rpy", "r", encoding="utf-8") as output_f:
                with open(f"test/sample/converted_2_{filename}.rpy", "r", encoding="utf-8") as sample_f:
                    output_lines = output_f.readlines()
                    sample_lines = sample_f.readlines()
                    for output_line, sample_line in zip(output_lines, sample_lines):
                        self.assertEqual(output_line, sample_line)

    def test_menu_tsv2rpy_1(self):
        menu_tsv2rpy.main("test/input_sample/menu_translated.tsv", "test/file/menu_converted_1.rpy", "japanese", False, False, "")
        with open("test/file/menu_converted_1.rpy", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_converted_1.rpy", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_menu_tsv2rpy_2(self):
        menu_tsv2rpy.main("test/input_sample/menu_translated.tsv", "test/file/menu_converted_2.rpy", "japanese", True, True, "test/file/menu_converted_2_")
        for filename in ["test1", "test2", "test3"]:
            with open(f"test/file/menu_converted_2_{filename}.rpy", "r", encoding="utf-8") as output_f:
                with open(f"test/sample/menu_converted_2_{filename}.rpy", "r", encoding="utf-8") as sample_f:
                    output_lines = output_f.readlines()
                    sample_lines = sample_f.readlines()
                    for output_line, sample_line in zip(output_lines, sample_lines):
                        self.assertEqual(output_line, sample_line)


    def test_menu_extract_1(self):
        menu_extract.main(["test/input_sample/menu_1.rpy"], "test/file/menu_extracted_1.tsv")
        with open("test/file/menu_extracted_1.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_extracted_1.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

    def test_menu_extract_2(self):
        menu_extract.main(["test/input_sample/menu_1.rpy", "test/input_sample/menu_2.rpy"], "test/file/menu_extracted_2.tsv")
        with open("test/file/menu_extracted_2.tsv", "r", encoding="utf-8") as output_f:
            with open("test/sample/menu_extracted_2.tsv", "r", encoding="utf-8") as sample_f:
                output_lines = output_f.readlines()
                sample_lines = sample_f.readlines()
                for output_line, sample_line in zip(output_lines, sample_lines):
                    self.assertEqual(output_line, sample_line)

if __name__ == "__main__":
    unittest.main()