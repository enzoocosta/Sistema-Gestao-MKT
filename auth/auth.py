from .models import User
from database.operations import DBOperations
import streamlit as st
import secrets
import extra_streamlit_components as stx
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self):
        """Gerenciador de autenticação de usuários"""
        self.db_ops = DBOperations()
        self.current_user = None
        self.cookie_manager = stx.CookieManager()
    
    def register_user(self, username, email, password):
        """Registra um novo usuário no sistema"""
        # Verifica se o usuário já existe
        if self.db_ops.get_user_by_username(username):
            st.error("Nome de usuário já está em uso!")
            return False
        
        # Gera hash da senha
        password_hash, salt = User.hash_password(password)
        # Adiciona o salt ao hash para armazenamento
        stored_hash = f"{salt}${password_hash}"
        
        # Cria o usuário no banco de dados
        if self.db_ops.create_user(username, email, stored_hash):
            st.success("Usuário registrado com sucesso! Faça login para continuar.")
            return True
        else:
            st.error("Erro ao registrar usuário.")
            return False
    
    def login_user(self, username, password, remember_me=False):
        """Autentica um usuário no sistema"""
        user_data = self.db_ops.get_user_by_username(username)
        if not user_data:
            st.error("Usuário não encontrado!")
            return False
        
        # Extrai o salt e o hash armazenado
        stored_hash_parts = user_data['password'].split('$')
        if len(stored_hash_parts) != 2:
            st.error("Erro no formato da senha armazenada!")
            return False
        
        salt, stored_hash = stored_hash_parts
        user = User(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            password_hash=stored_hash
        )
        
        # Verifica a senha
        if user.verify_password(password, salt):
            self.current_user = user
            st.session_state['authenticated'] = True
            st.session_state['user_id'] = user.id
            st.session_state['username'] = user.username
            
            # Configura cookie se "Lembrar de mim" estiver marcado
            if remember_me:
                self._set_remember_me_cookie(username)
            
            st.rerun()
            return True
        else:
            st.error("Senha incorreta!")
            return False
    
    def _set_remember_me_cookie(self, username):
        """Configura cookie para lembrar o usuário"""
        try:
            self.cookie_manager.set(
                'remember_me',
                username,
                expires_at=datetime.now() + timedelta(days=30)
            )
        except:
            st.warning("Não foi possível configurar o cookie 'Lembrar de mim'")
    
    def _get_remembered_user(self):
        """Obtém usuário lembrado pelo cookie"""
        try:
            return self.cookie_manager.get('remember_me')
        except:
            return None
    
    def check_remembered_user(self):
        """Verifica se há um usuário lembrado e preenche o formulário"""
        remembered_user = self._get_remembered_user()
        if remembered_user:
            return remembered_user
        return ""
    
    def logout_user(self):
        """Desconecta o usuário atual"""
        self.current_user = None
        st.session_state['authenticated'] = False
        st.session_state['user_id'] = None
        st.session_state['username'] = None
        # Remove o cookie ao fazer logout
        try:
            self.cookie_manager.delete('remember_me')
        except:
            pass
        st.experimental_rerun()
    
    def is_authenticated(self):
        """Verifica se há um usuário autenticado"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user_id(self):
        """Retorna o ID do usuário autenticado"""
        return st.session_state.get('user_id')
    
    def get_current_username(self):
        """Retorna o nome de usuário autenticado"""
        return st.session_state.get('username')