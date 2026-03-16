"""Scrapers for Brazilian funding agencies"""

from typing import List, Optional
from datetime import datetime
import re
from .base import BaseScraper, GrantOpportunity


class FAPESPScraper(BaseScraper):
    """Scraper for FAPESP (Fundação de Amparo à Pesquisa do Estado de SP)"""
    
    BASE_URL = "https://fapesp.br/oportunidades/"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search FAPESP opportunities"""
        opportunities = []
        
        # FAPESP has different categories
        categories = [
            'chamadas',
            'auxilio_pesquisa',
            'bolsas',
        ]
        
        for category in categories:
            url = f"{self.BASE_URL}{category}"
            soup = self.fetch_page(url)
            
            if not soup:
                continue
            
            # Find opportunity listings
            listings = soup.find_all('div', class_='oportunidade-item')
            
            for item in listings:
                try:
                    title_elem = item.find('h3') or item.find('h2') or item.find('a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    if link and not link.startswith('http'):
                        link = f"https://fapesp.br{link}"
                    
                    description_elem = item.find('div', class_='description') or item.find('p')
                    description = description_elem.get_text(strip=True) if description_elem else ""
                    
                    # Extract deadline
                    deadline = None
                    deadline_elem = item.find(text=re.compile(r'Prazo|Deadline'))
                    if deadline_elem:
                        date_match = re.search(r'(\d{2}/\d{2}/\d{4})', str(deadline_elem))
                        if date_match:
                            deadline = self.parse_date(date_match.group(1))
                    
                    full_text = f"{title} {description}"
                    matched_keywords = self.matches_keywords(full_text, keywords)
                    
                    if matched_keywords:
                        opportunities.append(GrantOpportunity(
                            title=title,
                            agency='FAPESP',
                            description=description,
                            url=link or self.BASE_URL,
                            deadline=deadline,
                            keywords=matched_keywords,
                            country='BR',
                            currency='BRL',
                        ))
                        
                except Exception as e:
                    continue
        
        return opportunities


class CNPqScraper(BaseScraper):
    """Scraper for CNPq (Conselho Nacional de Desenvolvimento Científico)"""
    
    BASE_URL = "https://www.gov.br/cnpq/pt-br/edicitais"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search CNPq opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        # CNPq uses gov.br structure
        listings = soup.find_all('article', class_='content') or soup.find_all('div', class_='edital-item')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a', class_='titulo')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link_elem = title_elem if title_elem.name == 'a' else item.find('a')
                link = link_elem.get('href', '') if link_elem else self.BASE_URL
                
                if link and not link.startswith('http'):
                    link = f"https://www.gov.br{link}"
                
                description_elem = item.find('p') or item.find('div', class_='description')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='CNPq',
                        description=description,
                        url=link,
                        keywords=matched_keywords,
                        country='BR',
                        currency='BRL',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class FAPERJScraper(BaseScraper):
    """Scraper for FAPERJ (Fundação Carlos Chagas Filho de Amparo à Pesquisa do RJ)"""
    
    BASE_URL = "https://www.faperj.br/edicitais/"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search FAPERJ opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        # Find edital listings
        listings = soup.find_all('div', class_='edital') or soup.find_all('article')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                if link and not link.startswith('http'):
                    link = f"https://www.faperj.br{link}"
                
                description_elem = item.find('p') or item.find('div', class_='resumo')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='FAPERJ',
                        description=description,
                        url=link or self.BASE_URL,
                        keywords=matched_keywords,
                        country='BR',
                        currency='BRL',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities


class FAPEMIGScraper(BaseScraper):
    """Scraper for FAPEMIG (Fundação de Amparo à Pesquisa de Minas Gerais)"""
    
    BASE_URL = "https://fapemig.br/chamadas-publicas/"
    
    def search(self, keywords: List[str]) -> List[GrantOpportunity]:
        """Search FAPEMIG opportunities"""
        opportunities = []
        
        soup = self.fetch_page(self.BASE_URL)
        if not soup:
            return opportunities
        
        listings = soup.find_all('div', class_='chamada') or soup.find_all('article')
        
        for item in listings:
            try:
                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                
                if link and not link.startswith('http'):
                    link = f"https://fapemig.br{link}"
                
                description_elem = item.find('p') or item.find('div', class_='descricao')
                description = description_elem.get_text(strip=True) if description_elem else ""
                
                full_text = f"{title} {description}"
                matched_keywords = self.matches_keywords(full_text, keywords)
                
                if matched_keywords:
                    opportunities.append(GrantOpportunity(
                        title=title,
                        agency='FAPEMIG',
                        description=description,
                        url=link or self.BASE_URL,
                        keywords=matched_keywords,
                        country='BR',
                        currency='BRL',
                    ))
                    
            except Exception as e:
                continue
        
        return opportunities
