import sys

FLAG_NO_FLAG = ""
PREFIX_FLAG = "-"


class ArgsParser:
    def __init__(self, sys_args: list[str]):
        current_flag = FLAG_NO_FLAG
        current_args = []
        self.__args = {}

        for token in sys_args:
            if self.__is_flag(token):
                self.__append_flag_and_args(current_flag, current_args)
                current_flag = token
                current_args.clear()
                continue

            current_args.append(token)

        self.__append_flag_and_args(current_flag, current_args)

    def is_empty(self):
        return len(self.__args) == 0

    def has_flag(self, key: str):
        return key in self.__args and len(self.__args[key]) == 0

    def get_string(self, key: str, def_value: str = None) -> str:
        if key not in self.__args:
            if def_value is None:
                raise RuntimeError(f"Key {key} was not presented in the cli")
            
            return def_value

        key_args = self.__args[key]

        if len(key_args) != 1:
            raise RuntimeError(
                f"Got more values ({len(key_args)}) than expected"
            )

        return key_args[0]

    def __append_flag_and_args(self, flag: str, args: list[str]):
        if flag in self.__args:
            raise RuntimeError(
                f"Flag {flag} has been at least twice on the input"
            )

        if len(args) == 0:
            return

        self.__args[flag] = args

    def __is_flag(self, token: str):
        return token.startswith(PREFIX_FLAG)

    def __str__(self) -> str:
        return f"ArgsParser{{args={self.__args}}}"


def create_parser_for_cli() -> ArgsParser:
    # skipping the first entry
    # as it is the python script's name
    sys_args = sys.argv[1:]
    return ArgsParser(sys_args)
