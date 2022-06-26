from pathlib import Path

from .data_model import LayoutLMPage

from transformers import AutoProcessor, AutoModelForTokenClassification

__all__ = ["process_page_image"]


def process_page_image(
    image: Path, processor: AutoProcessor, model: AutoModelForTokenClassification
) -> LayoutLMPage:
    encoding = processor(
        image, truncation=True, return_offsets_mapping=True, return_tensors="pt"
    )
    offset_mapping = encoding.pop("offset_mapping")

    outputs = model(**encoding)
    last_hidden_states = outputs.last_hidden_state

    page = LayoutLMPage(source=image)
    return page
