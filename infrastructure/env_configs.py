import os

from dotenv import load_dotenv


class EnvironmentConfig:

    @staticmethod
    def get_env_variable(variable:str):
        load_dotenv()
        result = os.getenv(variable)
        if not result:
            raise Exception(f"Environmental variable: {variable} not found")
        return result