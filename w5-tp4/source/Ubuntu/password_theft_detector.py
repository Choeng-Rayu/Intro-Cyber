#!/usr/bin/env python3
"""
BROWSER PASSWORD THEFT DETECTION & PREVENTION SYSTEM

This defensive tool focuses on:
1. Real-time monitoring of browser password database access
2. Detection of suspicious processes accessing keyring
3. File integrity monitoring for Login Data files
4. Alerting system for potential theft attempts
5. Automated defensive responses

DEFENSIVE PURPOSE: Protect users from password-stealing malware
"""

import os
import sqlite3
import hashlib
import json
import time
import psutil
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import threading


class PasswordTheftDetector:
    """Real-time detection system for password theft attempts"""
    
    def __init__(self):
        self.home = Path.home()
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Browser paths to monitor
        self.browser_paths = {
            'chrome': self.home / '.config/google-chrome/Default/Login Data',
            'chromium': self.home / '.config/chromium/Default/Login Data',
            'brave': self.home / '.config/BraveSoftware/Brave-Browser/Default/Login Data',
            'edge': self.home / '.config/microsoft-edge/Default/Login Data',
        }
        
        # File integrity baselines
        self.file_hashes = {}
        self.access_log = defaultdict(list)
        self.suspicious_processes = []
        
        # Alert thresholds
        self.max_accesses_per_minute = 3
        self.suspicious_keywords = ['python', 'bash', 'sh', 'perl', 'ruby', 'node']
        
        self.monitoring = False
    
    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash of file for integrity checking"""
        if not filepath.exists():
            return None
        
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (PermissionError, IOError):
            return None
    
    def initialize_baselines(self):
        """Create baseline hashes for all browser databases"""
        print("🔐 Initializing file integrity baselines...")
        print("=" * 80)
        
        for browser, path in self.browser_paths.items():
            if path.exists():
                file_hash = self.calculate_file_hash(path)
                if file_hash:
                    self.file_hashes[str(path)] = {
                        'hash': file_hash,
                        'size': path.stat().st_size,
                        'mtime': path.stat().st_mtime,
                        'browser': browser,
                        'baseline_time': datetime.now().isoformat()
                    }
                    # print(f"✓ {browser:10} - Baseline created Password: {file_hash[:16]}...")
                    print(f"✓ {browser:10} - Baseline created Password: {path}...")

                else:
                    print(f"✗ {browser:10} - Could not read file")
            else:
                print(f"- {browser:10} - Not installed")
        
        print("=" * 80)
        print(f"📊 Monitoring {len(self.file_hashes)} browser databases\n")
    
    def check_file_integrity(self):
        """Check if any browser database has been modified"""
        violations = []
        
        for filepath, baseline in self.file_hashes.items():
            path = Path(filepath)
            if not path.exists():
                violations.append({
                    'type': 'FILE_DELETED',
                    'browser': baseline['browser'],
                    'path': filepath,
                    'severity': 'CRITICAL'
                })
                continue
            
            current_hash = self.calculate_file_hash(path)
            current_size = path.stat().st_size
            current_mtime = path.stat().st_mtime
            
            # Check for modifications
            if current_hash != baseline['hash']:
                violations.append({
                    'type': 'FILE_MODIFIED',
                    'browser': baseline['browser'],
                    'path': filepath,
                    'old_hash': baseline['hash'][:16],
                    'new_hash': current_hash[:16] if current_hash else 'N/A',
                    'size_change': current_size - baseline['size'],
                    'severity': 'HIGH'
                })
            
            # Check for suspicious access times
            if current_mtime != baseline['mtime']:
                hour = datetime.fromtimestamp(current_mtime).hour
                if hour < 6 or hour > 23:  # Late night access
                    violations.append({
                        'type': 'SUSPICIOUS_ACCESS_TIME',
                        'browser': baseline['browser'],
                        'path': filepath,
                        'access_time': datetime.fromtimestamp(current_mtime).isoformat(),
                        'severity': 'MEDIUM'
                    })
        
        return violations
    
    def scan_processes_accessing_databases(self):
        """Find processes currently accessing browser databases"""
        suspicious = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
                try:
                    # Get open files
                    open_files = proc.open_files()
                    
                    for file in open_files:
                        # Check if accessing any browser database
                        for browser, db_path in self.browser_paths.items():
                            if str(db_path) in file.path:
                                # Check if it's not the legitimate browser
                                proc_name = proc.info['name'].lower()
                                
                                is_legitimate = any(b in proc_name for b in ['chrome', 'chromium', 'brave', 'edge', 'firefox'])
                                
                                if not is_legitimate:
                                    suspicious.append({
                                        'type': 'UNAUTHORIZED_ACCESS',
                                        'process_name': proc.info['name'],
                                        'pid': proc.info['pid'],
                                        'cmdline': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else 'N/A',
                                        'username': proc.info['username'],
                                        'browser_db': browser,
                                        'file_path': file.path,
                                        'severity': 'CRITICAL',
                                        'timestamp': datetime.now().isoformat()
                                    })
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        
        except Exception as e:
            print(f"⚠️  Error scanning processes: {e}")
        
        return suspicious
    
    def check_keyring_access(self):
        """Monitor processes accessing system keyring"""
        suspicious = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    proc_name = proc.info['name'].lower()
                    
                    # Look for keyring-related keywords
                    keyring_keywords = ['secretstorage', 'keyring', 'libsecret', 'gnome-keyring']
                    
                    if any(keyword in cmdline.lower() for keyword in keyring_keywords):
                        # Check if it's a suspicious process type
                        if any(suspicious_type in proc_name for suspicious_type in self.suspicious_keywords):
                            suspicious.append({
                                'type': 'KEYRING_ACCESS',
                                'process_name': proc.info['name'],
                                'pid': proc.info['pid'],
                                'cmdline': cmdline,
                                'username': proc.info['username'],
                                'severity': 'HIGH',
                                'timestamp': datetime.now().isoformat()
                            })
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        
        except Exception as e:
            print(f"⚠️  Error checking keyring access: {e}")
        
        return suspicious
    
    def analyze_database_queries(self, browser_path):
        """Analyze recent queries to browser database (if accessible)"""
        analysis = {
            'accessible': False,
            'credential_count': 0,
            'recent_modifications': False,
            'suspicious_activity': []
        }
        
        if not browser_path.exists():
            return analysis
        
        try:
            # Try read-only access
            conn = sqlite3.connect(f"file:{browser_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            analysis['accessible'] = True
            
            # Count credentials
            cursor.execute("SELECT COUNT(*) FROM logins")
            analysis['credential_count'] = cursor.fetchone()[0]
            
            # Check for recent modifications (if table has timestamp columns)
            try:
                cursor.execute("SELECT MAX(date_created), MAX(date_last_used) FROM logins")
                dates = cursor.fetchone()
                if dates[0] or dates[1]:
                    analysis['recent_modifications'] = True
            except sqlite3.Error:
                pass
            
            conn.close()
            
        except sqlite3.Error as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def generate_alert(self, detections):
        """Generate alert report for detected threats"""
        if not detections:
            return None
        
        alert = {
            'alert_id': hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
            'timestamp': datetime.now().isoformat(),
            'severity': max([d.get('severity', 'LOW') for d in detections], 
                          key=lambda x: ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'].index(x)),
            'detection_count': len(detections),
            'detections': detections,
            'recommended_actions': self.get_recommended_actions(detections)
        }
        
        return alert
    
    def get_recommended_actions(self, detections):
        """Provide recommended actions based on detections"""
        actions = []
        
        detection_types = [d['type'] for d in detections]
        severities = [d.get('severity', 'LOW') for d in detections]
        
        if 'UNAUTHORIZED_ACCESS' in detection_types:
            actions.extend([
                "🚨 IMMEDIATE: Terminate unauthorized processes accessing password database",
                "🔒 Change all saved passwords from a different device",
                "🔍 Run full system malware scan",
                "💻 Review running processes and startup items"
            ])
        
        if 'KEYRING_ACCESS' in detection_types:
            actions.extend([
                "⚠️  Investigate processes accessing system keyring",
                "🔐 Consider using hardware security key (YubiKey)",
                "📝 Review installed applications and scripts"
            ])
        
        if 'FILE_MODIFIED' in detection_types or 'FILE_DELETED' in detection_types:
            actions.extend([
                "🔄 Restore browser database from backup if available",
                "🔍 Check system logs for unauthorized activity",
                "🛡️  Enable file integrity monitoring (AIDE/Tripwire)"
            ])
        
        if 'CRITICAL' in severities:
            actions.insert(0, "🆘 CRITICAL THREAT: Disconnect from network immediately")
            actions.append("📞 Consider contacting security professional")
        
        # Always add general recommendations
        actions.extend([
            "✓ Enable 2FA on all accounts",
            "✓ Use dedicated password manager (Bitwarden, 1Password)",
            "✓ Keep system and browser updated"
        ])
        
        return actions
    
    def save_alert(self, alert):
        """Save alert to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_alert_{timestamp}.json"
        filepath = self.data_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(alert, f, indent=2)
        
        return filepath
    
    def display_alert(self, alert):
        """Display alert in terminal"""
        severity_colors = {
            'LOW': '💚',
            'MEDIUM': '💛',
            'HIGH': '🧡',
            'CRITICAL': '🔴'
        }
        
        print("\n" + "=" * 80)
        print(f"{severity_colors[alert['severity']]} SECURITY ALERT - {alert['severity']} SEVERITY")
        print("=" * 80)
        print(f"Alert ID: {alert['alert_id']}")
        print(f"Time: {alert['timestamp']}")
        print(f"Detections: {alert['detection_count']}")
        print()
        
        print("DETECTED THREATS:")
        print("-" * 80)
        for i, detection in enumerate(alert['detections'], 1):
            print(f"\n{i}. {detection['type']} - {detection.get('severity', 'UNKNOWN')}")
            for key, value in detection.items():
                if key not in ['type', 'severity']:
                    print(f"   {key}: {value}")
        
        print("\n" + "=" * 80)
        print("RECOMMENDED ACTIONS:")
        print("=" * 80)
        for action in alert['recommended_actions']:
            print(f"  {action}")
        print("=" * 80 + "\n")
    
    def run_single_scan(self):
        """Run a single comprehensive security scan"""
        print("🔍 Running security scan...")
        print("=" * 80)
        
        all_detections = []
        
        # 1. File integrity check
        print("\n1️⃣  Checking file integrity...")
        integrity_violations = self.check_file_integrity()
        if integrity_violations:
            print(f"   ⚠️  Found {len(integrity_violations)} integrity violations")
            all_detections.extend(integrity_violations)
        else:
            print("   ✓ No integrity violations")
        
        # 2. Process monitoring
        print("\n2️⃣  Scanning for unauthorized database access...")
        process_violations = self.scan_processes_accessing_databases()
        if process_violations:
            print(f"   🚨 Found {len(process_violations)} unauthorized accesses")
            all_detections.extend(process_violations)
        else:
            print("   ✓ No unauthorized access detected")
        
        # 3. Keyring monitoring
        print("\n3️⃣  Monitoring keyring access...")
        keyring_violations = self.check_keyring_access()
        if keyring_violations:
            print(f"   ⚠️  Found {len(keyring_violations)} suspicious keyring accesses")
            all_detections.extend(keyring_violations)
        else:
            print("   ✓ No suspicious keyring access")
        
        # 4. Database analysis
        print("\n4️⃣  Analyzing browser databases...")
        for browser, path in self.browser_paths.items():
            if path.exists():
                analysis = self.analyze_database_queries(path)
                if analysis['accessible']:
                    print(f"   ✓ {browser}: {analysis['credential_count']} credentials stored")
        
        print("\n" + "=" * 80)
        
        # Generate alert if threats detected
        if all_detections:
            alert = self.generate_alert(all_detections)
            self.display_alert(alert)
            saved_path = self.save_alert(alert)
            print(f"💾 Alert saved to: {saved_path}\n")
            return alert
        else:
            print("✅ No threats detected - System appears secure\n")
            return None
    
    def run_continuous_monitoring(self, interval=60):
        """Run continuous monitoring loop"""
        print("🛡️  Starting continuous monitoring...")
        print(f"📊 Scan interval: {interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        self.monitoring = True
        scan_count = 0
        
        try:
            while self.monitoring:
                scan_count += 1
                print(f"\n{'='*80}")
                print(f"Scan #{scan_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*80}")
                
                self.run_single_scan()
                
                if self.monitoring:
                    print(f"⏳ Next scan in {interval} seconds...")
                    time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            self.monitoring = False
    
    def setup_system_monitoring(self):
        """Provide instructions for system-level monitoring setup"""
        print("=" * 80)
        print("SYSTEM-LEVEL MONITORING SETUP")
        print("=" * 80)
        print()
        
        print("To enable advanced monitoring, run these commands:\n")
        
        print("1️⃣  FILE INTEGRITY MONITORING (auditd):")
        print("-" * 80)
        for browser, path in self.browser_paths.items():
            if path.exists():
                print(f"# Monitor {browser} database")
                print(f"sudo auditctl -w {path} -p rwxa -k browser_password_{browser}")
        print()
        print("# View audit logs:")
        print("sudo ausearch -k browser_password_chrome -i")
        print()
        
        print("2️⃣  PROCESS MONITORING:")
        print("-" * 80)
        print("# Monitor for secretstorage usage:")
        print("ps aux | grep -E 'secret|keyring' | grep -v grep")
        print()
        print("# Real-time process monitoring:")
        print("watch -n 5 'ps aux | grep -E \"secret|keyring\" | grep -v grep'")
        print()
        
        print("3️⃣  NETWORK MONITORING:")
        print("-" * 80)
        print("# Monitor for data exfiltration:")
        print("sudo tcpdump -i any -n 'tcp port 443' -w /tmp/traffic.pcap")
        print()
        
        print("4️⃣  INSTALL INTRUSION DETECTION:")
        print("-" * 80)
        print("# Install AIDE (Advanced Intrusion Detection Environment)")
        print("sudo apt install aide")
        print("sudo aideinit")
        print("sudo aide --check")
        print()
        
        print("=" * 80)


class PasswordSecurityEducator:
    """Educational component about password security"""
    
    @staticmethod
    def explain_best_practices():
        """Explain password security best practices"""
        print("=" * 80)
        print("PASSWORD SECURITY BEST PRACTICES")
        print("=" * 80)
        print()
        
        practices = {
            "🔐 Use Password Manager": [
                "Install: Bitwarden (open-source), 1Password, or KeePassXC",
                "Benefits: Master password required for each access",
                "Encryption: Separate from OS keyring, more secure",
                "Sync: Encrypted cloud sync across devices"
            ],
            "🔑 Enable Two-Factor Authentication (2FA)": [
                "Authenticator apps: Authy, Google Authenticator",
                "Hardware keys: YubiKey, Google Titan",
                "SMS: Better than nothing but less secure",
                "Recovery codes: Store safely offline"
            ],
            "🛡️ Browser Security": [
                "Don't save passwords in browser (if possible)",
                "Use browser master password (Firefox supports this)",
                "Keep browser updated to latest version",
                "Use browser sandboxing (Firejail, Flatpak)"
            ],
            "🔍 Security Monitoring": [
                "Enable file integrity monitoring (AIDE)",
                "Monitor browser database access (auditd)",
                "Regular security scans (ClamAV, rkhunter)",
                "Review login activity on all accounts"
            ],
            "💻 System Security": [
                "Keep OS and all software updated",
                "Enable firewall (ufw on Ubuntu)",
                "Use AppArmor/SELinux profiles",
                "Don't run untrusted code/downloads",
                "Regular backups of important data"
            ]
        }
        
        for category, items in practices.items():
            print(f"\n{category}")
            print("-" * 80)
            for item in items:
                print(f"  • {item}")
        
        print("\n" + "=" * 80)
        print()


def main():
    """Main function with menu system"""
    detector = PasswordTheftDetector()
    educator = PasswordSecurityEducator()
    
    print("\n" + "🛡️" * 40)
    print("BROWSER PASSWORD THEFT DETECTION & PREVENTION SYSTEM")
    print("Defensive Security Tool - Protect Your Credentials")
    print("🛡️" * 40)
    print()
    
    while True:
        print("=" * 80)
        print("MAIN MENU")
        print("=" * 80)
        print("1. Initialize security baselines")
        print("2. Run single security scan")
        print("3. Start continuous monitoring")
        print("4. View best practices")
        print("5. Setup system-level monitoring")
        print("6. Exit")
        print("=" * 80)
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            detector.initialize_baselines()
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            if not detector.file_hashes:
                print("\n⚠️  Please initialize baselines first (Option 1)")
            else:
                detector.run_single_scan()
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            if not detector.file_hashes:
                print("\n⚠️  Please initialize baselines first (Option 1)")
            else:
                interval = input("\nScan interval in seconds (default: 60): ").strip()
                interval = int(interval) if interval.isdigit() else 60
                detector.run_continuous_monitoring(interval)
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            educator.explain_best_practices()
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            detector.setup_system_monitoring()
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            print("\n👋 Exiting... Stay secure!")
            break
        
        else:
            print("\n❌ Invalid option. Please try again.")
        
        print("\n")


if __name__ == "__main__":
    main()
