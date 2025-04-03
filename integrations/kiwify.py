from typing import Dict, Any
from .base import BasePlatformIntegration

class KiwifyIntegration(BasePlatformIntegration):
    PLATFORM_NAME = 'Kiwify'
    BASE_URL = 'https://api.kiwify.com.br/v1/'
    
    def _default_headers(self) -> Dict[str, str]:
        headers = super()._default_headers()
        headers['Authorization'] = f'Bearer {self.credentials["api_key"]}'
        return headers
    
    def _refresh_token(self) -> bool:
        return True  # Kiwify não usa OAuth2
    
    def get_sales(self, start_date: str, end_date: str) -> Dict[str, Any]:
        params = {
            'filter[start_date]': start_date,
            'filter[end_date]': end_date
        }
        response = self.session.get(f"{self.BASE_URL}orders", params=params)
        self._handle_api_error(response)
        return response.json()
    
    def get_products(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.BASE_URL}products")
        self._handle_api_error(response)
        return response.json()