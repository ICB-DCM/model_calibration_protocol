import pypesto.sample
from pypesto.store import write_result

from _helpers import (
    optimizers,
    pypesto_problem,

    get_estimate_result,
    get_best_optimizer,

    sample_output_path,

    # settings
    n_samples,
    sampler,
    geweke_settings,
)


optimizers = get_estimate_result(optimizers, pypesto_problem)
best_optimizer = get_best_optimizer(optimizers)

result = pypesto.sample.sample(
    pypesto_problem,
    n_samples,
    sampler,
    x0=best_optimizer['mle'],
)
pypesto.sample.geweke_test(result=result, **geweke_settings)
write_result(result=result, filename=sample_output_path())
