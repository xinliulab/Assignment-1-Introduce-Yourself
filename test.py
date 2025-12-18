"""
Tests for Assignment 1 – Introduce Yourself
Run with:  pytest
"""

import json
import os
import re
import pytest

PROFILE_FILE = "profile.json"

REQUIRED_FIELDS = {
    "name": str,
    "student_id": str,
    "hobbies": list,
    "expectation": str,
    "bio": str,
    "photo": str,
}


@pytest.fixture(scope="session")
def profile_data():
    """Load profile.json once for all tests."""
    assert os.path.isfile(PROFILE_FILE), f"{PROFILE_FILE} not found."
    with open(PROFILE_FILE, "r", encoding="utf-8") as fp:
        try:
            return json.load(fp)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{PROFILE_FILE} is not valid JSON: {exc}")


def test_required_fields_present(profile_data):
    missing = [k for k in REQUIRED_FIELDS if k not in profile_data]
    assert not missing, f"Missing required field(s): {', '.join(missing)}"


def test_field_types(profile_data):
    for field, expected_type in REQUIRED_FIELDS.items():
        assert isinstance(
            profile_data[field], expected_type
        ), f"Field '{field}' must be of type {expected_type.__name__}"


def test_hobbies_non_empty(profile_data):
    hobbies = profile_data["hobbies"]
    assert hobbies, "hobbies list cannot be empty."
    assert all(isinstance(h, str) and h.strip() for h in hobbies), (
        "Each hobby must be a non‑empty string."
    )


def test_student_id_format(profile_data):
    sid = profile_data["student_id"]
    assert re.fullmatch(r"\d{5,6}", sid), (
        "student_id must be a 5‑ or 6‑digit numeric string."
    )


def test_bio_sentence_count(profile_data):
    bio = profile_data["bio"].strip()
    sentences = [s for s in re.split(r"[.!?]", bio) if s.strip()]
    assert 1 <= len(sentences) <= 10, "bio should contain between 1 and 10 sentences."


def test_photo_file_exists(profile_data):
    photo = profile_data["photo"]
    assert re.fullmatch(r".+\.(jpg|jpeg|png)", photo, re.IGNORECASE), (
        "photo must reference a .jpg, .jpeg, or .png file."
    )
    assert os.path.isfile(photo), f"Photo file '{photo}' not found in repository root."
