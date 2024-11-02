# Use this file to define all your scientific functions (as SNR or BER evaluations)
import numpy as np


def calculate_snr(signal_power, noise_power):
    """Calculate the SNR in dB."""
    return 10 * np.log10(signal_power / noise_power)
