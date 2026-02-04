import ctypes
import os
import time
import json

class MasmLibrary:
    def __init__(self, dll_name="Masm_api2.dll"):
        self.dll_path = os.path.abspath(dll_name)
        self.masm_engine = ctypes.WinDLL(self.dll_path)
        self.masm_engine.Main_func.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint64]
        self.intel_file = "t.txt"
        self.text = ""

    def strike(self, api_key, prompt):
        ai_link = b"/v1beta/models/gemma-3-4b-it:generateContent?key=" + api_key.encode('utf-8') + b'\x00'
        prefix = b'{ "contents": [{ "parts":[{ "text": "'
        suffix = b'" }] }] }'
        ai_body = prefix + prompt.encode('utf-8') + suffix
        body_len = len(ai_body)

        try:
            print(f"👊 STRIKING: {body_len} bytes...")
            self.masm_engine.Main_func(ai_link, ai_body, body_len)
            raw_data = self._collect_intel()
            self._parse_payload(raw_data)
            return self.text
        except Exception as e:
            self.text = f"💀 THE TRENCH COLLAPSED: {e}"
            return self.text
            
    def _parse_payload(self, raw_data):
        try:
            if "💀" in raw_data:
                self.text = raw_data
                return
            parsed = json.loads(raw_data)
            self.text = parsed['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            self.text = raw_data

    def _collect_intel(self):
        timeout = 5.0
        start = time.time()
        while not os.path.exists(self.intel_file) or os.path.getsize(self.intel_file) == 0:
            if time.time() - start > timeout:
                return "💀 ERROR: Trench Timeout"
            time.sleep(0.1)
        time.sleep(0.2)
        with open(self.intel_file, "r", encoding="utf-8") as f:
            data = f.read()
        os.remove(self.intel_file)
        return data

if __name__ == "__main__":
    my_key = "YOUR_KEY_HERE"
    lib = MasmLibrary("Masm_api2.dll")
    lib.strike(my_key, "Explain the beauty of x64 assembly.")
    print(f"\n🏛️ THE RESPONSE:\n{lib.text}")
