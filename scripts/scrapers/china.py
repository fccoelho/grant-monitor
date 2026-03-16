"""Scrapers for Chinese funding agencies"""

from typing import List, Optional
from datetime import datetime
import re
from .base import BaseScraper, GrantOpportunity


class NSFCScraper(BaseScraper):
    """Scraper for NSFC (National Natural Science Foundation of China)"""
    
    BASE_URL = "https://www.nsfc.gov.cn/english/"
    ENGLISH_URL = "https://www.nsfc.gov.cn/english/site_1/index.html"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search NSFC funding opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.ENGLISH_URL)
        if not soup:
            return opportunities
        
        # NSFC English site has announcements
        listings = soup.find_all('div', class_='news-item') or soup.find_all('li')
        
        for item in listings:
            try:
                title_elem = item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                if link and not link.startswith('http'):
                    link = f"https://www.nsfc.gov.cn{link}"
                
                # Try to find date
                date_elem = item.find('span', class_='date') or item.find(text=re.compile(r'\d{4}-\d{2}-\d{2}'))
                publish_date = None
                if date_elem:
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', str(date_elem))
                    if date_match:
                        publish_date = self.parse_date(date_match.group(1))
                
                full_text = title
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='NSFC (China)',
                        description="National Natural Science Foundation of China - funding opportunity",
                        url=link or self.ENGLISH_URL,
                        publish_date=publish_date,
                        keywords=matched_keywords,
                        country='CN',
                        currency='CNY',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class MOSTScraper(BaseScraper):
    """Scraper for MOST (Ministry of Science and Technology of China)"""
    
    BASE_URL = "http://www.most.gov.cn/eng/"
    PROGRAMS_URL = "https://en.most.gov.cn/index.html"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search MOST funding opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.PROGRAMS_URL)
        if not soup:
            return opportunities
        
        listings = soup.find_all('div', class_='program') or soup.find_all('article')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                if link and not link.startswith('http'):
                    link = f"http://www.most.gov.cn{link}"
                
                description_elem = item.find('p') or item.find('div', class_='summary')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='MOST (China)',
                        description=description,
                        url=link or self.PROGRAMS_URL,
                        keywords=matched_keywords,
                        country='CN',
                        currency='CNY',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class CASScraper(BaseScraper):
    """Scraper for CAS (Chinese Academy of Sciences)"""
    
    BASE_URL = "https://english.cas.cn"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search CAS funding opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        listings = soup.find_all('div', class_='news-item') or soup.find_all('li')
        
        for item in listings:
            try:
                title_elem = item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                if link and not link.startswith('http'):
                    link = f"https://www.cas.cn{link}"
                
                full_text = title
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='CAS (China)',
                        description="Chinese Academy of Sciences - funding opportunity",
                        url=link or self.BASE_URL,
                        keywords=matched_keywords,
                        country='CN',
                        currency='CNY',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class ChinaMedicalBoardScraper(BaseScraper):
    """Scraper for China Medical Board"""
    
    BASE_URL = "https://www.chinamedicalboard.org/funding-opportunities"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search China Medical Board opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        listings = soup.find_all('div', class_='opportunity') or soup.find_all('article')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                if link and not link.startswith('http'):
                    link = f"https://www.chinamedicalboard.org{link}"
                
                description_elem = item.find('p') or item.find('div', class_='summary')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='China Medical Board',
                        description=description,
                        url=link or self.BASE_URL,
                        keywords=matched_keywords,
                        country='US',  # HQ in US but focuses on China
                        currency='USD',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class BeltAndRoadScraper(BaseScraper):
    """Scraper for Belt and Road Initiative funding"""
    
    BASE_URL = "https://www.beltandroad.gov.cn/"
    # This is primarily a Chinese government site
    # Many universities also have Belt and Road programs
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search Belt and Road opportunities"""
        opportunities = []
        
        # Belt and Road funding is distributed across many institutions
        # We check the main portal
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        listings = soup.find_all('div', class_='news-item') or soup.find_all('li')
        
        for item in listings:
            try:
                title_elem = item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '')
                
                if link and not link.startswith('http'):
                    link = f"https://www.beltandroad.gov.cn{link}"
                
                full_text = title
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='Belt and Road Initiative',
                        description="Belt and Road Initiative funding opportunity",
                        url=link or self.BASE_URL,
                        keywords=matched_keywords,
                        country='CN',
                        currency='CNY',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities
