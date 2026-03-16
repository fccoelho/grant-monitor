# Grant Database Schema

## Tables

### grants
Main table for storing grant opportunities.

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PRIMARY KEY | MD5 hash of portal+url+title |
| portal | TEXT NOT NULL | Source portal (fapesp, cnpq, nih, etc.) |
| title | TEXT NOT NULL | Grant title |
| description | TEXT | Brief description |
| url | TEXT | Link to full edital |
| deadline | TEXT | ISO 8601 deadline date |
| status | TEXT | open / closed / upcoming |
| eligibility | TEXT | Who can apply |
| amount | TEXT | Funding amount |
| keywords | TEXT | JSON array of matched keywords |
| created_at | TEXT | ISO 8601 timestamp |
| updated_at | TEXT | ISO 8601 timestamp |
| notified | INTEGER | 0/1 - whether user was notified |

### checks
Log of when each portal was checked.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| checked_at | TEXT | ISO 8601 timestamp |
| portal | TEXT | Portal name |
| grants_found | INTEGER | Number of grants found |

## Database Location

```
~/.nanobot/workspace/grant-monitor/grants.db
```

## Query Examples

### Get all open grants
```sql
SELECT * FROM grants WHERE status = 'open' ORDER BY deadline;
```

### Get grants closing within 30 days
```sql
SELECT * FROM grants 
WHERE status = 'open' 
  AND deadline IS NOT NULL 
  AND julianday(deadline) - julianday('now') <= 30
ORDER BY deadline;
```

### Get grants by portal
```sql
SELECT * FROM grants WHERE portal = 'fapesp' AND status = 'open';
```

### Count grants by status
```sql
SELECT status, COUNT(*) FROM grants GROUP BY status;
```
