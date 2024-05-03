"""Utilities for the website"""
from os import listdir, mkdir, path, remove
from shutil import rmtree

from librosa import load  # pylint: disable = no-name-in-module
from soundfile import write as sf_write


def remove_uploads() -> None:
    """Remove all files in the uploads folder"""
    for upload in listdir("./uploads/"):
        remove(f"./uploads/{upload}")


def remove_temp_file() -> None:
    """Remove the temporary file"""
    if "tmp.wav" in listdir("./uploads/"):
        remove("./uploads/tmp.wav")


def remove_chunks() -> None:
    """Remove all chunks"""
    if path.exists("./uploads/chunks"):
        rmtree("./uploads/chunks")


def remove_file(filename: str) -> None:
    """Remove a file"""
    if path.exists(filename):
        remove(filename)


def maketempfile_wav(wav_file: str):
    """Make a temporary file for the pitch calculation"""
    temp_data, _ = load(wav_file, sr=16000)  # type: ignore
    if not path.exists("./uploads/"):
        mkdir("./uploads")
    tmp_file = "./uploads/tmp.wav"
    sf_write(tmp_file, temp_data, 16000)  # type: ignore
    return tmp_file


def audio_to_wav(filename: str) -> str:
    """Convert audio-files to wav"""
    temp_data, _ = load(filename, sr=16000)  # type: ignore
    new_file = filename[:-3] + "wav"
    sf_write(new_file, temp_data, 16000)  # type: ignore
    return new_file


if __name__ == "__main__":
    clips_dir = path.join(
        "D:",
        "!Vakken_22_23",
        "Bachelorproef",
        "Bachelorproef",
        "Elderspeak website",
        "Python",
        "Tests",
        "test_clips",
    )
    for filename in listdir(clips_dir):
        audio_to_wav(f"{clips_dir}\\{filename}")
