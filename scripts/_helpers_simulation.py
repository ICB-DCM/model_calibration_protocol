from typing import Sequence

import amici.petab_objective
import pandas as pd

from _helpers_problem import (
    petab_problem,
    pypesto_problem,
)


def get_simulation_df(
    x: Sequence[float],
) -> pd.DataFrame:
    simulation = amici.petab_objective.simulate_petab(
        petab_problem,
        pypesto_problem.objective.amici_model,
        problem_parameters=dict(zip(
            pypesto_problem.x_names,
            x,
        )),
        scaled_parameters=True,
    )

    simulation_df = amici.petab_objective.rdatas_to_simulation_df(
        simulation['rdatas'],
        model=pypesto_problem.objective.amici_model,
        measurement_df=petab_problem.measurement_df,
    )

    return simulation_df
