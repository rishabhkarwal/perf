import sys
import importlib
from pathlib import Path
from utils import find_max_n, log


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

    target_time = 1.0
    log(f'\n{target_time}s')
    for label, func in methods.items():
        find_max_n(func, label, target=target_time)


if __name__ == '__main__':
    main()
