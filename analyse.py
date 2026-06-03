import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from utils import log, DEBUG


COLOUR_MAP = 'twilight_shifted'


def format_title(title):
    """
    Formats algorithm names into mathematically correct titles
    """
    # replace underscores with spaces
    name = title.replace('_', ' ')
    name = name.title()

    # mathematical special cases
    name = name.replace('N Th ', r'$n^{\text{th}}$ ')
    name = name.replace('N ', '$n$ ')

    return name


def plot(data, algorithm='plot'):
    """
    Generates a log-log plot to compare asymptotic time complexity of algorithms
    """
    os.makedirs('plots', exist_ok=True)
    filename = os.path.join('plots', f'{algorithm}.png')

    # built-in colourmaps for automatic colour scaling
    cmap = plt.get_cmap(COLOUR_MAP)
    n_series = len(data)
    
    # generate colours by splitting the spectrum into equal segments
    colours = [cmap((i + 1) / (n_series + 1)) for i in range(n_series)]
    
    # colours
    background = '#1c1c1c' # dark grey
    text       = '#ffffff' # white for contrast
    axis       = '#666666' # light grey for axes
    
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Inter', 'Helvetica', 'Arial'],
        'text.color': text,
    })

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=background)
    ax.set_facecolor(background)
    
    # plot data
    for i, (label, (x, y)) in enumerate(data.items()):
        colour = colours[i]
        ax.plot(
            x, y, 
            marker='o', markersize=5, 
            linestyle='-', linewidth=2, 
            label=label, color=colour,
            markerfacecolor=background, markeredgewidth=1.5
        )

        # annotate the end of the line
        ax.text(x[-1] * 1.3, y[-1], f'{label}\n$n={int(x[-1]):,}$', color=colours[i], fontsize=10, va='center')

    # x-axis configuration
    ax.set_xscale('log')
    ax.set_xlabel('Input Size (n)', fontsize=10, labelpad=10, color=text)
    
    # y-axis configuration
    ax.set_yscale('log')
    target_ticks = [0.0001, 0.001, 0.01, 0.1, 1.0]
    ax.set_yticks(target_ticks)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f'{y:g}'))
    ax.set_ylabel('Time (seconds)', fontsize=10, labelpad=10, color=text)

    # axis styling
    for side in ['bottom', 'left']:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color(axis)
        ax.spines[side].set_linewidth(1.5)
        
    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
        
    ax.tick_params(axis='both', which='both', colors=text, length=5, width=1.5)
    
    # grid
    ax.grid(True, which='major', color='#333333', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # title
    ax.set_title(format_title(algorithm), fontsize=16, pad=20, color=text, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, facecolor=background)
    if DEBUG: log(f'graph successfully saved to [blue]{filename}[/blue]')
