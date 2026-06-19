from deep_translator import GoogleTranslator

class MedicalTranslator:
    def __init__(self):
        print("\n[Setup] Google Translator লোড হচ্ছে...")
        # এখানে কোনো বড় মডেল ডাউনলোড হবে না, তাই কাজ অনেক দ্রুত হবে
        self.bn_to_en = GoogleTranslator(source='bn', target='en')
        self.en_to_bn = GoogleTranslator(source='en', target='bn')

    def translate_to_english(self, bangla_text):
        try:
            return self.bn_to_en.translate(bangla_text)
        except Exception as e:
            print(f"Error in EN translation: {e}")
            return bangla_text

    def translate_to_bengali(self, english_text):
        try:
            # বড় টেক্সট হলে গুগল একবারে অনুবাদ করতে পারে, বাক্য ভাঙার দরকার নেই
            return self.en_to_bn.translate(english_text)
        except Exception as e:
            print(f"Error in BN translation: {e}")
            return english_text