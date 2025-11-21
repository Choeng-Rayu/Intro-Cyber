#!/usr/bin/env python3
"""
BROWSER SECURITY AUDIT TOOL (Educational - Defensive Security)

This tool demonstrates:
1. What sensitive data browsers store and WHERE
2. How to detect outdated/vulnerable browser versions
3. How to audit browser security configurations
4. Defense mechanisms against data theft attacks

EDUCATIONAL PURPOSE ONLY - Learn to DEFEND against attacks
"""

import os
import subprocess
import json
import sqlite3
from pathlib import Path
from datetime import datetime


class BrowserSecurityAuditor:
    """Audit browser security and demonstrate attack surface"""
    
    def __init__(self):
        self.home = Path.home()
        self.browsers = {
            'chrome': self.home / '.config/google-chrome/Default',
            'chromium': self.home / '.config/chromium/Default',
            'firefox': self.home / '.mozilla/firefox',
            'brave': self.home / '.config/BraveSoftware/Brave-Browser/Default',
        }
        self.vulnerabilities_found = []
        self.sensitive_data_locations = []
        self.browser_versions = {}
        self.audit_timestamp = datetime.now().isoformat()
        
        # Create data directory if it doesn't exist
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def print_header(self):
        print("=" * 80)
        print("BROWSER SECURITY AUDIT - EDUCATIONAL TOOL")
        print("Understanding Attack Surfaces to Build Better Defenses")
        print("=" * 80)
        print()
    
    def check_browser_versions(self):
        """Detect outdated browser versions - KEY DEFENSE #1"""
        print("[1] CHECKING BROWSER VERSIONS (Outdated = Vulnerable)")
        print("-" * 80)
        
        browser_commands = {
            'Google Chrome': ['google-chrome', '--version'],
            'Chromium': ['chromium-browser', '--version'],
            'Firefox': ['firefox', '--version'],
            'Brave': ['brave-browser', '--version'],
        }
        
        for browser, cmd in browser_commands.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.browser_versions[browser] = {
                        'version': version,
                        'installed': True,
                        'status': 'active'
                    }
                    print(f"✓ {browser}: {version}")
                    print(f"  → Check https://chromiumdash.appspot.com/releases for latest version")
                    print(f"  → DEFENSE: Keep browsers updated to patch known CVEs\n")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                self.browser_versions[browser] = {
                    'version': 'N/A',
                    'installed': False,
                    'status': 'not_found'
                }
                print(f"✗ {browser}: Not installed or not in PATH\n")
    
    def demonstrate_sensitive_data_locations(self):
        """EDUCATIONAL: Show what attackers target and WHY"""
        print("\n[2] SENSITIVE DATA STORAGE LOCATIONS")
        print("-" * 80)
        print("Understanding what attackers want helps you protect it better.\n")
        
        for browser_name, profile_path in self.browsers.items():
            if profile_path.exists():
                print(f"📁 {browser_name.upper()} Profile: {profile_path}")
                
                # Key files attackers target
                sensitive_files = {
                    'Login Data': 'SQLite DB with encrypted passwords',
                    'Cookies': 'Session tokens for websites',
                    'History': 'Browsing history (SQLite)',
                    'Bookmarks': 'User bookmarks',
                    'Web Data': 'Autofill data (addresses, credit cards)',
                    'Preferences': 'Settings and configurations',
                }
                
                for filename, description in sensitive_files.items():
                    file_path = profile_path / filename
                    if file_path.exists():
                        size = file_path.stat().st_size
                        perms = oct(file_path.stat().st_mode)[-3:]
                        print(f"  ├─ {filename:15} | {description:30} | {size:,} bytes | Perms: {perms}")
                        self.sensitive_data_locations.append({
                            'browser': browser_name,
                            'file': filename,
                            'path': str(file_path),
                            'size': size,
                            'permissions': perms,
                            'description': description,
                            'exists': True
                        })
                    else:
                        print(f"  ├─ {filename:15} | {description:30} | NOT FOUND")
                
                print(f"  └─ DEFENSE TIPS:")
                print(f"     • Use browser's password manager WITH master password")
                print(f"     • Enable 2FA on all accounts")
                print(f"     • Clear cookies regularly")
                print(f"     • Use private browsing for sensitive activities\n")
    
    def audit_file_permissions(self):
        """Check if browser data has secure permissions"""
        print("\n[3] FILE PERMISSION AUDIT")
        print("-" * 80)
        print("Weak permissions = Easy access for malware\n")
        
        for location in self.sensitive_data_locations:
            if isinstance(location, dict):
                path = Path(location['path'])
            else:
                path = Path(location)
            
            if path.exists():
                stat_info = path.stat()
                perms = oct(stat_info.st_mode)[-3:]
                
                # Check if permissions are too open
                if perms != '600' and perms != '700':
                    print(f"⚠️  WEAK PERMISSIONS: {path.name}")
                    print(f"   Path: {path}")
                    print(f"   Current: {perms} | Recommended: 600 (user read/write only)")
                    print(f"   Fix: chmod 600 '{path}'")
                    self.vulnerabilities_found.append({
                        'type': 'weak_permissions',
                        'file': str(path),
                        'filename': path.name,
                        'current_perms': perms,
                        'recommended_perms': '600',
                        'severity': 'medium'
                    })
                else:
                    print(f"✓ Good permissions: {path.name} ({perms})")
        print()
    
    def demonstrate_password_encryption(self):
        """EDUCATIONAL: Show how browsers encrypt passwords (but don't decrypt)"""
        print("\n[4] PASSWORD ENCRYPTION ANALYSIS")
        print("-" * 80)
        print("This demonstrates WHY encrypted ≠ safe from local attacks\n")
        
        for browser_name, profile_path in self.browsers.items():
            login_db = profile_path / 'Login Data'
            if login_db.exists():
                print(f"🔐 {browser_name.upper()} Password Storage")
                print(f"   Database: {login_db}")
                
                try:
                    # Read database structure (educational)
                    conn = sqlite3.connect(f"file:{login_db}?mode=ro", uri=True)
                    cursor = conn.cursor()
                    
                    # Count stored credentials
                    cursor.execute("SELECT COUNT(*) FROM logins")
                    count = cursor.fetchone()[0]
                    print(f"   Stored credentials: {count}")
                    
                    # Show table structure (not actual passwords)
                    cursor.execute("PRAGMA table_info(logins)")
                    columns = cursor.fetchall()
                    print(f"   Database columns: {', '.join([col[1] for col in columns])}")
                    
                    print(f"\n   HOW ATTACKERS EXPLOIT THIS:")
                    print(f"   1. Chrome encrypts passwords using OS-level encryption (Linux: libsecret/keyring)")
                    print(f"   2. Encryption key is tied to USER account, not a password")
                    print(f"   3. If attacker runs code AS YOUR USER → they can decrypt!")
                    print(f"   4. Exploit grants code execution → game over")
                    
                    print(f"\n   DEFENSE STRATEGIES:")
                    print(f"   ✓ Use a dedicated password manager (1Password, Bitwarden)")
                    print(f"   ✓ Enable browser master password if available")
                    print(f"   ✓ Use disk encryption (LUKS on Linux)")
                    print(f"   ✓ Lock screen when away from computer")
                    print(f"   ✓ Keep browser updated to prevent code execution exploits\n")
                    
                    conn.close()
                except sqlite3.Error as e:
                    print(f"   Database locked or inaccessible: {e}\n")
    
    def demonstrate_attack_flow(self):
        """EDUCATIONAL: Explain the complete attack chain"""
        print("\n[5] COMPLETE ATTACK FLOW EXPLANATION")
        print("-" * 80)
        print("Understanding the full attack helps you defend at EACH stage\n")
        
        attack_stages = [
            {
                'stage': '1. Initial Access',
                'attacker_action': 'Victim visits malicious website or opens phishing email',
                'exploit': 'Triggers browser vulnerability (memory corruption, XSS, etc.)',
                'defense': [
                    'Keep browser updated',
                    'Use ad blocker',
                    'Enable Safe Browsing',
                    'Don\'t click suspicious links'
                ]
            },
            {
                'stage': '2. Code Execution',
                'attacker_action': 'Exploit runs JavaScript or native code',
                'exploit': 'Escapes browser sandbox (if unpatched vulnerability)',
                'defense': [
                    'Update OS kernel',
                    'Use security-focused browser (Brave, Firefox)',
                    'Enable site isolation',
                    'Disable unnecessary browser features'
                ]
            },
            {
                'stage': '3. Privilege Escalation',
                'attacker_action': 'Code runs with user privileges',
                'exploit': 'Can now read user files including browser data',
                'defense': [
                    'Use AppArmor/SELinux to restrict browser',
                    'Run browser in Firejail sandbox',
                    'Use separate user account for browsing',
                    'Enable file access monitoring'
                ]
            },
            {
                'stage': '4. Data Collection',
                'attacker_action': 'Reads Login Data, Cookies, History databases',
                'exploit': 'Decrypts passwords using OS APIs',
                'defense': [
                    'Use password manager instead of browser',
                    'Enable 2FA everywhere',
                    'Use hardware security keys (YubiKey)',
                    'Monitor file access logs'
                ]
            },
            {
                'stage': '5. Exfiltration',
                'attacker_action': 'Sends data to attacker server',
                'exploit': 'Uses HTTPS, DNS tunneling, or other covert channels',
                'defense': [
                    'Use firewall to block suspicious connections',
                    'Monitor network traffic',
                    'Use DNS filtering (Pi-hole)',
                    'Enable intrusion detection (Snort, Suricata)'
                ]
            },
            {
                'stage': '6. Persistence',
                'attacker_action': 'Installs malicious browser extension',
                'exploit': 'Continues monitoring even after reboot',
                'defense': [
                    'Audit browser extensions regularly',
                    'Only install extensions from official stores',
                    'Review extension permissions',
                    'Use browser extension allowlist'
                ]
            }
        ]
        
        for stage in attack_stages:
            print(f"{'='*80}")
            print(f"{stage['stage']}: {stage['attacker_action']}")
            print(f"{'='*80}")
            print(f"Exploit Technique: {stage['exploit']}\n")
            print("DEFENSE MECHANISMS:")
            for i, defense in enumerate(stage['defense'], 1):
                print(f"  {i}. {defense}")
            print()
    
    def security_recommendations(self):
        """Provide actionable security recommendations"""
        print("\n[6] SECURITY RECOMMENDATIONS")
        print("-" * 80)
        
        print("IMMEDIATE ACTIONS:")
        print("  1. Update all browsers to latest version")
        print("  2. Enable 2FA on critical accounts (email, banking, social media)")
        print("  3. Install password manager (Bitwarden, 1Password)")
        print("  4. Review and remove unused browser extensions")
        print("  5. Clear cookies and browsing data regularly\n")
        
        print("MEDIUM-TERM HARDENING:")
        print("  6. Enable disk encryption (LUKS/FileVault/BitLocker)")
        print("  7. Set up firewall rules to block suspicious traffic")
        print("  8. Install browser security extensions (uBlock Origin, HTTPS Everywhere)")
        print("  9. Use DNS-level blocking (Pi-hole, NextDNS)")
        print("  10. Enable automatic security updates\n")
        
        print("ADVANCED SECURITY:")
        print("  11. Run browser in sandbox (Firejail, Flatpak)")
        print("  12. Use separate browser profiles for different activities")
        print("  13. Enable AppArmor/SELinux browser confinement")
        print("  14. Set up file integrity monitoring (AIDE, Tripwire)")
        print("  15. Use hardware security keys for authentication\n")
    
    def create_monitoring_script(self):
        """Generate a script to monitor browser data access"""
        print("\n[7] CREATING MONITORING SCRIPT")
        print("-" * 80)
        
        monitor_script = """#!/bin/bash
# Browser Data Access Monitor - Defensive Security Tool
# This script monitors access to sensitive browser files and alerts on suspicious activity

BROWSER_DIRS=(
    "$HOME/.config/google-chrome/Default"
    "$HOME/.config/chromium/Default"
    "$HOME/.mozilla/firefox"
    "$HOME/.config/BraveSoftware/Brave-Browser/Default"
)

LOG_FILE="$HOME/browser_access_monitor.log"

echo "[$(date)] Browser security monitoring started" | tee -a "$LOG_FILE"

# Monitor file access using inotify
for DIR in "${BROWSER_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        echo "Monitoring: $DIR"
        
        # Watch for access to sensitive files
        inotifywait -m -e access -e open --format '%T %w%f %e' --timefmt '%Y-%m-%d %H:%M:%S' \\
            "$DIR/Login Data" \\
            "$DIR/Cookies" \\
            "$DIR/History" \\
            2>/dev/null | while read line; do
                echo "[ALERT] $line" | tee -a "$LOG_FILE"
                
                # Optional: Send notification
                # notify-send "Browser Security Alert" "Suspicious access detected: $line"
        done &
    fi
done

echo "Monitoring active. Logs: $LOG_FILE"
echo "Press Ctrl+C to stop"
wait
"""
        
        script_path = Path.home() / 'browser_monitor.sh'
        with open(script_path, 'w') as f:
            f.write(monitor_script)
        
        os.chmod(script_path, 0o755)
        
        print(f"✓ Created monitoring script: {script_path}")
        print(f"  Usage: ./{script_path.name}")
        print(f"  Requires: inotify-tools (install: sudo apt install inotify-tools)")
        print(f"  This script will alert you when programs access browser data")
        print(f"  Unexpected access = potential malware activity!\n")
    
    def save_audit_results(self):
        """Save audit results to JSON file in data directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"browser_security_audit_{timestamp}.json"
        filepath = self.data_dir / filename
        
        audit_data = {
            'audit_timestamp': self.audit_timestamp,
            'audit_type': 'browser_security_audit',
            'system_info': {
                'home_directory': str(self.home),
                'audit_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            'browser_versions': self.browser_versions,
            'sensitive_data_locations': self.sensitive_data_locations,
            'vulnerabilities_found': self.vulnerabilities_found,
            'summary': {
                'total_browsers_detected': len([b for b in self.browser_versions.values() if b['installed']]),
                'total_sensitive_files': len(self.sensitive_data_locations),
                'total_vulnerabilities': len(self.vulnerabilities_found),
                'security_status': 'vulnerable' if self.vulnerabilities_found else 'secure'
            },
            'recommendations': [
                'Update all browsers to latest version',
                'Enable 2FA on critical accounts',
                'Install password manager (Bitwarden, 1Password)',
                'Review and remove unused browser extensions',
                'Clear cookies and browsing data regularly',
                'Enable disk encryption (LUKS/FileVault/BitLocker)',
                'Set up firewall rules',
                'Run browser in sandbox (Firejail, Flatpak)'
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(audit_data, f, indent=2)
        
        return filepath
    
    def generate_report(self):
        """Generate comprehensive security report"""
        print("\n[8] SECURITY AUDIT SUMMARY")
        print("=" * 80)
        
        if self.vulnerabilities_found:
            print(f"⚠️  Found {len(self.vulnerabilities_found)} potential vulnerabilities:\n")
            for vuln in self.vulnerabilities_found:
                print(f"  • {vuln['type']}: {vuln.get('filename', vuln['file'])}")
        else:
            print("✓ No obvious vulnerabilities detected")
        
        print(f"\n📊 Sensitive data locations identified: {len(self.sensitive_data_locations)}")
        
        # Save results to file
        saved_file = self.save_audit_results()
        print(f"\n💾 Audit results saved to: {saved_file}")
        
        print(f"\nREMEMBER:")
        print("  • Security is a process, not a destination")
        print("  • Defense in depth: multiple layers of protection")
        print("  • Update regularly, monitor actively, respond quickly")
        print("  • Understanding attacks = building better defenses")
        print("=" * 80)
    
    def run_audit(self):
        """Run complete security audit"""
        self.print_header()
        self.check_browser_versions()
        self.demonstrate_sensitive_data_locations()
        self.audit_file_permissions()
        self.demonstrate_password_encryption()
        self.demonstrate_attack_flow()
        self.security_recommendations()
        self.create_monitoring_script()
        self.generate_report()


if __name__ == "__main__":
    auditor = BrowserSecurityAuditor()
    auditor.run_audit()
