#!/usr/bin/env python3
"""
Simple SQLite database for tracking research grants.
"""
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path


class GrantDatabase:
    """Manage grant opportunities database."""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Store in workspace
            base = Path.home() / ".nanobot" / "workspace" / "grant-monitor"
            base.mkdir(parents=True, exist_ok=True)
            db_path = base / "grants.db"
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS grants (
                    id TEXT PRIMARY KEY,
                    portal TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    url TEXT,
                    deadline TEXT,
                    status TEXT DEFAULT 'open',
                    eligibility TEXT,
                    amount TEXT,
                    keywords TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    notified INTEGER DEFAULT 0
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    checked_at TEXT,
                    portal TEXT,
                    grants_found INTEGER
                )
            """)
    
    def _generate_id(self, grant):
        """Generate unique ID from grant data."""
        key = f"{grant.get('portal', '')}:{grant.get('url', '')}:{grant.get('title', '')}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def add_grant(self, grant):
        """Add a grant to database. Returns True if new, False if exists."""
        grant_id = self._generate_id(grant)
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id FROM grants WHERE id = ?", (grant_id,))
            if cursor.fetchone():
                # Update existing
                conn.execute("""
                    UPDATE grants SET
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (
                    grant.get('status', 'open'),
                    now,
                    grant_id
                ))
                return False
            
            # Insert new
            conn.execute("""
                INSERT INTO grants (id, portal, title, description, url, deadline,
                                  status, eligibility, amount, keywords, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                grant_id,
                grant.get('portal', ''),
                grant.get('title', ''),
                grant.get('description', ''),
                grant.get('url', ''),
                grant.get('deadline', ''),
                grant.get('status', 'open'),
                grant.get('eligibility', ''),
                grant.get('amount', ''),
                json.dumps(grant.get('keywords', [])),
                now,
                now
            ))
            return True
    
    def get_grants(self, status=None, portal=None, days_to_deadline=None):
        """Get grants with optional filters."""
        query = "SELECT * FROM grants WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if portal:
            query += " AND portal = ?"
            params.append(portal)
        
        if days_to_deadline:
            query += " AND deadline IS NOT NULL AND deadline != ''"
            query += " AND julianday(deadline) - julianday('now') <= ?"
            params.append(days_to_deadline)
        
        query += " ORDER BY deadline"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_notified(self, grant_id):
        """Mark a grant as notified."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE grants SET notified = 1 WHERE id = ?", (grant_id,))
    
    def log_check(self, portal, grants_found):
        """Log a check event."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO checks (checked_at, portal, grants_found)
                VALUES (?, ?, ?)
            """, (datetime.now().isoformat(), portal, grants_found))


if __name__ == "__main__":
    # Test
    db = GrantDatabase()
    print(f"Database initialized at: {db.db_path}")
