#!/usr/bin/env python3
"""
BROWSER PASSWORD ENCRYPTION EDUCATION TOOL

This tool demonstrates:
1. HOW browsers encrypt passwords (the encryption mechanism)
2. WHY this encryption can be bypassed by local malware
3. WHAT defenses prevent this attack
4. HOW to detect if someone is attempting this

EDUCATIONAL PURPOSE ONLY - Understanding encryption to build defenses
"""

import os
import sqlite3
from pathlib import Path
import json
from datetime import datetime


class BrowserEncryptionEducator:
    """Educational tool explaining browser password encryption"""
    
    def __init__(self):
        self.home = Path.home()
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def explain_encryption_mechanism(self):
        """Explain how Chrome encrypts passwords on Linux"""
        print("=" * 80)
        print("CHROME PASSWORD ENCRYPTION - HOW IT WORKS")
        print("=" * 80)
        print()
        
        explanation = {
            "encryption_method": "AES-128 CBC with PBKDF2",
            "key_storage": "OS-level keyring (libsecret/gnome-keyring on Linux)",
            "key_derivation": "Derived from user's login session",
            "encryption_flow": [
                "1. User saves password in Chrome",
                "2. Chrome generates encryption key from OS keyring",
                "3. Password is encrypted with AES-128",
                "4. Encrypted password stored in 'Login Data' SQLite database",
                "5. Password blob prefix: 'v10' or 'v11' indicates encryption version"
            ],
            "decryption_flow": [
                "1. Chrome needs password (user visits site)",
                "2. Chrome requests encryption key from OS keyring",
                "3. OS checks: Is requester the same user who encrypted?",
                "4. If yes → OS provides key",
                "5. Chrome decrypts password with key",
                "6. Password filled into login form"
            ],
            "vulnerability": [
                "⚠️  CRITICAL ISSUE: OS keyring checks USER, not PROCESS",
                "⚠️  Any code running as YOUR user can request the key",
                "⚠️  No master password requirement (by default)",
                "⚠️  No additional authentication needed"
            ]
        }
        
        print("ENCRYPTION PROCESS:")
        for step in explanation["encryption_flow"]:
            print(f"  {step}")
        
        print("\nDECRYPTION PROCESS:")
        for step in explanation["decryption_flow"]:
            print(f"  {step}")
        
        print("\n" + "⚠️" * 40)
        print("WHY THIS IS VULNERABLE TO LOCAL MALWARE:")
        print("⚠️" * 40)
        for vuln in explanation["vulnerability"]:
            print(f"  {vuln}")
        
        return explanation
    
    def demonstrate_database_structure(self):
        """Show the structure of Login Data database (educational)"""
        print("\n" + "=" * 80)
        print("LOGIN DATA DATABASE STRUCTURE")
        print("=" * 80)
        print()
        
        chrome_login = self.home / '.config/google-chrome/Default/Login Data'
        
        if not chrome_login.exists():
            print("❌ Chrome Login Data not found")
            return None
        
        print(f"📁 Database: {chrome_login}")
        print(f"📊 Size: {chrome_login.stat().st_size:,} bytes")
        print()
        
        try:
            # Read-only connection
            conn = sqlite3.connect(f"file:{chrome_login}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # Get table schema
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='logins'")
            schema = cursor.fetchone()
            
            if schema:
                print("TABLE SCHEMA:")
                print(schema[0])
                print()
            
            # Get column information
            cursor.execute("PRAGMA table_info(logins)")
            columns = cursor.fetchall()
            
            print("COLUMNS IN 'logins' TABLE:")
            for col in columns:
                col_id, name, col_type, notnull, default, pk = col
                print(f"  • {name:20} - {col_type:10} {'(PRIMARY KEY)' if pk else ''}")
            
            # Count credentials (no actual data)
            cursor.execute("SELECT COUNT(*) FROM logins")
            count = cursor.fetchone()[0]
            print(f"\n📊 Total saved credentials: {count}")
            
            # Explain the important columns
            print("\nKEY COLUMNS EXPLAINED:")
            column_explanations = {
                "origin_url": "Website URL where password is used",
                "username_value": "Username/email (stored in plaintext!)",
                "password_value": "ENCRYPTED password (blob data)",
                "date_created": "When credential was saved",
                "times_used": "How often this password was auto-filled"
            }
            
            for col, explanation in column_explanations.items():
                print(f"  • {col:20} → {explanation}")
            
            conn.close()
            
            print("\n" + "🔐" * 40)
            print("WHAT ATTACKERS SEE:")
            print("🔐" * 40)
            print("  ✓ Usernames are in PLAINTEXT (no decryption needed)")
            print("  ✓ Website URLs are in PLAINTEXT")
            print("  ✓ Passwords are ENCRYPTED blobs starting with 'v10' or 'v11'")
            print("  ✓ To decrypt: Attacker needs the encryption key from OS keyring")
            print()
            
            return {
                "database_path": str(chrome_login),
                "credential_count": count,
                "columns": [col[1] for col in columns]
            }
            
        except sqlite3.Error as e:
            print(f"❌ Database locked or inaccessible: {e}")
            print("   (This is normal if Chrome is running)")
            return None
    
    def explain_attack_scenario(self):
        """Explain how malware exploits this vulnerability"""
        print("\n" + "=" * 80)
        print("ATTACK SCENARIO - HOW MALWARE STEALS PASSWORDS")
        print("=" * 80)
        print()
        
        attack_steps = [
            {
                "step": "1. Initial Compromise",
                "attacker_action": "Victim runs malicious code (fake download, phishing attachment, etc.)",
                "technical_detail": "Malware gains execution as the victim's user account",
                "why_it_works": "No privilege escalation needed - runs with user permissions"
            },
            {
                "step": "2. Locate Login Database",
                "attacker_action": "Malware searches for ~/.config/google-chrome/Default/Login Data",
                "technical_detail": "Standard path, easy to find",
                "why_it_works": "File is readable by the user (needs to be for Chrome)"
            },
            {
                "step": "3. Request Encryption Key",
                "attacker_action": "Malware calls OS keyring APIs (libsecret on Linux)",
                "technical_detail": """
                Python example concept (what malware does):
                
                import secretstorage
                connection = secretstorage.dbus_init()
                collection = secretstorage.get_default_collection(connection)
                
                # Request Chrome's encryption key
                items = collection.search_items({'application': 'chrome'})
                for item in items:
                    key = item.get_secret()  # OS provides key!
                """,
                "why_it_works": "OS sees request from user's process → grants access"
            },
            {
                "step": "4. Decrypt Passwords",
                "attacker_action": "Malware uses key to decrypt password blobs",
                "technical_detail": """
                Decryption process:
                1. Read encrypted blob from database
                2. Strip 'v10' or 'v11' prefix
                3. Use key from keyring with AES decryption
                4. Result: plaintext password
                """,
                "why_it_works": "Standard crypto - if you have the key, you can decrypt"
            },
            {
                "step": "5. Exfiltrate Data",
                "attacker_action": "Send username/password pairs to attacker server",
                "technical_detail": "HTTPS POST to hide in normal traffic, or DNS tunneling",
                "why_it_works": "Looks like normal web browsing to firewalls"
            }
        ]
        
        for step_info in attack_steps:
            print(f"{step_info['step']}: {step_info['attacker_action']}")
            print(f"   Technical: {step_info['technical_detail'].strip()}")
            print(f"   Why it works: {step_info['why_it_works']}")
            print()
        
        return attack_steps
    
    def explain_defenses(self):
        """Explain how to defend against this attack"""
        print("=" * 80)
        print("DEFENSE STRATEGIES - HOW TO PREVENT PASSWORD THEFT")
        print("=" * 80)
        print()
        
        defenses = {
            "Prevention (Stop malware execution)": [
                "✓ Keep browser updated (prevents exploit → code execution)",
                "✓ Don't run untrusted code/downloads",
                "✓ Use browser sandboxing (Firejail, Flatpak)",
                "✓ Enable AppArmor/SELinux profiles",
                "✓ Run antivirus/anti-malware software"
            ],
            "Mitigation (Limit damage if compromised)": [
                "✓ Use dedicated password manager (1Password, Bitwarden, KeePassXC)",
                "✓ Enable 2FA on all accounts (stolen password alone won't work)",
                "✓ Use hardware security keys (YubiKey)",
                "✓ Set browser master password (Chrome doesn't have this, use Firefox)",
                "✓ Don't save passwords in browser at all"
            ],
            "Detection (Know when attack happens)": [
                "✓ Monitor Login Data file access with auditd",
                "✓ Watch for secretstorage/keyring API calls",
                "✓ Use file integrity monitoring (AIDE, Tripwire)",
                "✓ Monitor network for data exfiltration",
                "✓ Regular security scans (ClamAV, rkhunter)"
            ],
            "Response (React to breach)": [
                "✓ Change all passwords immediately (from different device)",
                "✓ Enable 2FA if not already active",
                "✓ Review account activity logs for unauthorized access",
                "✓ Scan system for malware",
                "✓ Consider system reinstall if heavily compromised"
            ]
        }
        
        for category, items in defenses.items():
            print(f"\n{category.upper()}")
            print("-" * 80)
            for item in items:
                print(f"  {item}")
        
        print("\n" + "🛡️" * 40)
        print("BEST DEFENSE: Use Password Manager + 2FA")
        print("🛡️" * 40)
        print("  • Password managers use separate encryption (not OS keyring)")
        print("  • Require master password for each use")
        print("  • 2FA means stolen password alone is useless")
        print("  • Hardware keys (YubiKey) provide strongest protection")
        print()
        
        return defenses
    
    def demonstrate_monitoring(self):
        """Show how to monitor for this type of attack"""
        print("=" * 80)
        print("MONITORING FOR PASSWORD THEFT ATTEMPTS")
        print("=" * 80)
        print()
        
        monitoring_config = {
            "file_monitoring": {
                "tool": "auditd",
                "commands": [
                    "# Monitor Login Data access",
                    "sudo auditctl -w ~/.config/google-chrome/Default/Login\\ Data -p ra -k chrome_passwords",
                    "",
                    "# Check audit logs",
                    "sudo ausearch -k chrome_passwords -i"
                ],
                "what_to_watch": [
                    "Access by non-Chrome processes",
                    "Access at unusual times (3 AM)",
                    "Multiple rapid accesses",
                    "Access from /tmp or /dev/shm processes"
                ]
            },
            "process_monitoring": {
                "tool": "process accounting",
                "commands": [
                    "# Watch for keyring access",
                    "ps aux | grep -E '(secret|keyring|gnome-keyring)'",
                    "",
                    "# Monitor with strace (for analysis)",
                    "sudo strace -e trace=open,openat -p $(pgrep chrome) 2>&1 | grep 'Login Data'"
                ],
                "what_to_watch": [
                    "Python/Bash scripts accessing keyring",
                    "Unknown processes calling secretstorage APIs",
                    "Processes outside normal Chrome paths"
                ]
            },
            "network_monitoring": {
                "tool": "tcpdump/Wireshark",
                "commands": [
                    "# Monitor for data exfiltration",
                    "sudo tcpdump -i any -n 'tcp port 443 or tcp port 80'",
                    "",
                    "# Watch for unusual uploads",
                    "sudo iftop -i wlan0"
                ],
                "what_to_watch": [
                    "Large uploads to unknown domains",
                    "Connections to IP addresses (not domains)",
                    "DNS queries to suspicious domains"
                ]
            }
        }
        
        for category, config in monitoring_config.items():
            print(f"\n{category.upper().replace('_', ' ')}")
            print("-" * 80)
            print(f"Tool: {config['tool']}")
            print("\nCommands:")
            for cmd in config['commands']:
                print(f"  {cmd}")
            print("\nWhat to watch for:")
            for item in config['what_to_watch']:
                print(f"  ⚠️  {item}")
        
        return monitoring_config
    
    def save_education_report(self, encryption_info, db_info, attack_steps, defenses, monitoring):
        """Save educational report to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"password_encryption_education_{timestamp}.json"
        filepath = self.data_dir / filename
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "report_type": "password_encryption_education",
            "encryption_mechanism": encryption_info,
            "database_structure": db_info,
            "attack_scenario": attack_steps,
            "defense_strategies": defenses,
            "monitoring_techniques": monitoring,
            "key_takeaways": [
                "Browser password encryption protects against remote attackers",
                "Local malware running as your user CAN decrypt passwords",
                "OS keyring checks USER identity, not process legitimacy",
                "Defense: Use password manager + 2FA + monitoring",
                "Detection: Monitor file access and keyring API calls",
                "Prevention: Keep software updated, don't run untrusted code"
            ],
            "practical_recommendations": [
                "Immediate: Stop saving passwords in browser",
                "Short-term: Install Bitwarden or 1Password",
                "Medium-term: Enable 2FA on all accounts",
                "Long-term: Get hardware security key (YubiKey)",
                "Ongoing: Monitor Login Data file access with auditd"
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    def run_education(self):
        """Run complete educational demonstration"""
        print("\n" + "🎓" * 40)
        print("BROWSER PASSWORD ENCRYPTION - EDUCATIONAL DEEP DIVE")
        print("Understanding the Vulnerability to Build Better Defenses")
        print("🎓" * 40)
        print()
        
        encryption_info = self.explain_encryption_mechanism()
        db_info = self.demonstrate_database_structure()
        attack_steps = self.explain_attack_scenario()
        defenses = self.explain_defenses()
        monitoring = self.demonstrate_monitoring()
        
        saved_file = self.save_education_report(
            encryption_info, db_info, attack_steps, defenses, monitoring
        )
        
        print("=" * 80)
        print("EDUCATION COMPLETE")
        print("=" * 80)
        print(f"\n💾 Full report saved to: {saved_file}")
        print("\n📚 KEY LESSONS:")
        print("  1. Encryption ≠ Security against local malware")
        print("  2. OS keyring provides key to ANY process running as you")
        print("  3. Best defense: Password manager + 2FA + monitoring")
        print("  4. Detection is critical - know when attack happens")
        print("  5. Prevention: Keep software updated, be careful what you run")
        print("\n" + "=" * 80)
        print()


if __name__ == "__main__":
    educator = BrowserEncryptionEducator()
    educator.run_education()
