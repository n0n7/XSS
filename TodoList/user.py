from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, uid, email):
        self.uid = uid
        self.email = email

    def is_active(self):
        return True  # You can customize this to deactivate users if needed

    def get_id(self):
        return str(self.uid)
    
    def get_email(self):
        return str(self.email)