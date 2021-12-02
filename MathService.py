import io
import base64
import numpy as np
import matplotlib.pyplot as plt

from dto import FloatingFreqDto, GraphsDto, CalculatedGraphsDto, ImageDto, MainImageDto


class MathService:

    def __get_first_lower(self, collection, x):
        for i, item in enumerate(collection):
            if item < x:
                return i, item
        return len(collection) - 1, collection[-1]

    def __get_sliced_array(self, collection, x):
        return collection[:self.__get_first_lower(collection, x)[0]]

    def __calculate_forward_fft(self, x, y):
        diff = (x[-1] - x[0])
        return np.fft.rfftfreq(len(y), diff / len(x)), np.fft.rfft(y)

    def __get_graphic_b64(self, x, y):
        plt.plot(x, y)
        bytes_to_save = io.BytesIO()
        plt.savefig(bytes_to_save, format='jpg')
        bytes_to_save.seek(0)
        b64_plot = base64.b64encode(bytes_to_save.read())
        plt.clf()
        return b64_plot.decode('utf-8')

    def fourier(self, dto: GraphsDto):
        data = list(map(lambda x: list(map(lambda y: float(y), x.split(','))),
                        dto.file.read().decode('utf-8').strip().split('\n')))

        x, y = np.array(data).T

        freqs, four_vals = self.__calculate_forward_fft(x, y)

        yf = np.fft.irfft(four_vals)

        spec1_b64 = self.__get_graphic_b64(freqs, np.abs(four_vals) / len(x))

        spec2_b64 = self.__get_graphic_b64(freqs, np.abs(four_vals) / len(x))

        source_b64 = self.__get_graphic_b64(x, y)

        target_b64 = self.__get_graphic_b64(x, yf)

        dispersion = ((yf - y) ** 2 / len(y)).sum()

        return CalculatedGraphsDto(MainImageDto('Спектрограмма разложения',
                                                'data:image/png;base64,' + spec1_b64,
                                                min(freqs),
                                                max(freqs),
                                                (freqs[-1] - freqs[0]) / 10),
                                   ImageDto('Спектрограмма разложения', 'data:image/png;base64,' + spec2_b64),
                                   ImageDto('Изначальный сигнал', 'data:image/png;base64,' + source_b64),
                                   ImageDto('Восстановленный сигнал', 'data:image/png;base64,' + target_b64),
                                   [x.tolist(), y.tolist(), freqs.tolist(), list(map(str, four_vals))],
                                   dispersion)

    def create_graphs(self, dto: GraphsDto):
        if dto.transformType == 'fourier':
            return self.fourier(dto)
        raise Exception("Not implemented yet")

    def create_cutted_graphs(self, dto: FloatingFreqDto):
        x, y, freqs, four_vals = dto.values

        four_vals = np.array(list(map(complex, four_vals)))
        four_vals = self.__get_sliced_array(four_vals, dto.maxFrequency)

        yf = np.fft.irfft(four_vals)

        spec1_b64 = self.__get_graphic_b64([], [])

        spec2_b64 = self.__get_graphic_b64(freqs, np.abs(four_vals) / len(freqs))

        source_b64 = self.__get_graphic_b64([], [])

        target_b64 = self.__get_graphic_b64(x, yf)

        dispersion = ((yf - y) ** 2 / len(y)).sum()

        return CalculatedGraphsDto(MainImageDto('Спектрограмма разложения',
                                                'data:image/png;base64,' + spec1_b64,
                                                min(freqs),
                                                max(freqs),
                                                (freqs[-1] - freqs[0]) / 10),
                                   ImageDto('Результат обрезания частот (спектрограмма)',
                                            'data:image/png;base64,' + spec2_b64),
                                   ImageDto('Изначальный сигнал', 'data:image/png;base64,' + source_b64),
                                   ImageDto('Восстановленный сигнал (с обрезанными частотами)',
                                            'data:image/png;base64,' + target_b64),
                                   [x, y, freqs, list(map(str, four_vals))],
                                   dispersion)
