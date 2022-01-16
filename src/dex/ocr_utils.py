from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

from .data_model import DocTreeDoc

__all__ = ["scan_text_in_images"]


def scan_text_in_images(image_paths: list[Path]):
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
