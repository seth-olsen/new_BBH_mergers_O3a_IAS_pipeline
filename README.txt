########################################################################
##  Seth Olsen - srolsen@princeton.edu
##  (last update: January 4, 2022)
########################################################################

  ----    New binary black hole (BBH) mergers in the O3a data    ----

This repository contains parameter estimation (PE) posteriors for the
ten new BBH merger events found in the LIGO--Virgo collaboration (LVC)
data from the first half of the third observing run (O3a) using the
IAS pipeline (described in doi:10.1103/PhysRevD.100.023011 and
doi:10.1103/PhysRevD.101.083030). These results are presented in
arXiv:####.#### (please cite this paper if using samples).

The parameters included in the feather files
<prior>/<evname>_posterior_samples.feather
are defined below.


# names for each parameter that are recognized by labelling system
param_names = {'mchirp': 'Detector Frame Chirp Mass',
               'q': 'Mass Ratio',
               'q1': 'Inverse Mass Ratio',
               'chieff': 'Effective Spin',
               'chip': 'In-Plane Spin Measure',
               'eta': 'Symmetric Mass Ratio',
               'm1': 'Detector Frame Larger Mass',
               'm2': 'Detector Frame Smaller Mass',
               'mtot': 'Detector Frame Total Mass',
               'm1_source': 'Source Frame Larger Mass',
               'm2_source': 'Source Frame Smaller Mass',
               'mtot_source': 'Source Frame Total Mass',
               'mchirp_source': 'Source Frame Chirp Mass',
               'd_luminosity': 'Luminosity Distance',
               'd_comoving': 'Comoving Distance',
               'd_hat': 'Effective Distance Over Chirp Mass',
               'z': 'Redshift',
               's1': 'Spin Magnitude of Larger Mass',
               's2': 'Spin Magnitude of Smaller Mass',
               's1theta': 'Spin Tilt of Larger Mass',
               's2theta': 'Spin Tilt of Smaller Mass',
               's1costheta': 'Spin Tilt Cosine of Larger Mass',
               's2costheta': 'Spin Tilt Cosine of Smaller Mass',
               's1phi': 'Spin Azimuth of Larger Mass',
               's2phi': 'Spin Azimuth of Smaller Mass',
               's1x': '(Dimensionless) Spin X-Component of Larger Mass',
               's1y': '(Dimensionless) Spin Y-Component of Larger Mass',
               's1z': '(Dimensionless) Spin Z-Component of Larger Mass',
               's2x': '(Dimensionless) Spin X-Component of Smaller Mass',
               's2y': '(Dimensionless) Spin Y-Component of Smaller Mass',
               's2z': '(Dimensionless) Spin Z-Component of Smaller Mass',
               'ra': 'Right Ascension',
               'dec': 'Declination',
               'psi': 'Polarization Phase',
               'vphi': 'Orbital Phase',
               'cosiota': 'Inclination Cosine',
               'iota': 'Inclination',
               'lnq': 'Log Mass Ratio',
               't_geocenter': 'Geocenter Time',
               'tgps': 'GPS Time',
               'lnl': 'Log Likelihood',
               'lnl_aux_H': 'Hanford Log Likelihood (Stationary Noise)',
               'lnl_aux_L': 'Livingston Log Likelihood (Stationary Noise)',
               'lnl_aux_V': 'Virgo Log Likelihood (Stationary Noise)',
               'lnPrior': 'Log Prior',
               'fplus_H': 'Hanford Antenna Plus',
               'fplus_L': 'Livingston Antenna Plus',
               'fplus_V': 'Virgo Antenna Plus',
               'fcross_H': 'Hanford Antenna Cross',
               'fcross_L': 'Livingston Antenna Cross',
               'fcross_V': 'Virgo Antenna Cross',
               'antenna_H': 'Hanford Antenna Response',
               'antenna_L': 'Livingston Antenna Response',
               'antenna_V': 'Virgo Antenna Response'}
               
