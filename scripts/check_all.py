#!/usr/bin/env python3
"""
Check all grant portals for new opportunities.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add skill directory to path
sys.path.insert(0, str(Path(__file__).parent))

from grant_database import GrantDatabase


def check_fapesp_mock(keywords):
    """Mock check for FAPESP - replace with real scraping/API."""
    print("🔍 Checking FAPESP...")
    # In production, this would scrape https://fapesp.br/oportunidades/
    # For now, return empty list with instructions
    return []


def check_cnpq_mock(keywords):
    """Mock check for CNPq - replace with real scraping/API."""
    print("🔍 Checking CNPq...")
    # In production, this would check https://www.gov.br/cnpq/pt-br/edicitais
    return []


def check_nih_mock(keywords):
    """Mock check for NIH - replace with real API."""
    print("🔍 Checking NIH...")
    # In production, use NIH Reporter API
    return []


def check_wellcome_mock(keywords):
    """Mock check for Wellcome Trust."""
    print("🔍 Checking Wellcome Trust...")
    return []


def check_nsfc_mock(keywords):
    """Mock check for NSFC (China)."""
    print("🔍 Checking NSFC (National Natural Science Foundation of China)...")
    # In production: https://www.nsfc.gov.cn/english/
    return []


def check_most_mock(keywords):
    """Mock check for MOST (China Ministry of Science and Technology)."""
    print("🔍 Checking MOST (Ministry of Science and Technology, China)...")
    # In production: http://www.most.gov.cn/
    return []


def check_cmb_mock(keywords):
    """Mock check for China Medical Board."""
    print("🔍 Checking China Medical Board...")
    # In production: https://www.chinamedicalboard.org/funding-opportunities
    return []


def main():
    parser = argparse.ArgumentParser(description="Check all grant portals")
    parser.add_argument("--keywords", default="dengue,epidemiologia", 
                        help="Comma-separated keywords to search")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--save", "-s", action="store_true", 
                        help="Save to database")
    args = parser.parse_args()
    
    keywords = [k.strip() for k in args.keywords.split(",")]
    print(f"\n🔎 Searching for: {', '.join(keywords)}\n")
    
    all_grants = []
    
    # Check each portal
    # 🇧🇷 Brazil
    all_grants.extend(check_fapesp_mock(keywords))
    all_grants.extend(check_cnpq_mock(keywords))
    
    # 🌍 International
    all_grants.extend(check_nih_mock(keywords))
    all_grants.extend(check_wellcome_mock(keywords))
    
    # 🇨🇳 China
    all_grants.extend(check_nsfc_mock(keywords))
    all_grants.extend(check_most_mock(keywords))
    all_grants.extend(check_cmb_mock(keywords))
    
    # Results
    print(f"\n✅ Found {len(all_grants)} opportunities\n")
    
    if all_grants:
        for grant in all_grants:
            print(f"📋 {grant.get('title', 'N/A')}")
            print(f"   Portal: {grant.get('portal', 'N/A')}")
            print(f"   Deadline: {grant.get('deadline', 'N/A')}")
            print(f"   URL: {grant.get('url', 'N/A')}\n")
    else:
        print("ℹ️ No new opportunities found (or manual checking required)")
        print("\n🔗 Manual portal links:")
        print("\n🇧🇷 Brazil:")
        print("   FAPESP: https://fapesp.br/oportunidades/")
        print("   CNPq: https://www.gov.br/cnpq/pt-br/edicitais")
        print("\n🌍 International:")
        print("   NIH: https://grants.nih.gov/funding/searchguide/index.html")
        print("   Wellcome: https://wellcome.org/grant-funding/schemes")
        print("\n🇨🇳 China:")
        print("   NSFC: https://www.nsfc.gov.cn/english/")
        print("   MOST: http://www.most.gov.cn/")
        print("   China Medical Board: https://www.chinamedicalboard.org/funding-opportunities\n")
    
    # Save to database if requested
    if args.save and all_grants:
        db = GrantDatabase()
        count = 0
        for grant in all_grants:
            if db.add_grant(grant):
                count += 1
        print(f"💾 Saved {count} new grants to database")
    
    # Output JSON if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(all_grants, f, indent=2)
        print(f"💾 Saved results to {args.output}")
    
    return len(all_grants)


if __name__ == "__main__":
    sys.exit(main())
