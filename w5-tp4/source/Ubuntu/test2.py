import subprocess
import platform
from datetime import datetime, timezone

# NOTE: This module is intentionally tailored to Ubuntu-based systems.
# It is scheduled to run in the background, so every command invocation
# must fail gracefully instead of prompting for user input.


def ensure_ubuntu_environment():
    """Stop execution early if we are not on Ubuntu/Linux."""
    if platform.system() != 'Linux':
        raise RuntimeError('This script only supports Ubuntu/Linux environments.')
    try:
        with open('/etc/os-release', 'r', encoding='utf-8') as release_file:
            data = release_file.read().lower()
            if 'ubuntu' not in data:
                raise RuntimeError('Non-Ubuntu distribution detected; aborting as requested.')
    except FileNotFoundError:
        raise RuntimeError('Unable to verify /etc/os-release; stopping to avoid incorrect results.')


def run_command(command):
    """Run shell command safely and return CompletedProcess or None on failure."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return result
    except FileNotFoundError:
        return None

def count_installed_packages():
    """Return counts for dpkg, snap, and flatpak applications."""
    dpkg_total = _count_dpkg_packages()
    snap_total = _count_snap_packages()
    flatpak_total = _count_flatpak_packages()
    totals = {
        'dpkg_packages': dpkg_total,
        'snap_apps': snap_total,
        'flatpak_apps': flatpak_total,
    }
    totals['overall'] = sum(value for value in totals.values())
    return totals


def _count_dpkg_packages():
    result = run_command(['dpkg', '-l'])
    if not result or result.returncode != 0:
        return 0
    line_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return max(0, line_count - 5)  # Skip header lines


def _count_snap_packages():
    result = run_command(['snap', 'list'])
    if not result or result.returncode != 0:
        return 0
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return max(0, len(lines) - 1)  # Snap list has one header line


def _count_flatpak_packages():
    result = run_command(['flatpak', 'list', '--app'])
    if not result or result.returncode != 0:
        return 0
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return len(lines)

def list_installed_packages():
    """List all installed packages"""
    result = run_command(['dpkg', '-l'])
    if not result or result.returncode != 0:
        return []
    lines = result.stdout.strip().split('\n')
    packages = []
    for line in lines[5:]:  # Skip dpkg header lines
        if line.startswith('ii'):
            parts = line.split()
            if len(parts) >= 2:
                package_name = parts[1]
                package_version = parts[2] if len(parts) > 2 else 'N/A'
                packages.append((package_name, package_version))
    return packages

def count_manual_packages():
    """Count manually installed packages"""
    result = run_command(['apt-mark', 'showmanual'])
    if not result or result.returncode != 0:
        return 0
    return len([pkg for pkg in result.stdout.strip().split('\n') if pkg])

def list_manual_packages():
    """List manually installed packages"""
    result = run_command(['apt-mark', 'showmanual'])
    if not result or result.returncode != 0:
        return []
    packages = result.stdout.strip().split('\n')
    return [pkg for pkg in packages if pkg]

def get_apt_outdated_packages():
    """Return metadata about apt packages that have updates available."""
    result = run_command(['apt', 'list', '--upgradable'])
    if not result or result.returncode != 0:
        return []

    outdated_entries = []
    for line in (line.strip() for line in result.stdout.splitlines() if line.strip()):
        if line.lower().startswith('listing...'):
            continue
        segments = line.split()
        if not segments:
            continue
        name = segments[0].split('/')[0]
        available_version = segments[1] if len(segments) > 1 else 'unknown'
        current_version = 'unknown'
        if '[upgradable from:' in line:
            current_version = line.split('[upgradable from:')[1].split(']')[0].strip()
        outdated_entries.append({
            'name': name,
            'source': 'apt',
            'available_version': available_version,
            'current_version': current_version,
            'raw': line
        })
    return outdated_entries


def get_snap_outdated_packages():
    """Return list of snaps that require refresh."""
    result = run_command(['snap', 'refresh', '--list'])
    if not result or result.returncode != 0:
        return []

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if len(lines) <= 1:
        return []

    outdated_entries = []
    for line in lines[1:]:  # Skip header row
        parts = line.split()
        if len(parts) < 2:
            continue
        name = parts[0]
        available_version = parts[1]
        outdated_entries.append({
            'name': name,
            'source': 'snap',
            'available_version': available_version,
            'current_version': 'unknown',
            'raw': line
        })
    return outdated_entries


def get_flatpak_outdated_packages():
    """Return list of Flatpak apps with pending updates."""
    result = run_command(
        ['flatpak', 'remote-ls', '--updates', '--columns=application,branch,version']
    )
    if not result or result.returncode != 0:
        return []

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    outdated_entries = []
    for line in lines:
        parts = [part.strip() for part in line.split('\t') if part.strip()]
        if not parts:
            parts = line.split()
        if not parts:
            continue
        name = parts[0]
        branch = parts[1] if len(parts) > 1 else 'unknown'
        version = parts[2] if len(parts) > 2 else 'unknown'
        outdated_entries.append({
            'name': name,
            'source': 'flatpak',
            'available_version': f'{version} ({branch})',
            'current_version': 'unknown',
            'raw': line
        })
    return outdated_entries


def get_all_outdated_packages():
    """Combine outdated applications from apt, snap, and flatpak."""
    outdated = []
    outdated.extend(get_apt_outdated_packages())
    outdated.extend(get_snap_outdated_packages())
    outdated.extend(get_flatpak_outdated_packages())
    return outdated

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

def get_package_status(manual_list, apt_outdated_lookup):
    """Divide manual packages into up-to-date vs outdated (apt only)."""
    if not manual_list:
        return None

    status_dict = {
        'up_to_date': [],
        'outdated': []
    }

    for package in manual_list:
        if package in apt_outdated_lookup:
            status_dict['outdated'].append(package)
        else:
            status_dict['up_to_date'].append(package)

    return status_dict

def get_security_risk_level(package_name):
    """
    Assess security risk level of a package based on known critical applications.
    Returns risk level and description.
    """
    # Critical packages that handle sensitive data
    critical_packages = {
        # Web Servers & Network
        'apache2': {'risk': 'CRITICAL', 'reason': 'Web server - exposes services to internet attacks', 'data_breach_score': 4},
        'nginx': {'risk': 'CRITICAL', 'reason': 'Web server - exposes services to internet attacks', 'data_breach_score': 4},
        'openssh-server': {'risk': 'CRITICAL', 'reason': 'Remote access - direct target for brute force attacks', 'data_breach_score': 4},
        'openssl': {'risk': 'CRITICAL', 'reason': 'Encryption library - affects all SSL/TLS connections', 'data_breach_score': 4},
        'curl': {'risk': 'HIGH', 'reason': 'Data transfer tool - can download malicious content', 'data_breach_score': 3},
        'wget': {'risk': 'HIGH', 'reason': 'Data transfer tool - can download malicious content', 'data_breach_score': 3},
        
        # Databases
        'mysql-server': {'risk': 'CRITICAL', 'reason': 'Database - stores sensitive user data', 'data_breach_score': 4},
        'postgresql': {'risk': 'CRITICAL', 'reason': 'Database - stores sensitive user data', 'data_breach_score': 4},
        'mongodb': {'risk': 'CRITICAL', 'reason': 'Database - stores sensitive user data', 'data_breach_score': 4},
        'redis-server': {'risk': 'HIGH', 'reason': 'Cache/Database - can store sensitive data', 'data_breach_score': 3},
        
        # Development & Scripting
        'python3': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code', 'data_breach_score': 3},
        'nodejs': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code', 'data_breach_score': 3},
        'php': {'risk': 'CRITICAL', 'reason': 'Web scripting - vulnerable to code injection', 'data_breach_score': 4},
        'ruby': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code', 'data_breach_score': 3},
        'perl': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code', 'data_breach_score': 3},
        'java': {'risk': 'HIGH', 'reason': 'Runtime environment - executes untrusted code', 'data_breach_score': 3},
        
        # System & Authentication
        'sudo': {'risk': 'CRITICAL', 'reason': 'Privilege escalation - critical for system security', 'data_breach_score': 4},
        'shadow': {'risk': 'CRITICAL', 'reason': 'Password storage - protects user credentials', 'data_breach_score': 4},
        'pam': {'risk': 'CRITICAL', 'reason': 'Authentication module - controls system access', 'data_breach_score': 4},
        'openssh-client': {'risk': 'HIGH', 'reason': 'SSH client - used for remote connections', 'data_breach_score': 3},
        
        # Utilities that handle sensitive data
        'gpg': {'risk': 'HIGH', 'reason': 'Encryption tool - protects sensitive communications', 'data_breach_score': 3},
        'git': {'risk': 'MEDIUM', 'reason': 'Version control - may access private repositories', 'data_breach_score': 2},
        'docker.io': {'risk': 'CRITICAL', 'reason': 'Container runtime - runs untrusted applications', 'data_breach_score': 4},
        'vim': {'risk': 'LOW', 'reason': 'Text editor - generally safe', 'data_breach_score': 1},
        'nano': {'risk': 'LOW', 'reason': 'Text editor - generally safe', 'data_breach_score': 1},
    }
    
    # Check if package is in critical list
    if package_name in critical_packages:
        return critical_packages[package_name]
    
    # Check for partial matches
    for critical_pkg, risk_info in critical_packages.items():
        if critical_pkg in package_name or package_name in critical_pkg:
            return risk_info
    
    # Default risk level
    return {
        'risk': 'MEDIUM',
        'reason': 'Unknown package - assign medium risk by default',
        'data_breach_score': 2
    }

def assess_outdated_security_risks(outdated_list):
    """Assess and rank outdated packages by their data-breach impact."""
    risk_ranking = {
        'CRITICAL': 4,
        'HIGH': 3,
        'MEDIUM': 2,
        'LOW': 1
    }

    assessed_packages = []
    for entry in outdated_list:
        package_name = entry['name'] if isinstance(entry, dict) else entry
        risk_info = get_security_risk_level(package_name)
        assessed_packages.append({
            'package': package_name,
            'source': entry.get('source') if isinstance(entry, dict) else 'apt',
            'risk': risk_info['risk'],
            'reason': risk_info['reason'],
            'rank': risk_ranking.get(risk_info['risk'], 0),
            'data_breach_score': risk_info.get('data_breach_score', 2),
            'metadata': entry if isinstance(entry, dict) else {}
        })

    assessed_packages.sort(
        key=lambda item: (item['data_breach_score'], item['rank']),
        reverse=True
    )
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

def _print_header():
    print("=" * 70)
    print("UBUNTU APPLICATION SECURITY OVERVIEW (BACKGROUND REPORT)")
    print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)


def _format_list(items, max_items=10):
    """Return a short printable list (caps at max_items)."""
    if not items:
        return "(none)"
    trimmed = items[:max_items]
    suffix = '' if len(items) <= max_items else f" … (+{len(items) - max_items} more)"
    return ', '.join(trimmed) + suffix


def main():
    ensure_ubuntu_environment()
    _print_header()

    installed_totals = count_installed_packages()
    manual_packages = list_manual_packages()
    gui_packages = filter_gui_packages(manual_packages)

    apt_outdated_entries = get_apt_outdated_packages()
    snap_outdated_entries = get_snap_outdated_packages()
    flatpak_outdated_entries = get_flatpak_outdated_packages()
    combined_outdated = apt_outdated_entries + snap_outdated_entries + flatpak_outdated_entries
    apt_outdated_lookup = {entry['name'] for entry in apt_outdated_entries}
    gui_outdated = [pkg for pkg in gui_packages if pkg in apt_outdated_lookup]
    gui_up_to_date = [pkg for pkg in gui_packages if pkg not in apt_outdated_lookup]
    status = get_package_status(manual_packages, apt_outdated_lookup)

    print("\n[Q1] INSTALLED APPLICATION COUNTS (Ubuntu-only)")
    print("-" * 70)
    print(f"dpkg (APT) packages : {installed_totals['dpkg_packages']}")
    print(f"Snap applications    : {installed_totals['snap_apps']}")
    print(f"Flatpak applications : {installed_totals['flatpak_apps']}")
    print(f"Overall applications : {installed_totals['overall']}")
    print(f"Manual apt packages  : {len(manual_packages)}")
    print(f"GUI manual packages  : {len(gui_packages)}")

    print("\n[Q2] UPDATE STATUS (Ubuntu repositories)")
    print("-" * 70)
    if status:
        print(f"Manual GUI up-to-date: {len(gui_up_to_date)}")
        print(f"Manual GUI outdated  : {len(gui_outdated)}")
        print(f"Sample up-to-date GUI apps   : {_format_list(gui_up_to_date)}")
        print(f"Sample outdated GUI apps      : {_format_list(gui_outdated)}")
    else:
        print("No manual packages detected; unable to build GUI status table.")

    print("\nDetailed per-source outdated counts:")
    print(f"APT packages needing updates    : {len(apt_outdated_entries)}")
    print(f"Snap apps needing refresh       : {len(snap_outdated_entries)}")
    print(f"Flatpak apps needing refresh    : {len(flatpak_outdated_entries)}")

    if apt_outdated_entries:
        print(f"→ APT sample: {_format_list([entry['name'] for entry in apt_outdated_entries])}")
    if snap_outdated_entries:
        print(f"→ Snap sample: {_format_list([entry['name'] for entry in snap_outdated_entries])}")
    if flatpak_outdated_entries:
        print(f"→ Flatpak sample: {_format_list([entry['name'] for entry in flatpak_outdated_entries])}")

    print("\n[Q3] HIGHEST DATA-BREACH RISK (Outdated apps)")
    print("-" * 70)
    if combined_outdated:
        risk_assessment = assess_outdated_security_risks(combined_outdated)
        most_dangerous = risk_assessment[0]
        print(f"Highest risk package : {most_dangerous['package']} ({most_dangerous['source']})")
        print(f"Risk level           : {most_dangerous['risk']}")
        print(f"Breach rationale     : {most_dangerous['reason']}")

        attack_vectors = get_attack_vectors(most_dangerous['package'])
        exploitation = explain_exploitation(most_dangerous['package'], attack_vectors)

        print("\nKnown vulnerabilities:")
        for vuln in attack_vectors['vulnerabilities']:
            print(f"   • {vuln}")

        print("\nCommon attack methods:")
        for method in attack_vectors['attack_methods']:
            print(f"   {method}")

        print("\nExploit flow:")
        for step in exploitation['steps']:
            print(f"   {step}")

        print("\nPotential impact:")
        for impact in exploitation['impact']:
            print(f"   {impact}")

        print("\nRecommended mitigations:")
        for prevention in exploitation['prevention']:
            print(f"   {prevention}")

        print(f"\n⚡ IMMEDIATE ACTION: Update '{most_dangerous['package']}' via {most_dangerous['source']}.")
    else:
        print("All tracked application sources are fully up-to-date.")

    print("\nReport complete.")


if __name__ == "__main__":
    main()
