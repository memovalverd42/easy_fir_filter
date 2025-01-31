"""
This file contains the definitions of fir filter types.
"""

from typing import TypedDict, Literal, NotRequired

FilterType = Literal["stopband", "lowpass", "highpass", "passband"]
FilterWindow = Literal["hamming", "blackman", "kaiser"]


class FilterConf(TypedDict):
    """
    This class represents the configuration of a digital FIR filter.
    """

    filter_type: FilterType
    """Type of filter (e.g., lowpass, highpass, bandpass, bandstop)."""

    window_type: FilterWindow
    """Type of window used for filter design (e.g., Hamming, Hamming, Blackman)."""

    passband_ripple_db: float  # Ap
    """Maximum allowable passband ripple in decibels (dB)."""

    stopband_attenuation_db: float  # As
    """Minimum required stopband attenuation in decibels (dB)."""

    passband_freq_hz: float  # fp
    """Passband edge frequency in Hz (for lowpass/highpass) or lower passband edge (for passband/stopband)."""

    stopband_freq_hz: float  # fs
    """Stopband edge frequency in Hz (for lowpass/highpass) or lower stopband edge (for passband/stopband)."""

    sampling_freq_hz: float  # F
    """Sampling frequency of the signal in Hz."""

    stopband_freq2_hz: NotRequired[float]  # fs2
    """Upper stopband edge frequency in Hz (required for passband/stopband filters)."""

    passband_freq2_hz: NotRequired[float]  # fp2
    """Upper passband edge frequency in Hz (required for passband/stopband filters)."""
