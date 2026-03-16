"""Base scraper class and data models"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GrantOpportunity:
    """Represents a grant/funding opportunity"""
    title: str
    agency: str
    description: str
    url: str
    publish_date: Optional[datetime] = None
    deadline: Optional[datetime] = None
    keywords: List[str] = field(default_factory=list)
    country: str = ""
    amount: Optional[str] = None
    currency: str = ""
    eligibility: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'title': self.title,
            'agency': self.agency,
            'description': self.description,
            'url': self.url,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'keywords': ','.join(self.keywords),
            'country': self.country,
            'amount': self.amount,
            'currency': self.currency,
            'eligibility': self.eligibility,
            'raw_data': str(self.raw_data),
        }


class BaseScraper(ABC):
    """Base class for all grant scrapers"""
    
    def __init__(self, delay: float = 1.0, timeout: int = 30):
        self.delay = delay  # Delay between requests
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.name = self.__class__.__name__.replace('Scraper', '')
        
    @abstractmethod
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search for grants matching keywords"""
        pass
    
    def fetch_page(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage"""
        try:
            logger.info(f"Fetching {url}")
            time.sleep(self.delay)
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_date(self, date_str: str, formats: List[str] = None) -> Optional[datetime]:
        """Parse date string to datetime"""
        if not formats:
            formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%B %d, %Y',
                '%d %B %Y',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
            ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        return None
    
    def matches_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """Check which keywords match the text"""
        text_lower = text.lower()
        return [kw for kw in keywords if kw.lower() in text_lower]
