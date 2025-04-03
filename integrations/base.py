from typing import Dict, Optional, Any, Union, List
import abc
import requests
from datetime import datetime, timedelta
import logging
from urllib.parse import urlencode
from datetime import datetime, date

class BasePlatformIntegration(abc.ABC):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.credentials: Dict[str, Any] = self._load_credentials()
        self.session = requests.Session()
        self.session.headers.update(self._default_headers())
    
    @property
    @abc.abstractmethod
    def PLATFORM_NAME(self) -> str:
        """Nome oficial da plataforma"""
        pass
    
    @property
    @abc.abstractmethod
    def BASE_URL(self) -> str:
        """URL base da API"""
        pass
    
    def _default_headers(self) -> Dict[str, str]:
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def _load_credentials(self) -> Dict[str, Any]:
        """Implemente conforme seu sistema de armazenamento"""
        return {}
    
    def _handle_api_error(self, response: requests.Response) -> None:
        if response.status_code == 401:
            self.logger.warning("Token expirado, tentando renovar...")
            if self._refresh_token():
                raise Exception("Token renovado, tente novamente")
        response.raise_for_status()
    
    @abc.abstractmethod
    def _refresh_token(self) -> bool:
        pass
    
    @abc.abstractmethod
    def get_sales(self, start_date: str, end_date: str) -> Dict[str, Any]:
        pass
    
    @abc.abstractmethod
    def get_products(self) -> Dict[str, Any]:
        pass
    
    def test_connection(self) -> bool:
        try:
            self.get_products()
            return True
        except Exception as e:
            self.logger.error(f"Falha na conexão: {str(e)}")
            return False