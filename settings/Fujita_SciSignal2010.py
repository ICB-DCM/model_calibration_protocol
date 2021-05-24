# See the settings file for Bruno_JExpBot2016_quick for descriptions of the
# settings here.

from pathlib import Path

import numpy as np


# =========================================================================== #
# Parameter estimation problem (PEtab)

petab_choice = 6

custom_petab = Path('custom_petab')
custom_petab_fujita = custom_petab / 'Fujita_SIA'

benchmark_petab = Path('Benchmark-Models-PEtab') / 'Benchmark-Models'

petab_yaml_paths = {
    0: benchmark_petab / 'Fujita_SciSignal2010' / 'Fujita_SciSignal2010.yaml',
    # reaction_5_k1 and reaction_5_k2
    1: custom_petab_fujita / 'benchmark_fixed1.yaml',
    # reaction_5_k1 and reaction_6_k1
    2: custom_petab_fujita / 'benchmark_fixed2.yaml',
    # reaction_5_k1 and scaling_pS6_tot
    3: custom_petab_fujita / 'benchmark_fixed3.yaml',
    # reaction_5_k1 and reaction_5_k2
    4: custom_petab_fujita / 'paper_fixed1.yaml',
    # reaction_5_k1 and reaction_6_k1
    5: custom_petab_fujita / 'paper_fixed2.yaml',
    # reaction_5_k1 and scaling_pS6_tot
    6: custom_petab_fujita / 'paper_fixed3.yaml',
}

setting_id = f'Fujita_SciSignal2010_{petab_choice}'
model_name = setting_id

petab_yaml_path = str(
    Path(__file__).parent.parent / petab_yaml_paths[petab_choice]
)

# =========================================================================== #
# Simulate

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


n_starts_plotted = 100

optimizers = {
    'fides_2d_hybrid': {
        'name': 'Fides 2D Hybrid',
        'optimizer':
            pypesto.optimize.FidesOptimizer(
                hessian_update=fides.HybridUpdate(),
                options={
                    fides.Options.SUBSPACE_DIM: fides.SubSpaceDim.TWO,
                },
            ),
        'n_starts': 1000,
        'color': 'indigo',
    },
    'scipy_lbfgsb': {
        'name': 'SciPy L-BFGS-B',
        'optimizer': pypesto.optimize.ScipyOptimizer(method='l-bfgs-b'),
        'n_starts': 1000,
        'color': 'dodgerblue',
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
    timepoints_global=np.linspace(0, 3600, 301)
)

geweke_settings = dict(
    zscore=2,
)
