"""This module contains the functions that process the requests from the website."""
import os
from datetime import datetime
from typing import Any

from .sound_analysis import calculate_loudness, calculate_pitch
from . import text_extraction
from .utilities import (
    audio_to_wav,
    remove_uploads,
    remove_temp_file,
    remove_chunks,
    remove_file,
)
from .audio_preprocessing import remove_noise_from_files



def error_response() -> str:
    """Make the HTML text for the error response"""
    return '<span class="text-muted">Er was een probleem met deze functie. Probeer opnieuw.</span>'


def generate_filename(speech_type: str = "") -> str:
    """Generate a filename for the audio file"""
    now = datetime.now()
    d_1 = now.strftime("%Y%m%d%H%M%S")
    return f"{d_1}_{speech_type}.wav" if speech_type else f"{d_1}.wav"


def process_elder(elder_file: str, extract_text: bool) -> dict[str, Any]:
    """Process the request from the elderspeak page"""
    response_data: dict[str, Any] = {
        "pitch": calculate_pitch(elder_file, elderspeak=True, stream=False),
        "loudness": calculate_loudness(elder_file, elderspeak=True),
    }

    if extract_text:
        text_features = text_extraction.extract_text_features(elder_file)

    else:
        text_features = {
            "speech_recognition": "Tekst-extractie is uitgeschakeld",
        }
    response_data = {**response_data, **text_features}

    remove_chunks()
    # remove_file(elder_file)
    # remove_uploads()
    return response_data


def process_audio(request):
    """Process the request from the audio page"""

    file_elder = generate_filename("elder")

    with open(os.path.abspath(file_elder), "wb") as data_file:
        data_file.write(request.files["audio_elder"].read())
    audio_to_wav(file_elder)

    extract_text = request.form.get("extract_text") == "true"


    elder_data = process_elder(file_elder, extract_text)

    response_data = remove_noise_from_files(file_elder)

    elder_data_filtered = process_elder(file_elder, False)


    response_data["elder"].update(elder_data)

    response_data["elder_filtered"] = elder_data_filtered

    remove_file(file_elder)

    return response_data
