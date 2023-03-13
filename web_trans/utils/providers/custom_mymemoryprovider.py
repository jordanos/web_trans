from requests import Session
from typing import List
from translate.providers.base import BaseProvider
from translate.exceptions import TranslationError


class CustomMyMemoryProvider(BaseProvider):
    """
    @MyMemoryProvider: This is a integration with Translated MyMemory API.
    Follow Informations:
      Website: https://mymemory.translated.net/
      Documentation: https://mymemory.translated.net/doc/spec.php
    Usage Tips: Use a valid email instead of the default.
        With a valid email you get 10 times more words/day to translate.
    For further information checkout:
    http://mymemory.translated.net/doc/usagelimits.php
                                                    Tips from: @Bachstelze
    """

    name = "MyMemory"
    base_url = "http://api.mymemory.translated.net/get"
    session = None

    def __init__(self, session: Session, proxies: List[dict] = None, **kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(CustomMyMemoryProvider, self).__init__(**kwargs)

        self.email = kwargs.get("email", "")
        self.languages = "{}|{}".format(self.from_lang, self.to_lang)
        self.session = session
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
        }
        self.proxies = proxies
        self.current_proxy = 0

    def _make_request(self, text: str) -> dict:
        params = {"q": text, "langpair": self.languages}
        if self.email:
            params["de"] = self.email

        # if self.session is None:
        #     self.session = requests.Session()
        if self.proxies is not None:
            response = self.session.get(
                self.base_url,
                params=params,
                headers=self.headers,
                proxies=self.proxies[self.current_proxy],
            )
            self.current_proxy += 1
            if self.current_proxy >= len(self.proxies):
                self.current_proxy = 0
        else:
            response = self.session.get(
                self.base_url,
                params=params,
                headers=self.headers,
            )
        response.raise_for_status()
        return response.json()

    def get_translation(self, text: str) -> str:
        data = self._make_request(text)

        translation = data["responseData"]["translatedText"]
        if data["responseStatus"] != 200:
            e = TranslationError(translation)
            e.json = data
            raise e
        if translation:
            return translation
        else:
            matches = data["matches"]
            next_best_match = next(match for match in matches)
            return next_best_match["translation"]
