import dill
from pypesto.ensemble import Ensemble, EnsembleType
from pypesto.predict.constants import AMICI_X, AMICI_Y

from _helpers import (
    engine,
    get_amici_predictors,
    load_sample_result,
    predict_state_output_path,
    predict_observable_output_path,
    pypesto_problem,

    custom_timepoints,
    ensemble_settings,
)

plotting_objective = pypesto_problem.objective.set_custom_timepoints(
    **custom_timepoints,
)
predictor_state, predictor_observable = \
    get_amici_predictors(plotting_objective)

result = load_sample_result(pypesto_problem=pypesto_problem)

ensemble = Ensemble.from_sample(
    result,
    x_names=result.problem.x_names,
    ensemble_type=EnsembleType.sample,
    lower_bound=result.problem.lb,
    upper_bound=result.problem.ub,
    **ensemble_settings,
)

print('Computing state predictions.')
prediction_state = ensemble.predict(
    predictor_state,
    prediction_id=AMICI_X,
    engine=engine,
)
prediction_state.compute_summary()
with open(predict_state_output_path(), 'wb') as f:
    dill.dump(prediction_state, f)
del prediction_state

print('Computing observable predictions.')
prediction_observable = ensemble.predict(
    predictor_observable,
    prediction_id=AMICI_Y,
    engine=engine,
)
prediction_observable.compute_summary()
with open(predict_observable_output_path(), 'wb') as f:
    dill.dump(prediction_observable, f)
