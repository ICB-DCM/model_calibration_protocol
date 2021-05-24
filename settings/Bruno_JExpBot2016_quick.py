from pathlib import Path

import numpy as np


# =========================================================================== #
# Parameter estimation problem (PEtab)

# Define a custom ID for this calibration, such that results are stored in a
# subfolder of the output folder, with this ID.
setting_id = 'Bruno_JExpBot2016_quick'
# The name of the model.
model_name = setting_id
# The path to the PEtab YAML file. Absolute paths are recommended.
# For compatibility between different users of these examples, a relative path
# is defined here. Relative to the location of this file, this path is
# equivalent to setting
# ```
# petab_yaml_path = (
#     '/PATH/TO/THIS/REPOSITORY/Benchmark-Models-PEtab/Benchmark-Models/'
#     'Bruno_JExpBot2016/Bruno_JExpBot2016.yaml'
# )
# ```
petab_yaml_path = str(
    Path(__file__).parent.parent / 'Benchmark-Models-PEtab' /
    'Benchmark-Models' / 'Bruno_JExpBot2016' / 'Bruno_JExpBot2016.yaml'
)

# =========================================================================== #
# Simulation

# AMICI is used for simulation, and settings here can be used to specify the
# the input to any AMICI solver setter that is callable from an AMICI solver
# instance.
# `None` to use the default AMICI solver setting.
amici_solver_settings = {
    # The number of integration steps before simulation fails.
    'setMaxSteps': int(1e6),
    # Absolute tolerance. Any float value is valid.
    'setAbsoluteTolerance': None,
    # Relative tolerance. Any float value is valid.
    'setRelativeTolerance': None,
}

# =========================================================================== #
# Parallelize

# The optimization and profiling tasks can be parallelized, if a
# parallelization engine is specified.

from pypesto.engine import (
    SingleCoreEngine,
    MultiProcessEngine,
)


# Number of CPU cores to use can be specified with `n_procs`.
# e.g.: MultiProcessEngine(n_procs=4).
# Defaults to the number of CPU cores that are available.
engine = MultiProcessEngine()

# =========================================================================== #
# Estimate

import fides
import pypesto.optimize


# Number of starts plotted in waterfall and parameters plots.
# Also used to restrict the number of starts processed when identifying
# possible local optima. Possible local optima beyond the first
# `n_starts_plotted` starts are ignored.
n_starts_plotted = 10

# Define the optimizers to use.
# The key is an arbitrary, but unique, ID for the optimizer.
# Value dictionaries involving the following keys.
# 'name': A human-readable description of the optimizer, for plotting.
# 'optimizer': The optimizer. Only a subset of the gradient-based
#              optimizers have been tested here.
# 'n_starts': The number of starts for a multi-start optimization.
# 'color': The color used when plotting optimizer results (e.g. waterfall
#          plot). Currently only tested with named colors from the `matplotlib`
#          package.
optimizers = {
    'scipy_lbfgsb': {
        'name': 'SciPy L-BFGS-B',
        'optimizer': pypesto.optimize.ScipyOptimizer(method='l-bfgs-b'),
        'n_starts': 10,
        'color': 'black',
    },
}

# =========================================================================== #
# Plot

# Plot only the graph and ticks, without axis labels or titles.
plot_ax_only = False

# =========================================================================== #
# Profile

# The optimizer used for likelihood profiling is the optimizer that produced
# the estimate with the highest likelihood.

from pypesto.profile import (
    ProfileOptions,
)


# Can be customized with options described in the pyPESTO documentation.
profile_options = ProfileOptions()

# Keys correspond to arguments of the `pypesto.profile.parameter_profile`
# method, and values are the desired values of the respective arguments.
profile_kwargs = {
    'engine': engine,
    'profile_options': profile_options,
}

# =========================================================================== #
# Sample

import pypesto.sample


# Number of samples to compute per chain.
n_samples = int(5e4)
# Number of chains, for parallel tempering.
n_chains = 3
# The sampler that will be used. Any pyPESTO sampler should be compatible here.
# Only tested with `AdaptiveMetropolisSampler`, and
# `AdaptiveParallelTemperingSampler` with
# `internal_sampler==AdaptiveMetropolisSampler()`.
sampler = pypesto.sample.AdaptiveParallelTemperingSampler(
    internal_sampler=pypesto.sample.AdaptiveMetropolisSampler(),
    n_chains=n_chains,
)

# Settings for the Ensemble constructor.
ensemble_settings = dict(
    # Apply a slice to the MCMC chain, to reduce the computational cost of, for
    # example, predictions.
    chain_slice=slice(None, None, 10),
)

# Custom timepoints used for plotting prediction simulations.
custom_timepoints = dict(
    timepoints_global=np.linspace(0, 180, 181)
)

# Settings for the Geweke test for chain convergence.
geweke_settings = dict(
    zscore=2,
)
