from typing import Dict, Any
from .base import BasePlatformIntegration
import base64
from datetime import datetime, timedelta

class HotmartIntegration(BasePlatformIntegration):
    PLATFORM_NAME = 'Hotmart'
    BASE_URL = 'https://api-developers.hotmart.com/v1/'
    AUTH_URL = 'https://api-sec-vlc.hotmart.com/security/oauth/token'
    
    def _default_headers(self) -> Dict[str, str]:
        headers = super()._default_headers()
        if 'access_token' in self.credentials:
            headers['Authorization'] = f'Bearer {self.credentials["access_token"]}'
        return headers
    
    def _refresh_token(self) -> bool:
        if not all(k in self.credentials for k in ['api_key', 'api_secret', 'refresh_token']):
            raise ValueError("Credenciais incompletas para renovação de token")
            
        auth_string = f"{self.credentials['api_key']}:{self.credentials['api_secret']}"
        basic_auth = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {basic_auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.credentials['refresh_token']
        }
        
        # Usando self.session em vez de requests direto
        response = self.session.post(
            self.AUTH_URL,
            headers=headers,
            data=payload,
            timeout=30
        )
        
        self._handle_api_error(response)
        
        token_data = response.json()
        self.credentials.update({
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token'],
            'expires_at': (datetime.now() + timedelta(seconds=token_data['expires_in'])).isoformat()
        })
        return True
    
    def get_sales(self, start_date: str, end_date: str) -> Dict[str, Any]:
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'max_results': 1000
        }
        response = self.session.get(
            f"{self.BASE_URL}sales/history",
            params=params,
            timeout=15
        )
        self._handle_api_error(response)
        return response.json()
    
    def get_products(self) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.BASE_URL}products",
            timeout=15
        )
        self._handle_api_error(response)
        return response.json()

    def get_purchases(self, transaction_status: str = 'APPROVED') -> Dict[str, Any]:
        """Método específico da Hotmart para obter compras"""
        params = {
            'transaction_status': transaction_status
        }
        response = self.session.get(
            f"{self.BASE_URL}purchases",
            params=params,
            timeout=15
        )
        self._handle_api_error(response)
        return response.json()