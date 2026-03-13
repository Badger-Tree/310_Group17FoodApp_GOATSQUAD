from abc import ABC, abstractmethod
import uuid
from datetime import datetime, timezone
from app.schemas.Role import UserRole
from app.schemas.User import CustomerCreate, StaffCreate


class UserFactory(ABC):
    @abstractmethod
    def create_user(self, payload) -> dict:
        pass

    @staticmethod
    def create_base_user(payload, role: UserRole) -> dict:
        """abstract class to create a base user, used by CustomerFactory and StaffFactory to create those specific types"""
        new_user = {"id":str(uuid.uuid4()), 
                    "email":payload.email.strip(), 
                    "first_name":payload.first_name.strip(), 
                    "last_name" : payload.last_name.strip(), 
                    "password" : payload.password.strip(), 
                    "role" : role.value,
                    "created_date": datetime.now(timezone.utc).isoformat()}
        return new_user

class CustomerFactory(UserFactory):
    def create_user(self, payload: CustomerCreate) -> dict:
        """creates an instance of a customer"""
        user = self.create_base_user(payload, UserRole.CUSTOMER)
        return user

class StaffFactory(UserFactory):
    def create_user(self, payload: StaffCreate) -> dict:
        """creates an instance of a staff user"""
        user = self.create_base_user(payload, UserRole.STAFF)
        return user