"""Text extraction module"""

import whisper

import spacy
import os
import string

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


def tag_words(text):
    nlp = spacy.load("nl_core_news_lg")

    doc = nlp(text)

    classified = []

    for token in doc:
        if token.text is not None:
            if "dim" in token.tag_ and token.text not in geen_verkleinwoorden:
                classified.append([token.text, "VKW"])
            elif "TSW" in token.tag_ or token.text.lower() in tussenwerpels_woorden:
                classified.append([token.text, "TSW"])
            elif "VNW" in token.tag_ and "1|mv" in token.tag_:
                classified.append([token.text, "CVNW"])
            else:
                classified.append([token.text, "NONE"])
        else:
            classified.append([token.text, "NONE"])

    return classified


def format_text(textlist):
    text = '</p></p><span class="green-highlight">Tussenwerpsels worden in groen aangeduid</span></p></p><span class="yellow-highlight">Verkleinwoorden worden in geel aangeduid</span></p></p><span class="pink-highlight">Collectieve voornaamwoorden worden in roze aangeduid</span></p></p>'
    num_VKW = 0
    num_CVNW = 0
    num_TSW = 0
    for word, tag in textlist:
        if word in string.punctuation:
            text = text[:-1]  # remove the added space from previous word
            text += word + ' '
        elif tag == 'NONE':
            text += word + ' '
        elif tag == 'TSW':
            text += f'<span class="green-highlight">{word}</span>' + ' '
            num_TSW += 1
        elif tag == 'VKW':
            text += f'<span class="yellow-highlight">{word}</span>' + ' '
            num_VKW += 1
        elif tag == 'CVNW':
            text += f'<span class="pink-highlight">{word}</span>' + ' '
            num_CVNW += 1

    text = 'Aantal Tussenwerpsels gebruikt: ' + str(num_TSW) + '</p></p>Aantal verkleinwoorden gebruikt: ' + str(
        num_VKW) + '</p></p>Aantal Collectieve Voornaamwoorden gebruikt: ' + str(num_CVNW) + text

    return text


def extract_text_features(filename: str):
    """Extract text features from a given audio file"""
    total_text = speech_recognition(filename)
    print('extracting features')
    total_text = tag_words(total_text)
    total_text = format_text(total_text)

    return {
        "speech_recognition": total_text,
    }
