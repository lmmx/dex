from pathlib import Path

from pydantic import BaseModel, model_validator

__all__ = ["OCRLine", "IndexPage", "Index"]


class OCRLine(BaseModel):
    bbox: tuple[float, float, float, float]
    confidence: float
    polygon: list[tuple[float, float]]
    text: str


class IndexPage(BaseModel):
    filename: str
    text_lines: list[OCRLine]
    languages: list[str] | None
    image_bbox: tuple[float, float, float, float]
    page: int


class Index(BaseModel):
    pages: list[IndexPage]

    @model_validator(mode="before")
    def pop_pages(cls, values: dict):
        if "pages" not in values:
            return {"pages": [dict(filename=k, **v[0]) for k, v in values.items()]}
        else:
            return values


# from fieldrouter import RoutingModel, Routing
#
# class SuryaModel(RoutingModel):
#     line: Routing(OCRLine, "pages.0.text_lines.0")
#
# a_line = SuryaModel.model_validate(modelled.model_dump())
