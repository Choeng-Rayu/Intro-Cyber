#!/usr/bin/env python3
"""
SENSITIVE DATA COLLECTOR (Educational - Defensive Security)

This tool demonstrates:
1. What sensitive data browsers store and WHERE
2. How to inventory browser data for security auditing
3. Understanding what attackers target

EDUCATIONAL PURPOSE ONLY - Learn what data exists to protect it better
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime


class SensitiveDataCollector:
    """Collect information about sensitive browser data locations"""
    
    def __init__(self):
        self.home = Path.home()
        self.browsers = {
            'chrome': self.home / '.config/google-chrome/Default',
            'chromium': self.home / '.config/chromium/Default',
            'firefox': self.home / '.mozilla/firefox',
            'brave': self.home / '.config/BraveSoftware/Brave-Browser/Default',
        }
        self.collected_data = []
        
        # Create data directory
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_browser_data_locations(self):
        """Collect information about sensitive browser files"""
        print("Collecting sensitive data locations...\n")
        
        sensitive_files = {
            'Login Data': 'Encrypted passwords database',
            'Cookies': 'Session tokens and authentication cookies',
            'History': 'Browsing history database',
            'Bookmarks': 'User bookmarks',
            'Web Data': 'Autofill data (addresses, credit cards)',
            'Preferences': 'Browser settings and configurations',
        }
        
        for browser_name, profile_path in self.browsers.items():
            if profile_path.exists():
                print(f"📁 {browser_name.upper()}: {profile_path}")
                
                for filename, description in sensitive_files.items():
                    file_path = profile_path / filename
                    
                    if file_path.exists():
                        file_info = {
                            'browser': browser_name,
                            'filename': filename,
                            'full_path': str(file_path),
                            'description': description,
                            'size_bytes': file_path.stat().st_size,
                            'permissions': oct(file_path.stat().st_mode)[-3:],
                            'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                            'exists': True
                        }
                        
                        # Try to get additional metadata for databases
                        if filename in ['Login Data', 'History', 'Cookies', 'Web Data']:
                            db_info = self._get_database_info(file_path, filename)
                            if db_info:
                                file_info['database_info'] = db_info
                        
                        self.collected_data.append(file_info)
                        print(f"  ✓ {filename}: {file_info['size_bytes']:,} bytes")
                
                print()
    
    def _get_database_info(self, db_path, db_type):
        """Get metadata from SQLite databases (read-only, no data extraction)"""
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            info = {
                'type': 'sqlite3',
                'tables': []
            }
            
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                
                info['tables'].append({
                    'name': table_name,
                    'row_count': count
                })
            
            conn.close()
            return info
            
        except sqlite3.Error:
            return {'type': 'sqlite3', 'status': 'locked_or_inaccessible'}
    
    def generate_summary(self):
        """Generate summary statistics"""
        summary = {
            'total_files_found': len(self.collected_data),
            'total_size_bytes': sum(item['size_bytes'] for item in self.collected_data),
            'browsers_with_data': list(set(item['browser'] for item in self.collected_data)),
            'file_types': {}
        }
        
        # Count by file type
        for item in self.collected_data:
            filename = item['filename']
            if filename not in summary['file_types']:
                summary['file_types'][filename] = 0
            summary['file_types'][filename] += 1
        
        return summary
    
    def save_collected_data(self):
        """Save collected data to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sensitive_data_collection_{timestamp}.json"
        filepath = self.data_dir / filename
        
        summary = self.generate_summary()
        
        output_data = {
            'collection_timestamp': datetime.now().isoformat(),
            'collection_type': 'browser_sensitive_data',
            'system_info': {
                'home_directory': str(self.home),
                'collection_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            'summary': summary,
            'sensitive_data_locations': self.collected_data,
            'security_notes': [
                'This data shows what attackers target in browser attacks',
                'Passwords in Login Data are encrypted but can be decrypted by malware running as your user',
                'Cookies contain session tokens that can hijack logged-in accounts',
                'History reveals browsing patterns and visited sites',
                'Web Data contains autofill information including addresses and payment methods'
            ],
            'defense_recommendations': [
                'Keep browsers updated to prevent code execution exploits',
                'Use dedicated password manager instead of browser storage',
                'Enable 2FA on all accounts to mitigate credential theft',
                'Use private browsing mode for sensitive activities',
                'Clear cookies and cache regularly',
                'Monitor file access to these locations for suspicious activity'
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        return filepath, summary
    
    def print_summary(self, summary):
        """Print collection summary"""
        print("=" * 70)
        print("SENSITIVE DATA COLLECTION SUMMARY")
        print("=" * 70)
        print(f"Total files found: {summary['total_files_found']}")
        print(f"Total size: {summary['total_size_bytes']:,} bytes ({summary['total_size_bytes'] / 1024 / 1024:.2f} MB)")
        print(f"Browsers with data: {', '.join(summary['browsers_with_data'])}")
        print(f"\nFile types found:")
        for file_type, count in summary['file_types'].items():
            print(f"  - {file_type}: {count}")
        print("=" * 70)
    
    def run_collection(self):
        """Run the data collection process"""
        print("=" * 70)
        print("BROWSER SENSITIVE DATA COLLECTOR")
        print("Understanding What Data Exists to Protect It Better")
        print("=" * 70)
        print()
        
        self.collect_browser_data_locations()
        
        saved_file, summary = self.save_collected_data()
        
        self.print_summary(summary)
        print(f"\n💾 Data saved to: {saved_file}")
        print("\n⚠️  REMEMBER: This data shows what attackers target.")
        print("   Protect these files by keeping browsers updated and using 2FA!\n")


if __name__ == "__main__":
    collector = SensitiveDataCollector()
    collector.run_collection()
