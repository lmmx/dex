from __future__ import annotations

from functools import partial
from pathlib import Path

from page_dewarp import cfg as dewarp_cfg
from page_dewarp.image import WarpedImage

from .library import Book
from .log_utils import Console
from .multiproc_utils import batch_multiprocess

__all__ = ["dewarp_and_save"]

dewarp_cfg["image_opts"].update({"PAGE_MARGIN_X": 10, "PAGE_MARGIN_Y": 0})

logger = Console(name=__name__).logger


def dewarp_and_save(input_image: Path, output_dir: Path | None = None) -> Path:
    dewarped_img = WarpedImage(input_image)  # Suppress STDOUT maybe?
    if output_dir is None:
        output_dir = input_image.parent / "dewarped"
        output_dir.mkdir(exist_ok=True)
    # Keep the input filename rather than allow `_thresh` to be appended to it
    out_path = output_dir / input_image.name
    if not dewarped_img.written:
        raise ValueError(f"Expected to write {out_path} from {input_image} but failed")
    Path(dewarped_img.outfile).rename(out_path)
    return out_path


def dewarp_images(book: Book) -> None:
    """
    Save dewarped versions of the images for this item if any have not been made
    yet. If any can't be dewarped, warn the user but continue anyway.

    Scan the text in the images into the :attr:`scanned` attribute.
    """
    item_images_to_dewarp = [img for img in book.images if not img.has_been_dewarped]
    dewarp_funcs = [partial(dewarp_and_save, img) for img in item_images_to_dewarp]
    if dewarp_funcs:
        batch_multiprocess(dewarp_funcs)
    # Sort so that the scanned results will also be sorted
    dewarped_images = sorted(  # noqa: F841
        [img.dewarped_path for img in book.images if img.has_been_dewarped]
    )
    unfixed = [img for img in book.images if not img.has_been_dewarped]
    if any(unfixed):
        logger.warning(f"Failed to dewarp all images for item {book.shelf.stem}")
        logger.info(f"Undewarped images: {unfixed}")
    else:
        logger.debug(f"Dewarped all images for item {book.shelf.stem}")
    return
