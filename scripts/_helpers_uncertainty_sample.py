import pypesto
from pypesto.store import read_result

from _helpers_paths import (
    sample_output_path,
)


def load_sample_result(
        pypesto_problem: pypesto.Problem = None,
):
    result = read_result(sample_output_path(), sample=True)
    if pypesto_problem is not None:
        result.problem = pypesto_problem
    return result
