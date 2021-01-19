import requests
from bs4 import BeautifulSoup
from io import StringIO
import argparse


class Translator:

    def __init__(self):
        self.translated_text = []
        self.translated_examples = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) Chrome/50.0.2661.102'}
        self.supported_languages = {"0": "All", "1": "Arabic", "2": "German", "3": "English", "4": "Spanish",
                                    "5": "French", "6": "Hebrew", "7": "Japanese", "8": "Dutch", "9": "Polish",
                                    "10": "Portuguese", "11": "Romanian", "12": "Russian", "13": "Turkish"}
        self.string_io = StringIO()

    def translate(self, src_language, trg_language, text_to_translate, print_length=1):
        connection_error = False
        if trg_language != "All":
            url = f"https://context.reverso.net/translation/{src_language.lower()}-{trg_language.lower()}/{text_to_translate}"

            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                self.decode_response(response.text)
                self.print_translations(trg_language, length=print_length)
            elif response.status_code == 404:
                print(f"Sorry, unable to find {text_to_translate}")
                connection_error = True
            elif response.status_code == 500:
                print("Something wrong with your internet connection")
                connection_error = True
        else:
            for trg_lang in [lang for lang in self.supported_languages.values() if lang not in ["All", src_language]]:
                url = f"https://context.reverso.net/translation/{src_language.lower()}-{trg_lang.lower()}/{text_to_translate}"

                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    self.decode_response(response.text)
                    self.print_translations(trg_lang, length=print_length)
                elif response.status_code == 404:
                    print(f"Sorry, unable to find {text_to_translate}")
                    connection_error = True
                    break
                elif response.status_code == 500:
                    print("Something wrong with your internet connection")
                    connection_error = True
                    break
        if not connection_error:
            with open(f"{text_to_translate}.txt", "w", encoding='utf-8') as f:
                f.write(self.string_io.getvalue())

    def decode_response(self, response):
        soup = BeautifulSoup(response, 'html.parser')

        # find the translation
        translations = soup.select("#translations-content > a")
        translations = [tran.text.strip() for tran in translations]

        # find the example translation
        src_example_translations = soup.select("#examples-content > .example > .src")
        trg_example_translations = soup.select("#examples-content > .example > .trg")
        example_translations = []
        for src_example, trg_example in zip(src_example_translations, trg_example_translations):
            example_translations.extend([src_example.text.strip(), trg_example.text.strip()])

        self.translated_text = translations
        self.translated_examples = example_translations

    def print_translations(self, trg_lang, length):
        print(f'{trg_lang} Translations:')
        self.string_io.write(f'\n{trg_lang} Translations:\n')
        words_length = length if len(self.translated_examples) >= length else len(self.translated_examples)
        for translation in self.translated_text[:words_length]:
            print(translation)
            self.string_io.write(translation + "\n")
        print(f'\n{trg_lang} Examples:')
        self.string_io.write(f'\n{trg_lang} Examples:\n')
        examples_length = length * 2 if len(self.translated_examples) >= length * 2 else len(self.translated_examples)
        # examples_length = len(self.translated_examples)
        for idx, example in enumerate(self.translated_examples[:examples_length]):
            if idx % 2 == 0:
                print(f'{example}:')
                self.string_io.write(f'{example}:\n')
            elif idx != examples_length - 1:
                print(f'{example}\n')
                self.string_io.write(f'{example}\n\n')
            else:
                print(f'{example}')
                self.string_io.write(f'{example}')

    def get_language(self, lang):
        return self.supported_languages[lang]


def main(args):
    translator = Translator()
    if args:
        src_lang = args.src_lang.title()
        trg_lang = args.trg_lang.title()
        word = args.word
    else:
        print("Hello, you're welcome to the translator. Translator supports:\n"
              "1. Arabic\n2. German\n3. English\n4. Spanish\n5. French\n"
              "6. Hebrew\n7. Japanese\n8. Dutch\n9. Polish\n10. Portuguese\n"
              "11. Romanian\n12. Russian\n13. Turkish")
        src_lang = input("Type the number of your language: ")
        src_lang = translator.get_language(src_lang)
        trg_lang = input("Type the number of a language you want to translate to or '0' to translate to all languages: ")
        trg_lang = translator.get_language(trg_lang)
        word = input("Type the word you want to translate:")
        print()

    # handling the wrong exceptions
    if src_lang not in translator.supported_languages.values():
        print(f"Sorry, the program doesn't support {src_lang}")
    elif trg_lang not in translator.supported_languages.values():
        print(f"Sorry, the program doesn't support {trg_lang}")
    else:
        if trg_lang != "All":
            translator.translate(src_lang, trg_lang, word, print_length=5)
        else:
            translator.translate(src_lang, trg_lang, word, print_length=1)


def parse_args():
    parser = argparse.ArgumentParser(description='Translator app.')
    parser.add_argument('src_lang', help='The source language')
    parser.add_argument('trg_lang', help='The target language')
    parser.add_argument('word', help='The word to translate')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
