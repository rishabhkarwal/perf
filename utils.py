import time
import multiprocessing
from rich.console import Console


_console = Console()
log      = _console.print

DEBUG    = True # controls whether debug prints are output

# timing
DEFAULT_TARGET_TIME = 1.0
TIMEOUT_MULTIPLIER  = 1.5

# search algorithm
GEOMETRIC_FACTOR    = 1.5 # rate at which 'n' expands during the exponential hunt phase


# layer 1: isolated execution worker

def _worker(func, n, queue):
    """
    Executes the target function in a strictly isolated process
    """
    try:
        start_time = time.perf_counter()
        _ = func(n)
        elapsed = time.perf_counter() - start_time
        queue.put((True, elapsed))
    except RecursionError:
        queue.put((False, 'recursion error'))
    except Exception as e:
        queue.put((False, str(e).lower()))


# layer 2: process controller

def _evaluate(func, n, target):
    """
    Spawns an isolated process for 'func(n)' and forcefully terminates if it exceeds the limit
    """
    soft_limit = target * TIMEOUT_MULTIPLIER
    queue = multiprocessing.Queue()
    
    p = multiprocessing.Process(target=_worker, args=(func, n, queue))
    p.start()
    
    # block main execution until the worker finishes or hits the soft limit
    p.join(soft_limit)
    
    if p.is_alive():
        # forcefully terminate the rogue process
        p.terminate()
        p.join()
        return False, 'timeout'
    
    if not queue.empty():
        success, result_or_err = queue.get()
        return success, result_or_err
        
    return False, 'unknown error'


# entry point

def find_max_n(func, label, target = DEFAULT_TARGET_TIME):
    """
    Locates the maximum 'n' computable within limits via two-phase search strategy
    """
    log(f'\n[bold blue]{label}[/bold blue]')
    
    n = 1
    lower_bound = 0
    upper_bound = None
    
    # phase 1: geometric hunt
    # multiplies 'n' by factor until the function times out - establishes a hard upper and lower bound
    if DEBUG: log('phase 1: geometric hunt for upper bound')
    while True:
        success, elapsed = _evaluate(func, n, target)
        
        if not success:
            upper_bound = n
            if DEBUG: log(f'hit limits at {n} (reason: {elapsed})')
            break
            
        if isinstance(elapsed, float) and elapsed > target:
            upper_bound = n
            if DEBUG: log(f'exceeded target time at {n} ({elapsed:.4f}s)')
            break
            
        lower_bound = n
        
        # grow n geometrically to scale past trivial numbers quickly
        n = max(n + 1, int(n * GEOMETRIC_FACTOR))
        
    # phase 2: binary search
    # finds the exact maximum threshold from the bounds
    if upper_bound is None:
        upper_bound = lower_bound + 1
        
    if DEBUG: log(f'phase 2: binary search between [{lower_bound}, {upper_bound}]')
    best_n = lower_bound
    low = lower_bound
    high = upper_bound - 1
    
    while low <= high:
        mid = (low + high) // 2
        success, elapsed = _evaluate(func, mid, target)
        
        if success and isinstance(elapsed, float) and elapsed <= target:
            best_n = mid
            low = mid + 1 # safe: search higher
        else:
            high = mid - 1 # exceeded: search lower
            
    log(f'[yellow]{best_n}[/yellow]')
    return best_n
