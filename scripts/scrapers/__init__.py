"""
Grant Monitor Scrapers Module

Scrapers for research funding portals:
- Brazil: FAPESP, CNPq, FAPERJ, FAPEMIG
- International: NIH, Wellcome Trust, ERC, Gates Foundation  
- China: NSFC, MOST, CAS, China Medical Board
"""

from .base import BaseScraper, GrantOpportunity
from .brazil import FAPESPScraper, CNPqScraper, FAPERJScraper, FAPEMIGScraper
from .international import NIHScraper, WellcomeScraper, ERCScraper, GatesScraper
from .china import NSFCScraper, MOSTScraper, CASScraper, ChinaMedicalBoardScraper

__all__ = [
    'BaseScraper',
    'GrantOpportunity',
    'FAPESPScraper',
    'CNPqScraper', 
    'FAPERJScraper',
    'FAPEMIGScraper',
    'NIHScraper',
    'WellcomeScraper',
    'ERCScraper',
    'GatesScraper',
    'NSFCScraper',
    'MOSTScraper',
    'CASScraper',
    'ChinaMedicalBoardScraper',
]
