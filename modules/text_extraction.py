"""Text extraction module"""

import math
import os
from collections import Counter
import re
import whisper

from pydub import AudioSegment
from pydub.utils import make_chunks, which
from unidecode import unidecode


from speech_recognition import Recognizer, AudioFile
from speech_recognition import UnknownValueError

os.chdir(os.path.abspath("\\".join(__file__.split("\\")[:-2])))
print(os.getcwd())
WORDS_DIR = "wordlists"



with open(f"{WORDS_DIR}/geen_verkleinwoorden.txt", "r", encoding="utf-8") as f:
    geen_verkleinwoorden = f.read().splitlines()

with open(f"{WORDS_DIR}/nietszeggendewoorden.txt", "r", encoding="utf-8") as f:
    nietzeggendewoorden = f.read().splitlines()

with open(f"{WORDS_DIR}/tussenwerpsels.txt", "r", encoding="utf-8") as f:
    tussenwerpels_woorden = f.read().splitlines()


def speech_recognition(filename: str):
    try:
        print("Transcribing")
        model = whisper.load_model("small")
        result = model.transcribe(filename, language="nl")
        print(result["text"])
        return result["text"]
    except Exception as error:
        error_message = f"Fout bij de spraakherkenning: {error}."
        print(error_message)
        return error_message


def extract_collectieve_voornaamwoorden(text: str):
    """Check if collective pronouns are used"""
    words = make_array_words(text)
    collectieve_voornaamwoorden_array = [word for word in words if word == "we"]
    if len(collectieve_voornaamwoorden_array) == 0:
        return '<span class="text-success">\
            Er werden geen collectieve voornaamwoorden gebruikt.\
                </span>'
    counter = dict(Counter(collectieve_voornaamwoorden_array))
    filtered_dict = {k: v for (k, v) in counter.items() if v > 1}
    filtered_set = set(filtered_dict.keys())
    if len(filtered_set) == 0:
        return '<span class="text-success">\
            Er werden niet genoeg collectieve voornaamwoorden gebruikt.\
                </span>'
    return highlight_words_in_text(text, filtered_set)


def extract_tussenwerpsels(text: str):
    """Check if interjections are used"""
    words = make_array_words(text)
    tussenwerpsels_array = [word for word in words if word in tussenwerpels_woorden]
    if len(tussenwerpsels_array) == 0:
        return (
            '<span class="text-success">Er werden geen tussenwerpsels gebruikt.</span>'
        )
    counter = dict(Counter(tussenwerpsels_array))
    filtered_dict = {k: v for (k, v) in counter.items() if v > 1}
    filtered_set = set(filtered_dict.keys())
    if len(filtered_set) == 0:
        return '<span class="text-success">\
            Er werden niet genoeg tussenwerpsels gebruikt.\
                </span>'
    return highlight_words_in_text(text, filtered_set)


def extract_verkleinwoorden(text: str):
    """Check if diminutives are used"""

    words = make_array_words(text)
    verkleinwoorden_array: list[str] = [
        word
        for word in words
        if (len(word) > 3 and word not in geen_verkleinwoorden)
        and (word.endswith(("je", "ke", "kes", "jes")))
    ]
    if len(verkleinwoorden_array) == 0:
        return '<span class="text-success">Er zijn geen verkleinwoorden gevonden</span>'
    return highlight_words_in_text(text, set(verkleinwoorden_array))


def replace_hey(text: str) -> str:
    """Replace the word like 'hey' with 'hey'"""
    text = text.replace(" hé ", " hey ")
    text = text.replace(" hè ", " hey ")
    text = text.replace(" he ", " hey ")
    text = text.replace(" hoi ", " hey ")
    text = text.replace(" hee ", " hey ")
    text = text.replace(" heyy ", " hey ")
    return text


def make_array_words(text: str) -> list[str]:
    """Make an array of words"""
    text = re.sub(r"\s{2,}", "", text.lower())
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    return words


def highlight_words_in_text(text: str, words: set[str]):
    """Highlight words in text"""
    text = text.lower()
    text = unidecode(text)
    for word in words:
        text = text.replace(unidecode(word), f'<span class="text-danger">{word}</span>')
    return text


def extract_text_features(filename: str) -> dict[str, str]:
    """Extract text features from a given audio file"""
    total_text = speech_recognition(filename)
    total_text = replace_hey(total_text)
    verkleinwoorden = extract_verkleinwoorden(total_text)

    collectieve_voornaamwoorden = extract_collectieve_voornaamwoorden(total_text)
    tussenwerpsels = extract_tussenwerpsels(total_text)

    return {
        "speech_recognition": total_text,
        "verkleinwoorden": verkleinwoorden,
        "collectieve_voornaamwoorden": collectieve_voornaamwoorden,
        "tussenwerpsels": tussenwerpsels,
    }
