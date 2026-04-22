import numpy as np
from scipy.ndimage import gaussian_filter1d


class Modulator:
    def __init__(self, sampling_rate=2000):
        self.sampling_rate = sampling_rate

    def get_time(self, data):
        return np.linspace(0, len(data), len(data) * self.sampling_rate,
                           endpoint=False)

    def smooth_data(self, data):
        repeated = np.repeat(data, self.sampling_rate)
        return gaussian_filter1d(repeated.astype(float),
                                 sigma=self.sampling_rate/20)

    def add_noise(self, signal, snr_db):
        if snr_db >= 100:
            return signal
        signal_power = np.mean(signal**2)
        noise_power = signal_power / (10**(snr_db / 10))
        noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
        return signal + noise

# modulation schemes
class ASKModulator(Modulator):
    def modulate(self, data, carrier_freq=5, snr=100):
        t = self.get_time(data)
        carrier = np.sin(2 * np.pi * carrier_freq * t)
        modulated = self.smooth_data(data) * carrier
        return t, self.add_noise(modulated, snr)


class FSKModulator(Modulator):
    def modulate(self, data, freq1=5, freq2=15, snr=100):
        t = self.get_time(data)
        f_array = freq1 + (freq2 - freq1) * self.smooth_data(data)
        modulated = np.sin(2 * np.pi * f_array * t)
        return t, self.add_noise(modulated, snr)


class PSKModulator(Modulator):
    def modulate(self, data, carrier_freq=5, snr=100):
        t = self.get_time(data)
        phase = np.pi * self.smooth_data(data)
        modulated = np.sin(2 * np.pi * carrier_freq * t + phase)
        return t, self.add_noise(modulated, snr)

# same as above but with amplitude parameter for more control over signal
# class FSKModulator(Modulator):
#     def modulate(self, data, freq1=5, freq2=15, snr=100, amplitude=1.0):
#         t = self.get_time(data)
#         f_array = freq1 + (freq2 - freq1) * self.smooth_data(data)
#         modulated = amplitude * np.sin(2 * np.pi * f_array * t)
#         return t, self.add_noise(modulated, snr)
#
#
# class PSKModulator(Modulator):
#     def modulate(self, data, carrier_freq=5, snr=100, amplitude=1.0):
#         t = self.get_time(data)
#         phase = np.pi * self.smooth_data(data)
#         modulated = amplitude * np.sin(2 * np.pi * carrier_freq * t + phase)
#         return t, self.add_noise(modulated, snr)
