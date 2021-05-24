from typing import Sequence

import numpy as np
import pypesto
from pypesto.objective.constants import (
    FVAL,
    X,
)
import pypesto.optimize
from pypesto.store import read_from_hdf5

from _helpers_paths import (
    estimate_output_path,
)

from _settings import (
    n_starts_plotted,
)

# The index of the MLE in a pyPESTO optimization result is always 0 due to
# sorting.
MLE = 0

# Added to divisions that may be zero.
SMALL_VALUE = np.spacing(1)


def get_estimate_result(
        optimizers: dict,
        pypesto_problem: pypesto.Problem,
) -> dict:
    """Load the result of a previous estimation.

    Parameters
    ----------
    optimizers:
        A dictionary similar to the dictionary named `optimizers` later in this
        file.
    pypesto_problem:
        The problem used for estimation.

    Returns
    -------
    The `optimizers` `dict` with result keys filled.
    """
    for optimizer_name in optimizers.keys():
        pypesto_result_hdf5_reader = \
            read_from_hdf5.OptimizationResultHDF5Reader(
                estimate_output_path(optimizer_name)
            )
        pypesto_result = pypesto_result_hdf5_reader.read()
        optimizers[optimizer_name]['result'] = pypesto_result
        # The pyPESTO problem, which includes all infomation required for
        # parameter estimation, can be recreated without much computational
        # overhead, so is not saved but simply set here.
        optimizers[optimizer_name]['result'].problem = pypesto_problem
        optimizers[optimizer_name]['mle'] = \
            pypesto_result.optimize_result.list[MLE][X]
    return optimizers


def get_best_optimizer(optimizers: dict) -> dict:
    """Get the optimizer for the estimate with the best MLE.

    Will return the first optimizer encountered in the loop, in the case of
    multiple optimizers having the same best MLE function value.

    Returns the optimizer as a `dict`, in the format of the nested dictionaries
    inside `optimizers` below.

    Parameters
    ----------
    optimizers:
        A dictionary similar to the dictionary named `optimizers` later in this
        file.

    Returns
    -------
    The optimizer `dict`.
    """
    fval0 = float('inf')
    name0 = None
    for name, description in optimizers.items():
        fval = description['result'].optimize_result.list[MLE][FVAL]
        if fval < fval0:
            fval0 = fval
            name0 = name
    if name0 is None:
        raise ValueError(
            'No optimization result with a non-infinite MLE function value.'
        )
    return optimizers[name0]


def get_n_converged_best(optimizer):
    global_cutoff = 1
    fval0 = optimizer['result'].optimize_result.list[0]['fval']
    return sum([
        o['fval'] - fval0 < global_cutoff
        for o in optimizer['result'].optimize_result.list
    ])


def get_local_optima(
        optimizers,
):
    local_optima = {}
    local_cutoff = 1
    for optimizer_id, optimizer_description in optimizers.items():
        # Skip starts in the possible global optimum
        first_index = get_n_converged_best(optimizer_description)
        result_list = optimizer_description['result'].optimize_result.list
        optima0 = {
            'fval': (
                np.inf
                if first_index not in result_list
                else result_list[first_index]['fval']
            ),
            'first': first_index,
            'length': 0,
        }
        # Skip if no local optima are possible because all starts converged.
        if first_index == len(result_list):
            local_optima[optimizer_id] = optima0
            continue
        optima = optima0.copy()
        remaining_starts = result_list[first_index + 1:n_starts_plotted]
        for start_index, start in enumerate(remaining_starts):
            if abs(start['fval'] - optima['fval']) < local_cutoff:
                optima['length'] += 1
            else:
                if optima['length'] > optima0['length']:
                    optima0 = optima.copy()
                next_start = result_list[start_index+1]
                optima = {
                    'fval': next_start['fval'],
                    'first': start_index+1,
                    'length': 0,
                }
        local_optima[optimizer_id] = optima0
    return local_optima


def root_mean_square_error(
        expectation: Sequence[float],
        observation: Sequence[float],
):
    expectation = np.array(expectation)
    observation = np.array(observation)
    return (
        np.sqrt(
            np.mean(
                np.square(
                    observation - expectation
                )
            )
        )
    )


def root_mean_absolute_error(
        expectation: Sequence[float],
        observation: Sequence[float],
):
    expectation = np.array(expectation)
    observation = np.array(observation)
    return (
        np.sqrt(
            np.mean(
                np.absolute(
                    observation - expectation
                )
            )
        )
    )


def normalized_root_mean_square_error(
        expectation: Sequence[float],
        observation: Sequence[float],
):
    expectation = np.array(expectation)
    observation = np.array(observation)
    return (
        root_mean_square_error(expectation, observation) /
        (expectation.max() - expectation.min() + SMALL_VALUE)
    )


def normalized_root_mean_absolute_error(
        expectation: Sequence[float],
        observation: Sequence[float],
):
    expectation = np.array(expectation)
    observation = np.array(observation)
    return (
        root_mean_absolute_error(expectation, observation) /
        (expectation.max() - expectation.min() + SMALL_VALUE)
    )


color_global_optimum = 'mediumseagreen'
color_local_optimum = 'burlywood'


from _settings import optimizers
optimizers = {
    k: {
        'id': k,
        'mle': None,
        'result': None,
        **v
    }
    for k, v in optimizers.items()
}
