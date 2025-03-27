import hashlib
import secrets

class User:
    def __init__(self, id, username, email, password_hash=None):
        """Modelo de usuário para autenticação"""
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
    
    @staticmethod
    def hash_password(password, salt=None):
        """Gera um hash seguro para a senha usando SHA-256"""
        if salt is None:
            salt = secrets.token_hex(16)
        salted_password = password + salt
        password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        return password_hash, salt
    
    def verify_password(self, password, salt):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        new_hash, _ = self.hash_password(password, salt)
        return new_hash == self.password_hash