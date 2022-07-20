from src.BIAnalsysis import BIAnalysis
import sys
import os

if __name__ == '__main__':
    path = sys.argv[1]

    if not os.path.isfile(path) or path.split('.')[1] != 'mfu':
        print("Zly format pliku lub plik nie istnieje")
    else:
        bia = BIAnalysis(path)
        bia.plot_cole_with_radius()
        bia.print_summary()
