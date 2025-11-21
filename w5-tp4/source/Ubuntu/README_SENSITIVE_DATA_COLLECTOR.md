# Sensitive Data Collection Tool

## Purpose
Collects and documents browser sensitive data locations for security awareness and defense planning.

## What It Does

### Data Collection
- **Scans browser profile directories** (Chrome, Firefox, Brave, Chromium)
- **Identifies sensitive files**:
  - `Login Data` - Encrypted passwords database
  - `Cookies` - Session tokens and authentication cookies
  - `History` - Browsing history database
  - `Bookmarks` - User bookmarks
  - `Web Data` - Autofill data (addresses, credit cards)
  - `Preferences` - Browser settings

### Metadata Collected
For each file:
- Full file path
- File size (bytes)
- File permissions
- Last modified timestamp
- Database structure (for SQLite files)
  - Table names
  - Row counts (shows how much data exists)

### Output Format
JSON file saved to `data/sensitive_data_collection_YYYYMMDD_HHMMSS.json`

## Example Output Structure

```json
{
  "collection_timestamp": "2025-11-21T08:38:15.123456",
  "summary": {
    "total_files_found": 6,
    "total_size_bytes": 17893758,
    "browsers_with_data": ["chrome"],
    "file_types": {
      "Login Data": 1,
      "Cookies": 1,
      "History": 1
    }
  },
  "sensitive_data_locations": [
    {
      "browser": "chrome",
      "filename": "Cookies",
      "full_path": "/home/user/.config/google-chrome/Default/Cookies",
      "description": "Session tokens and authentication cookies",
      "size_bytes": 1474560,
      "permissions": "600",
      "last_modified": "2025-11-21T08:37:42.881233",
      "database_info": {
        "type": "sqlite3",
        "tables": [
          {"name": "cookies", "row_count": 3067}
        ]
      }
    }
  ],
  "security_notes": [...],
  "defense_recommendations": [...]
}
```

## Usage

```bash
python3 collect_sensitive_data.py
```

## What This Shows (Educational)

### Why Attackers Target This Data

1. **Login Data (Passwords)**
   - Contains encrypted credentials
   - Can be decrypted if malware runs as your user
   - Gives access to all saved accounts

2. **Cookies (Session Tokens)**
   - Active session tokens bypass login
   - No password needed if attacker steals cookies
   - Direct account hijacking

3. **History (Browsing Patterns)**
   - Reveals visited sites
   - Shows banking, shopping, social media usage
   - Intelligence for targeted attacks

4. **Web Data (Autofill)**
   - Credit card information
   - Home addresses
   - Phone numbers, emails
   - Personal identification data

## Defense Strategy

### Understanding = Protection
By knowing:
- **WHAT** data exists → You can protect it
- **WHERE** it's stored → You can monitor it
- **HOW MUCH** exists → You can assess risk

### Recommended Actions
1. ✅ Use dedicated password manager (not browser)
2. ✅ Enable 2FA on all accounts
3. ✅ Clear cookies regularly
4. ✅ Monitor file access to these locations
5. ✅ Keep browsers updated
6. ✅ Use private browsing for sensitive sites

## Files Generated

- **Location**: `/home/user/academic/Year3/Intro-Cyber/w5-tp4/data/`
- **Naming**: `sensitive_data_collection_YYYYMMDD_HHMMSS.json`
- **Size**: ~7-8 KB per collection
- **Format**: JSON (human-readable and machine-parsable)

## Privacy Note

This tool only collects:
- ✅ File metadata (paths, sizes, timestamps)
- ✅ Database structure (table names, row counts)

It does NOT collect:
- ❌ Actual passwords
- ❌ Cookie values
- ❌ Browsing history URLs
- ❌ Personal data content

**Read-only access** - No data is extracted or decrypted.

## Educational Value

### For Security Students
- Learn what data browsers store
- Understand attack surface
- Practice defensive thinking
- Document security posture over time

### For System Administrators
- Audit browser data exposure
- Assess organizational risk
- Plan data protection policies
- Monitor sensitive file growth

## Related Tools

- `browser_security_audit.py` - Full security audit with recommendations
- `browser_defense_simulator.py` - Interactive defense training
- `browser_monitor.sh` - Real-time file access monitoring

---

**Remember**: Understanding what attackers target is the first step in building effective defenses!
