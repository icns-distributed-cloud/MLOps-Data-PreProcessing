"""

"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
from collections import OrderedDict
from enum import Enum

# todo: 상대경로나 절대경로로 model_context.py 모듈
# from {} import Variable, Variables, Model, ModelContext
from .model_context import Variable, Variables, Model, ModelContext


class ModelType(Enum):
    LSTM = "LSTM"


class ModelContextBuilder:
      # todo: 모델 type 많아지면 enum으로 관리

    def __init__(self):
        self.feature_id: str = None
        self.x: List[Variable] = []
        self.y: Variable = None
        self.model_type: str = None
        self.hyperparameter: Optional[Dict[str, Any]] = None
        self.state_dict: OrderedDict = None  # only pytorch

    def set_feature_id(self, feature_id: str) -> ModelContextBuilder:
        if not isinstance(feature_id, str):
            raise TypeError("feature id must be string")
        self.feature_id = feature_id
        return self

    def add_x_i(self, x_i: Variable) -> ModelContextBuilder:
        self.x.append(x_i)
        return self

    def set_y(self, y: Variable) -> ModelContextBuilder:
        self.y = y
        return self

    def set_model_type(self, model_type: ModelType) -> ModelContextBuilder:
        self.model_type = model_type.value
        return self

    def set_model_hyperparameter(self, hyperparameter: Dict[str, Any]) -> ModelContextBuilder:
        if not isinstance(hyperparameter, dict):
            raise TypeError("hyperparameter must be dictionary")
        self.hyperparameter = hyperparameter
        return self

    def set_model_state_dict(self, state_dict: OrderedDict) -> ModelContextBuilder:
        if not isinstance(state_dict, OrderedDict):
            raise TypeError("State dict must be torch's state dict(OrderedDict in Python)")
        self.state_dict = state_dict
        return self

    def build(self) -> ModelContext:
        self.__validate_fulfillment_raise_exception_when_required_field_is_none()
        variables = Variables(self.x, self.y)
        model = Model(self.model_type, self.hyperparameter, self.state_dict)
        return ModelContext(self.feature_id, variables, model)

    def __validate_fulfillment_raise_exception_when_required_field_is_none(self):
        if self.feature_id is None: raise ValueError("feature id has not been set")
        if len(self.x) == 0: raise ValueError("variable x has not been added")
        if self.y is None: raise ValueError("variable y has not been set")
        if self.model_type is None: raise ValueError("model type has not been set")
        if self.state_dict is None: raise ValueError("state dict has not been set")
