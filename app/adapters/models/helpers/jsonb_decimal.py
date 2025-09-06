import json
from decimal import Decimal
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import TypeDecorator


class JSONBWithDecimal(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value, default=self._decimal_encoder)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value, parse_float=Decimal)
        return value

    def _decimal_encoder(self, obj):
        if isinstance(obj, Decimal):
            # Convert Decimal to a float
            return float(obj)
        # Fallback for other types
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )
