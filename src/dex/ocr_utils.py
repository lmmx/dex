from __future__ import annotations

from pathlib import Path
from typing import Literal, overload

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

from .data_model import DocTreeDoc, LayoutLMDoc
from .layoutlmv3 import process_page_image

__all__ = ["scan_text_in_images"]


@overload
def scan_text_in_images(
    image_paths: list[Path], layoutlm: Literal[False]
) -> DocTreeDoc:
    ...


@overload
def scan_text_in_images(
    image_paths: list[Path], layoutlm: Literal[True]
) -> LayoutLMDoc:
    ...


def scan_text_in_images(
    image_paths: list[Path], layoutlm: bool = False
) -> DocTreeDoc | LayoutLMDoc:
    if layoutlm:
        processed_pages = [process_page_image(p) for p in image_paths]
        processor = AutoProcessor.from_pretrained("microsoft/layoutlmv3-large", apply_ocr=True)
        model = AutoModelForTokenClassification.from_pretrained("microsoft/layoutlmv3-large")
        doc = LayoutLMDoc(pages=processed_pages)
    else:
        model_config = {
            "det_arch": "db_resnet50",
            "reco_arch": "crnn_vgg16_bn",
            "pretrained": True,
        }
        model = ocr_predictor(**model_config)
        multi_img_doc = DocumentFile.from_images(image_paths)
        result = model(multi_img_doc)
        result_dict = result.export()
        doc = DocTreeDoc.from_dict(result_dict)
    return doc
