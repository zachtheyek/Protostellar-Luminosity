import numpy as np
import statsmodels.api as sm
from scipy.stats import chisquare, pearsonr

def check_nan(df):
    print(f'Percentage of missing values in each column:\n\n{round(df.isnull().sum().sort_values(ascending=False) / len(df.index) * 100, 2)}\n')

def lin_reg(x, y):
    x = sm.add_constant(x)
    # Fit linear regression
    model = sm.OLS(y, x)
    # Compute linear coefficients
    results = model.fit()
    # Return slope, unc_slope, intercept, unc_intercept
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

def make_legend(df, wavelength, ax):
    # Map class to subplot position
    class_map = {'0': (0, 0), 
                 '1a': (0, 1), 
                 '1b': (1, 0), 
                 'All': (1, 1)}
    # Repeat the following process for all 4 subplots
    for class_name in class_map:
        # Partition data based on class
        if class_name == 'All':
            x, y = df['L_int (Lsun)'], df['Flux (erg cm^-2 s^-1)']
            log_x, log_y = df['log(L_int)'], df['log(Flux)']
        else:
            x, y = df[df['Class'] == class_name]['L_int (Lsun)'], df[df['Class'] == class_name]['Flux (erg cm^-2 s^-1)']
            log_x, log_y = df[df['Class'] == class_name]['log(L_int)'], df[df['Class'] == class_name]['log(Flux)']
        # Compute relevant metrics
        m, unc_m, b, unc_b = lin_reg(x, y)
        lin_rcs, log_rcs = chi_sq(x, y, log_x, log_y, m, b)
        lin_corr, log_corr = corr_coef(x, y, log_x, log_y)
        # Write results
        with open('../data/lin_coef.csv', 'a') as coef, open('../data/corr_coef.csv', 'a') as corr:
            coef.write(f'{class_name}, {wavelength}, {m}, {unc_m}, {b}, {unc_b}\n')
            corr.write(f'{class_name}, {wavelength}, {lin_rcs}, {log_rcs}, {lin_corr}, {log_corr}\n')
        # Make legend
        row, col = class_map[class_name]
        ax[row][col].legend([f'$F = L^{{{m:.2f}\pm{unc_m:.2f}}} \cdot 10^{{{b:.2f}\pm{unc_b:.2f}}}$'], loc='best')