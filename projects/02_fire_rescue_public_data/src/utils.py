"""Utility functions for the Seoul rescue activity analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd


# Column names in the original CSV (Korean)
COL_REPORT_DATE = "신고년월일"
COL_REPORT_TIME = "신고시각"
COL_DISPATCH_DATE = "출동년월일"
COL_DISPATCH_TIME = "출동시각"
COL_CITY = "발생장소_시"
COL_DISTRICT = "발생장소_구"
COL_NEIGHBORHOOD = "발생장소_동"
COL_CAUSE = "사고원인"
COL_CATEGORY = "사고원인코드명_사고종별"


@dataclass(frozen=True)
class QCConfig:
    """Basic quality-control thresholds for dispatch delay."""
    min_delay_min: float = 0.0
    max_delay_min: float = 120.0  # treat beyond this as outliers for 'typical delay' summaries


def load_seoul_data(csv_path: Path) -> pd.DataFrame:
    """Load the prepared Seoul-only CSV (UTF-8)."""
    df = pd.read_csv(csv_path)
    return df


def _parse_datetime(date_series: pd.Series, time_series: pd.Series) -> pd.Series:
    """Combine date and time strings into a pandas datetime series."""
    return pd.to_datetime(date_series.astype(str) + " " + time_series.astype(str), errors="coerce")


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create datetime and delay features."""
    df = df.copy()
    df["report_dt"] = _parse_datetime(df[COL_REPORT_DATE], df[COL_REPORT_TIME])
    df["dispatch_dt"] = _parse_datetime(df[COL_DISPATCH_DATE], df[COL_DISPATCH_TIME])

    df["dispatch_delay_min"] = (
        (df["dispatch_dt"] - df["report_dt"]).dt.total_seconds() / 60.0
    )

    df["month"] = df["report_dt"].dt.to_period("M").astype(str)
    df["hour"] = df["report_dt"].dt.hour
    df["dow"] = df["report_dt"].dt.day_name()

    return df


def apply_basic_qc(df: pd.DataFrame, cfg: QCConfig = QCConfig()) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split data into (clean, excluded) based on simple dispatch-delay rules."""
    mask = (df["dispatch_delay_min"] >= cfg.min_delay_min) & (df["dispatch_delay_min"] <= cfg.max_delay_min)
    clean = df.loc[mask].copy()
    excluded = df.loc[~mask].copy()
    return clean, excluded


def category_translation_map() -> Dict[str, str]:
    """English translations for the most common categories (not exhaustive)."""
    return {
        "기타화재": "Other fire-related",
        "소방시설 오작동": "Fire system malfunction",
        "기타 안전조치": "Other safety assistance",
        "기타": "Other (unspecified)",
        "기타 수난": "Other water rescue",
        "벌집제거(기타벌)": "Wasp nest removal",
        "문 개방": "Door opening",
        "신변확인": "Welfare check",
        "실화": "Accidental fire",
        "승객용승강기": "Passenger elevator",
        "개": "Dog-related",
        "기타 승강기": "Other elevator",
    }


def translate_categories(series: pd.Series) -> pd.Series:
    m = category_translation_map()
    return series.map(lambda x: m.get(x, x))
