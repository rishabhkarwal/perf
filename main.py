import sys
import time
import importlib
from pathlib import Path
from utils import find_max_n, log, DEBUG
from analyse import plot


TARGET_DIR = 'n_th_fibonacci'


# module loader

def _load_methods(directory):
    """
    Dynamically scans the target directory and imports the 'f' function from every Python file found within it
    """
    methods = {}
    path = Path(directory)
    
    if not path.is_dir():
        log(f'[bold red]error:[/bold red] directory "{directory}" not found')
        sys.exit(1)
        
    # iterate through all .py files in the directory
    for file in path.glob('*.py'):
            
        module_name = f'{directory}.{file.stem}'
        
        try:
            module = importlib.import_module(module_name)
            
            # look for the function named 'f'
            if hasattr(module, 'f'):
                # format the filename into a clean label
                label = file.stem.replace('_', ' ').title()
                methods[label] = module.f
            else:
                log(f'[bold yellow]warning:[/bold yellow] "{file.name}" — no function "f" defined')
                
        except Exception as e:
            log(f'[bold red]error loading module "{module_name}":[/bold red] {e}')
            
    return methods


# entry point

def main():
    methods = _load_methods(TARGET_DIR)
    
    if not methods:
        log(f'[bold red]no benchmarkable methods found in "{TARGET_DIR}"[/bold red]')
        sys.exit(1)

    data = {}
    time_limit = 1.0
    MAX_PLOT_POINTS = 100 # maximum number of points to compute per curve
    
    log(f'\n[yellow]{time_limit}s[/yellow]')
    for label, func in methods.items():

        times = []

        N = find_max_n(func, label, target=time_limit)

        if DEBUG: log(f'gathering points up to {N}') # logarithmically spaced
        
        # determine the test points
        if N <= MAX_PLOT_POINTS:
            # if 'N' is small, test every single integer
            points = list(range(1, N + 1))
        else:
            # calculate the geometric ratio for perfectly spaced points on a log axis
            ratio = N ** (1 / (MAX_PLOT_POINTS - 1))
            
            # generate the points
            points = sorted(list(set(int(1 * (ratio ** i)) for i in range(MAX_PLOT_POINTS)))) # cast to int & remove duplicates using a set
            
            if points[-1] != N: points.append(N)

        # execute only the calculated points
        for n in points:
            try:
                start_time = time.perf_counter()
                _ = func(n)
                elapsed = time.perf_counter() - start_time

                if elapsed > time_limit: break
                
                times.append(elapsed)
                
            except RecursionError:
                break

        data[label] = (points[:len(times)], times)

    if DEBUG: log('\ngenerating graph')
    plot(data, TARGET_DIR)

if __name__ == '__main__':
    main()
