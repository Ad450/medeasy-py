from typing import Optional

from application.dto import RegisterUserDto, RoleDto, LoginUserDto
from application.utils.auth_helper import AuthHelper
from domain.enums import Role
from domain.models import User
from infrastructure.base_repository import BaseRepository
from fastapi import HTTPException


class AuthenticationService:
    @property
    def __user_repository(self) -> BaseRepository:
        return BaseRepository(User)

    @property
    def __auth_helper(self) -> AuthHelper:
        return AuthHelper()

    def register(self, dto: RegisterUserDto) -> User:
        is_existing_user = self.__user_repository.get_by_email(email=dto.email)
        if is_existing_user:
            raise HTTPException(status_code=401, detail="user already exists")

        new_user = User(
            email= dto.email,
            password = self.__auth_helper.hash_password(dto.password),
            role = self.__get_role_from_dto(dto.role)
        )
        user_created = self.__user_repository.save(new_user)
        if not user_created:
            raise HTTPException(status_code=500, detail="could not create user")
        return user_created

    def __get_role_from_dto(self, dto: RoleDto) -> Optional[Role]:
        if dto == RoleDto.ALL:
            return Role.ALL
        elif dto == RoleDto.PATIENT:
            return Role.PATIENT
        elif dto == RoleDto.PRACTITIONER:
            return Role.PRACTITIONER
        else:
            raise HTTPException(status_code=404, detail="role not found")

    def login(self, dto: LoginUserDto):
        existing_user = self.__user_repository.get_by_email(email=dto.email)
        if not existing_user:
            raise HTTPException(status_code=404, detail="user not found")

        if self.__auth_helper.hash_password(dto.password) != existing_user.password:
            raise HTTPException(status_code=401, detail="password does not match")

        return self.__auth_helper.generate_tokens(email=dto.email, role=existing_user.role)

