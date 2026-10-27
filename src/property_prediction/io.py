"""Reading and writing compound files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_smiles_json(path: Path, smiles_column: str = "smiles") -> pd.DataFrame:
    """Load records keyed by source ID into a (source_id, smiles) frame."""
    frame = pd.read_json(path, orient="index")
    if smiles_column not in frame.columns:
        raise ValueError(f"{path.name} has no {smiles_column!r} column; found {list(frame.columns)}")

    frame = frame[[smiles_column]].rename_axis("source_id").reset_index()
    return frame[frame[smiles_column].astype(str).str.strip().ne("")]


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    """Write a frame, creating the parent directory if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
