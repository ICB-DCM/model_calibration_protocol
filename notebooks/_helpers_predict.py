from functools import partial

import dill
import numpy as np
from pypesto.predict.constants import AMICI_STATUS, AMICI_T, AMICI_X, AMICI_Y
from pypesto.predict import AmiciPredictor


# This post_processor will transform the output of the simulation tool
# such that the output is compatible with the next steps.
def post_processor(amici_outputs, output_type, output_ids):
    outputs = [
        amici_output[output_type] if amici_output[AMICI_STATUS] == 0
        else np.full((len(amici_output[AMICI_T]), len(output_ids)), np.nan)
        for amici_output in amici_outputs
    ]
    return outputs


def get_amici_predictors(amici_objective):
    # Setup post-processors for both states and observables.
    state_ids = amici_objective.amici_model.getStateIds()
    observable_ids = amici_objective.amici_model.getObservableIds()
    post_processor_x = partial(
        post_processor,
        output_type=AMICI_X,
        output_ids=state_ids,
    )
    post_processor_y = partial(
        post_processor,
        output_type=AMICI_Y,
        output_ids=observable_ids,
    )

    # Create pyPESTO predictors for states and observables
    predictor_x = AmiciPredictor(
        amici_objective,
        post_processor=post_processor_x,
        output_ids=state_ids,
    )
    predictor_y = AmiciPredictor(
        amici_objective,
        post_processor=post_processor_y,
        output_ids=observable_ids,
    )

    return predictor_x, predictor_y
