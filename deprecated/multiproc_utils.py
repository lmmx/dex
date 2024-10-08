import multiprocessing as mp
from multiprocessing import Pool

from more_itertools import chunked
from tqdm import tqdm

__all__ = ["batch_multiprocess_with_return"]


def batch_multiprocess_with_return(
    function_list,
    pool_results=None,
    n_cores=mp.cpu_count(),
    show_progress=True,
    tqdm_desc=None,
):
    """
    Run a list of functions on `n_cores` (default: all CPU cores),
    with the option to show a progress bar using tqdm (default: shown).
    """
    iterator = [*chunked(function_list, n_cores)]
    pool_results = pool_results if pool_results else []
    pool = Pool(processes=n_cores)
    if show_progress:
        iterator = tqdm(iterator, desc=tqdm_desc)
    for func_batch in iterator:
        for f in func_batch:
            pool.apply_async(func=f, callback=pool_results.append)
    pool.close()
    pool.join()
    return pool_results
