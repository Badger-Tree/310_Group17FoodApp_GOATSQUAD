from abc import ABC, abstractmethod
import uuid
from datetime import datetime, timezone
from app.schemas.Role import UserRole
from app.schemas.User import CustomerCreate, StaffCreate


##abstract methods
class UserFactory(ABC):
    @abstractmethod
    def create_user(self, payload) -> dict:
        pass

    @staticmethod
    def create_base_user(payload, role: UserRole) -> dict:
        new_user = {"id":str(uuid.uuid4()), 
                    "email":payload.email.strip(), 
                    "first_name":payload.first_name.strip(), 
                    "last_name" : payload.last_name.strip(), 
                    "password" : payload.password.strip(), 
                    "role" : role.value,
                    "created_date": datetime.now(timezone.utc).isoformat()}
        return new_user

##concrete methods, could also put these in their own file like in prof's hotel demo?
class CustomerFactory(UserFactory):
    def create_user(self, payload: CustomerCreate) -> dict:
        user = self.create_base_user(payload, UserRole.CUSTOMER)
        # removed since saved_address isn't a list in the new user csv
        # user["saved_addresses"] = []
        return user

class StaffFactory(UserFactory):
    def create_user(self, payload: StaffCreate) -> dict:
        user = self.create_base_user(payload, UserRole.STAFF)
        return user