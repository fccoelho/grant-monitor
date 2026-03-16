#!/usr/bin/env python3
"""
Check upcoming grant deadlines.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from grant_database import GrantDatabase


def days_until(deadline_str):
    """Calculate days until deadline."""
    try:
        deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        now = datetime.now(deadline.tzinfo)
        delta = deadline - now
        return delta.days
    except:
        return None


def main():
    parser = argparse.ArgumentParser(description="Check upcoming deadlines")
    parser.add_argument("--days", "-d", type=int, default=30,
                        help="Show grants closing within N days")
    parser.add_argument("--urgent", "-u", action="store_true",
                        help="Only show grants closing within 7 days")
    
    args = parser.parse_args()
    
    days = 7 if args.urgent else args.days
    
    db = GrantDatabase()
    grants = db.get_grants(status='open', days_to_deadline=days)
    
    if not grants:
        print(f"\n✅ No grants closing within {days} days!")
        return 0
    
    print(f"\n⏰ Grants closing within {days} days:\n")
    
    for grant in grants:
        days_left = days_until(grant['deadline'])
        
        if days_left is not None and days_left < 0:
            icon = "❌"
            status = "OVERDUE"
        elif days_left is not None and days_left <= 7:
            icon = "🔴"
            status = f"{days_left} days"
        elif days_left is not None and days_left <= 14:
            icon = "🟡"
            status = f"{days_left} days"
        else:
            icon = "🟢"
            status = f"{days_left} days" if days_left else "Unknown"
        
        print(f"{icon} {grant['title']}")
        print(f"   Portal: {grant['portal'].upper()}")
        print(f"   Deadline: {grant['deadline']} ({status})")
        print(f"   URL: {grant['url']}")
        print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
