"""Module for audio preprocessing"""

from typing import Any
import numpy as np
import noisereduce as nr
import librosa
import soundfile as sf
import pydub


def get_silence_mask(samples: np.ndarray, threshold: float) -> np.ndarray:
    """Get the mask for the silence"""
    return np.abs(samples) > threshold


def remove_silence(samples: np.ndarray, threshold: float) -> np.ndarray:
    """Remove silence"""
    return samples[get_silence_mask(samples, threshold)]


def remove_voice_original(
        original: np.ndarray, filtered: np.ndarray, threshold: float
) -> np.ndarray:
    """Remove voice"""
    return original[~get_silence_mask(filtered, threshold)]


def get_base_noise(samples: np.ndarray, sample_rate: int) -> np.ndarray:
    """Get the base noise"""
    filtered = nr.reduce_noise(
        y=samples, sr=sample_rate, prop_decrease=0.95, stationary=False
    )
    threshold = float(np.average(np.abs(filtered)) / 100)
    return remove_voice_original(samples, filtered, threshold=threshold)


def process_audio(
        samples: np.ndarray, sample_rate: int, noise: np.ndarray
) -> np.ndarray:
    """Process the audio to remove noise and silence"""
    samples_denoised_static = nr.reduce_noise(
        y=samples, sr=sample_rate, y_noise=noise, stationary=True
    )
    threshold = float(np.average(np.abs(samples_denoised_static)) / 100)
    samples_denoised_static = remove_silence(
        samples_denoised_static, threshold=threshold
    )
    return samples_denoised_static


def get_noise_profile(
        elder_samples: np.ndarray, sample_rate: int
) -> np.ndarray:
    """Get the noise profile"""
    noise_elder = get_base_noise(elder_samples, sample_rate)
    return noise_elder


def preprocess_audio(elder_samples: np.ndarray, sample_rate: int
                     ) -> np.ndarray:
    """Preprocess the audio"""
    noise = get_noise_profile(elder_samples, sample_rate)
    elder_samples = process_audio(elder_samples, sample_rate, noise)
    return elder_samples


def get_silence_stats(original, filtered, sample_rate):
    """Get the silence stats"""
    original_length = len(original) / sample_rate
    filtered_length = len(filtered) / sample_rate
    silence_length = original_length - filtered_length
    silence_percentage = silence_length / original_length * 100

    return {
        "original_length": round(original_length, 1),
        "filtered_length": round(filtered_length, 1),
        "silence_length": round(silence_length, 1),
        "silence_percentage": round(silence_percentage, 2),
    }


def low_pass_filter(filename: str):
    """Apply low pass filter"""
    audio = pydub.AudioSegment.from_wav(filename)
    audio = audio.low_pass_filter(1000)
    audio.export(filename, format="wav")


def remove_noise_from_files(file_elder: str) -> dict[str, Any]:
    """Remove noise from the files"""
    low_pass_filter(file_elder)

    elder_samples, sample_rate = librosa.load(file_elder)

    elder_samples_post = preprocess_audio(
        elder_samples, int(sample_rate)
    )

    sf.write(file_elder, elder_samples_post, int(sample_rate))

    silence_stats_elder = get_silence_stats(
        elder_samples, elder_samples_post, sample_rate=sample_rate
    )

    return {
        "elder": silence_stats_elder,
    }
