from typing import Dict, Any
from .base import BasePlatformIntegration
import json
from datetime import datetime, date, timedelta

class EduzzIntegration(BasePlatformIntegration):
    PLATFORM_NAME = 'Eduzz'
    BASE_URL = 'https://api.eduzz.com/'
    
    def __init__(self, user_id: int):
        super().__init__(user_id)
        self.token_url = f"{self.BASE_URL}oauth/token"
    
    def _default_headers(self) -> Dict[str, str]:
        headers = super()._default_headers()
        headers['Authorization'] = f'Bearer {self.credentials.get("access_token", "")}'
        return headers
    
    def _refresh_token(self) -> bool:
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.credentials.get('refresh_token'),
            'client_id': self.credentials['api_key'],
            'client_secret': self.credentials['api_secret']
        }
        response = self.session.post(self.token_url, data=payload)
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
            'page': 1,
            'per_page': 100
        }
        response = self.session.get(f"{self.BASE_URL}v1/sales", params=params)
        self._handle_api_error(response)
        return response.json()
    
    def get_products(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.BASE_URL}v1/products")
        self._handle_api_error(response)
        return response.json()