from petab.C import (
    OBSERVABLE_ID,
    SIMULATION_CONDITION_ID,
    MEASUREMENT,
    SIMULATION,
)

from _helpers import (
    optimizers,
    pypesto_problem,
    get_simulation_df,
    get_estimate_result,
    petab_problem,
    get_best_optimizer,

    root_mean_square_error,
    normalized_root_mean_square_error,
    root_mean_absolute_error,
    normalized_root_mean_absolute_error,
)


optimizers = get_estimate_result(optimizers, pypesto_problem)
best_optimizer = get_best_optimizer(optimizers)
simulation_df = get_simulation_df(best_optimizer['mle'])

observable_ids = petab_problem.observable_df.index
condition_ids = petab_problem.condition_df.index

measured = []
simulated = []
for condition_index, condition_id in enumerate(condition_ids):
    for observable_index, observable_id in enumerate(observable_ids):
        subset_measurement_df = petab_problem.measurement_df
        subset_measurement_df = subset_measurement_df[
            petab_problem.measurement_df[SIMULATION_CONDITION_ID]
            == condition_id
        ]
        subset_measurement_df = subset_measurement_df[
            petab_problem.measurement_df[OBSERVABLE_ID] == observable_id
        ]
        measured.extend(subset_measurement_df[MEASUREMENT])

        subset_simulation_df = simulation_df
        subset_simulation_df = subset_simulation_df[
            simulation_df[SIMULATION_CONDITION_ID] == condition_id
        ]
        subset_simulation_df = subset_simulation_df[
            simulation_df[OBSERVABLE_ID] == observable_id
        ]
        simulated.extend(subset_simulation_df[SIMULATION])

rmse = root_mean_square_error(measured, simulated)
nrmse = normalized_root_mean_square_error(measured, simulated)
rmae = root_mean_absolute_error(measured, simulated)
nrmae = normalized_root_mean_absolute_error(measured, simulated)

print(f'Root mean square error: {rmse}')
print(f'Normalized root mean square error: {nrmse}')
print(f'Root mean absolute error: {rmae}')
print(f'Normalized root mean absolute error: {nrmae}')
