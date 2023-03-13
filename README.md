# Web transformations
This project will enable you to do transformations on html files. one example would be translating static webpages to the desired language.

## Translate language of a folder containing html files
- Go to root of this repo and run `python main.py --src=<path to folder containing html files> --to-lang=<language code, eg: for hindi -> "hi"`
- If we pass `--clone=<no>` it will assume it has already duplicated the folder before and It'll continue from where it stopped. However, if we omit to pass the flag, it will duplicate/clone the folder and start a fresh session.