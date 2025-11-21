#!/usr/bin/env python3
"""
BROWSER ATTACK DEFENSE SIMULATOR
Educational tool demonstrating how to DETECT and PREVENT browser attacks

This shows defensive security concepts:
1. How to detect suspicious file access patterns
2. How to implement defense mechanisms
3. How to respond to potential threats

ETHICAL USE ONLY - For learning defense strategies
"""

import os
import time
import hashlib
from pathlib import Path
from datetime import datetime
import json


class BrowserDefenseSimulator:
    """Demonstrates defensive security techniques"""
    
    def __init__(self):
        self.home = Path.home()
        self.chrome_profile = self.home / '.config/google-chrome/Default'
        self.monitored_files = [
            'Login Data',
            'Cookies',
            'History',
            'Web Data'
        ]
        self.file_hashes = {}
        self.access_log = []
    
    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash to detect file modifications"""
        try:
            sha256 = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return None
    
    def baseline_files(self):
        """Create baseline hashes of browser files (integrity monitoring)"""
        print("=" * 80)
        print("DEFENSE TECHNIQUE #1: File Integrity Monitoring")
        print("=" * 80)
        print("Creating baseline hashes of sensitive browser files...")
        print("Any modification will be detected!\n")
        
        for filename in self.monitored_files:
            filepath = self.chrome_profile / filename
            if filepath.exists():
                file_hash = self.calculate_file_hash(filepath)
                self.file_hashes[str(filepath)] = {
                    'hash': file_hash,
                    'size': filepath.stat().st_size,
                    'modified': filepath.stat().st_mtime,
                    'baseline_time': time.time()
                }
                print(f"✓ Baselined: {filename}")
                print(f"  Hash: {file_hash[:16]}...")
                print(f"  Size: {filepath.stat().st_size:,} bytes\n")
        
        print(f"💾 Baseline saved. Any tampering will be detected!\n")
    
    def check_integrity(self):
        """Check if monitored files have been modified"""
        print("=" * 80)
        print("DEFENSE TECHNIQUE #2: Integrity Verification")
        print("=" * 80)
        print("Checking for unauthorized modifications...\n")
        
        violations = []
        for filepath_str, baseline in self.file_hashes.items():
            filepath = Path(filepath_str)
            if filepath.exists():
                current_hash = self.calculate_file_hash(filepath)
                current_size = filepath.stat().st_size
                
                if current_hash != baseline['hash']:
                    violations.append({
                        'file': filepath.name,
                        'type': 'hash_mismatch',
                        'baseline_hash': baseline['hash'][:16],
                        'current_hash': current_hash[:16],
                    })
                    print(f"🚨 ALERT: {filepath.name} has been MODIFIED!")
                    print(f"   Baseline hash: {baseline['hash'][:32]}...")
                    print(f"   Current hash:  {current_hash[:32]}...")
                    print(f"   → Possible malware activity or normal browser update\n")
                elif current_size != baseline['size']:
                    print(f"⚠️  {filepath.name} size changed (browser update?)")
                    print(f"   Baseline: {baseline['size']:,} bytes")
                    print(f"   Current:  {current_size:,} bytes\n")
                else:
                    print(f"✓ {filepath.name} - No changes detected\n")
        
        if not violations:
            print("✅ All monitored files are intact!\n")
        else:
            print(f"⚠️  Found {len(violations)} potential security incidents\n")
        
        return violations
    
    def demonstrate_access_monitoring(self):
        """Show how to monitor file access patterns"""
        print("=" * 80)
        print("DEFENSE TECHNIQUE #3: Access Pattern Monitoring")
        print("=" * 80)
        print("Monitoring which processes access browser data...\n")
        
        print("NORMAL ACCESS PATTERNS:")
        print("  ✓ Chrome/Brave browser processes (expected)")
        print("  ✓ Backup software (if scheduled)")
        print("  ✓ Anti-virus scanner (periodic scans)\n")
        
        print("SUSPICIOUS ACCESS PATTERNS:")
        print("  🚨 Unknown Python/Bash scripts")
        print("  🚨 Processes running from /tmp/ or /dev/shm/")
        print("  🚨 Access at unusual times (3 AM)")
        print("  🚨 Rapid sequential access to multiple files")
        print("  🚨 Processes with names mimicking system tools\n")
        
        print("MONITORING COMMAND:")
        print("  sudo auditctl -w ~/.config/google-chrome/Default/Login\\ Data -p ra")
        print("  sudo ausearch -f 'Login Data' --interpret\n")
        
        print("REAL-TIME MONITORING:")
        print("  inotifywait -m -e access ~/.config/google-chrome/Default/Login\\ Data\n")
    
    def demonstrate_network_defense(self):
        """Show network-level defenses"""
        print("=" * 80)
        print("DEFENSE TECHNIQUE #4: Network Traffic Monitoring")
        print("=" * 80)
        print("Detecting data exfiltration attempts...\n")
        
        print("NORMAL BROWSER TRAFFIC:")
        print("  ✓ HTTPS to known domains (google.com, github.com)")
        print("  ✓ DNS queries to legitimate resolvers")
        print("  ✓ Moderate bandwidth usage\n")
        
        print("SUSPICIOUS TRAFFIC (Possible exfiltration):")
        print("  🚨 Large uploads to unknown domains")
        print("  🚨 Connections to IP addresses (not domains)")
        print("  🚨 Unusual ports (4444, 8080, 31337)")
        print("  🚨 DNS tunneling (excessive DNS queries)")
        print("  🚨 Tor/VPN usage by browser (unexpected)\n")
        
        print("MONITORING COMMANDS:")
        print("  # Show all Chrome connections")
        print("  sudo netstat -tunap | grep chrome\n")
        
        print("  # Monitor uploaded data")
        print("  sudo iftop -i wlan0\n")
        
        print("  # DNS query monitoring")
        print("  sudo tcpdump -i any port 53\n")
        
        print("  # Deep packet inspection")
        print("  sudo wireshark -i wlan0 -f 'tcp port 443'\n")
    
    def demonstrate_sandboxing(self):
        """Show how to run browser in isolated environment"""
        print("=" * 80)
        print("DEFENSE TECHNIQUE #5: Application Sandboxing")
        print("=" * 80)
        print("Isolate browser to limit damage from exploits...\n")
        
        print("FIREJAIL SANDBOX:")
        print("  # Run Chrome in isolated environment")
        print("  firejail --seccomp --private --private-tmp google-chrome\n")
        
        print("  Benefits:")
        print("    ✓ Browser can't access other user files")
        print("    ✓ Limited system call access (--seccomp)")
        print("    ✓ Isolated /tmp directory")
        print("    ✓ Network namespace isolation\n")
        
        print("FLATPAK SANDBOX:")
        print("  # Install sandboxed Chrome")
        print("  flatpak install flathub org.chromium.Chromium")
        print("  flatpak run org.chromium.Chromium\n")
        
        print("  Benefits:")
        print("    ✓ Mandatory Access Control")
        print("    ✓ Portal-based file access")
        print("    ✓ Automatic updates")
        print("    ✓ Per-app permissions\n")
        
        print("APPARMOR PROFILE:")
        print("  # Enable AppArmor confinement")
        print("  sudo aa-enforce /etc/apparmor.d/usr.bin.google-chrome")
        print("  sudo systemctl reload apparmor\n")
    
    def demonstrate_incident_response(self):
        """Show how to respond to suspected breach"""
        print("=" * 80)
        print("DEFENSE TECHNIQUE #6: Incident Response")
        print("=" * 80)
        print("What to do if you suspect browser compromise...\n")
        
        print("IMMEDIATE ACTIONS (First 5 minutes):")
        print("  1. Disconnect from network")
        print("     sudo nmcli networking off")
        print("  2. Kill suspicious processes")
        print("     pkill -9 chrome")
        print("  3. Take memory snapshot (if forensics needed)")
        print("     sudo dd if=/dev/mem of=/tmp/memory.dump bs=1M\n")
        
        print("SHORT-TERM RESPONSE (First hour):")
        print("  4. Change all passwords from DIFFERENT device")
        print("  5. Enable 2FA on critical accounts")
        print("  6. Review browser extensions")
        print("     chrome://extensions")
        print("  7. Check cron jobs and startup items")
        print("     crontab -l")
        print("     ls ~/.config/autostart/")
        print("  8. Scan for malware")
        print("     sudo clamscan -r --bell -i ~/")
        print("     sudo rkhunter --check\n")
        
        print("FORENSIC ANALYSIS:")
        print("  9. Check browser process tree")
        print("     ps auxf | grep chrome")
        print("  10. Review network connections")
        print("     sudo netstat -tunap")
        print("  11. Examine recent file access")
        print("     find ~/.config/google-chrome -type f -mmin -60")
        print("  12. Check system logs")
        print("     sudo journalctl -xe | grep -i chrome")
        print("  13. Analyze browser history")
        print("     sqlite3 ~/.config/google-chrome/Default/History")
        print("       SELECT url, visit_count, last_visit_time FROM urls;")
        print("  14. Export logs for analysis")
        print("     sudo ausearch -ts recent > audit_log.txt\n")
        
        print("RECOVERY:")
        print("  15. Reinstall browser from official source")
        print("  16. Create new browser profile")
        print("  17. Restore bookmarks from backup")
        print("  18. Re-enable network after verification")
        print("  19. Monitor closely for 30 days\n")
    
    def generate_defense_checklist(self):
        """Create actionable security checklist"""
        print("=" * 80)
        print("BROWSER SECURITY DEFENSE CHECKLIST")
        print("=" * 80)
        
        checklist = {
            "Daily": [
                "[ ] Check browser version is up-to-date",
                "[ ] Review suspicious browser warnings",
                "[ ] Clear unnecessary cookies and cache",
            ],
            "Weekly": [
                "[ ] Audit installed browser extensions",
                "[ ] Review browser permissions (camera, mic, location)",
                "[ ] Check for suspicious network connections",
                "[ ] Verify file integrity of browser profile",
            ],
            "Monthly": [
                "[ ] Update all software and OS patches",
                "[ ] Run full anti-malware scan",
                "[ ] Review 2FA settings on accounts",
                "[ ] Audit saved passwords and remove duplicates",
                "[ ] Check for rootkits (rkhunter, chkrootkit)",
            ],
            "Quarterly": [
                "[ ] Penetration test your own system",
                "[ ] Review firewall rules",
                "[ ] Update security policies",
                "[ ] Train on new attack techniques",
                "[ ] Backup browser profile and verify restore",
            ]
        }
        
        for period, items in checklist.items():
            print(f"\n{period.upper()} TASKS:")
            for item in items:
                print(f"  {item}")
        
        print("\n" + "=" * 80)
        print()
        
        # Save checklist to file
        checklist_path = self.home / 'browser_security_checklist.json'
        with open(checklist_path, 'w') as f:
            json.dump(checklist, f, indent=2)
        
        print(f"💾 Checklist saved to: {checklist_path}\n")
    
    def run_simulation(self):
        """Run complete defense demonstration"""
        print("\n" + "=" * 80)
        print("BROWSER ATTACK DEFENSE SIMULATOR")
        print("Learning Defense Through Understanding Attacks")
        print("=" * 80 + "\n")
        
        self.baseline_files()
        input("Press Enter to check file integrity...")
        
        self.check_integrity()
        input("Press Enter to see access monitoring...")
        
        self.demonstrate_access_monitoring()
        input("Press Enter to see network defenses...")
        
        self.demonstrate_network_defense()
        input("Press Enter to see sandboxing techniques...")
        
        self.demonstrate_sandboxing()
        input("Press Enter to see incident response...")
        
        self.demonstrate_incident_response()
        
        self.generate_defense_checklist()
        
        print("=" * 80)
        print("SIMULATION COMPLETE")
        print("=" * 80)
        print("\nKey Takeaways:")
        print("  1. Defense in depth - Multiple layers of protection")
        print("  2. Monitoring is essential - Know what's normal")
        print("  3. Incident response planning - Prepare before breach")
        print("  4. Regular updates - Patches are your first defense")
        print("  5. Education - Understanding attacks builds better defenses")
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    simulator = BrowserDefenseSimulator()
    simulator.run_simulation()
