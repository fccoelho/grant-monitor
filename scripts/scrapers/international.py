"""Scrapers for international funding agencies"""

from typing import List, Optional
from datetime import datetime
import re
from .base import BaseScraper, GrantOpportunity


class NIHScraper(BaseScraper):
    """Scraper for NIH (National Institutes of Health) - USA"""
    
    BASE_URL = "https://grants.nih.gov/funding/searchguide/index.html"
    API_URL = "https://api.reporter.nih.gov/v1/projects/Search"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search NIH funding opportunities"""
        opportunities = []
        
        # Try to use NIH API if available
        try:
            # NIH has an API for funded projects but not specifically for FOAs
            # We'll scrape the funding opportunity page
            soup = self.fetch_page(self.BASE_URL)
            
            if not soup:
                return opportunities
            
            # Look for funding opportunity announcements
            listings = soup.find_all('div', class_='opportunity') or soup.find_all('tr')
            
            for item in listings:
                try:
                    title_elem = item.find('a') or item.find('td', class_='title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    
                    if link and not link.startswith('http'):
                        link = f"https://grants.nih.gov{link}"
                    
                    # Look for description
                    desc_elem = item.find('td', class_='description') or item.find_next('td')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Look for deadline
                    deadline = None
                    date_elem = item.find('td', class_='date') or item.find(text=re.compile(r'expires|deadline|due', re.I))
                    if date_elem:
                        date_match = re.search(r'(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})', str(date_elem))
                        if date_match:
                            deadline = self.parse_date(date_match.group(1))
                    
                    full_text = f"{title} {description}"
                    matched_keywords = self.matches_keywords(full_text, keywords)
                    
                    if matched_keywords:
                        opportunities.append(GrantOpportunity(
                            title=title,
                            agency='NIH',
                            description=description,
                            url=link or self.BASE_URL,
                            deadline=deadline,
                            keywords=matched_keywords,
                            country='US',
                            currency='USD',
                        ))
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            pass
        
        return opportunities


class WellcomeScraper(BaseScraper):
    """Scraper for Wellcome Trust - UK"""
    
    BASE_URL = "https://wellcome.org/grant-funding/schemes"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search Wellcome Trust funding opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        # Wellcome has scheme listings
        listings = soup.find_all('div', class_='scheme') or soup.find_all('article')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                if link and not link.startswith('http'):
                    link = f"https://wellcome.org{link}"
                
                description_elem = item.find('p') or item.find('div', class_='summary')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='Wellcome Trust',
                        description=description,
                        url=link or self.BASE_URL,
                        keywords=matched_keywords,
                        country='UK',
                        currency='GBP',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class ERCScraper(BaseScraper):
    """Scraper for ERC (European Research Council)"""
    
    BASE_URL = "https://erc.europa.eu/apply-grant"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search ERC funding opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        listings = soup.find_all('div', class_='call') or soup.find_all('article')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                if link and not link.startswith('http'):
                    link = f"https://erc.europa.eu{link}"
                
                description_elem = item.find('p') or item.find('div', class_='description')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='ERC',
                        description=description,
                        url=link or self.BASE_URL,
                        keywords=matched_keywords,
                        country='EU',
                        currency='EUR',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class GatesScraper(BaseScraper):
    """Scraper for Bill & Melinda Gates Foundation"""
    
    BASE_URL = "https://www.gatesfoundation.org/about/careers"
    # Gates uses workday and doesn't have a traditional grants listing
    # We look for RFPs (Request for Proposals)
    RFP_URL = "https://www.gatesfoundation.org/about/our-work"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search Gates Foundation opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.RFP_URL)
        if not soup:
            return opportunities
        
        listings = soup.find_all('div', class_='grant') or soup.find_all('article')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                if link and not link.startswith('http'):
                    link = f"https://www.gatesfoundation.org{link}"
                
                description_elem = item.find('p') or item.find('div', class_='summary')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='Gates Foundation',
                        description=description,
                        url=link or self.RFP_URL,
                        keywords=matched_keywords,
                        country='US',
                        currency='USD',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities
