# -*- coding: utf-8 -*-
"""Shared normalization utilities for saved-output evaluation."""
import re
import unicodedata
import pandas as pd


def normalize_text(value, remove_space=True):
    if pd.isna(value):
        return ""
    s = unicodedata.normalize("NFKC", str(value)).strip()
    s = s.replace("ㆍ", "·")
    if remove_space:
        s = re.sub(r"\s+", "", s)
    return s.lower()


def split_items(value):
    if pd.isna(value) or str(value).strip() == "":
        return []
    s = str(value).replace("\n", "|")
    return [x.strip() for x in re.split(r"[|]", s) if x.strip()]
