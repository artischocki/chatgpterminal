import openai
from typing import Dict
import os

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalTrueColorFormatter

openai.organization = os.environ.get("MY_OPENAI_ORGANIZATION")
openai.api_key = os.environ.get("MY_OPENAI_API_KEY")

DEFAULT_MODEL = 'gpt-3.5-turbo'
DEFAULT_ROLE = "You are a helpful assistant."

class Conversation:
    def __init__(self, model: str = DEFAULT_MODEL, role: str = DEFAULT_ROLE, max_tokens: int = 300) -> None:
        self._model = model
        self._role = role
        self._max_tokens = max_tokens
        # messages are saved in a list that starts with the system instruction
        # of the role
        self._messages = [{"role": "system", "content": self._role}]

    def new_user_message(self, prompt: str) -> None:
        self._messages.append({"role": "user", "content": prompt})
        response = self._create_response()
        self._messages.append(response)
        self._print_message()

    def _create_response(self) -> Dict[str, str]:
        response = openai.ChatCompletion.create(
                model=self._model,
                max_tokens=self._max_tokens,
                messages=self._messages
                )
        return response.choices[0].message

    def _print_message(self, idx: int = -1) -> None:
        # check for code and highlight it
        message = self._messages[idx]["content"]
        # code starts with ```language and ends with ```, 
        # so split at `` so you can differentiate 
        # between the start of the code (`x) and the end (`)
        message_parts = message.split("``")
        if len(message_parts) == 1:
            # no code parts detected
            print("\n" + message)

        else:
            # code parts detected
            print("\n")
            for message_part in message_parts:
                if message_part[0] == "`" and message_part[1].isalpha():
                    language = message_part.splitlines()[0][1:]
                    lexer = get_lexer_by_name(language)
                    print(highlight("``" + message_part, lexer, TerminalTrueColorFormatter()))
                else:
                    print("``" + message_part)


    def save(self) -> None:
        pass

    def clear(self) -> None:
        del self._messages[1:]

    def _debug_messages(self) -> None:
        print(self._messages)

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


def system_dialogue(user_input: str, conversation: Conversation):
    if user_input == "help":
        with open(os.path.join("sys_dialogue", "help.txt"), "r") as f:
            print(f.read())
    elif user_input == "exit":
        conversation.save()
        exit()
    elif user_input == "new":
        conversation.save()
        conversation.clear()
    elif user_input == "model":
        print(f"Current model:\n{conversation.model}\n")
        with open(os.path.join("sys_dialogue", "model.txt"), "r") as f:
            print(f.read())
        while True:
            model_idx = input("model_idx:")
            if model_idx.isdigit():
                if int(model_idx) >= 0 and int(model_idx) < 4:
                    models = {"0": "gpt-3.5-turbo",
                              "1": "gpt-3.5-turbo-16k",
                              "2": "gpt-4",
                              "3": "gpt-4-32k"}
                    model = models[model_idx]
                    conversation.model = model
                    print(f"New model:\n{conversation.model}\n")
                    break
                else:
                    print("Input out of range!")
                    continue
            else:
                print("Invalid input! Try again.")
                continue
    elif user_input == "max_tokens":
        print(f"Current max_tokens:\n{conversation.max_tokens}\n")
        max_tokens = input("New max_tokens: ")
        conversation.max_tokens = max_tokens
    elif user_input == "correct":
        pass # todo
    elif user_input == "debug":
        conversation._debug_messages()


def main():
    conversation = Conversation()
    
    while True:
        user_input = input("\n> ")
        if user_input[0] == "/":
            system_dialogue(user_input[1:], conversation)
            continue
        conversation.new_user_message(user_input)


if __name__ == "__main__":
    main()
