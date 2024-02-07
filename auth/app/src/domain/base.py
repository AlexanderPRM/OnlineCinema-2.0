"""Module with base domain classes."""

import uuid
from abc import ABC, abstractmethod

import pydantic as pd


class BaseDTO(pd.BaseModel, from_attributes=True):
    """Base Data Transfer Object (DTO)."""

    id: uuid.UUID


class Base(ABC):
    """Base represent of object which provides methods for work with DTO."""

    @classmethod
    @abstractmethod
    def create(cls, entity: BaseDTO):
        """Create instance of representing class.

        Args:
            entity (BaseDTO): Entity of data transfer object.

        Returns:
            Base: Return new instance of class.
        """
