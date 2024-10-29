from argostranslate import package, translate
# Suppress stanza/pytorch warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="stanza")

package.install_from_path('en_zh.argosmodel') # 这里的模型地址，根据自己放置模型地址去写即可

class Translator():
    def __init__(self, from_lang="Chinese", to_lang="English") -> None:
        pass

    def translate(self, value):
        installed_languages = translate.get_installed_languages()

        translation_en_es = installed_languages[0].get_translation(installed_languages[1])
        print(translation_en_es)
        aa = translation_en_es.translate(value)
        self.result_t = aa
        return self.result_t

print(Translator().translate('help'))