from pathlib import Path

import matplotlib.pyplot as plt
from pypesto.predict.constants import OUTPUT
import pypesto.visualize
from pypesto.visualize.sampling import _get_condition_and_output_ids

from _helpers import (
    get_predictions,
    plot_output_path,

    fix_plot_style,
    increase_ax_ticklabels,
    remove_ax_labels,
    plot_ax_only,
)


fix_plot_style()

prediction_x, prediction_y = get_predictions()

credibility_interval_levels = [90, 95, 99]

state_condition_ids, state_ids = \
    _get_condition_and_output_ids(prediction_x.prediction_summary)
observable_condition_ids, observable_ids = \
    _get_condition_and_output_ids(prediction_y.prediction_summary)

plot_size = (5, 5)

# =========================================================================== #
# Plot state predictions

print('Plotting prediction profiles of sampling, by state, grouped by output.')
predict_states_plot_output_path = Path(plot_output_path('predict_states'))
predict_states_plot_output_path.mkdir(parents=True, exist_ok=True)
for index, (condition_id, state_id) in enumerate(
    zip(state_condition_ids, state_ids)
):
    plot_id = f'{state_id}__{condition_id}'
    axes = pypesto.visualize.sampling_prediction_trajectories(
        prediction_x,
        levels=credibility_interval_levels,
        size=plot_size,
        axis_label_padding=60,
        groupby=OUTPUT,
        condition_ids=[condition_id],
        output_ids=[state_id],
    )
    if plot_ax_only:
        ax = axes.flat[0]
        remove_ax_labels(ax)
        increase_ax_ticklabels(ax)
        for text in plt.gcf().texts:
            text.set_text('')
        ax.get_legend().set_visible(False)
        plt.gcf().artists[0].set_visible(False)
    else:
        plt.tight_layout()
    plt.savefig(str(predict_states_plot_output_path / f'{plot_id}.svg'))

# =========================================================================== #
# Plot state predictions

print(
    'Plotting prediction profiles of sampling, by observable, grouped by '
    'output.'
)
predict_observables_plot_output_path = \
    Path(plot_output_path('predict_observables'))
predict_observables_plot_output_path.mkdir(parents=True, exist_ok=True)
for index, (condition_id, observable_id) in enumerate(
    zip(observable_condition_ids, observable_ids)
):
    plot_id = f'{observable_id}__{condition_id}'
    axes = pypesto.visualize.sampling_prediction_trajectories(
        prediction_y,
        levels=credibility_interval_levels,
        size=plot_size,
        axis_label_padding=60,
        groupby=OUTPUT,
        condition_ids=[condition_id],
        output_ids=[observable_id],
    )
    if plot_ax_only:
        ax = axes.flat[0]
        remove_ax_labels(ax)
        increase_ax_ticklabels(ax)
        for text in plt.gcf().texts:
            text.set_text('')
        ax.get_legend().set_visible(False)
        plt.gcf().artists[0].set_visible(False)
    else:
        plt.tight_layout()
    plt.savefig(str(predict_observables_plot_output_path / f'{plot_id}.svg'))
