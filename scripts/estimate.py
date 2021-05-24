import pypesto.optimize
import pypesto.store

from _helpers import (
    estimate_output_path,
    optimizers,
    pypesto_problem,
    engine,
)


for optimizer_name, optimizer_description in optimizers.items():
    # Optimize
    pypesto_result = pypesto.optimize.minimize(
        problem=pypesto_problem,
        optimizer=optimizer_description['optimizer'],
        n_starts=optimizer_description['n_starts'],
        engine=engine,
    )
    # Save results to a file.
    pypesto_result_hdf5_writer = \
        pypesto.store.OptimizationResultHDF5Writer(
            estimate_output_path(optimizer_name)
        )
    pypesto_result_hdf5_writer.write(pypesto_result)
