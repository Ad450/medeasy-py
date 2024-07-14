from typing import Any

import argon2
import jwt
from datetime import datetime, timedelta, timezone
from application.dto import RoleDto
from infrastructure.env_configs import EnvironmentConfig


class AuthHelper:

    def hash_password(self, password: str) -> bytes:
        bpassword = f'b{password}'.encode()

        hashed_password = argon2.hash_password(bpassword)
        return hashed_password

    def generate_tokens(self, email: str, role: RoleDto) -> Any:
        return {
            "access_token": self.generate_access_token(email=email, role=role),
            "refresh_token": self.generate_refresh_token()
        }

    def generate_access_token(self, email: str, role: RoleDto):
        alg = EnvironmentConfig.get_env_variable(variable="JWT_ALG")
        secret = EnvironmentConfig.get_env_variable(variable="JWT_SECRET")
        expiry = EnvironmentConfig.get_env_variable(variable="JWT_EXPIRY")
        issuer = EnvironmentConfig.get_env_variable(variable="ISSUER")
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(hours=int(expiry))

        token = jwt.encode({
            "email": email,
            "role": role,
            "exp": expiration_time,
            "iss": issuer
        }, secret, algorithm=alg)
        if not token:
            raise Exception("Could not generate token")
        return str(token)

    def generate_refresh_token(self) -> str:
        refresh_expiry = EnvironmentConfig.get_env_variable(variable="JWT_EXPIRY")
        alg = EnvironmentConfig.get_env_variable(variable="JWT_ALG")
        secret = EnvironmentConfig.get_env_variable(variable="JWT_SECRET")
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(days=int(refresh_expiry))

        refresh_token = jwt.encode({"exp": expiration_time}, secret, algorithm=alg)
        return refresh_token
