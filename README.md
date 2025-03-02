# Easy FIR Filter

A Python library for simplified design of symmetric FIR (Finite Impulse Response) digital filters.

## Description

`easy_fir_filter` provides a high-level interface for designing and calculating FIR filter coefficients based on a user-defined filter configuration. This library focuses on simplicity and usability, allowing researchers, engineers, and signal processing enthusiasts to create optimized FIR filters with ease.

## Features

- Simplified FIR filter design using clear and concise configuration
- Support for different window types, including Kaiser, Hamming, and Blackman
- Automatic calculation of critical parameters such as passband/stopband attenuation
- Optimal filter order determination
- Precise results with configurable rounding control
- Implementation based on solid mathematical principles

## Installation

```bash
pip install easy-fir-filter
```

## Quick Usage

```python
from easy_fir_filter import EasyFirFilter
from easy_fir_filter.types import FilterConf

# Filter configuration
filter_conf: FilterConf = {
    "filter_type": "lowpass",       # Lowpass filter
    "window_type": "kaiser",        # Kaiser window
    "passband_freq_hz": 1000,       # Passband edge at 1000 Hz
    "stopband_freq_hz": 1100,       # Stopband edge at 1100 Hz
    "sampling_freq_hz": 8000,       # 8 kHz sampling rate
    "passband_ripple_db": 1,        # 1 dB ripple in passband
    "stopband_attenuation_db": 60   # 60 dB attenuation in stopband
}

# Create and initialize the filter
fir_filter = EasyFirFilter(filter_conf, round_to=6)

# Calculate filter coefficients
coefficients = fir_filter.calculate_filter()

print(f"FIR filter coefficients: {coefficients}")
```

## Filter Configuration

The filter configuration is defined through a `FilterConf` TypedDict with the following parameters:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `filter_type` | Filter type: "lowpass", "highpass", "bandpass", or "bandstop" | Yes |
| `window_type` | Window type: "kaiser", "hamming", or "blackman" | Yes |
| `passband_freq_hz` | Passband edge frequency in Hz (for lowpass/highpass) or lower passband edge (for bandpass/bandstop) | Yes |
| `stopband_freq_hz` | Stopband edge frequency in Hz (for lowpass/highpass) or lower stopband edge (for bandpass/bandstop) | Yes |
| `sampling_freq_hz` | Sampling frequency of the signal in Hz | Yes |
| `passband_ripple_db` | Maximum allowable passband ripple in decibels (dB) | Yes |
| `stopband_attenuation_db` | Minimum required stopband attenuation in decibels (dB) | Yes |
| `passband_freq2_hz` | Upper passband edge frequency in Hz (required for bandpass/bandstop filters) | For bandpass/bandstop only |
| `stopband_freq2_hz` | Upper stopband edge frequency in Hz (required for bandpass/bandstop filters) | For bandpass/bandstop only |

### Example Configurations

#### Lowpass Filter
```python
lowpass_conf = {
    "filter_type": "lowpass",
    "window_type": "kaiser",
    "passband_freq_hz": 1000,       # Frequencies below 1000 Hz pass
    "stopband_freq_hz": 1200,       # Frequencies above 1200 Hz stop
    "sampling_freq_hz": 8000,       # 8 kHz sampling rate
    "passband_ripple_db": 1,        # 1 dB ripple in passband
    "stopband_attenuation_db": 60   # 60 dB attenuation in stopband
}
```

#### Bandpass Filter
```python
bandpass_conf = {
    "filter_type": "bandpass",
    "window_type": "hamming",
    "passband_freq_hz": 300,        # Lower passband edge
    "passband_freq2_hz": 3400,      # Upper passband edge
    "stopband_freq_hz": 150,        # Lower stopband edge
    "stopband_freq2_hz": 3600,      # Upper stopband edge
    "sampling_freq_hz": 16000,      # 16 kHz sampling rate
    "passband_ripple_db": 1,        # 1 dB ripple in passband
    "stopband_attenuation_db": 50   # 50 dB attenuation in stopband
}
```

## Design Process

The `EasyFirFilter` class implements the following design process:

1. Validation of the filter configuration
2. Calculation of the minimum tolerance (delta) between passband and stopband
3. Calculation of passband ripple and stopband attenuation
4. Determination of the D parameter for the Kaiser window (if used)
5. Calculation of the optimal filter order
6. Generation of impulse response coefficients
7. Application of the selected window
8. Calculation of the final FIR filter coefficients

## Advanced Examples

### Lowpass Filter with Kaiser Window

```python
filter_conf = {
    "filter_type": "lowpass",
    "window_type": "kaiser",
    "passband_freq_hz": 2000,
    "stopband_freq_hz": 2200,
    "sampling_freq_hz": 44100,
    "passband_ripple_db": 0.5,
    "stopband_attenuation_db": 80
}

fir_filter = EasyFirFilter(filter_conf)
coefficients = fir_filter.calculate_filter()
```

### Bandpass Filter with Hamming Window

```python
filter_conf = {
    "filter_type": "bandpass",
    "window_type": "hamming",
    "passband_freq_hz": 300,
    "passband_freq2_hz": 3400,
    "stopband_freq_hz": 150,
    "stopband_freq2_hz": 3600,
    "sampling_freq_hz": 16000,
    "passband_ripple_db": 1,
    "stopband_attenuation_db": 50
}

fir_filter = EasyFirFilter(filter_conf)
coefficients = fir_filter.calculate_filter()
```

## Architecture

The package uses a factory design pattern to create the appropriate filter and window objects:

- `EasyFirFilter`: Main class providing the user interface
- `FilterFactory`: Creates filters and windows based on configuration
- `FilterConfValidator`: Validates the filter configuration
- Specific interfaces for different types of filters and windows

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request or open an Issue to discuss proposed changes.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## Acknowledgements

Some of the filter design techniques used in this package were inspired by:

DeFatta, D. J., Lucas, J. G., & Hodgkiss, W. S. (1988). *Digital Signal Processing: A System Design Approach*. John Wiley & Sons. ISBN: 9780471837886, 0471837881
