"""Text extraction module"""

import math
import os
from collections import Counter
import re

from pydub import AudioSegment
from pydub.utils import make_chunks, which
from unidecode import unidecode


from speech_recognition import Recognizer, AudioFile
from speech_recognition import UnknownValueError

os.chdir(os.path.abspath("\\".join(__file__.split("\\")[:-2])))
print(os.getcwd())
WORDS_DIR = "wordlists"


geen_verkleinwoorden = ()
with open(f"{WORDS_DIR}/geen_verkleinwoorden.txt", "r", encoding="utf-8") as f:
    geen_verkleinwoorden = f.read().splitlines()

nietzeggendewoorden = ()
with open(f"{WORDS_DIR}/nietszeggendewoorden.txt", "r", encoding="utf-8") as f:
    nietzeggendewoorden = f.read().splitlines()

tussenwerpels_woorden = ()
with open(f"{WORDS_DIR}/tussenwerpsels.txt", "r", encoding="utf-8") as f:
    tussenwerpels_woorden = f.read().splitlines()


def speech_recognition(filename: str):
    """Convert audio file to text"""
    recognizer = Recognizer()
    try:
        print(filename, " to chunks")
        AudioSegment.converter = which("ffmpeg")
        myaudio: AudioSegment = AudioSegment.from_file(filename)  # type: ignore
        channel_count: int = myaudio.channels  # Get channels    # type: ignore
        # sample_width = myaudio.sample_width  # Get sample width
        duration_in_sec: float = len(myaudio) / 1000
        sample_rate: int = myaudio.frame_rate  # type: ignore

        print("duration_in_sec=", duration_in_sec)
        print("frame_rate=", sample_rate)  # type: ignore
        bit_rate = (
            16  # assumption , you can extract from mediainfo("test.wav") dynamically
        )

        wav_file_size: float = (
            sample_rate * bit_rate * channel_count * duration_in_sec
        ) / 20
        print("wav_file_size = ", wav_file_size)

        chunk_length_in_sec = math.ceil(
            (duration_in_sec * 20000000) / wav_file_size
        )  # in sec
        chunk_length_ms = chunk_length_in_sec * 2000
        chunks: list[AudioSegment] = make_chunks(myaudio, chunk_length_ms)  # type: ignore

        # Export all of the individual chunks as wav files

        if not os.path.exists("./uploads/chunks"):
            os.makedirs("./uploads/chunks")

        for i, chunk in enumerate(chunks):
            chunk_name = f"./uploads/chunks/chunck{i}.flac"
            print("exporting", chunk_name)
            chunk.export(chunk_name, format="flac")  # type: ignore
    except Exception as error:
        error_message = f"Fout bij het bewerken van de audiofile: {error}."
        print(error_message)
        return error_message

    chunk_dir = "./uploads/chunks/"

    nr_of_items = len(
        [
            name
            for name in os.listdir(chunk_dir)
            if os.path.isfile(os.path.join(chunk_dir, name))
        ]
    )

    total_text = ""

    try:
        for i in range(nr_of_items):
            # Speech Recognition
            audio_file = AudioFile(f"./uploads/chunks/chunck{i}.flac")
            with audio_file as source:
                recognizer.adjust_for_ambient_noise(source)  # type: ignore
                audio = recognizer.record(source)  # type: ignore
                text = recognize_google_safe(
                    recognizer, audio_data=audio, language="nl-BE"
                )

                total_text += text
                print("######## Google Recognize ####################")
                print(text)
                print("##############################################")
        return total_text.strip()
    except Exception as error:
        error_message = f"Fout bij de spraakherkenning: test123{error}."
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


def herhalende_zinnen(text: str) -> str:
    """Check if sentences are repeated"""
    nz_woorden = nietzeggendewoorden
    words = make_array_words(text)

    cache: list[str] = []
    to_be_deleted: list[str] = []
    repetition: list[str] = []

    for word in words:
        while len(cache) >= 25:
            cache.pop(0)
        if word not in nz_woorden:
            cache.append(word)  # type: ignore

    same_equals = {word: cache.count(word) for word in cache}

    if same_equals:
        for word in same_equals:
            if same_equals[word] == 1:
                to_be_deleted.append(word)
            else:
                repetition.append(word)
        for word in to_be_deleted:
            del same_equals[word]

    if len(repetition) == 0:
        return '<span class="text-success">Er zijn geen herhalingen gevonden</span>'
    return highlight_words_in_text(text, set(repetition))


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
    herhalingen = herhalende_zinnen(total_text)
    collectieve_voornaamwoorden = extract_collectieve_voornaamwoorden(total_text)
    tussenwerpsels = extract_tussenwerpsels(total_text)

    return {
        "speech_recognition": total_text,
        "verkleinwoorden": verkleinwoorden,
        "herhalingen": herhalingen,
        "collectieve_voornaamwoorden": collectieve_voornaamwoorden,
        "tussenwerpsels": tussenwerpsels,
    }


def recognize_google_safe(
    recognizer: Recognizer, audio_data, language: str = "nl-NL"
) -> str:  # type: ignore
    """Safe version of recognize_google"""
    try:
        text = recognizer.recognize_google(audio_data, language=language)  # type: ignore
        if isinstance(text, str):
            return " " + text
        else:
            return " " + " ".join(text)  # type: ignore
    except UnknownValueError:
        error_message = "!!Er is geen tekst herkend in het spraakbericht.!!"
        print(error_message)
        return ""
