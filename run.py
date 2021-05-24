from pathlib import Path
from subprocess import run
import sys
import shutil


scripts_path = Path('scripts')
settings_path = Path('settings')


def get_script(script_filename: str) -> str:
    return str(scripts_path / script_filename)


settings_paths = sorted([*settings_path.iterdir()], key=lambda x: x.stem)

settings = {
    str(setting_id): setting_path
    for setting_id, setting_path in enumerate(settings_paths, start=1)
}

print(
    'The following settings are available:\n'
    + '\n'.join([
        f'{setting_id}: {setting_path.stem}'
        for setting_id, setting_path in settings.items()
    ])
)

# Get the user's chosen setting.
while True:
    setting_id = input('\n\nWhich setting would you like? ')
    if setting_id in settings:
        break
    print(
        'The selected setting did not match an available setting. '
        f'Selected setting: {setting_id}'
    )

# Copy the chosen settings to the scripts directory for usage by the tasks.
settings_output_path = scripts_path / '_settings.py'
if settings_output_path.exists():
    raise FileExistsError(
        'A settings file already exists in the scripts directory. Please '
        f'remove {settings_output_path} then try again.'
    )
shutil.copy(settings[setting_id], settings_output_path)

# Describe the available tasks.
tasks = {
    '3.1': {
        'description': 'Estimate parameters.',
        'script': 'estimate.py',
    },
    '3.2': {
        'description': 'Plot: fit, waterfall, parameters.',
        'script': 'estimate_plot.py',
    },
    '4.1': {
        'description': 'Assess estimate fit.',
        'script': 'estimate_assess_fit.py',
    },
    '5.1_sample': {
        'description': 'Sample from posterior.',
        'script': 'uncertainty_sample.py',
    },
    '5.1_plot_sample': {
        'description': 'Plot: sample trace, marginals, credibility intervals.',
        'script': 'uncertainty_sample_plot.py',
    },
    '5.1_profile': {
        'description': 'Profile likelihood.',
        'script': 'uncertainty_profile.py',
    },
    '5.1_plot_profile': {
        'description': 'Plot: likelihood profile.',
        'script': 'uncertainty_profile_plot.py',
    },
    '6.1': {
        'description': 'Compute states and observables of samples.',
        'script': 'uncertainty_sample_predict.py',
    },
    '6.1_plot': {
        'description': 'Plot: state and observable prediction uncertainties.',
        'script': 'uncertainty_sample_predict_plot.py',
    },
}

print(
    'The following tasks are available to run:\n'
    + '\n'.join([
        f'{task_id}: {task["description"]}'
        for task_id, task in tasks.items()
    ])
)

# Get the user's chosen task.
while True:
    task_id = input('\n\nWhich task would you like to run? ')
    if task_id in tasks:
        break
    print(
        'The selected task did not match an available task. '
        f'Selected task: {task_id}'
    )
task = tasks[task_id]

# Run the chosen task.
print(
    f'Starting task {task_id}: {task["description"]}\n'
    f'Now running "{task["script"]}"'
)
run(['python3', get_script(task['script'])])
print(f'Completed task {task_id}: {task["description"]}\n')

# Remove the custom settings that were copied to the scripts directory.
settings_output_path.unlink()
