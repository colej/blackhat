"""
Instrument specific definitions for central wavelengths / plotting features


"""

import yaml



def get_central_wavelength(passband, method):
    """
    Return the central wavelength for a given band.

    Parameters
    ----------
    band : str
        The name of the band to use.
    method: str
        The name of the  method used to calculate the central wavelength
    """
    with open('/lhome/colej/python/blackhat/passbands.yaml', 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader)
    f.close()


    if passband in cfg:
        if method in cfg[passband]:
            return cfg[passband][method]
    #     else:
    #         raise Exception('Method used to calculate the central wavelength'
    #                         'is not known')
    # else:
    #     raise Exception(
    #         "Central wavelength unknown for band %s. Add it to "
    #         "avocado.instruments.band_central_wavelengths." % band
    #         )

def get_passband_plot_color(passband):
    with open('/lhome/colej/python/blackhat/passbands.yaml', 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader)
    f.close()

    if passband in cfg:
        return cfg[passband]['color']

def get_passband_plot_marker(passband):
    with open('/lhome/colej/python/blackhat/passbands.yaml', 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader)
    f.close()

    if passband in cfg:
        return cfg[passband]['marker']
