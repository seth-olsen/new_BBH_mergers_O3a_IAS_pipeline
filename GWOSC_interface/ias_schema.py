"""Interface IAS catalog with GWOSC schema."""

import inspect
import json
from pathlib import Path
import numpy as np
import pandas as pd

import schema


REPO_URL = \
    'https://github.com/seth-olsen/new_BBH_mergers_O3a_IAS_pipeline/tree/main'
CATALOG_NAME = 'IAS-O3a'
CATALOG_DESCRIPTION = inspect.cleandoc("""
    We report the detection of ten new binary black hole (BBH) mergers in the
    publicly released data from the the first half of the third observing run
    (O3a) of advanced LIGO and advanced Virgo. We identify candidates using an
    updated version of the IAS search pipeline and compile a catalog of signals
    that pass a significance threshold of astrophysical probability greater
    than 0.5 (following the GWTC-2.1 and 3-OGC catalogs). The updated IAS
    pipeline is sensitive to a larger region of parameter space, applies a
    template prior that accounts for different search volume as a function of
    intrinsic parameters, and uses an improved coherent detection statistic
    that optimally combines the data from the Hanford and Livingston detectors.
    Among the ten new events, we observe interesting astrophysical scenarios
    including sources with confidently large effective spin parameters in both
    the positive and negative directions, high-mass black holes that are
    difficult to form in stellar collapse models due to (pulsational) pair
    instability, and low-mass mergers that bridge the gap between neutron stars
    and the lightest observed black holes. We infer source parameters in the
    upper and lower black hole mass gaps with both extreme and near-unity mass
    ratios, and one of the possible neutron star--black hole mergers is well
    localized for electromagnetic counterpart searches. We detect all of the
    GWTC-2.1 BBH mergers with coincident data in Hanford and Livingston except
    for three loud events that get vetoed, which is compatible with the
    false-positive rate of our veto procedure, and three that fall below the
    detection threshold. We also return to significance the event
    GW190909_114149, which was reduced to a sub-threshold trigger after its
    initial appearance in GWTC-2. This amounts to a total of 42 BBH mergers
    detected by our pipeline's search of the coincident Hanford--Livingston O3a
    data.
    """).replace('\n', ' ')
DOI = 'https://doi.org/10.1103/PhysRevD.106.043009'

TOPDIR = Path(__file__).parents[1]
WAVEFORM_FAMILY = 'IMRPhenomXPHM'

PRIORDIRS = sorted(TOPDIR.glob('*Prior*'))


def _load_metadata(path):
    with open(path, encoding='utf-8') as file:
        metadata_dict = json.load(file)

    for eventdict in metadata_dict.values():
        del eventdict['maximization_pars']  # These differ across priordirs
                                            # and don't matter for our purposes
    return metadata_dict


METADATA_DICT, *_ = (_load_metadata(path)
                     for path in TOPDIR.glob('*/metadata.json'))
assert all(METADATA_DICT == metadata_dict for metadata_dict in _)


def _get_eventnames(priordir):
    paths = sorted(priordir.glob('*_posterior_samples.feather'))
    eventnames = [path.name.removesuffix('_posterior_samples.feather')
                  for path in paths]
    return eventnames


EVENTNAMES, *_ = [_get_eventnames(priordir) for priordir in PRIORDIRS]
assert all(EVENTNAMES == eventnames for eventnames in _)


KEYS = (
    'chirp_mass_source',
    'chirp_mass',
    'mass_1_source',
    'mass_2_source',
    'total_mass_source',
    'chi_eff',
    'luminosity_distance',
    'redshift',
    )

_NAMING_MAP = {
    'mchirp_source': 'chirp_mass_source',
    'mchirp': 'chirp_mass',
    'm1_source': 'mass_1_source',
    'm2_source': 'mass_2_source',
    'mtot': 'total_mass_source',
    'chieff': 'chi_eff',
    'd_luminosity': 'luminosity_distance',
    'z': 'redshift',}


def make_event(eventname, description=None, priors=None,
               keys=KEYS):
    """Return ``schema.Event`` with IAS event."""
    if priors is None:
        priordirs = PRIORDIRS
    else:
        priordirs = [TOPDIR/prior for prior in priors]

    pe_sets = []
    for priordir in priordirs:
        link = schema.Link(
            url=f'{REPO_URL}/{priordir.name}',
            content_type='posterior-samples',
            description='GitHub repository with samples for this PE run.')

        samples = pd.read_feather(
            priordir/f'{eventname}_posterior_samples.feather'
            ).rename(columns=_NAMING_MAP)

        parameter_set = schema.ParameterSet.from_samples(
            samples=samples[list(keys)],
            name=priordir.name,
            type='pe',
            data_url=REPO_URL,
            waveform_family=WAVEFORM_FAMILY,
            links=[link]
            )
        pe_sets.append(parameter_set)

    gps = round(METADATA_DICT[eventname]['tgps'], 1)
    eventdata_dic = np.load(TOPDIR/'Data'/f'{eventname}_data.npz')
    detectors = [f'{det}1' for det in eventdata_dic['detector_names'][()]]

    return schema.Event(eventname, gps, detectors, pe_sets, description)


def make_catalog(eventnames=EVENTNAMES, **kwargs):
    """Return ``schema.Catalog`` with IAS catalog."""
    events = [make_event(eventname, **kwargs) for eventname in eventnames]
    return schema.Catalog(name=CATALOG_NAME,
                          description=CATALOG_DESCRIPTION,
                          doi=DOI,
                          events=events)
