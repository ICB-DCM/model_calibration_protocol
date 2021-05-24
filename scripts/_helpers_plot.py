import seaborn as sns


sns.set_style('ticks')

label_bbox_style = dict(
    boxstyle='round',
    fc='white',
    ec='k',
    alpha=0.75,
)

plateau_bbox_style = dict(
    alpha=0.50,
    ec=(0, 0, 0, 0),
    boxstyle='round,pad=0.1',
    zorder=10,
)


def increase_ax_ticklabels(ax: 'matplotlib.axes.Axes'):
    ax.xaxis.set_tick_params(labelsize='large')
    ax.yaxis.set_tick_params(labelsize='large')


def remove_ax_labels(ax: 'matplotlib.axes.Axes'):
    ax.set_title('')
    ax.set_xlabel('')
    ax.set_ylabel('')


def fix_plot_style():
    sns.set_style('ticks')
