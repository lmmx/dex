from __future__ import annotations

from pathlib import Path

from page_dewarp.image import WarpedImage

__all__ = ["dewarp_and_save"]


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
