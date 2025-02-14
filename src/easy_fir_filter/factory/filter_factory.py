"""
This file contains the implementation of the FilterFactory class.
"""

from easy_fir_filter.interfaces.filter_interface import IFilter
from easy_fir_filter.interfaces.window_interface import IWindow
from easy_fir_filter.types.fir_filter_conf import FilterConf, FilterWindow


class FilterFactory:
    """
    Factory class to create different filter and window instances.
    """

    _FILTERS = {
        "lowpass": "easy_fir_filter.filters.lowpass_filter.LowpassFilter",
        "highpass": "easy_fir_filter.filters.highpass_filter.HighpassFilter",
        "bandstop": "easy_fir_filter.filters.bandstop_filter.BandstopFilter",
        "bandpass": "easy_fir_filter.filters.bandpass_filter.BandpassFilter",
    }

    _WINDOWS = {
        "hamming": "easy_fir_filter.windows.hamming_window.HammingWindow",
        "blackman": "easy_fir_filter.windows.blackman_window.BlackmanWindow",
        "kaiser": "easy_fir_filter.windows.kaiser_window.KaiserWindow",
    }

    @staticmethod
    def create_filter(filter_conf: FilterConf, round_to: int = 4) -> IFilter:
        """
        Creates and returns the appropriate filter based on the filter type.

        Args:
            filter_conf (FilterConf): Configuration containing:
                - filter_type (str): The type of filter to create ('lowpass', 'highpass').
                - sampling_freq_hz (float): Sampling frequency in Hz.
                - passband_freq_hz (float): Passband frequency in Hz.
                - stopband_freq_hz (float): Stopband frequency in Hz.
            round_to (int, optional): Number of decimal places for rounding the filter coefficients. Defaults to 4.

        Returns:
            IFilter: The created filter instance.

        Raises:
            ValueError: If an invalid filter type is provided.
        """
        filter_type = filter_conf.get("filter_type")

        if filter_type not in FilterFactory._FILTERS:
            raise ValueError(f"Invalid filter type '{filter_type}' provided.")

        filter_class = FilterFactory._FILTERS[filter_type]
        module_path, class_name = filter_class.rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        filter_cls = getattr(module, class_name)

        return filter_cls(filter_conf, round_to)

    @staticmethod
    def create_window(window: FilterWindow, round_to: int = 4) -> IWindow:
        """
        Creates and returns the appropriate window instance based on the window type.

        Args:
            window (FilterWindow): Configuration containing the window type.
            round_to (int, optional): Number of decimal places for rounding the window coefficients. Defaults to 4.

        Returns:
            IWindow: The created window instance.

        Raises:
            ValueError: If an invalid window type is provided.
        """
        if window not in FilterFactory._WINDOWS:
            raise ValueError(f"Invalid window type '{window}' provided.")

        window_class = FilterFactory._WINDOWS[window]
        module_path, class_name = window_class.rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        window_cls = getattr(module, class_name)

        return window_cls(round_to)
