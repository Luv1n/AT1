import hashlib

class User():
    def __init__(self, email, first_name, last_name, password_input):
        self.email = email
        self.first_name = first_name
        self.last_name = first_name
        self.password_hash = self.hash_password(password_input) 
        self.token = self.generate_token(email)

    def generate_token(self, email):
        return self.email
    
    def revoke_token(self):
        self.token = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password_input):
        return self.password_hash == self.hash_password(password_input)

    def user_data(self): 
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
