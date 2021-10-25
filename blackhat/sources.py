import numpy as np
import celerite2 as clt2
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from astropy.stats import biweight_location

from .telescopes import get_central_wavelength, get_passband_plot_color, get_passband_plot_marker

def apply_mapping(df, new_column, mapped_column, map_func):

    df[new_column] = df[mapped_column].map(map_func)

    return df


class BG_Source:

    """
    This is a BlackGEM source with the associated catalog and telescope
    metadata, observations, as well as the associated class probabilities.

    All inputs need to be dict-like objects or panda DataFrames



    observations : pandas.DataFrame
        Observations of the object's light curve. This should be a pandas
        DataFrame with at least the following columns:

        - time: The time of each observation.
        - band: The band used for the observation.
        - flux: The measured flux value of the observation.
        - flux_error: The flux measurement uncertainty of the observation.

    """
    def __init__(self, source_metadata, telescope_metadata,
                 observations, class_probabilities, central_wvl_method='mean'):
        self.source_metadata = source_metadata
        self.telescope_metadata = telescope_metadata
        self.obs = observations
        self.class_probabilities = class_probabilities
        self.central_wvl_method = central_wvl_method

        self._default_kernel = 'Matern32Kernel'
        self.condidtion_GP = None
        self.kernel_parameters = None

        self.wavelength_scale = 4500. # Aangstrom


    # def __repr__(self):
    #     return f"{type(self).__name__}(object_id={self.metadata['object_id']})"

    @property
    def passbands(self):
        """
        Returns a dictionary containing the unique passbands that we have
        observations for, the central wavelength per passband, as well as the
        number of observations per passband.


        """

        unique_passbands = sorted(self.obs['passband'].unique())

        passband_dict = {'{}'.format(passband): {'nobs': self.get_nobs(passband),
                       'wavelength_center': get_central_wavelength(passband,
                       self.central_wvl_method), 'marker': get_passband_plot_marker(passband),
                       'color': get_passband_plot_color(passband) }
                       for passband in unique_passbands }

        return passband_dict


    def get_passband_to_wavelength_mapping(self):
        """
        This function creates the mapping from passband to wavelength that we
        will apply to our observations for the 2-D GP.
        """
        return { passband: self.passbands[passband]['wavelength_center'] for passband
                 in passbands}

    def prepare_observations(self):

        try:
            prepped_obs = apply_mapping(self.obs, 'wavelength', 'passband',
                                        self.get_passband_to_wavelength_mapping())
            self.obs = prepped_obs
            return True

        except:
            return False


    def get_nobs(self, passband):
        """
        Function to return the number of observations for this source in a
        given passband.
        """

        return (self.obs.where(self.obs['passband']==passband).dropna()).flux.size


    def update_gp(self, scale_obs, length_scale_obs, scale_wvl, replace=True):

        """
        Updates the GP. Checks if a conditioned GP already exists and returns
        either the existing or updated GP.
        """

        if self.conditioned_GP is None:
            gp_, gp_parameters = self.condition_GP()
            self.conditioned_GP = gp_
            self.kernel_parameters = gp_parameters
        else:
            if replace:
                gp_, gp_parameters = self.condition_GP()
                self.conditioned_GP = gp_
                self.kernel_parameters = gp_parameters
            else:
                print('Kernel has already been conditioned')

        return self.condidtion_GP, self.kernel_parameters

    def conditione_GP(self, scale_obs, length_scale_obs, scale_wvl):

        y = self.obs['flux']
        y_err = self.obs['flux_error']
        wvls = self.obs['passband'].map()


    def plot_obs(self, ax=None):

        x_min = self.obs.mjd.min() - 10.
        x_max = self.obs.mjd.max() + 10.

        if ax is None:
            fig, ax = plt.subplots(1,1, figsize=(6.6957, 6.6957))

        for ii, passband in enumerate(self.passbands):
            obs_per_passband = self.obs.where(self.obs.passband==passband).dropna()
            ax.errorbar( obs_per_passband.mjd, y=obs_per_passband.flux,
                         yerr=obs_per_passband.flux_error,
                         fmt=self.passbands[passband]['marker'],
                         c=self.passbands[passband]['color'], label=passband)

        ax.set_xlabel(r'${\rm MJD~[d]}$', fontsize=14)
        ax.set_ylabel(r'${\rm Instrumental~Flux}$', fontsize=14)
        ax.set_xlim(x_min, x_max)
        ax.legend()
        ax.figure.tight_layout()
