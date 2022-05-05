import numpy as np
import statsmodels.api as sm
from scipy.stats import chisquare, pearsonr
import matplotlib.pyplot as plt
from decimal import Decimal

def check_nan(df):
    print(f'Percentage of missing values in each column:\n\n{round(df.isnull().sum().sort_values(ascending=False) / len(df.index) * 100, 2)}\n')

def lin_reg(x, y):
    x = sm.add_constant(x)
    # Fit linear regression
    model = sm.OLS(y, x)
    # Compute linear coefficients
    results = model.fit()
    return results.params[1], results.bse[1], results.params[0], results.bse[0]

def chi_sq(x, y, log_x, log_y, m, b):
    # Compute reduced-chi squared (linear space)
    try:
      lin_rcs, _ = chisquare(y, x**m * 10**b)
    except ValueError:
      lin_rcs = np.nan
    # Compute reduced-chi squared (log10 space)
    log_rcs, _ = chisquare(log_y, m * log_x + b)
    return lin_rcs, log_rcs

def corr_coef(x, y, log_x, log_y):
    # Compute correlation coefficient (linear space)
    lin_corr, _ = pearsonr(x, y)
    # Compute correlation coefficient (log10 space)
    log_corr, _ = pearsonr(log_x, log_y)
    return lin_corr, log_corr

def make_plot(x, y, log_x, log_y, nclass, wavelength, display=False, write=True, save=True, clear=True):
    # Make plot
    plt.scatter(x, y, s=10)
    # Customize plot
    plt.title(f'Flux vs Internal Luminosity: Class {nclass}')
    plt.xlabel('Internal Luminosity (L$_{sun}$)')
    plt.ylabel('Flux (erg cm$^{-2}$ s$^{-1}$)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(1e-1, 1e5)
    plt.ylim(1e-12, 1e-5)
    # Compute linear coefficients
    m, b, unc_m, unc_b = lin_reg(x, y)
    # Evaluate goodness-of-fit via reduced-chi squared
    lin_rcs, log_rcs = chi_sq(x, y, log_x, log_y, m, b)
    # Calculate correlation coefficients
    lin_corr, log_corr = corr_coef(x, y, log_x, log_y)
    # Visualize linear regression
    X = np.linspace(1e-1, 1e5)
    Y = X**m * 10**b
    plt.plot(X, Y, color='k')
    if wavelength == 'All':
        plt.legend([f'All wavelengths', f'$F = 10^{{{b:.2f}}} \cdot L^{{{m:.2f}}}$'])
    else:
        plt.legend([f'{Decimal(wavelength):.2e} microns', f'$F = 10^{{{b:.2f}}} \cdot L^{{{m:.2f}}}$'])
    # Miscellaneous
    if display:
        # Display plot
        plt.show()
    if write:
        # Record linear and correlation coefficients 
        with open('../data/lin_coef.csv', 'a') as coef, open('../data/corr_coef.csv', 'a') as corr:
            coef.write(f'{nclass}, {wavelength}, {m}, {unc_m}, {b}, {unc_b}\n')
            corr.write(f'{nclass}, {wavelength}, {lin_rcs}, {log_rcs}, {lin_corr}, {log_corr}\n')
        coef.close()
        corr.close()
    if save:
        # Save plot
        if nclass == '0 & 1' and wavelength == 'All':
            plt.savefig(f'../data/Figures/flux_vs_lint_0n1_master.eps')
        elif nclass == '0 & 1' and wavelength != 'All':
            plt.savefig(f'../data/Figures/flux_vs_lint_0n1_{Decimal(wavelength):.2e}.eps')
        elif nclass != '0 & 1' and wavelength == 'All':
            plt.savefig(f'../data/Figures/flux_vs_lint_{nclass}_master.eps')
        else:
            plt.savefig(f'../data/Figures/flux_vs_lint_{nclass}_{Decimal(wavelength):.2e}.eps')
    if clear:
        # Clear plot
        plt.clf()