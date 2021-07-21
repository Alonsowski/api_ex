from dataclasses import dataclass

@dataclass
class Exchange:
    name_from: str
    name_to: str
    rate: float