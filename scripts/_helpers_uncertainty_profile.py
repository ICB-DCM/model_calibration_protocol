import pypesto.sample
from pypesto.store import read_result

from _helpers_paths import (
    profile_output_path,
)


def load_profile_result(
        pypesto_problem: pypesto.Problem,
):
    result = read_result(profile_output_path(), optimize=True, profile=True)
    result.problem = pypesto_problem
    return result
