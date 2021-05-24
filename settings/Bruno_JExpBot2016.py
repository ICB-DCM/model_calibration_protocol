# See the settings file for Bruno_JExpBot2016_quick for descriptions of the
# settings here.

from pathlib import Path

import numpy as np


# =========================================================================== #
# Parameter estimation problem (PEtab)

setting_id = 'Bruno_JExpBot2016'
model_name = setting_id
petab_yaml_path = str(
    Path(__file__).parent.parent / 'Benchmark-Models-PEtab' /
    'Benchmark-Models' / model_name / f'{model_name}.yaml'
)

# =========================================================================== #
# Simulation

amici_solver_settings = {
    'setMaxSteps': int(1e6),
    'setAbsoluteTolerance': None,
    'setRelativeTolerance': None,
}

# =========================================================================== #
# Parallelize

from pypesto.engine import (
    SingleCoreEngine,
    MultiProcessEngine,
)


engine = MultiProcessEngine()

# =========================================================================== #
# Estimate

import fides
import pypesto.optimize


n_starts_plotted = 50

optimizers = {
    'scipy_lbfgsb': {
        'name': 'SciPy L-BFGS-B',
        'optimizer': pypesto.optimize.ScipyOptimizer(method='l-bfgs-b'),
        'n_starts': 50,
        'color': 'black',
    },
}

# =========================================================================== #
# Plot

plot_ax_only = True

# =========================================================================== #
# Profile

from pypesto.profile import (
    ProfileOptions,
)


profile_options = ProfileOptions()

profile_kwargs = {
    'engine': engine,
    'profile_options': profile_options,
}

# =========================================================================== #
# Sample

import pypesto.sample


n_samples = int(1e6)
n_chains = 3
sampler = pypesto.sample.AdaptiveParallelTemperingSampler(
    internal_sampler=pypesto.sample.AdaptiveMetropolisSampler(),
    n_chains=n_chains,
)

ensemble_settings = dict(
    chain_slice=slice(None, None, 1000),
)

custom_timepoints = dict(
    timepoints_global=np.linspace(0, 180, 181)
)

geweke_settings = dict(
    zscore=0.1,
)
