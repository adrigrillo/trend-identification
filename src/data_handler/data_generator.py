import random
import numpy as np

from src.data_handler.data_handler import generate_synthetic_data, create_function_file


def generate_with_name(file_name: str, num_files: int):
    for i in range(num_files):
        name = f'/{file_name}_{str(i + 1)}.ini'
        generate_synthetic_data('function', name)


# Generate time series with trend, seasonality and noise
def generate_data(name: str = 'time_series_',
                  poly_max_degree: int = 3,
                  poly_slope_steps: int = 5,
                  data_points: int = 300,
                  sig_noise_ratio: list = np.linspace(0,3,10),
                  seasonalities: list = ['np.sin(y)', 'np.sin(3*y)+2*np.cos(y)']):

    # Alternatives for seasonalities, with 3 components increasing in frequency and decreasing in amplitude.
    seasonalities: list = [ 'np.random.uniform(size=1)*1*np.sin((y*2*np.pi)*(np.random.uniform(size=1)*10+1)+(np.random.uniform(size=1)*2*np.pi))'\
                            + '+np.random.uniform(size=1)*0.5*np.sin((y*2*np.pi)*(np.random.uniform(size=1)*20+1)+(np.random.uniform(size=1)*2*np.pi))'\
                            + '+np.random.uniform(size=1)*0.25*np.sin((y*2*np.pi)*(np.random.uniform(size=1)*50+1)+(np.random.uniform(size=1)*2*np.pi))' \
                            for x in range(10) ]

    # generate trend functions:
    # 12 structures
    trend_structures: list = [
        'a*x**0',
        'a*x**1',
        'a*x**2',
        'a*x**3',
        'a*(x+1)**-3',
        'a*x**(1/2)',
        'a*x**(1/3)',
        'a*x**3 - a*x**2',
        'a*x**5 - a*x**2 + a*x',
        'a*np.sin((x*2*np.pi)/(b*2+1) + c*np.pi)',
        'a*5**x'
    ]

    trends: list = np.empty([0, len(trend_structures)])

    coefficients = np.empty([0, 3])

    # This is done to remember what random values were set for the coefficients.
    for i in range(10):
        a, b, c = np.random.uniform(),  np.random.uniform(),  np.random.uniform()

        # Add coefficients
        trend_set = np.copy(trend_structures)
        trend_set = np.core.defchararray.replace(trend_set, 'a', str(a))
        trend_set = np.core.defchararray.replace(trend_set, 'b', str(b))
        trend_set = np.core.defchararray.replace(trend_set, 'c', str(c))

        trends = np.append(trends, [trend_set], axis=0)

        coefficients = np.append(coefficients, [[a, b, c]], axis=0)

    index = 0
    for i in range(len(trends)):
        for noise in sig_noise_ratio:
            for seasonality in seasonalities:

                for j in range(len(trends[i])):

                    trend = trends[i][j]
                    index += 1
                    # create .ini function file
                    create_function_file(name + str(index), trend, data_points, noise, seasonality, coefficients[i], trend_structures[j])
                    # create .csv data file
                    generate_synthetic_data('function', name + str(index) + '.ini')


if __name__ == '__main__':
    generate_data()
    #generate_with_name('func', 5)
