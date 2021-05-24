import sys

import petab
import pypesto.petab

from _helpers_paths import (
    model_output_path,
)

from _settings import (
    model_name,
    petab_yaml_path,
    amici_solver_settings,
)


# Load the PEtab problem.
petab_problem = petab.Problem.from_yaml(petab_yaml_path)

# Import the model
sys.path.insert(0, model_output_path())
pypesto_importer = pypesto.petab.PetabImporter(
    petab_problem,
    output_folder=model_output_path(),
    model_name=model_name
)
pypesto_objective = pypesto_importer.create_objective()

for setter, value in amici_solver_settings.items():
    if value is None:
        continue
    getattr(pypesto_objective.amici_solver, setter)(value)

# Create the pyPESTO problem
pypesto_problem = pypesto_importer.create_problem(pypesto_objective)
