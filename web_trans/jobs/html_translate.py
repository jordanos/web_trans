from web_trans.jobs.base import BaseJob
from web_trans.utils.translator import CustomTranslator
from bs4 import BeautifulSoup, Tag, NavigableString
from tqdm import tqdm


class HtmlTranslate(BaseJob):
    def __init__(
        self, translator: CustomTranslator, src_file_path: str, dest_file_path: str
    ) -> None:
        self.translator = translator
        self.src_file_path = src_file_path
        self.dest_file_path = dest_file_path

    def execute_job(self) -> None:
        html = open(self.src_file_path).read()
        soup = BeautifulSoup(markup=html, features="html.parser")

        text_elements = [
            element
            for element in soup.find_all(string=True)
            if element.parent.name not in ["script", "style"]
        ]

        for element in tqdm(text_elements):
            # Extract the text from the element
            text = element.get_text(strip=True)
            # Skip the element if it's empty
            if not text:
                continue
            # Translate the texts
            translated = self.translator.translate(text)
            # Replace the text in the element
            element.replace_with(translated)

        with open(self.dest_file_path, "w") as file:
            file.write(soup.prettify())
