from pydantic import BaseModel


class OcrResult(BaseModel):
    cords: list[tuple[int, int]]
    text: str
    confidence: float
