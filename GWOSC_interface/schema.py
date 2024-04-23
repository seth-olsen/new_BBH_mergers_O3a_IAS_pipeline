"""
Dataclasses for organizing a catalog of parameter estimation results in
a format compatible with the Gravitational Wave Open Science Center.
"""
import dataclasses
import numpy as np
import pandas as pd


UNITS = dict.fromkeys(('chirp_mass_source',
                       'chirp_mass',
                       'mass_1_source',
                       'mass_2_source',
                       'total_mass_source'),
                      'Msun') | {'luminosity_distance': 'Mpc'}


@dataclasses.dataclass
class ParameterValue:
    """
    Summary of the measurement of a single parameter.

    Fields
    ------
    name: str
        Parameter name.

    median: float
        Median.

    upper_95: float
        95th percentile minus median.

    lower_05: float
        5th percentile minus median.

    upper_limit, lower_limit: bool

    sigfigs: int
        Number of significant figures.

    unit: str or None
    """
    name: str
    best: float
    upper: float
    lower: float
    upper_limit: bool = False
    lower_limit: bool = False
    sigfigs: int = None
    unit: str = None

    @classmethod
    def from_series(cls, name: str, series: pd.Series):
        q05, median, q95 = series.quantile((0.05, 0.5, 0.95))
        error = median - q05, q95 - median
        kwargs = _condition_value_and_error(median, error)
        return cls(name=name, unit=UNITS.get(name), **kwargs)


@dataclasses.dataclass
class Link:
    url: str
    content_type: str
    description: str


@dataclasses.dataclass
class SearchResult:
    """Summary of the significance obtained by a search pipeline."""
    pipeline: str
    pastro: float
    far: float  # (1/yr)


@dataclasses.dataclass
class ParameterSet:
    """Summary of a single parameter-estimation run."""
    name: str
    kind: str
    data_url: str
    waveform_family: str
    parameters: list[ParameterValue]
    links: list[Link] = None

    @classmethod
    def from_samples(cls,
                     samples: pd.DataFrame,
                     name,
                     kind,
                     data_url,
                     waveform_family,
                     links=None):
        """
        Constructor from a ``pandas.DataFrame`` of posterior samples.
        """
        parameters = [ParameterValue.from_series(*item)
                      for item in samples.items()]
        return cls(name=name,
                   kind=kind,
                   data_url=data_url,
                   waveform_family=waveform_family,
                   parameters=parameters,
                   links=links,
                  )


@dataclasses.dataclass
class Event:
    """Parameter estimation runs for a single event."""
    name: str
    gps: float
    detectors: list[str]
    search: list[SearchResult]
    pe_sets: list[ParameterSet]
    description: str = None


@dataclasses.dataclass
class Catalog:
    """Contains events detected/analyzed by a pipeline.

    Fields
    ------
    name: str
        The name of the catalog.
    description: str
        A description of the catalog.
    doi: str
        The full URL to the publication DOI related to this catalog.
    events: list of ``Event`` instances
        
    """
    name: str
    description: str
    doi: str
    events: list[Event]


def _condition_value_and_error(value, error) -> dict:
    """
    Pass a value and its uncertainty, return a dictionary with
    value, error and significant figures given by the uncertainties.

    Parameters
    ----------
    value: float
    error: (err_minus, err_plus)
    """
    error = np.abs(error)
    min_error = np.min(error)

    if min_error == 0:
        return {'best': float(f'{value:.2g}'),
                'lower': float(f'{-error[0]:.2g}'),
                'upper': float(f'{error[1]:.2g}'),
                'sigfigs': None}

    last_decimal = _first_decimal_place(min_error)
    if f'{min_error:e}'.startswith('1'):
        last_decimal += 1

    first_decimal = _first_decimal_place(value)

    def truncate(val):
        rounded = round(val, last_decimal)
        if last_decimal > 0:
            return rounded
        return int(rounded)

    truncated_value = truncate(value)
    err_minus = truncate(value - error[0] - truncated_value)
    err_plus = truncate(value + error[1] - truncated_value)
    return {'best': truncated_value,
            'lower': err_minus,
            'upper': err_plus,
            'sigfigs': last_decimal - first_decimal + 1}


def _first_decimal_place(value) -> int:
    return int(np.ceil(-np.log10(np.abs(value))))
