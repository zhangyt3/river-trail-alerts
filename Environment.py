import os


class Environment:
    def get(self, var: str) -> str:
        return os.environ[var]

