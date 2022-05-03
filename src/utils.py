import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chisquare, pearsonr
from decimal import Decimal
import matplotlib.pyplot as plt

def check_nan(df):
    print(f'Percentage of missing values:\n\n{round(df.isnull().sum().sort_values(ascending=False) / len(df.index) * 100, 2)}\n')

def lin_reg(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x)
    results = model.fit()
    return results.params[1], results.bse[1], results.params[0], results.bse[0]

def corr_coef(x, y, log_x, log_y):
    lin_corr, _ = pearsonr(x, y)
    log_corr, _ = pearsonr(log_x, log_y)
    return lin_corr, log_corr

def chi_sq(x, y, log_x, log_y, m, b):
    try:
      lin_rcs, _ = chisquare(y, x**m * 10**b)
    except ValueError:
      lin_rcs = np.nan
    log_rcs, _ = chisquare(log_y, m * log_x + b)
    return lin_rcs, log_rcs

def make_plot(x, y, m, b, nclass, wavelength, display=False, save=True, clear=True):
    # Make plot
    plt.scatter(x, y, s=10)
    # Visualize linear regression
    X = np.linspace(1e-1, 1e5)
    Y = X**m * 10**b
    plt.plot(X, Y, color='k')
    # Customize plot
    plt.title(f'Flux vs Internal Luminosity')
    plt.xlabel('Internal Luminosity (L$_{sun}$)')
    plt.ylabel('Flux (erg cm$^{-2}$ s$^{-1}$)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(1e-1, 1e5)
    plt.ylim(1e-12, 1e-5)
    plt.legend([f'{Decimal(wavelength):.2e} microns, {nclass}', f'$y = 10^{{{b:.2f}}} \cdot x^{{{m:.2f}}}$'])
    # Miscellaneous
    if display:
        plt.show()
    if save:
        plt.savefig(f'Figures/flux_vs_lint_{nclass}_{Decimal(wavelength):.2e}.eps')
    if clear:
        plt.clf()