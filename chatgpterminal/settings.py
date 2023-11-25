from typing import Dict, Any, List

from blessed import Terminal

# All Settings fields and their options
FIELDS = {
        "max_tokens": range(1000, 10000),
        "model": [""]
        }



class Settings():
    """
    This class handles all possible settings and offers a tui selector
    """
    def __init__(self, fields: Dict[str, Any]) -> None:
        """
        fields: all possible settings
        """
        # Create a terminal instance
        self._term = Terminal()
        self._fields = fields

    def select(self) -> None:
        # Keep track of the selected field
        current_field = 0
        with self._term.fullscreen(), self._term.cbreak(), self._term.hidden_cursor():
            while True:
                # Clear the terminal
                print(self._term.clear())

                # Display the fields
                for i, (name, value) in enumerate(self._fields.items()):
                    # Highlight the selected field
                    field_str = f"> {name}: {value}" if i == current_field else f"  {name}: {value}"
                    print(self._term.move_yx(self._term.height // 2 + i, self._term.width // 2 - len(name) // 2) + field_str)

                # Get user input
                with self._term.cbreak():
                    key = self._term.inkey()

                if key.code == self._term.KEY_DOWN:
                    current_field = (current_field + 1) % len(self._fields)

                elif key.code == self._term.KEY_UP:
                    current_field = (current_field - 1) % len(self._fields)
                elif key == "\n":
                    # Handle the field selection
                    field = list(self._fields.keys())[current_field]

                    if isinstance(self._fields[field], bool):
                        self._fields[field] = not self._fields[field]
                    elif isinstance(self._fields[field], str):
                        value = input("Enter a value: ")
                        self._fields[field] = value.strip()
                    elif isinstance(self._fields[field], int):
                        value = input("Enter an integer value: ")
                        try:
                            self._fields[field] = int(value.strip())
                        except ValueError:
                            pass



class BaseField():
    def __init__(self, value: Any) -> None:
        raise NotImplementedError

    @property
    def value(self) -> Any:
        raise NotImplementedError

    def on_select(self) -> Any:
        raise NotImplementedError


class IntField(BaseField):
    def __init__(self, value: int, options: List[int]) -> None:
        if not isinstance(value, int):
            raise ValueError
        self._value = value
        self._options = options

    @property
    def value(self) -> int:
        return self._value

    def on_select(self) -> None:
        value = input("Enter an integer value: ")
        if not value in self._options:
            self.on_select()
        try:
            self._value = int(value.strip())
        except ValueError:
            self.on_select()


class StrField(BaseField):
    def __init__(self, value: str, options: List[str]) -> None:
        if not isinstance(value, str):
            raise ValueError
        self._value = value
        self._options = options

    @property
    def value(self) -> str:
        return self._value

    def on_select(self) -> None:
        value = input("Enter a value: ")
        if not value in self._options:
            self.on_select()
        self._value = value.strip()


class BoolField(BaseField):
    def __init__(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError
        self._value = value

    @property
    def value(self) -> bool:
        return self._value

    def on_select(self) -> None:
        self._value = not self._value


