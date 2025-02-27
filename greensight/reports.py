import matplotlib.pyplot as plt

from pathlib import Path


def save_figure(
    fig: plt.Figure, directory: Path, filename: str, save_pdf: bool = False
):
    """
    Saves a Matplotlib figure as a PDF in the specified directory.

    Parameters:
    - fig: Matplotlib figure object (e.g., plt.gcf() for current figure)
    - directory: Target directory to save the file
    - filename: Desired filename (without extension)

    Returns:
    - Full file path of the saved PDF
    """
    # Ensure the directory exists
    assert directory.is_dir()

    # png
    file_path = directory / f"{filename}.png"
    fig.savefig(file_path, format="png", bbox_inches="tight")

    # pdf
    if save_pdf:
        file_path = directory / f"{filename}.pdf"
        fig.savefig(file_path, format="pdf", bbox_inches="tight")

    return file_path
