#!/usr/bin/env python3
import re

from pathlib import Path


def _coerce_asset_name(name):
  if isinstance(name, (bytes, bytearray)):
    name = name.decode("utf-8", "ignore")
  return str(name or "").strip()


def canonicalize_theme_asset_name(name):
  text = Path(_coerce_asset_name(name)).stem.lower()
  tokens = [token for token in re.findall(r"[a-z0-9]+", text) if token != "by"]
  return "".join(tokens)


def find_matching_theme_asset_name(candidates, requested_name):
  requested_raw = Path(_coerce_asset_name(requested_name)).stem.lower()
  requested_key = canonicalize_theme_asset_name(requested_name)

  for candidate in candidates:
    candidate_raw = Path(_coerce_asset_name(candidate)).stem.lower()
    if candidate_raw == requested_raw:
      return candidate

  for candidate in candidates:
    if canonicalize_theme_asset_name(candidate) == requested_key:
      return candidate

  return None


def find_matching_theme_asset_file(directory, requested_name):
  directory = Path(directory)
  if not directory.is_dir():
    return None

  candidates = sorted(file for file in directory.iterdir() if file.is_file())
  matched_name = find_matching_theme_asset_name([file.stem for file in candidates], requested_name)
  if matched_name is None:
    return None

  matched_path = directory / matched_name
  if matched_path.is_file():
    return matched_path

  matched_stem = Path(matched_name).stem
  for file in candidates:
    if file.stem == matched_stem:
      return file

  return None
