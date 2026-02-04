from dataclasses import dataclass

@dataclass(frozen=True)
class PipelineConfig:
    input_path: str
    output_path: str

    shuffle_partitions: int = 16
