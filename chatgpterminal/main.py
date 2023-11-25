import os

from colorama import Fore, Back, Style

from .conversation import Conversation


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
    user_prompt = Back.BLUE + Fore.BLACK + " You " \
                + Back.BLACK + Fore.BLUE + "\ue0b0 " + Style.RESET_ALL
    gpt_prompt = Back.GREEN + Fore.BLACK + " GPT " \
               + Back.BLACK + Fore.GREEN + "\ue0b0 " + Style.RESET_ALL
    try:
        while True:
            print()
            user_input = input(user_prompt)
            print()
            if user_input[0] == "/":
                system_dialogue(user_input[1:], conversation)
                continue
            print(gpt_prompt, end="")
            conversation.new_user_message(user_input)
    except EOFError:
        # listen for CTRL + D
        conversation.save()
        exit()


if __name__ == "__main__":
    main()
