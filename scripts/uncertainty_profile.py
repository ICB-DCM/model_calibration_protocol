import pypesto.profile
from pypesto.store import write_result

from _helpers import (
    optimizers,
    pypesto_problem,

    get_estimate_result,
    get_best_optimizer,

    profile_output_path,

    # settings
    profile_kwargs,
)


optimizers = get_estimate_result(optimizers, pypesto_problem)
best_optimizer = get_best_optimizer(optimizers)

result = pypesto.profile.parameter_profile(
    problem=pypesto_problem,
    result=best_optimizer['result'],
    optimizer=best_optimizer['optimizer'],
    **profile_kwargs,
)

# FIXME
write_result(result=result, filename=profile_output_path(), sample=False,)
