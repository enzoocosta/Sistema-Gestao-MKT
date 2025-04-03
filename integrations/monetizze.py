from typing import Dict, Any
from .base import BasePlatformIntegration
import hashlib
from datetime import datetime, date, timedelta

class MonetizzeIntegration(BasePlatformIntegration):
    PLATFORM_NAME = 'Monetizze'
    BASE_URL = 'https://api.monetizze.com.br/2.1/'
    
    def _default_headers(self) -> Dict[str, str]:
        headers = super()._default_headers()
        headers['Authorization'] = self._generate_auth_header()
        return headers
    
    def _generate_auth_header(self) -> str:
        """Monetizze usa hash MD5 de email+token+data"""
        email = self.credentials['email']
        token = self.credentials['api_token']
        current_date = datetime.now().strftime('%Y-%m-%d')
        hash_str = f"{email}{token}{current_date}"
        hash_md5 = hashlib.md5(hash_str.encode()).hexdigest()
        return f"BASIC {email}:{hash_md5}"
    
    def _refresh_token(self) -> bool:
        return True  # Monetizze não usa OAuth2
    
    def get_sales(self, start_date: str, end_date: str) -> Dict[str, Any]:
        params = {
            'dataInicio': start_date,
            'dataFim': end_date
        }
        response = self.session.get(f"{self.BASE_URL}transacoes", params=params)
        self._handle_api_error(response)
        return response.json()
    
    def get_products(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.BASE_URL}produtos")
        self._handle_api_error(response)
        return response.json()
    
    def get_subscriptions(self) -> Dict[str, Any]:
        """Método específico da Monetizze para assinaturas"""
        response = self.session.get(f"{self.BASE_URL}assinaturas")
        self._handle_api_error(response)
        return response.json()