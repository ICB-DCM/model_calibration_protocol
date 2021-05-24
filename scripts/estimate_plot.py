from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyBboxPatch
from petab.C import (
    OBSERVABLE_ID,
    SIMULATION_CONDITION_ID,
    CONDITION_NAME,
    TIME,
    MEASUREMENT,
    SIMULATION,
    NOISE_PARAMETERS,
)
import pypesto.visualize


# Various helper methods, related to saving and loading, are kept separately in
# the "_helpers.py" file and imported here.
from _helpers import (
    plot_output_path,

    optimizers,
    pypesto_problem,
    get_simulation_df,
    get_local_optima,
    get_n_converged_best,
    get_estimate_result,
    petab_problem,
    get_best_optimizer,

    n_starts_plotted,

    color_global_optimum,
    color_local_optimum,

    plot_ax_only,
    remove_ax_labels,
    increase_ax_ticklabels,
    label_bbox_style,
    plateau_bbox_style,
)


optimizers = get_estimate_result(optimizers, pypesto_problem)

best_optimizer = get_best_optimizer(optimizers)

pypesto_results = [o['result'] for o in optimizers.values()]
pypesto_results_names = [o['name'] for o in optimizers.values()]
pypesto_results_colors = [to_rgba(o['color']) for o in optimizers.values()]

global_length = get_n_converged_best(best_optimizer)

global_first = 0

local_optima = get_local_optima(optimizers)
local_first = local_optima[best_optimizer['id']]['first']
local_last = local_first + local_optima[best_optimizer['id']]['length']
if local_first == 0:
    print('No local optima detected, except any possible global optimum.')

# =========================================================================== #
# Waterfall plot

print('Plotting waterfall.')

point_width = 1.0

ax = pypesto.visualize.waterfall(
    pypesto_results,
    legends=pypesto_results_names,
    start_indices=n_starts_plotted,
    size=(7, 5),
    colors=pypesto_results_colors,
)

patch_padding = 0.05
y_optimum = 1
y_lower = y_optimum * 10**(-patch_padding)
y_upper = y_optimum * 10**(+patch_padding)
ax.annotate(
    'Possible global optimum',
    xy=(global_first + global_length/2, y_upper),
    xycoords='data',
    xytext=(0.05, 0.2),
    textcoords='axes fraction',
    bbox={**label_bbox_style, 'fc': color_global_optimum},
    arrowprops=dict(arrowstyle='->', ec='k')
)
plateau = FancyBboxPatch(
    (global_first - point_width/2, y_lower),
    global_length,
    y_upper - y_lower,
    fc=color_global_optimum,
    **plateau_bbox_style,
)
ax.add_patch(plateau)

first_local = True
plot_only_first_local = False
for optimizer_name, optima in local_optima.items():
    if optima['first'] == 0 or optima['length'] < 2:
        continue
    if plot_only_first_local and not first_local:
        break
    y = optima['fval']
    c = 0.3
    ax.annotate(
        'Possible local optimum',
        xy=(optima['first'] + optima['length']/2, y),
        xycoords='data',
        xytext=(0.05, 0.5),
        textcoords='axes fraction',
        bbox=(
            {**label_bbox_style, 'fc': color_local_optimum}
            if first_local
            else None
        ),
        alpha=None if first_local else 0,
        arrowprops=dict(arrowstyle='->', ec='k')
    )
    plateau = FancyBboxPatch(
        (optima['first'] - point_width/2, y),
        optima['length'],
        y*c,
        fc=color_local_optimum,
        **plateau_bbox_style,
    )
    ax.add_patch(plateau)
    first_local = False

if plot_ax_only:
    increase_ax_ticklabels(ax)
    remove_ax_labels(ax)

plt.savefig(plot_output_path('waterfall.svg'))

# =========================================================================== #
# Parameters plot

print('Plotting parameters.')

colors = ['grey'] * n_starts_plotted

if local_last != local_first:
    colors[local_first:local_last+1] = \
        [color_local_optimum] * (local_last+1 - local_first)

if global_first == 0:
    colors[global_first:global_length] = \
        [color_global_optimum] * (global_length - global_first)

colors = [
    to_rgba(c)
    if c != 'grey'
    else (*to_rgba(c)[:3], 0.1)
    for c in colors
]
ax = pypesto.visualize.parameters(
    best_optimizer['result'],
    start_indices=n_starts_plotted,
    size=(8, 8),
)
ax.set_xlabel('log10(Parameter value)')
ax.set_title('')
for color_index, color in enumerate(colors):
    if color_index >= len(ax.lines):
        break
    ax.lines[color_index].set_color(color)

if plot_ax_only:
    increase_ax_ticklabels(ax)
    remove_ax_labels(ax)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=45, ha='right')


plt.savefig(plot_output_path('parameters.svg'))

# =========================================================================== #
# Fit plot

print('Plotting fit.')

fit_plot_output_path = Path(plot_output_path('fit'))
fit_plot_output_path.mkdir(parents=True, exist_ok=True)

simulation_df = get_simulation_df(best_optimizer['mle'])


observable_ids = list(petab_problem.observable_df.index)
condition_ids = list(petab_problem.condition_df.index)
condition_names = list([
    petab_problem.condition_df.loc[condition_id][CONDITION_NAME]
    for condition_id in condition_ids
])

for condition_index, condition_id in enumerate(condition_ids):
    for observable_index, observable_id in enumerate(observable_ids):
        plot_id = f'{observable_id}_{condition_id}'

        subset_measurement_df = petab_problem.measurement_df
        subset_measurement_df = subset_measurement_df[
            petab_problem.measurement_df[SIMULATION_CONDITION_ID] ==
            condition_id
        ]
        subset_measurement_df = subset_measurement_df[
            petab_problem.measurement_df[OBSERVABLE_ID] == observable_id
        ]
        if len(subset_measurement_df) == 0:
            continue

        subset_simulation_df = simulation_df
        subset_simulation_df = subset_simulation_df[
            simulation_df[SIMULATION_CONDITION_ID] == condition_id
        ]
        subset_simulation_df = subset_simulation_df[
            simulation_df[OBSERVABLE_ID] == observable_id
        ]

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.errorbar(
            subset_measurement_df[TIME],
            subset_measurement_df[MEASUREMENT],
            yerr=subset_measurement_df[NOISE_PARAMETERS],
            fmt='.',
            color='k',
        )

        ax.plot(
            subset_simulation_df[TIME],
            subset_simulation_df[SIMULATION],
            color='black',
        )
        if not plot_ax_only:
            ax.set_title(plot_id)
        increase_ax_ticklabels(ax)
        plt.tight_layout()
        plt.savefig(fit_plot_output_path / f'{plot_id}.svg')
