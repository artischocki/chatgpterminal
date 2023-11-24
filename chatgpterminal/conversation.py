from typing import List
import os

import openai

from .message import Message, Prompt, Response

openai.organization = os.environ.get("OPENAI_ORGANIZATION")
openai.api_key = os.environ.get("OPENAI_API_KEY")

DEFAULT_MODEL = 'gpt-3.5-turbo'

class Conversation:
    def __init__(
            self,
            model: str = DEFAULT_MODEL,
            max_tokens: int = 1000,
            ) -> None:
        self._model = model
        self._max_tokens = max_tokens
        # messages are saved in a list that starts with the system instruction
        # of the role
        starting_message = Message()
        self._messages = [starting_message]


    def new_user_message(self, prompt: str) -> None:
        user_message = Prompt(content=prompt)
        self._messages.append(user_message)
        response = Response(self._model, self._max_tokens, self.as_list())
        self._messages.append(response)


    def as_list(self) -> List[str]:
        messages_as_list = []
        for message in self._messages:
            messages_as_list.append({"role": message.role, "content": message.content})
        return messages_as_list


    def save(self) -> None:
        pass

    def clear(self) -> None:
        del self._messages[1:]

    def _debug_messages(self) -> None:
        print(self._messages)

    def change_last_message(self) -> None:
        del self._messages[-2:]

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value):
        self._max_tokens = value
