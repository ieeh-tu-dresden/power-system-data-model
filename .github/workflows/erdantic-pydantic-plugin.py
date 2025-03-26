# Code based on https://erdantic.drivendata.org/stable/extending/  # noqa: INP001
from html import escape
from pathlib import Path
from typing import Any
from typing import ClassVar
from typing import TypeGuard

import erdantic as erd
import pydantic
import pydantic_core
from erdantic.core import EntityRelationshipDiagram
from erdantic.core import FieldInfo
from erdantic.core import FullyQualifiedName
from erdantic.core import ModelInfo
from erdantic.core import SortedDict
from erdantic.exceptions import UnresolvableForwardRefError
from erdantic.plugins import register_plugin
from typenames import REMOVE_ALL_MODULES
from typenames import typenames

from psdm.base import AttributeData
from psdm.steadystate_case.case import Case as SteadystateCase
from psdm.topology.topology import Topology
from psdm.topology_case.case import Case as TopologyCase

PydanticModel = type[pydantic.BaseModel]


class FieldInfoWithDefault(FieldInfo):
    """Custom FieldInfo subclass that adds a 'default_value' field and diagram column."""

    default_value: str

    _dot_row_template = (
        """<tr>"""
        """<td>{name}</td>"""
        """<td>{type_name}</td>"""
        """<td port="{name}" width="36">{default_value}</td>"""
        """</tr>"""
    )

    @classmethod
    def from_raw_type(  # noqa: ANN206
        cls,
        model_full_name: FullyQualifiedName,
        name: str,
        raw_type: type,
        raw_default_value: Any,  # noqa: ANN401
    ):
        default_value = "" if raw_default_value is pydantic_core.PydanticUndefined else repr(raw_default_value)
        field_info = cls(
            model_full_name=model_full_name,
            name=name,
            type_name=typenames(raw_type, remove_modules=REMOVE_ALL_MODULES),
            default_value=default_value,
        )
        field_info._raw_type = raw_type  # noqa: SLF001
        return field_info

    def to_dot_row(self) -> str:
        return self._dot_row_template.format(
            name=self.name,
            type_name=self.type_name,
            default_value=escape(self.default_value),  # Escape HTML-unsafe characters
        )


class ModelInfoWithDefault(ModelInfo):
    """Custom ModelInfo subclass that uses FieldInfoWithDefault instead of FieldInfo."""

    fields: ClassVar[dict[str, FieldInfoWithDefault]] = {}


class EntityRelationshipDiagramWithDefault(EntityRelationshipDiagram):
    """Custom EntityRelationshipDiagram subclass that uses ModelInfoWithDefault instead of ModelInfo."""

    models: SortedDict[str, ModelInfoWithDefault] = SortedDict()


def is_pydantic_model(obj: Any) -> TypeGuard[PydanticModel]:  # noqa: ANN401
    """Predicate function to determine if an object is a Pydantic model (not an instance).

    Also excludes AttributeData from being considered a Pydantic model in context of erdantic schema graph.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object is a Pydantic model, False otherwise.
    """
    if isinstance(obj, type) and obj.__name__ == AttributeData.__name__:
        return False
    return isinstance(obj, type) and issubclass(obj, pydantic.BaseModel)


def get_fields_from_pydantic_model_with_default(
    model: pydantic.BaseModel,
) -> list[FieldInfoWithDefault]:
    """Copied from erdantic.plugins.pydantic.get_fields_from_pydantic_model and modified to extract default values of fields."""
    try:
        # Rebuild model schema to resolve forward references
        model.model_rebuild()
    except pydantic.errors.PydanticUndefinedAnnotation as e:
        model_full_name = FullyQualifiedName.from_object(model)
        forward_ref = e.name
        msg = (
            f"Failed to resolve forward reference '{forward_ref}' in the type annotations for "
            f"Pydantic model {model_full_name}. "
            "You should use the model's model_rebuild() method to manually resolve it."
        )
        raise UnresolvableForwardRefError(
            msg,
            name=forward_ref,
            model_full_name=model_full_name,
        ) from e

    return [
        FieldInfoWithDefault.from_raw_type(
            model_full_name=FullyQualifiedName.from_object(model),
            name=name,
            # typing special forms currently get typed as object
            # https://github.com/python/mypy/issues/9773
            raw_type=pydantic_field_info.annotation or Any,  # type: ignore [arg-type]
            raw_default_value=pydantic_field_info.default,
        )
        for name, pydantic_field_info in model.model_fields.items()
    ]


if __name__ == "__main__":
    # Register this plugin. Will override erdantic's built-in 'pydantic' plugin.
    register_plugin(
        "pydantic",
        is_pydantic_model,
        get_fields_from_pydantic_model_with_default,
    )

    # Generate the erdantic schema graphs (entity relationship diagrams) for the Topology, TopologyCase, and SteadystateCase models
    f_top = Path("./docs/entity_rel__topology.png")
    f_top.parent.mkdir(exist_ok=True, parents=True)
    erd.create(Topology).draw(f_top)
    f_topc = Path("./docs/entity_rel__topology_case.png")
    f_topc.parent.mkdir(exist_ok=True, parents=True)
    erd.create(TopologyCase).draw(f_topc)
    f_ssc = Path("./docs/entity_rel__steady_state_case.png")
    f_ssc.parent.mkdir(exist_ok=True, parents=True)
    erd.create(SteadystateCase).draw(f_ssc)
