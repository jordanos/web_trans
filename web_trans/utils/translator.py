import json
import requests
from translate import Translator
from translate.exceptions import InvalidProviderError
from translate.providers import MicrosoftProvider, DeeplProvider, LibreProvider
from web_trans.utils.providers.custom_mymemoryprovider import CustomMyMemoryProvider
from web_trans.utils.providers.custom_libre import CustomLibre

DEFAULT_PROVIDER = CustomMyMemoryProvider
TRANSLATION_API_MAX_LENGTH = 500

PROVIDERS_CLASS = {
    "mymemory": CustomMyMemoryProvider,
    "microsoft": MicrosoftProvider,
    "deepl": DeeplProvider,
    "libre": CustomLibre,
}


class TranslatorMod(Translator):
    def __init__(
        self,
        to_lang,
        from_lang="en",
        provider=None,
        secret_access_key=None,
        region=None,
        **kwargs,
    ) -> None:
        self.available_providers = list(PROVIDERS_CLASS.keys())
        self.from_lang = from_lang
        self.to_lang = to_lang
        if provider and provider not in self.available_providers:
            raise InvalidProviderError(
                "Provider class invalid. "
                "Please check providers list below: {!r}".format(
                    self.available_providers
                )
            )

        provider_class = PROVIDERS_CLASS.get(provider, DEFAULT_PROVIDER)

        self.provider = provider_class(
            from_lang=from_lang,
            to_lang=to_lang,
            secret_access_key=secret_access_key,
            region=region,
            **kwargs,
        )


class CustomTranslator:
    def __init__(
        self, dest: str, cache_path: str, proxies: list[dict] = None, **kwargs
    ) -> None:
        self.dest = dest
        self.cache_path = cache_path
        self.cache = None
        session = requests.Session()
        self.translator_api = TranslatorMod(
            to_lang=dest, session=session, proxies=proxies, **kwargs
        )
        self.load_cache()

    def translate(self, text: str) -> str:
        # check if it exists in cache
        if text in self.cache:
            return self.cache[text]
        # check char length
        if len(text) >= TRANSLATION_API_MAX_LENGTH:
            return text
        # get from api if not in cache
        translated = self.translator_api.translate(text)
        if translated.startswith("MYMEMORY WARNING"):
            self.save_cache()
            raise Exception(f"Translation error: {translated}")
        self.cache[text] = translated
        self.save_cache()
        return translated

    def load_cache(self) -> None:
        try:
            with open(self.cache_path, "r") as file:
                json_data = file.read()
                data = json.loads(json_data)
                self.cache = data
        except FileNotFoundError:
            # todo: log
            with open(self.cache_path, "w") as file:
                file.write(json.dumps({}))
            self.cache = {}

    def save_cache(self) -> None:
        with open(self.cache_path, "w") as file:
            file.write(json.dumps(self.cache))
