from dataclasses import dataclass

@dataclass
class Fee:
    name_from: str
    name_to: str
    value: float
