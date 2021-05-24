from pathlib import Path

from _settings import (
    setting_id,
)


output_path = Path('output') / setting_id


def prepare_path(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def model_output_path() -> str:
    path = output_path / 'import' / 'model'
    return prepare_path(path)


def estimate_output_path(optimizer_name: str) -> str:
    path = output_path / 'estimate' / f'{optimizer_name}.hdf5'
    return prepare_path(path)


def plot_output_path(name: str) -> str:
    path = output_path / 'plot' / name
    return prepare_path(path)


def predict_state_output_path() -> str:
    path = output_path / 'predict' / 'states.dill'
    return prepare_path(path)


def predict_observable_output_path() -> str:
    path = output_path / 'predict' / 'observables.dill'
    return prepare_path(path)


def profile_output_path() -> str:
    path = output_path / 'profile' / 'profile.hdf5'
    return prepare_path(path)


def sample_output_path() -> str:
    path = output_path / 'sample' / 'sample.hdf5'
    return prepare_path(path)
