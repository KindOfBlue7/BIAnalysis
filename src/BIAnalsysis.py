from typing import Dict, List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import pandas


class BIAnalysis:
    """
    Class for estimating body composition based on Bioelectrical Impedance Analysis.

    Sources:
     - https://nutritionj.biomedcentral.com/articles/10.1186/1475-2891-6-18
     - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7767207/pdf/ijerph-17-09433.pdf
    """
    def __init__(self, file_path: str):
        data = self.read_file(file_path)
        self.height = float(data[2].split(' ')[1])
        self.weight = float(data[3].split(' ')[1])
        self.age = int(data[4].split(' ')[1])
        self.sex = data[5].split(' ')[1]
        self.bmi = self.calculate_bmi()
        self.impedance_data = self.extract_impedance_data(data)
        self.freq, self.react = self.get_freq_react_data()
        self.radius, self.center = self.calculate_radius()
        self.ffm = self.calculate_ffm()
        self.ri, self.re = self.calculate_resistance()
        self.ecw, self.icw, self.tbw = self.calculate_body_water()
        self.summary = self.get_summary()

    def read_file(self, path: str) -> List[str]:
        """
        Reads input file and returns data as list of rows.
        """
        with open(path) as f:
            data = f.read().split('\n')
        
        return data

    def extract_impedance_data(self, data: List[str]) -> List[List[float]]:
        """
        Extracts impedance data as a list of lists of points.
        """
        return [line.split(',') for line in data[13:-1]]

    def calculate_bmi(self) -> float:
        return self.weight/((self.height/100) ** 2)

    def get_freq_react_data(self) -> Tuple[List[float], List[float]]:
        """
        Returns tuple of list: (frequency, reactance).
        """
        freq = []
        react = []
        for sample in self.impedance_data:
            freq.append(float(sample[1]))
            react.append(float(sample[2]))
        return freq, react

    def plot_cole(self) -> None:
        """
        Plots Cole plot from impedance data.
        """
        plt.scatter(self.freq, self.react)
        plt.show()

    def plot_cole_with_radius(self,) -> None:
        """
        Plots Cole plot with calculated optimized radius.
        """
        figure, axes = plt.subplots()
        figure.set_size_inches(10,10)
        plt.scatter(self.freq, self.react)
        draw_circle = plt.Circle(self.center, self.radius, fill=False, color='red')
        axes.set_aspect(1)
        axes.add_artist(draw_circle)
        plt.show()

    def calc_R(self, xc, yc):
        return np.sqrt((self.freq-xc)**2 + (self.react-yc)**2)

    def f_2(self, c):
        Ri = self.calc_R(*c)
        return Ri - Ri.mean()

    def calculate_radius(self) -> Tuple[float, Tuple[float]]:
        """
        Calculates optimal radius of a circle for a cole plot. Returns tuple of
        a radius and a center.
        """
        x_m = np.mean(self.freq)
        center_estimate = x_m, 0.0
        center, ier = optimize.leastsq(self.f_2, center_estimate)
        Ri = self.calc_R(*center)
        R = np.mean(Ri)
        return R, center

    def calculate_ffm(self) -> float:
        """
        Calculates Fat Free Mass.
        """
        FFM = []
        for i in range(len(self.freq)):
            FFM_i = 0.7374 * (self.height ** 2) / self.freq[i]
            FFM_i += 0.1763 * self.weight
            FFM_i -= 0.1773 * self.age
            FFM_i += 0.1198 * self.react[i]
            FFM_i -= 2.4658
            FFM.append(FFM_i)

        return np.mean(FFM)

    def calculate_resistance(self) -> Tuple[float]:
        """
        Calculates intracellular and extracellular resistance.
        """
        a = self.center[0]
        b = self.center[1]
        r = self.radius
        x2 = np.sqrt((r ** 2) - (b ** 2)) + a
        x1 = -np.sqrt((r ** 2) - (b ** 2)) + a
        Re = x2
        Ri = (x1*Re)/(Re - x1)
        return Ri, Re

    def calculate_body_water(self) -> Tuple[float, float, float]:
        """
        Calculates extracellular, intracellular and total body water.
        """
        k_ecw = 0.188/self.bmi + 0.2883
        k_icw = 5.8758/self.bmi + 0.4194
        ecw = k_ecw * np.power((self.height ** 2 * np.sqrt(self.weight))/self.re, 2/3)
        icw = k_icw * np.power((self.height ** 2 * np.sqrt(self.weight))/self.ri, 2/3)
        tbw = ecw + icw
        return ecw, icw, tbw
    
    def get_summary(self) -> Dict:
        """
        Returns dict with measured and calculated values.
        """
        return dict(
            height=self.height,
            weight=self.weight,
            age=self.age,
            sex=self.sex,
            bmi=self.bmi,
            ri=self.ri,
            re=self.re,
            ffm=self.ffm,
            ecw=self.ecw,
            icw=self.icw,
            tbw=self.tbw
        )

    def export_analysis_file(self, output_filename: str) -> None:
        """
        Exports analysis as a json file.
        """
        pass

    def print_summary(self) -> None:
        """
        Prints summary.
        """
        print('{:25s} {:.3f}'.format('Wzrost', self.height))
        print('{:25s} {:.3f}'.format('Waga', self.weight))
        print('{:25s} {:.3f}'.format('Wiek', self.age))
        print('{:25s} {:s}'.format('Plec', self.sex))
        print('{:25s} {:.3f}'.format('BMI', self.bmi))
        print('{:25s} {:.3f}'.format('Rezystancja Re', self.re))
        print('{:25s} {:.3f}'.format('Rezystancja Ri', self.ri))
        print('{:25s} {:.3f}'.format('Masa beztluszczowa', self.ffm))
        print('{:25s} {:.3f}'.format('Plyn pozakomorkowy', self.ecw))
        print('{:25s} {:.3f}'.format('Plyn wewnatrzkomorkowy', self.icw))
        print('{:25s} {:.3f}'.format('Calkowita zawartosc plynu', self.tbw))
