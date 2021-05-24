from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pypesto.visualize
from pypesto.visualize.sampling import get_data_to_plot

from _helpers import (
    load_sample_result,
    plot_output_path,
    pypesto_problem,
    optimizers,
    get_best_optimizer,
    get_estimate_result,

    increase_ax_ticklabels,
    remove_ax_labels,
    fix_plot_style,
    plot_ax_only,
)

fix_plot_style()

optimizers = get_estimate_result(optimizers, pypesto_problem)
best_optimizer = get_best_optimizer(optimizers)

pypesto_result = load_sample_result(pypesto_problem)

# =========================================================================== #
# Function trace

print('Plotting function trace.')

# Temporarily switch the sign of values, as the plotting function also switches
# the sign.
pypesto_result.sample_result.trace_neglogpost[0] = \
    -pypesto_result.sample_result.trace_neglogpost[0]
ax = pypesto.visualize.sampling_fval_traces(
    pypesto_result,
    full_trace=True,
    stepsize=100,
    size=(10, 5),
)
pypesto_result.sample_result.trace_neglogpost[0] = \
    -pypesto_result.sample_result.trace_neglogpost[0]
ax.set_ylabel('Function value')

ax.collections[0].set_color('black')

increase_ax_ticklabels(ax)
if plot_ax_only:
    remove_ax_labels(ax)
plt.savefig(plot_output_path('trace_fval.png'), dpi=600)

# =========================================================================== #
# Marginal densities

print('Plotting marginal distributions.')
marginals_plot_output_path = Path(plot_output_path('marginals'))
marginals_plot_output_path.mkdir(parents=True, exist_ok=True)

for parameter_index, parameter_id in enumerate(pypesto_problem.x_names):
    _, fvals, _, _, _, = get_data_to_plot(
        result=pypesto_result,
        i_chain=0,
        stepsize=100,
        par_indices=[parameter_index],
    )
    _, ax = plt.subplots(figsize=(5, 5))
    g = sns.displot(
        fvals[parameter_id],
        kind='hist',
        kde=True,
        rug=True,
        color='k',
        ax=ax,
    )

    if plot_ax_only:
        ax2 = plt.gcf().get_children()[1]
        remove_ax_labels(ax2)
        increase_ax_ticklabels(ax2)
        ax2.set_xlabel('')
        ax2.set_ylabel('')
    else:
        g.set_axis_labels(f'log10({parameter_id})', 'Density')
    increase_ax_ticklabels(ax)
    plt.tight_layout()
    plt.savefig(str(marginals_plot_output_path / f'{parameter_id}.svg'))

# =========================================================================== #
# Credibility intervals

print('Plotting credibility intervals.')
ci_levels = [99, 95, 90]
plot_size = (16, 9)

ax = pypesto.visualize.sampling_parameter_cis(
    pypesto_result,
    alpha=ci_levels,
    size=plot_size,
)
ax.set_ylabel('')
ax.set_xlabel('log10(' + ax.get_xlabel() + ')')
plt.savefig(plot_output_path('parameter_ci.svg'))
