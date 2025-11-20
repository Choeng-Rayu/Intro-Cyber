import subprocess
import os

def count_installed_packages():
    """Count all installed packages using dpkg"""
    try:
        # Run dpkg -l command and count lines
        result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            # Subtract 5 to account for header lines in dpkg -l output
            line_count = len(result.stdout.strip().split('\n'))
            total_packages = line_count - 5  # dpkg -l has 5 header lines
            return max(0, total_packages)  # Ensure non-negative
        else:
            print("Error running dpkg command")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def list_installed_packages():
    """List all installed packages"""
    try:
        result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            # Skip the first 5 header lines
            packages = []
            for line in lines[5:]:
                if line.startswith('ii'):
                    # Extract package name and version
                    parts = line.split()
                    if len(parts) >= 2:
                        package_name = parts[1]
                        package_version = parts[2] if len(parts) > 2 else "N/A"
                        packages.append((package_name, package_version))
            return packages
        else:
            print("Error running dpkg command")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def count_manual_packages():
    """Count manually installed packages"""
    try:
        result = subprocess.run(['apt-mark', 'showmanual'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            manual_packages = len(result.stdout.strip().split('\n'))
            return manual_packages
        else:
            print("Error running apt-mark command")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def list_manual_packages():
    """List manually installed packages"""
    try:
        result = subprocess.run(['apt-mark', 'showmanual'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            packages = result.stdout.strip().split('\n')
            return [pkg for pkg in packages if pkg]  # Remove empty strings
        else:
            print("Error running apt-mark command")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_outdated_packages():
    """Check which packages have updates available"""
    try:
        result = subprocess.run(['apt', 'list', '--upgradable'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            outdated = {}
            # Skip header line if present
            for line in lines[1:] if lines else []:
                if line.strip():
                    parts = line.split('/')
                    if len(parts) >= 1:
                        package_name = parts[0].strip()
                        outdated[package_name] = True
            return outdated
        else:
            return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def is_gui_application(package_name):
    """
    Determine if a package is a GUI application.
    Returns True if it's a known GUI application.
    """
    gui_applications = {
        # Desktop Environments
        'gnome-shell', 'kde-plasma-desktop', 'xfce4', 'lxde', 'mate-desktop',
        'cinnamon', 'budgie-desktop', 'deepin-desktop-environment',
        
        # Web Browsers
        'firefox', 'chromium', 'chromium-browser', 'google-chrome', 'opera',
        'vivaldi', 'brave-browser', 'edge',
        
        # Office & Productivity
        'libreoffice', 'libreoffice-calc', 'libreoffice-writer', 'libreoffice-impress',
        'openoffice', 'onlyoffice-desktopeditors', 'wps-office',
        
        # Graphics & Design
        'gimp', 'inkscape', 'blender', 'krita', 'darktable', 'rawtherapee',
        'photoshop', 'corel', 'affinity-photo', 'affinity-designer',
        
        # Development Tools with GUI
        'vscode', 'visual-studio-code', 'code', 'sublime-text', 'atom',
        'pycharm', 'pycharm-community', 'intellij-idea-community', 'intellij-idea',
        'webstorm', 'clion', 'goland', 'phpstorm',
        'qtcreator', 'codeblocks', 'geany', 'gedit', 'pluma',
        
        # Media Players
        'vlc', 'mpv', 'kodi', 'smplayer', 'celluloid', 'gnome-music',
        'audacious', 'clementine', 'rhythmbox',
        
        # Media Creation & Editing
        'kdenlive', 'shotcut', 'openshot', 'davinci-resolve', 'audacity',
        'obs-studio', 'streamlabs-obs', 'handbrake', 'ffmpeg-gui',
        
        # Communication & Social
        'telegram-desktop', 'discord', 'slack', 'zoom', 'skype',
        'thunderbird', 'evolution', 'betterbird',
        
        # File Managers
        'nautilus', 'nemo', 'thunar', 'dolphin', 'pcmanfm', 'caja',
        'ranger-gui', 'spacefm', 'ultracopier',
        
        # System Tools with GUI
        'gparted', 'gnome-disks', 'kde-partition-manager', 'baobab',
        'gnome-system-monitor', 'ksysguard', 'htop-gui', 'gtop',
        'gnome-control-center', 'system-settings',
        
        # Viewers & Document Tools
        'evince', 'okular', 'atril', 'mupdf', 'zathura',
        'ristretto', 'eog', 'gthumb', 'feh',
        
        # Gaming
        'steam', 'lutris', 'playonlinux', 'wine', 'proton', 'dosbox',
        
        # Virtualization
        'virtualbox', 'virt-manager', 'vmware-workstation', 'hyper-v',
        'qemu', 'kvm', 'bochs',
        
        # Database Tools
        'dbeaver', 'pgadmin', 'mysql-workbench', 'nosqlbooster',
        'sqlite-browser', 'adminer', 'robomongo',
        
        # Terminal & Shell (GUI-based)
        'gnome-terminal', 'konsole', 'xfce4-terminal', 'terminator',
        'tilix', 'alacritty', 'kitty-gui', 'wezterm-gui',
        
        # Settings & Configuration
        'dconf-editor', 'kdeconnect', 'indicator', 'gsettings-list',
        
        # Others GUI apps
        'guake', 'uget', 'transmission', 'qbittorrent', 'deluge',
        'calibre', 'mcomix', 'evince', 'xpdf', 'gpicview',
    }
    
    # Check if package name matches any GUI application
    package_lower = package_name.lower()
    for gui_app in gui_applications:
        if gui_app in package_lower or package_lower in gui_app:
            return True
    
    return False

def filter_gui_packages(manual_list):
    """Filter and return only GUI applications from manual package list"""
    if not manual_list:
        return []
    
    gui_packages = []
    for package in manual_list:
        if is_gui_application(package):
            gui_packages.append(package)
    
    return gui_packages

def get_package_status():
    """Get status of all manual packages (up-to-date or outdated)"""
    try:
        manual_list = list_manual_packages()
        outdated_dict = check_outdated_packages()
        
        if not manual_list:
            return None
        
        status_dict = {
            'up_to_date': [],
            'outdated': []
        }
        
        for package in manual_list:
            if package in outdated_dict:
                status_dict['outdated'].append(package)
            else:
                status_dict['up_to_date'].append(package)
        
        return status_dict
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_security_risk_level(package_name):
    """
    Assess security risk level of a package based on known critical applications.
    Returns risk level and description.
    """
    # Critical packages that handle sensitive data
    critical_packages = {
        # Web Servers & Network
        'apache2': {'risk': 'CRITICAL', 'reason': 'Web server - exposes services to internet attacks'},
        'nginx': {'risk': 'CRITICAL', 'reason': 'Web server - exposes services to internet attacks'},
        'openssh-server': {'risk': 'CRITICAL', 'reason': 'Remote access - direct target for brute force attacks'},
        'openssl': {'risk': 'CRITICAL', 'reason': 'Encryption library - affects all SSL/TLS connections'},
        'curl': {'risk': 'HIGH', 'reason': 'Data transfer tool - can download malicious content'},
        'wget': {'risk': 'HIGH', 'reason': 'Data transfer tool - can download malicious content'},
        
        # Databases
        'mysql-server': {'risk': 'CRITICAL', 'reason': 'Database - stores sensitive user data'},
        'postgresql': {'risk': 'CRITICAL', 'reason': 'Database - stores sensitive user data'},
        'mongodb': {'risk': 'CRITICAL', 'reason': 'Database - stores sensitive user data'},
        'redis-server': {'risk': 'HIGH', 'reason': 'Cache/Database - can store sensitive data'},
        
        # Development & Scripting
        'python3': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code'},
        'nodejs': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code'},
        'php': {'risk': 'CRITICAL', 'reason': 'Web scripting - vulnerable to code injection'},
        'ruby': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code'},
        'perl': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code'},
        'java': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code'},
        
        # System & Authentication
        'sudo': {'risk': 'CRITICAL', 'reason': 'Privilege escalation - critical for system security'},
        'shadow': {'risk': 'CRITICAL', 'reason': 'Password storage - protects user credentials'},
        'pam': {'risk': 'CRITICAL', 'reason': 'Authentication module - controls system access'},
        'openssh-client': {'risk': 'HIGH', 'reason': 'SSH client - used for remote connections'},
        
        # Utilities that handle sensitive data
        'gpg': {'risk': 'HIGH', 'reason': 'Encryption tool - protects sensitive communications'},
        'git': {'risk': 'MEDIUM', 'reason': 'Version control - may access private repositories'},
        'docker.io': {'risk': 'CRITICAL', 'reason': 'Container runtime - runs untrusted applications'},
        'vim': {'risk': 'LOW', 'reason': 'Text editor - generally safe'},
        'nano': {'risk': 'LOW', 'reason': 'Text editor - generally safe'},
    }
    
    # Check if package is in critical list
    if package_name in critical_packages:
        return critical_packages[package_name]
    
    # Check for partial matches
    for critical_pkg, risk_info in critical_packages.items():
        if critical_pkg in package_name or package_name in critical_pkg:
            return risk_info
    
    # Default risk level
    return {'risk': 'MEDIUM', 'reason': 'Unknown package - assign medium risk by default'}

def assess_outdated_security_risks(outdated_list):
    """
    Assess and rank outdated packages by security risk.
    Returns sorted list with risk levels.
    """
    risk_ranking = {
        'CRITICAL': 4,
        'HIGH': 3,
        'MEDIUM': 2,
        'LOW': 1
    }
    
    assessed_packages = []
    for package in outdated_list:
        risk_info = get_security_risk_level(package)
        assessed_packages.append({
            'package': package,
            'risk': risk_info['risk'],
            'reason': risk_info['reason'],
            'rank': risk_ranking.get(risk_info['risk'], 0)
        })
    
    # Sort by risk rank (highest first)
    assessed_packages.sort(key=lambda x: x['rank'], reverse=True)
    return assessed_packages

def get_attack_vectors(package_name):
    """
    Explain how attackers exploit specific outdated applications.
    Returns common attack vectors and exploitation methods.
    """
    attack_vectors_db = {
        # Web Servers
        'apache2': {
            'vulnerabilities': [
                'CVE-2023-25690: HTTP request smuggling attack',
                'CVE-2022-36760: Denial of Service via crafted requests',
                'CVE-2021-44790: Buffer overflow in mod_lua'
            ],
            'attack_methods': [
                '🔓 RCE (Remote Code Execution) - Execute arbitrary code on server',
                '🌐 Web Shell Injection - Upload malicious files to gain persistent access',
                '💥 HTTP Request Smuggling - Bypass security controls to access data',
                '⚠️ Path Traversal - Access files outside intended directories',
                '📊 Information Disclosure - Extract sensitive server information'
            ]
        },
        'nginx': {
            'vulnerabilities': [
                'CVE-2023-44487: HTTP/2 Rapid Reset (DoS)',
                'CVE-2022-41741: Memory disclosure vulnerability',
                'CVE-2021-3618: Off-by-one buffer overflow'
            ],
            'attack_methods': [
                '🔓 RCE (Remote Code Execution) - Execute arbitrary code',
                '💥 Denial of Service - Crash server with malformed requests',
                '🔐 Cache Poisoning - Inject malicious content into cache',
                '📊 Information Disclosure - Leak sensitive headers'
            ]
        },
        
        # SSH
        'openssh-server': {
            'vulnerabilities': [
                'CVE-2023-38408: Potential Denial of Service',
                'CVE-2022-2881: Authorization bypass in specific configs',
                'CVE-2021-41617: Privilege escalation via sudo'
            ],
            'attack_methods': [
                '🔓 Brute Force Attack - Guess weak passwords to gain shell access',
                '🔑 SSH Key Theft - Steal private keys to impersonate users',
                '👤 Privilege Escalation - Exploit to become root user',
                '💻 Reverse Shell - Create backdoor for persistent access',
                '🕵️ Man-in-the-Middle - Intercept unencrypted traffic'
            ]
        },
        
        # Databases
        'mysql-server': {
            'vulnerabilities': [
                'CVE-2023-21911: SQL injection in authentication',
                'CVE-2022-21903: Authentication bypass',
                'CVE-2021-2109: Privilege escalation'
            ],
            'attack_methods': [
                '💾 SQL Injection - Extract/modify sensitive database data',
                '🔓 Authentication Bypass - Login without credentials',
                '📊 Data Exfiltration - Steal user data and credentials',
                '🗑️ Database Deletion - Malicious data destruction',
                '🚀 UDF Injection - Execute system commands via stored procedures'
            ]
        },
        'postgresql': {
            'vulnerabilities': [
                'CVE-2023-39417: SQL injection vulnerability',
                'CVE-2022-41862: Privilege escalation',
                'CVE-2021-3393: Buffer overflow'
            ],
            'attack_methods': [
                '💾 SQL Injection - Extract/modify sensitive data',
                '🔓 Authentication Bypass - Unauthorized access',
                '📊 Data Theft - Exfiltrate databases',
                '👤 Privilege Escalation - Become superuser',
                '🖥️ Command Execution - Execute OS commands'
            ]
        },
        
        # Web Scripting
        'php': {
            'vulnerabilities': [
                'CVE-2023-38545: Buffer overflow in HTTP client',
                'CVE-2022-31625: Security restriction bypass',
                'CVE-2021-21703: Local privilege escalation'
            ],
            'attack_methods': [
                '🔓 Remote Code Execution - Execute PHP code via $_GET/$_POST',
                '⬆️ File Upload Exploit - Upload malicious PHP shells',
                '🌐 Local File Inclusion - Read arbitrary files from server',
                '🔐 Session Hijacking - Steal user session tokens',
                '💉 Code Injection - Inject malicious code into web pages'
            ]
        },
        
        # SSL/TLS & Encryption
        'openssl': {
            'vulnerabilities': [
                'CVE-2023-46807: Potential DoS vulnerability',
                'CVE-2022-3786: Buffer overflow in X.509 verification',
                'CVE-2021-4160: Overflow in X.509 certificate verification'
            ],
            'attack_methods': [
                '🔓 SSL Stripping - Downgrade HTTPS to HTTP',
                '🔐 Man-in-the-Middle Attack - Intercept encrypted traffic',
                '🎭 Certificate Spoofing - Impersonate legitimate websites',
                '💥 Denial of Service - Crash services with malformed certs',
                '🔑 Key Recovery - Potentially extract encryption keys'
            ]
        },
        
        # SSH Client
        'openssh-client': {
            'vulnerabilities': [
                'CVE-2023-38408: Similar to server vulnerabilities',
                'CVE-2022-2881: Authorization issues',
                'CVE-2021-41617: Privilege escalation'
            ],
            'attack_methods': [
                '🎣 SSH Hijacking - Intercept SSH connections',
                '🔑 Credential Theft - Steal SSH keys from user machine',
                '🕵️ Man-in-the-Middle - Monitor SSH traffic',
                '👤 Privilege Escalation - Exploit to gain higher privileges'
            ]
        },
        
        # Docker
        'docker.io': {
            'vulnerabilities': [
                'CVE-2023-28840: Container escape vulnerability',
                'CVE-2022-36109: Privilege escalation',
                'CVE-2021-21284: Container image validation bypass'
            ],
            'attack_methods': [
                '🚀 Container Escape - Break out to host system',
                '👤 Privilege Escalation - Become root on host',
                '💾 Data Breach - Access host filesystem from container',
                '🔓 Host Compromise - Install rootkit/backdoor on host',
                '🌐 Lateral Movement - Attack other containers/services'
            ]
        }
    }
    
    # Check if package has known attack vectors
    for pkg, vectors in attack_vectors_db.items():
        if pkg in package_name or package_name in pkg:
            return vectors
    
    # Default attack vectors for unknown packages
    return {
        'vulnerabilities': [
            'Unknown CVE - Check security databases',
            'Potential zero-day exploits',
            'Community-reported vulnerabilities'
        ],
        'attack_methods': [
            '🔓 Potential code execution',
            '💥 Possible denial of service',
            '📊 Potential data leakage',
            '🔐 Security bypass risks',
            '👤 Unauthorized access vectors'
        ]
    }

def explain_exploitation(package_name, attack_vectors):
    """
    Provide detailed explanation of how attackers exploit the vulnerability
    """
    exploitation_guide = {
        'steps': [],
        'impact': [],
        'prevention': []
    }
    
    # Generic exploitation flow
    exploitation_guide['steps'] = [
        '1. Reconnaissance - Attacker scans to identify outdated software version',
        '2. Vulnerability Research - Look up known CVEs for that version',
        '3. Exploit Development/Download - Obtain or write exploit code',
        '4. Attack Delivery - Execute exploit via network/upload/injection',
        '5. Payload Execution - Malicious code runs on the system',
        '6. Persistence - Install backdoor/rootkit for future access',
        '7. Data Exfiltration - Steal data or pivot to other systems'
    ]
    
    exploitation_guide['impact'] = [
        '🚨 System Compromise - Complete control over the application',
        '💾 Data Breach - Access to all data processed by the application',
        '🔐 Credential Theft - User passwords and authentication tokens',
        '🌐 Network Compromise - Lateral movement to other systems',
        '💰 Financial Loss - Ransomware, theft, extortion',
        '📊 Reputation Damage - Loss of customer trust',
        '⚖️ Legal Consequences - GDPR/compliance violations'
    ]
    
    exploitation_guide['prevention'] = [
        '✅ Immediate: Update to latest patched version',
        '✅ Network: Isolate vulnerable service from internet',
        '✅ Monitoring: Enable security logging and alerts',
        '✅ Access Control: Restrict who can access the service',
        '✅ Firewall: Block suspicious traffic patterns',
        '✅ Regular: Schedule patching for all software quarterly',
        '✅ Scan: Regular vulnerability scanning and penetration testing'
    ]
    
    return exploitation_guide

# Run the functions
if __name__ == "__main__":
    print("=" * 70)
    print("THIRD-PARTY GUI APPLICATIONS - SECURITY RISK ANALYSIS")
    print("=" * 70)
    
    # Get package status
    status = get_package_status()
    
    if status:
        # Filter only GUI applications
        all_manual = list_manual_packages()
        gui_packages = filter_gui_packages(all_manual)
        
        # Separate GUI packages into up-to-date and outdated
        outdated_dict = check_outdated_packages()
        
        gui_up_to_date = [pkg for pkg in gui_packages if pkg not in outdated_dict]
        gui_outdated = [pkg for pkg in gui_packages if pkg in outdated_dict]
        
        total_gui = len(gui_packages)
        up_to_date_count = len(gui_up_to_date)
        outdated_count = len(gui_outdated)
        
        print(f"\n�️  Total third-party GUI applications: {total_gui}")
        print(f"✅ GUI apps up-to-date: {up_to_date_count}")
        print(f"⚠️  GUI apps outdated (need updates): {outdated_count}\n")
        
        # Display outdated GUI packages with security risk analysis
        if gui_outdated:
            print("-" * 70)
            print("🔴 OUTDATED GUI APPLICATIONS - SECURITY RISK ASSESSMENT:")
            print("-" * 70)
            
            # Get risk assessment
            risk_assessment = assess_outdated_security_risks(gui_outdated)
            
            # Color codes for risk levels
            risk_symbols = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }
            
            for i, pkg_risk in enumerate(risk_assessment, 1):
                symbol = risk_symbols.get(pkg_risk['risk'], '❓')
                print(f"\n{i}. {symbol} {pkg_risk['package']}")
                print(f"   Risk Level: {pkg_risk['risk']}")
                print(f"   Reason: {pkg_risk['reason']}")
            
            # Identify most dangerous GUI app
            if risk_assessment:
                most_dangerous = risk_assessment[0]
                print("\n" + "-" * 70)
                print("🚨 MOST DANGEROUS GUI APPLICATION:")
                print("-" * 70)
                print(f"Package: {most_dangerous['package']}")
                print(f"Risk Level: {most_dangerous['risk']}")
                print(f"Reason: {most_dangerous['reason']}")
                
                # Get attack vectors for most dangerous app
                attack_vectors = get_attack_vectors(most_dangerous['package'])
                print(f"\n📋 KNOWN VULNERABILITIES (CVEs):")
                for vuln in attack_vectors['vulnerabilities']:
                    print(f"   • {vuln}")
                
                print(f"\n⚔️  ATTACK METHODS (How attackers exploit this):")
                for method in attack_vectors['attack_methods']:
                    print(f"   {method}")
                
                # Show exploitation details
                exploitation = explain_exploitation(most_dangerous['package'], attack_vectors)
                
                print(f"\n🔴 EXPLOITATION STEPS (Attack Flow):")
                for step in exploitation['steps']:
                    print(f"   {step}")
                
                print(f"\n💣 POTENTIAL IMPACT:")
                for impact in exploitation['impact']:
                    print(f"   {impact}")
                
                print(f"\n🛡️  PREVENTION & MITIGATION:")
                for prevention in exploitation['prevention']:
                    print(f"   {prevention}")
                
                print(f"\n⚡ IMMEDIATE ACTION: Update '{most_dangerous['package']}' immediately!")
                print("-" * 70)
        else:
            print("\n" + "-" * 70)
            print("🎉 All GUI applications are up-to-date!")
            print("-" * 70)
        
        # Display up-to-date GUI packages
        if gui_up_to_date:
            print("\n" + "-" * 70)
            print("✅ UP-TO-DATE GUI APPLICATIONS:")
            print("-" * 70)
            for i, package in enumerate(gui_up_to_date, 1):
                print(f"{i}. {package}")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)
        print(f"Total manual packages: {len(all_manual)}")
        print(f"GUI applications found: {total_gui}")
        print(f"GUI apps with updates available: {outdated_count}")
        print(f"GUI apps that are current: {up_to_date_count}")
        print("=" * 70)
    else:
        print("No third-party applications found or error occurred.")
