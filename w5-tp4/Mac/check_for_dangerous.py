import subprocess

def check_dangerous_outdated_apps():
    """
    Identifies which outdated applications pose the highest security risk.
    Apps are ranked by severity based on the type of data they handle.
    """
    
    # Security risk categories (High to Low)
    HIGH_RISK_APPS = {
        'browsers': ['Google Chrome', 'Safari', 'Brave Browser', 'Firefox', 'Edge'],
        'dev_tools': ['Xcode', 'Android Studio', 'VSCode', 'Visual Studio'],
        'communication': ['Telegram', 'Discord', 'Messenger', 'Slack', 'WhatsApp', 'Zoom'],
        'cloud_storage': ['OneDrive', 'Dropbox', 'Google Drive', 'iCloud'],
        'office': ['Microsoft Word', 'Excel', 'PowerPoint', 'Outlook'],
    }
    
    MEDIUM_RISK_APPS = {
        'media': ['Spotify', 'iTunes', 'VLC'],
        'design': ['Canva', 'Photoshop', 'Illustrator'],
        'productivity': ['Pages', 'Numbers', 'Keynote', 'OneNote'],
    }
    
    LOW_RISK_APPS = {
        'utilities': ['CleanMyMac', 'PDF Expert'],
        'entertainment': ['iMovie', 'GarageBand', 'Roblox'],
    }
    
    try:
        # Get outdated apps from App Store
        result = subprocess.run(["mas", "outdated"], capture_output=True, text=True)
        outdated = result.stdout.strip()
        
        if not outdated:
            print("✅ All App Store apps are up to date!")
            return
        
        outdated_lines = outdated.split('\n')
        
        print("=" * 70)
        print("🔴 SECURITY RISK ANALYSIS - OUTDATED APPLICATIONS")
        print("=" * 70)
        print()
        
        high_risk_found = []
        medium_risk_found = []
        low_risk_found = []
        unknown_risk = []
        
        for line in outdated_lines:
            parts = line.split()
            if len(parts) < 2:
                continue
                
            app_name = ' '.join(parts[1:-2])  # Extract app name
            current_version = parts[-2]
            new_version = parts[-1].replace(')', '')
            
            # Categorize risk level
            risk_level = "UNKNOWN"
            found = False
            
            # Check HIGH RISK
            for category, apps in HIGH_RISK_APPS.items():
                if any(risk_app.lower() in app_name.lower() for risk_app in apps):
                    high_risk_found.append({
                        'name': app_name,
                        'category': category,
                        'current': current_version,
                        'new': new_version,
                        'line': line
                    })
                    found = True
                    break
            
            # Check MEDIUM RISK
            if not found:
                for category, apps in MEDIUM_RISK_APPS.items():
                    if any(risk_app.lower() in app_name.lower() for risk_app in apps):
                        medium_risk_found.append({
                            'name': app_name,
                            'category': category,
                            'current': current_version,
                            'new': new_version,
                            'line': line
                        })
                        found = True
                        break
            
            # Check LOW RISK
            if not found:
                for category, apps in LOW_RISK_APPS.items():
                    if any(risk_app.lower() in app_name.lower() for risk_app in apps):
                        low_risk_found.append({
                            'name': app_name,
                            'category': category,
                            'current': current_version,
                            'new': new_version,
                            'line': line
                        })
                        found = True
                        break
            
            if not found:
                unknown_risk.append({
                    'name': app_name,
                    'current': current_version,
                    'new': new_version,
                    'line': line
                })
        
        # Display HIGH RISK apps
        if high_risk_found:
            print("🔴 CRITICAL RISK - UPDATE IMMEDIATELY!")
            print("-" * 70)
            print("These apps handle sensitive data (passwords, financial info, personal")
            print("communications). Outdated versions may have known security vulnerabilities.")
            print()
            for app in high_risk_found:
                print(f"  ⚠️  {app['name']}")
                print(f"      Category: {app['category'].replace('_', ' ').title()}")
                print(f"      Version: {app['current']} → {app['new']}")
                print(f"      Risk: Potential data breach, credential theft, malware")
                print()
        
        # Display MEDIUM RISK apps
        if medium_risk_found:
            print("🟡 MODERATE RISK - UPDATE SOON")
            print("-" * 70)
            print("These apps may contain personal content or project files.")
            print()
            for app in medium_risk_found:
                print(f"  ⚠️  {app['name']}")
                print(f"      Category: {app['category'].replace('_', ' ').title()}")
                print(f"      Version: {app['current']} → {app['new']}")
                print()
        
        # Display LOW RISK apps
        if low_risk_found:
            print("🟢 LOW RISK - Update when convenient")
            print("-" * 70)
            for app in low_risk_found:
                print(f"  • {app['name']} ({app['current']} → {app['new']})")
            print()
        
        # Display UNKNOWN apps
        if unknown_risk:
            print("⚪ UNKNOWN RISK")
            print("-" * 70)
            for app in unknown_risk:
                print(f"  • {app['name']} ({app['current']} → {app['new']})")
            print()
        
        # Summary
        print("=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)
        print(f"  Critical Risk: {len(high_risk_found)} app(s)")
        print(f"  Moderate Risk: {len(medium_risk_found)} app(s)")
        print(f"  Low Risk: {len(low_risk_found)} app(s)")
        print(f"  Unknown Risk: {len(unknown_risk)} app(s)")
        print()
        
        if high_risk_found:
            print("🚨 RECOMMENDATION: Update critical apps IMMEDIATELY using:")
            print("   mas upgrade")
            print()
            print("   Or update individually in the App Store.")
        
    except FileNotFoundError:
        print("❌ 'mas' is not installed. Install it using: brew install mas")

if __name__ == "__main__":
    check_dangerous_outdated_apps()
