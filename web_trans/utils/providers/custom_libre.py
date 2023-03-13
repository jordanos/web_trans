import time
from requests import Session
from translate.providers.base import BaseProvider
from translate.exceptions import TranslationError


class CustomLibre(BaseProvider):
    """Libre translation api prvider"""

    name = "Libre"
    base_url = "https://libretranslate.com/translate"
    session = None

    def __init__(self, session: Session, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except TypeError:
            super(CustomLibre, self).__init__(**kwargs)

        self.email = kwargs.get("email", "")
        self.languages = "{}|{}".format(self.from_lang, self.to_lang)
        self.session = session
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
            # "Content-Type": "application/json",
            # "Cookie": "session=cfe01acf-1133-40f5-b3a5-87750af96f75; _ga_KPKM1EP5EW=GS1.1.1678684574.3.1.1678684603.0.0.0; _ga=GA1.1.1962327522.1678664930",
            "Origin": "https://libretranslate.com",
        }

    def _make_request(self, text: str) -> dict:
        body = {
            "q": text,
            "source": "auto",
            "target": self.to_lang,
            "format": "text",
            "api_key": "",
            "secret": "ZZL8Z4L",
        }

        # if self.session is None:
        #     self.session = requests.Session()
        response = self.session.post(self.base_url, data=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_translation(self, text: str) -> str:
        data = self._make_request(text)
        time.sleep(2)

        translation = data["translatedText"]
        if translation:
            return translation
        raise Exception("Translation error")
