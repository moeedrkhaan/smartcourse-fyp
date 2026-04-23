"""
Fetch and clean course dataset for SmartCourse.

Usage examples:
  python data/fetch_and_clean.py --source-file data/raw/courses.csv
  python data/fetch_and_clean.py --source-url "https://example.com/courses.csv"

Outputs:
  - data/processed/courses_cleaned.csv
  - data/courses.json (API/model ready)
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


COLUMN_ALIASES: Dict[str, List[str]] = {
    "id": ["id", "course_id", "courseid", "course id"],
    "title": ["title", "course_title", "course name", "course", "name"],
    "provider": ["provider", "university", "institution", "platform"],
    "department": ["department", "category", "subject", "domain"],
    "description": [
        "description",
        "course_description",
        "summary",
        "about",
        "details",
    ],
    "level": ["level", "difficulty", "difficulty_level", "course level"],
    "rating": ["rating", "course_rating", "stars", "score", "num_reviews", "reviews"],
    "duration": ["duration", "course_duration", "length", "content_duration"],
    "students": ["students", "enrollments", "learners", "subscribers", "num_subscribers"],
    "url": ["url", "link", "course_url"],
    "tags": ["tags", "skills", "keywords", "topics"],
}


def build_description(row: pd.Series, col_map: Dict[str, str]) -> str:
    """Create a useful fallback description when raw description is unavailable."""
    parts: List[str] = []

    title_col = col_map.get("title")
    department_col = col_map.get("department")
    level_col = col_map.get("level")
    duration_col = col_map.get("duration")

    if title_col:
        title = clean_text(row.get(title_col, ""))
        if title:
            parts.append(f"Course: {title}.")

    if department_col:
        department = clean_text(row.get(department_col, ""))
        if department:
            parts.append(f"Category: {department}.")

    if level_col:
        level = clean_text(row.get(level_col, ""))
        if level:
            parts.append(f"Level: {level}.")

    if duration_col:
        duration = clean_text(row.get(duration_col, ""))
        if duration:
            parts.append(f"Duration: {duration}.")

    if not parts:
        parts.append("General online course.")

    return " ".join(parts).strip()


def normalize_col(col: str) -> str:
    return re.sub(r"\s+", " ", col.strip().lower())


def resolve_columns(df: pd.DataFrame) -> Dict[str, str]:
    normalized = {normalize_col(c): c for c in df.columns}
    resolved: Dict[str, str] = {}

    for target, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                resolved[target] = normalized[alias]
                break

    return resolved


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = re.sub(r"[^\w\s.,:;!?()'\"/-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_tags(value: object) -> List[str]:
    if pd.isna(value):
        return []

    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]

    text = str(value).strip()
    if not text:
        return []

    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except Exception:
            pass

    for sep in ["|", ",", ";"]:
        if sep in text:
            return [p.strip() for p in text.split(sep) if p.strip()]

    return [text]


def fetch_dataset(source_file: str | None, source_url: str | None) -> pd.DataFrame:
    if source_file:
        path = Path(source_file)
        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {source_file}")
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() == ".json":
            return pd.read_json(path)
        raise ValueError("Unsupported source file format. Use CSV or JSON.")

    if source_url:
        lower_url = source_url.lower()
        if lower_url.endswith(".csv"):
            return pd.read_csv(source_url)
        if lower_url.endswith(".json"):
            return pd.read_json(source_url)
        raise ValueError("Unsupported source URL format. Use a .csv or .json URL.")

    raise ValueError("Provide either --source-file or --source-url")


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Dataset is empty")

    col_map = resolve_columns(df)

    required = ["title"]
    missing = [c for c in required if c not in col_map]
    if missing:
        raise ValueError(f"Missing required source columns for: {', '.join(missing)}")

    out = pd.DataFrame()

    if "id" in col_map:
        out["id"] = df[col_map["id"]].astype(str).str.strip()
    else:
        out["id"] = [str(i + 1) for i in range(len(df))]

    out["title"] = df[col_map["title"]].apply(clean_text)
    if "description" in col_map:
        out["description"] = df[col_map["description"]].apply(clean_text)
    else:
        out["description"] = df.apply(lambda row: build_description(row, col_map), axis=1)

    out["provider"] = (
        df[col_map["provider"]].apply(clean_text)
        if "provider" in col_map
        else "Unknown Provider"
    )
    out["department"] = (
        df[col_map["department"]].apply(clean_text)
        if "department" in col_map
        else "General"
    )
    out["level"] = (
        df[col_map["level"]].apply(clean_text)
        if "level" in col_map
        else "Not specified"
    )
    out["duration"] = (
        df[col_map["duration"]].apply(clean_text)
        if "duration" in col_map
        else "Self-paced"
    )
    out["students"] = (
        df[col_map["students"]].apply(clean_text)
        if "students" in col_map
        else "N/A"
    )

    if "rating" in col_map:
        out["rating"] = pd.to_numeric(df[col_map["rating"]], errors="coerce").fillna(0.0)
    else:
        out["rating"] = 0.0

    out["rating"] = out["rating"].clip(lower=0.0, upper=5.0)

    if "url" in col_map:
        out["url"] = df[col_map["url"]].apply(clean_text)
    else:
        out["url"] = ""

    # Common fallback for platform datasets that only have URL and no provider.
    if "provider" not in col_map:
        out.loc[out["url"].str.contains("udemy", case=False, na=False), "provider"] = "Udemy"

    if "tags" in col_map:
        out["tags"] = df[col_map["tags"]].apply(parse_tags)
    else:
        out["tags"] = [[] for _ in range(len(out))]

    out = out[(out["title"] != "") & (out["description"] != "")].copy()

    dedupe_key = (
        out["title"].str.lower().str.strip() + "||" + out["description"].str.lower().str.strip()
    )
    out = out.loc[~dedupe_key.duplicated()].copy()

    out["id"] = [str(i + 1) for i in range(len(out))]

    out = out[
        [
            "id",
            "title",
            "provider",
            "department",
            "description",
            "level",
            "duration",
            "students",
            "rating",
            "url",
            "tags",
        ]
    ]

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and clean SmartCourse dataset")
    parser.add_argument("--source-file", type=str, default=None, help="Path to local CSV/JSON")
    parser.add_argument("--source-url", type=str, default=None, help="CSV/JSON URL")
    parser.add_argument(
        "--output-csv",
        type=str,
        default="data/processed/courses_cleaned.csv",
        help="Cleaned CSV output path",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default="data/courses.json",
        help="Model/API ready JSON output path",
    )
    args = parser.parse_args()

    raw_df = fetch_dataset(args.source_file, args.source_url)
    cleaned_df = clean_dataset(raw_df)

    output_csv = Path(args.output_csv)
    output_json = Path(args.output_json)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)

    cleaned_df.to_csv(output_csv, index=False, encoding="utf-8")
    output_json.write_text(cleaned_df.to_json(orient="records", force_ascii=False), encoding="utf-8")

    print("=" * 60)
    print("SmartCourse Data Pipeline Completed")
    print("=" * 60)
    print(f"Raw rows:     {len(raw_df)}")
    print(f"Clean rows:   {len(cleaned_df)}")
    print(f"Output CSV:   {output_csv}")
    print(f"Output JSON:  {output_json}")
    print("=" * 60)


if __name__ == "__main__":
    main()
