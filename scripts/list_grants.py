#!/usr/bin/env python3
"""
List grants from the database.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from grant_database import GrantDatabase


def format_grant(grant):
    """Format a grant for display."""
    lines = [
        f"📋 {grant['title']}",
        f"   Portal: {grant['portal'].upper()}",
        f"   Status: {grant['status']}",
    ]
    
    if grant.get('deadline'):
        lines.append(f"   Deadline: {grant['deadline']}")
    
    if grant.get('amount'):
        lines.append(f"   Amount: {grant['amount']}")
    
    if grant.get('url'):
        lines.append(f"   URL: {grant['url']}")
    
    if grant.get('description'):
        desc = grant['description'][:100]
        if len(grant['description']) > 100:
            desc += "..."
        lines.append(f"   Description: {desc}")
    
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="List tracked grants")
    parser.add_argument("--status", choices=['open', 'closed', 'upcoming'],
                        help="Filter by status")
    parser.add_argument("--portal", 
                        choices=['fapesp', 'cnpq', 'nih', 'wellcome', 'faperj', 'fapemig',
                                'nsfc', 'most', 'cas', 'cmb'],
                        help="Filter by portal")
    parser.add_argument("--limit", "-n", type=int, default=50,
                        help="Maximum results to show")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON")
    
    args = parser.parse_args()
    
    db = GrantDatabase()
    grants = db.get_grants(status=args.status, portal=args.portal)
    
    if not grants:
        print("No grants found matching criteria.")
        return 0
    
    grants = grants[:args.limit]
    
    if args.json:
        import json
        print(json.dumps(grants, indent=2))
    else:
        print(f"\n📊 Showing {len(grants)} grants:\n")
        for grant in grants:
            print(format_grant(grant))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
