from pathlib import Path
import numpy as np

DIR_ROOT: Path = Path(__file__).parent.parent
DIR_DATA = DIR_ROOT / "data"


def normalize_array(arr):
    """Normalize a NumPy array to the range [0, 1]."""
    arr_min = np.min(arr)
    arr_max = np.max(arr)
    return (
        (arr - arr_min) / (arr_max - arr_min)
        if arr_max != arr_min
        else np.zeros_like(arr)
    )
