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


def pitch_response(response) -> str:
    """Make the HTML text for the pitch comparison"""
    response_dict = {
        "hoger": 'text-danger">Hoger',
        "normaal": 'text-success">Lager of niet significant hoger',
    }
    return f'<span class="{response_dict[response]}</span>'


def loudness_response(response) -> str:
    """Make the HTML text for the loudness comparison"""
    response_dict = {
        "hoger": 'text-danger">Luider',
        "normaal": 'text-success">Stiller of niet significant luider',
    }
    return f'<span class="{response_dict[response]}</span>'


def error_response() -> str:
    """Make the HTML text for the error response"""
    return '<span class="text-muted">Er was een probleem met deze functie. Probeer opnieuw.</span>'


def compare_pitch(normal: float, current: float) -> str:
    """Compare the pitch of the normal and elderspeak audio"""
    if normal and current:
        current, normal = round(current, 2), round(normal, 2)
        difference: float = 100
        if current > normal + difference:
            return pitch_response("hoger").format((normal), current)
        return pitch_response("normaal").format(normal, current)
    return error_response()


def compare_loudness(normal: float, current: float) -> str:
    """Compare the loudness of the normal and elderspeak audio"""
    if normal and current:
        current, normal = round(current, 2), round(normal, 2)
        difference: float = 4
        if current > normal + difference:
            return loudness_response("hoger").format(normal, current)
        return loudness_response("normaal").format(normal, current)
    return error_response()


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
            "verkleinwoorden": "Tekst-extractie is uitgeschakeld",
            "herhalingen": "Tekst-extractie is uitgeschakeld",
            "collectieve_voornaamwoorden": "Tekst-extractie is uitgeschakeld",
            "tussenwerpsels": "Tekst-extractie is uitgeschakeld",
        }
    response_data = {**response_data, **text_features}

    remove_chunks()
    # remove_file(elder_file)
    # remove_uploads()
    return response_data


def process_normal(normal_file: str) -> dict[str, Any]:
    """Process the request from the normal page"""

    response_data = {
        "pitch": calculate_pitch(wav_file=normal_file, elderspeak=False, stream=False),
        "loudness": calculate_loudness(wav_file=normal_file, elderspeak=False),
    }

    # remove_file(normal_file)
    remove_temp_file()
    return response_data


def process_audio(request):
    """Process the request from the audio page"""

    file_normal = generate_filename("normal")
    file_elder = generate_filename("elder")

    with open(os.path.abspath(file_normal), "wb") as data_file:
        data_file.write(request.files["audio_normal"].read())
    audio_to_wav(file_normal)

    with open(os.path.abspath(file_elder), "wb") as data_file:
        data_file.write(request.files["audio_elder"].read())
    audio_to_wav(file_elder)

    extract_text = request.form.get("extract_text") == "true"

    normal_data = process_normal(file_normal)
    elder_data = process_elder(file_elder, extract_text)

    response_data = remove_noise_from_files(file_normal, file_elder)
    normal_data_filtered = process_normal(file_normal)
    elder_data_filtered = process_elder(file_elder, False)

    response_data["normal"].update(normal_data)
    response_data["elder"].update(elder_data)
    response_data["normal_filtered"] = normal_data_filtered
    response_data["elder_filtered"] = elder_data_filtered

    response_data["pitch_comparison"] = compare_pitch(
        response_data["normal"]["pitch"], response_data["elder"]["pitch"]
    )
    response_data["loudness_comparison"] = compare_loudness(
        response_data["normal"]["loudness"], response_data["elder"]["loudness"]
    )
    remove_file(file_normal)
    remove_file(file_elder)

    return response_data
