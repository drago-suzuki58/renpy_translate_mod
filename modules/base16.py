import binascii
import re

import modules.run_logs as logs

# Base16エンコード
def base16_encode(s):
    try:
        encoded = binascii.hexlify(s.encode()).decode()
        logs.logs("DEBUG", "Encoded", f"{s} -> {encoded}")
        return encoded
    except Exception as e:
        logs.logs("ERROR", "Encode", f"Failed to encode reason: {e}\tText:{s}")
        return s

def base16_decode(s):
    try:
        decoded = binascii.unhexlify(s.encode()).decode()
        logs.logs("DEBUG", "Decoded", f"{s} -> {decoded}")
        return decoded
    except Exception as e:
        logs.logs("ERROR", "Decode", f"Failed to decode reason: {e}\tText:{s}")
        return s

def encode_matches(pattern, text):
    matches = re.findall(pattern, text)
    for match in matches:
        encoded_match = base16_encode(match) # 括弧ごとエンコードする
        text = text.replace(match, f'"[{encoded_match}]"') # エンコードしたものを括弧で囲む
    return text

def decode_matches(text):
    matches = re.findall(r"\[.*?\]", text) # 後でこれごと置換するので[]ごと取得
    for match in matches:
        decoded_match = base16_decode(match[1:-1]) # []を取り除く
        text = text.replace(match, decoded_match)
    return text
