from dataclasses import dataclass


@dataclass
class Model:
    name: str
    input_schema: dict
    output_schema: dict
    status: str
    type: str
