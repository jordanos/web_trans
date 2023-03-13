import argparse
import logging
import sys
import json
from web_trans.jobs.collect_files import CollectFiles
from web_trans.jobs.clone_dir import CloneDir
from web_trans.jobs.html_translate import HtmlTranslate
from web_trans.utils.translator import CustomTranslator

# setup logging and track logs
logging.basicConfig(
    filename="session.log",
    filemode="w",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


# make a clone of the directory
# collect desired files from cloned directory
# execute jobs [translation]

unprocessed_html_files_path = "./unprocessed_html_files.json"
# proxies = [
#     {
#         "http": "167.172.238.6:9997",
#         "https": "167.172.238.6:9997",
#     },
# ]
proxies = None


def translate_lang(
    src_path: str, dest_path: str, dest_lang: str, is_clone: bool = True
) -> None:
    """Translate html files to specified language

    Args:
        src_path (str): source directory path
        dest_path (str): destination directory path
        dest_lang (str): destination language in two letters as in google translate. eg: [hi -> hindi]
        is_clone (bool, optional): boolean field to clone or not. Defaults to True.
    """
    if is_clone:
        logging.info("Cloning Dir...")
        clone = CloneDir(src_path, dest_path)
        clone.execute_job()
        logging.info("Done cloning.")

    if is_clone:
        logging.info("Collecting files...")
        collect = CollectFiles(dest_path, "html")
        html_files = collect.execute_job()
        logging.info("Done collecting.")
    else:
        with open(unprocessed_html_files_path, "r") as file:
            data = json.loads(file.read())
            html_files = data["html_files"]

    logging.info(f"{len(html_files)} html files to translate.")
    translator = CustomTranslator(
        dest=dest_lang,
        cache_path=f"./translated-{dest_lang}.json",
        proxies=proxies,
        # email="johndoe@gmail.com",
    )
    for i, html_file in enumerate(html_files):
        logging.info(f"Translating {html_file} to {dest_lang}")
        html_trans = HtmlTranslate(translator, html_file, html_file)
        html_trans.execute_job()
        translator.save_cache()
        del html_files[i]
        with open(unprocessed_html_files_path, "w") as file:
            data = {"html_files": html_files}
            file.write(json.dumps(data))
        logging.info(f"Done! {len(html_files) -1 - i} html files left.")


def str2bool(v: str) -> bool:
    """_summary_

    Args:
        v (str): _description_

    Raises:
        argparse.ArgumentTypeError: _description_

    Returns:
        bool: _description_
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make website transformations.")
    parser.add_argument(
        "--src",
        "-s",
        required=True,
        help="Source directory path.",
    )
    parser.add_argument(
        "--to-lang",
        "-to",
        required=True,
        help="Translate to language. eg: --to-lang=hi",
    )
    parser.add_argument(
        "--clone",
        "-c",
        required=False,
        type=str2bool,
        nargs="?",
        const=True,
        default=True,
        help="Clone directory and start a fresh session",
    )
    args = parser.parse_args()

    src_path = args.src
    dest_lang = args.to_lang
    clone = args.clone
    paths = src_path.split("/")
    paths[-1] = paths[-1] + f" translated to {dest_lang}"
    dest_path = "/".join(paths)
    translate_lang(src_path, dest_path, dest_lang, clone)
