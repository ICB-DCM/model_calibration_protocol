from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import pypesto.visualize

from _helpers import (
    load_profile_result,
    plot_output_path,
    pypesto_problem,

    fix_plot_style,
    increase_ax_ticklabels,
    remove_ax_labels,
    plot_ax_only,
    color_global_optimum,
)

fix_plot_style()

profiles_plot_output_path = Path(plot_output_path('profiles'))
profiles_plot_output_path.mkdir(parents=True, exist_ok=True)

mle_color = to_rgba(color_global_optimum)
profile_color = to_rgba('black')
confidence_level = 0.95

pypesto_result = load_profile_result(pypesto_problem)

reference = pypesto.visualize.create_references({
    'x': pypesto_result.optimize_result.list[0]['x'],
    'fval': pypesto_result.optimize_result.list[0]['fval'],
    'color': mle_color,
})


for parameter_index, parameter_id in enumerate(pypesto_problem.x_names):
    if parameter_index > 1:
        break
    ax, = pypesto.visualize.profiles(
        pypesto_result,
        profile_indices=[parameter_index],
        reference=reference,
        size=(5, 5),
        colors=profile_color,
    )
    if plot_ax_only:
        increase_ax_ticklabels(ax)
        remove_ax_labels(ax)
        ax_lb, ax_ub = ax.get_xlim()
        if ax_lb <= pypesto_problem.lb[parameter_index] <= ax_ub:
            plt.axvline(
                x=pypesto_problem.lb[parameter_index],
                linestyle=':',
                color='gray',
            )
        if ax_lb <= pypesto_problem.ub[parameter_index] <= ax_ub:
            plt.axvline(
                x=pypesto_problem.ub[parameter_index],
                linestyle=':',
                color='gray',
            )
        plt.locator_params(axis='x', nbins=5)
    plt.savefig(str(profiles_plot_output_path / f'{parameter_id}.svg'))
