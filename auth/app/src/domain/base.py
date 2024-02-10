"""Module with base domain classes."""

from __future__ import annotations

import uuid
from abc import ABC

import pydantic as pd


class BaseDTO(pd.BaseModel, from_attributes=True):
    """Base Data Transfer Object (DTO)."""

    id: uuid.UUID


class Base(ABC):
    """Base represent of object which provides methods for work with DTO."""
