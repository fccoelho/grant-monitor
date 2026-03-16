#!/usr/bin/env python3
"""
Check all grant portals for new opportunities using real scrapers.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add skill directory to path
sys.path.insert(0, str(Path(__file__).parent))

from grant_database import GrantDatabase
from scrapers import (
    FAPESPScraper, CNPqScraper, FAPERJScraper, FAPEMIGScraper,
    NIHScraper, WellcomeScraper, ERCScraper, GatesScraper,
    NSFCScraper, MOSTScraper, CASScraper, ChinaMedicalBoardScraper
)


# Map of scrapers
SCRAPERS = {
    # Brazil
    'FAPESP': FAPESPScraper,
    'CNPq': CNPqScraper,
    'FAPERJ': FAPERJScraper,
    'FAPEMIG': FAPEMIGScraper,
    # International
    'NIH': NIHScraper,
    'Wellcome Trust': WellcomeScraper,
    'ERC': ERCScraper,
    'Gates Foundation': GatesScraper,
    # China
    'NSFC (China)': NSFCScraper,
    'MOST (China)': MOSTScraper,
    'CAS (China)': CASScraper,
    'China Medical Board': ChinaMedicalBoardScraper,
}


def check_portal(scraper_class, keywords):
    """Check a single portal using its scraper"""
    scraper_name = scraper_class.__name__.replace('Scraper', '')
    print(f"🔍 Checking {scraper_name}...")
    
    try:
        scraper = scraper_class(delay=1.0)
        results = scraper.search(keywords)
        
        if results:
            print(f"   ✓ Found {len(results)} opportunities")
        else:
            print(f"   - No matching opportunities")
        
        return results
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Check all grant portals for funding opportunities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search with default keywords
  python3 check_all.py
  
  # Search for specific keywords
  python3 check_all.py --keywords "dengue,global health"
  
  # Save to database
  python3 check_all.py --save
  
  # Export to JSON
  python3 check_all.py --output grants.json
  
  # Check only specific portals
  python3 check_all.py --portals FAPESP,NIH
        """
    )
    parser.add_argument(
        "--keywords", 
        default="dengue,epidemiologia,global health",
        help="Comma-separated keywords to search (default: dengue,epidemiologia,global health)"
    )
    parser.add_argument(
        "--portals",
        help="Comma-separated list of portals to check (default: all)"
    )
    parser.add_argument(
        "--output", "-o", 
        help="Output JSON file"
    )
    parser.add_argument(
        "--save", "-s", 
        action="store_true",
        help="Save to database"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    args = parser.parse_args()
    
    keywords = [k.strip() for k in args.keywords.split(",")]
    print(f"\n🔎 Searching for: {', '.join(keywords)}\n")
    
    # Select scrapers to run
    if args.portals:
        portal_names = [p.strip() for p in args.portals.split(",")]
        selected_scrapers = {}
        for name in portal_names:
            # Find matching scraper
            for key, scraper_class in SCRAPERS.items():
                if name.lower() in key.lower() or key.lower() in name.lower():
                    selected_scrapers[key] = scraper_class
                    break
    else:
        selected_scrapers = SCRAPERS
    
    print(f"📡 Checking {len(selected_scrapers)} portals...\n")
    
    all_grants = []
    stats = {}
    
    # Run all scrapers
    for portal_name, scraper_class in selected_scrapers.items():
        results = check_portal(scraper_class, keywords)
        stats[portal_name] = len(results)
        all_grants.extend(results)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    
    for portal, count in stats.items():
        status = "✓" if count > 0 else "-"
        print(f"  {status} {portal}: {count} opportunities")
    
    print(f"\n✅ Total: {len(all_grants)} opportunities found\n")
    
    # Detailed output
    if args.verbose and all_grants:
        print(f"{'='*60}")
        print(f"📋 DETAILED RESULTS")
        print(f"{'='*60}\n")
        
        for i, grant in enumerate(all_grants, 1):
            print(f"{i}. {grant.title}")
            print(f"   Agency: {grant.agency}")
            print(f"   Country: {grant.country}")
            print(f"   Deadline: {grant.deadline.strftime('%Y-%m-%d') if grant.deadline else 'N/A'}")
            print(f"   URL: {grant.url}")
            print(f"   Keywords: {', '.join(grant.keywords)}")
            if grant.amount:
                print(f"   Amount: {grant.amount} {grant.currency}")
            print()
    
    # Save to database
    if args.save:
        db = GrantDatabase()
        saved = 0
        duplicates = 0
        
        for grant in all_grants:
            if db.add_grant(grant.to_dict()):
                saved += 1
            else:
                duplicates += 1
        
        print(f"💾 Database: {saved} new, {duplicates} duplicates")
    
    # Output JSON
    if args.output:
        output_data = [g.to_dict() for g in all_grants]
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Exported to {args.output}")
    
    # Manual links reminder
    if not all_grants:
        print("\n🔗 Manual portal links:")
        print("\n🇧🇷 Brazil:")
        print("   FAPESP: https://fapesp.br/oportunidades/")
        print("   CNPq: https://www.gov.br/cnpq/pt-br/edicitais")
        print("   FAPERJ: https://www.faperj.br/edicitais/")
        print("   FAPEMIG: https://fapemig.br/chamadas-publicas/")
        print("\n🌍 International:")
        print("   NIH: https://grants.nih.gov/")
        print("   Wellcome: https://wellcome.org/grant-funding/schemes")
        print("   ERC: https://erc.europa.eu/apply-grant")
        print("   Gates: https://www.gatesfoundation.org/")
        print("\n🇨🇳 China:")
        print("   NSFC: https://www.nsfc.gov.cn/english/")
        print("   MOST: http://www.most.gov.cn/eng/")
        print("   CAS: https://www.cas.cn/eng/")
        print("   China Medical Board: https://www.chinamedicalboard.org/funding-opportunities")
        print()
    
    return len(all_grants)


if __name__ == "__main__":
    sys.exit(main())
