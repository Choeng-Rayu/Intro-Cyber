#!/usr/bin/env python3
import subprocess
import json
import socket
import sys
import os
from datetime import datetime
from pathlib import Path
import threading

class SystemInfoGatherer:
    def __init__(self):
        self.info = {
            'timestamp': datetime.now().isoformat(),
            'hostname': socket.gethostname(),
            'applications': [],
            'vulnerabilities': [],
            'system_info': {},
        }
        
        self.vuln_db = {
            'curl': {'7.64.0': ['CVE-2019-3822', 'CVE-2019-3823'], '7.68.0': ['CVE-2020-8169']},
            'wget': {'1.20.0': ['CVE-2018-20225'], '1.20.1': ['CVE-2018-20225']},
            'openssh-server': {'7.4': ['CVE-2018-15473'], '7.6': ['CVE-2019-9778']},
            'openssl': {'1.1.0': ['CVE-2019-1559'], '1.1.1': ['CVE-2020-1971']},
            'bash': {'4.3': ['CVE-2014-6271', 'CVE-2014-7169'], '4.4': ['CVE-2016-3189']},
            'sudo': {'1.8.20': ['CVE-2019-14287'], '1.8.27': ['CVE-2019-14287']},
            'python3': {'3.6': ['CVE-2019-9740', 'CVE-2019-9947'], '3.7': ['CVE-2019-9740']},
        }
        
        self.cve_details = {
            'CVE-2019-3822': {'severity': 'HIGH', 'impact': 'RCE', 'cvss': 8.1},
            'CVE-2019-3823': {'severity': 'HIGH', 'impact': 'RCE', 'cvss': 8.1},
            'CVE-2014-6271': {'severity': 'CRITICAL', 'impact': 'Shellshock RCE', 'cvss': 9.8},
            'CVE-2014-7169': {'severity': 'CRITICAL', 'impact': 'Shellshock RCE', 'cvss': 9.8},
            'CVE-2018-20225': {'severity': 'HIGH', 'impact': 'Code Execution', 'cvss': 8.8},
            'CVE-2018-15473': {'severity': 'MEDIUM', 'impact': 'User Enumeration', 'cvss': 5.3},
            'CVE-2019-14287': {'severity': 'CRITICAL', 'impact': 'Privilege Escalation', 'cvss': 9.8},
            'CVE-2019-1559': {'severity': 'MEDIUM', 'impact': 'Information Disclosure', 'cvss': 5.3},
            'CVE-2020-1971': {'severity': 'MEDIUM', 'impact': 'Certificate Bypass', 'cvss': 5.3},
            'CVE-2019-9740': {'severity': 'HIGH', 'impact': 'URL Open', 'cvss': 8.6},
            'CVE-2019-9947': {'severity': 'HIGH', 'impact': 'URL Open', 'cvss': 8.6},
            'CVE-2019-9778': {'severity': 'HIGH', 'impact': 'RCE', 'cvss': 7.0},
            'CVE-2016-3189': {'severity': 'HIGH', 'impact': 'Buffer Overflow', 'cvss': 7.8},
            'CVE-2020-8169': {'severity': 'MEDIUM', 'impact': 'DoS', 'cvss': 5.3},
        }

    def get_installed_apps(self):
        apps = []
        
        try:
            result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True, timeout=10)
            for line in result.stdout.split('\n'):
                if line.startswith('ii'):
                    parts = line.split()
                    if len(parts) >= 4:
                        apps.append({'name': parts[1], 'version': parts[2], 'source': 'dpkg'})
        except:
            pass
        
        try:
            result = subprocess.run(['apt', 'list', '--installed'], capture_output=True, text=True, timeout=10)
            for line in result.stdout.split('\n')[1:]:
                if '/' in line:
                    parts = line.split('/')
                    name = parts[0].strip()
                    if not any(app['name'] == name for app in apps):
                        version = line.split()[1] if len(line.split()) > 1 else 'unknown'
                        apps.append({'name': name, 'version': version, 'source': 'apt'})
        except:
            pass
        
        try:
            result = subprocess.run(['snap', 'list'], capture_output=True, text=True, timeout=10)
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        apps.append({'name': parts[0], 'version': parts[1], 'source': 'snap'})
        except:
            pass
        
        unique_apps = {}
        for app in apps:
            if app['name'] not in unique_apps:
                unique_apps[app['name']] = app
        
        self.info['applications'] = list(unique_apps.values())
        return unique_apps

    def check_vulnerabilities(self):
        vulns = []
        
        for app in self.info['applications']:
            app_name = app['name'].lower()
            app_version = app['version']
            
            if app_name in self.vuln_db:
                for vuln_ver, cve_list in self.vuln_db[app_name].items():
                    if vuln_ver in app_version or app_version.startswith(vuln_ver):
                        for cve_id in cve_list:
                            if cve_id in self.cve_details:
                                vuln_data = self.cve_details[cve_id]
                                vulns.append({
                                    'cve_id': cve_id,
                                    'application': app_name,
                                    'version': app_version,
                                    'severity': vuln_data['severity'],
                                    'impact': vuln_data['impact'],
                                    'cvss': vuln_data['cvss']
                                })
        
        self.info['vulnerabilities'] = vulns
        return vulns

    def get_system_info(self):
        try:
            with open('/etc/os-release', 'r') as f:
                os_data = {}
                for line in f:
                    if '=' in line:
                        key, val = line.strip().split('=', 1)
                        os_data[key] = val.strip('"')
                self.info['system_info']['os'] = os_data.get('NAME', 'Unknown')
        except:
            self.info['system_info']['os'] = 'Unknown'
        
        try:
            result = subprocess.run(['uptime', '-p'], capture_output=True, text=True, timeout=5)
            self.info['system_info']['uptime'] = result.stdout.strip()
        except:
            self.info['system_info']['uptime'] = 'Unknown'
        
        try:
            result = subprocess.run(['hostname', '-I'], capture_output=True, text=True, timeout=5)
            self.info['system_info']['ip_addresses'] = result.stdout.strip()
        except:
            self.info['system_info']['ip_addresses'] = 'Unknown'
        
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                self.info['system_info']['disk'] = lines[1]
        except:
            self.info['system_info']['disk'] = 'Unknown'
        
        try:
            result = subprocess.run(['free', '-h'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                self.info['system_info']['memory'] = lines[1]
        except:
            self.info['system_info']['memory'] = 'Unknown'

    def send_to_server(self, server_ip, server_port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_ip, int(server_port)))
            
            data = json.dumps(self.info)
            length = len(data)
            sock.send(length.to_bytes(4, 'big'))
            sock.send(data.encode())
            sock.close()
            return True
        except:
            return False

    def save_to_file(self):
        try:
            Path('data').mkdir(exist_ok=True)
            filename = f"data/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.info, f, indent=2)
            return filename
        except:
            return None

    def run(self):
        self.get_installed_apps()
        self.check_vulnerabilities()
        self.get_system_info()


class DataReceiver:
    def __init__(self):
        self.connection_count = 0
    
    def start_server(self, host='127.0.0.1', port=5555):
        print(f"[*] Starting server on {host}:{port}")
        
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(5)
            
            print(f"[+] Server listening...\n")
            
            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                    self.connection_count += 1
                    print(f"[+] Connection #{self.connection_count} from {client_address[0]}:{client_address[1]}")
                    
                    length_bytes = client_socket.recv(4)
                    if not length_bytes:
                        client_socket.close()
                        continue
                    
                    data_length = int.from_bytes(length_bytes, 'big')
                    data = b''
                    
                    while len(data) < data_length:
                        chunk = client_socket.recv(min(4096, data_length - len(data)))
                        if not chunk:
                            break
                        data += chunk
                    
                    client_socket.close()
                    
                    if data:
                        victim_data = json.loads(data.decode())
                        
                        print(f"    Hostname: {victim_data.get('hostname', 'N/A')}")
                        print(f"    Apps: {len(victim_data.get('applications', []))}")
                        print(f"    Vulns: {len(victim_data.get('vulnerabilities', []))}\n")
                        
                        Path('received_data').mkdir(exist_ok=True)
                        filename = f"received_data/{victim_data.get('hostname', 'victim')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        with open(filename, 'w') as f:
                            json.dump(victim_data, f, indent=2)
                        
                        print(f"    [+] Saved to {filename}\n")
                
                except Exception as e:
                    print(f"    [-] Error: {e}\n")
                    continue
        
        except KeyboardInterrupt:
            print("\n[*] Server stopped")
        except Exception as e:
            print(f"[-] Error: {e}")


def show_menu():
    print("\n" + "="*50)
    print("  VULNERABILITY SCANNER & DATA RECEIVER")
    print("="*50)
    print("1. Scan this system")
    print("2. Scan and save to file")
    print("3. Scan and send to server")
    print("4. Start receiver server")
    print("5. View last scan results")
    print("6. Exit")
    print("="*50)
    return input("Select option (1-6): ").strip()


def view_last_scan():
    try:
        data_dir = Path('data')
        if not data_dir.exists():
            print("[-] No scan results found")
            return
        
        files = sorted(data_dir.glob('scan_*.json'), key=lambda x: x.stat().st_mtime, reverse=True)
        if not files:
            print("[-] No scan results found")
            return
        
        latest = files[0]
        with open(latest, 'r') as f:
            data = json.load(f)
        
        print(f"\n[+] Latest scan: {latest}")
        print(f"    Hostname: {data.get('hostname', 'N/A')}")
        print(f"    Applications: {len(data.get('applications', []))}")
        print(f"    Vulnerabilities: {len(data.get('vulnerabilities', []))}")
        
        vulns = data.get('vulnerabilities', [])
        if vulns:
            print(f"\n    Critical/High Vulns:")
            for vuln in vulns[:5]:
                if vuln['severity'] in ['CRITICAL', 'HIGH']:
                    print(f"      • {vuln['cve_id']} ({vuln['application']}) - {vuln['impact']}")
    except Exception as e:
        print(f"[-] Error viewing results: {e}")


def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            print("\n[*] Scanning system...")
            gatherer = SystemInfoGatherer()
            gatherer.run()
            print("[+] Scan complete!")
            print(f"    Applications: {len(gatherer.info['applications'])}")
            print(f"    Vulnerabilities: {len(gatherer.info['vulnerabilities'])}")
        
        elif choice == '2':
            print("\n[*] Scanning system...")
            gatherer = SystemInfoGatherer()
            gatherer.run()
            filename = gatherer.save_to_file()
            print(f"[+] Scan saved to {filename}")
        
        elif choice == '3':
            print("\n[*] Scanning system...")
            gatherer = SystemInfoGatherer()
            gatherer.run()
            
            server_ip = input("Enter server IP: ").strip()
            server_port = input("Enter server port (default 5555): ").strip() or '5555'
            
            print(f"[*] Sending to {server_ip}:{server_port}...")
            if gatherer.send_to_server(server_ip, server_port):
                print(f"[+] Data sent successfully")
                gatherer.save_to_file()
            else:
                print(f"[-] Failed to send data")
        
        elif choice == '4':
            host = input("Enter listen address (default 127.0.0.1): ").strip() or '127.0.0.1'
            port_input = input("Enter listen port (default 5555): ").strip() or '5555'
            
            try:
                port = int(port_input)
                receiver = DataReceiver()
                receiver.start_server(host, port)
            except ValueError:
                print("[-] Invalid port number")
            except Exception as e:
                print(f"[-] Error: {e}")
        
        elif choice == '5':
            view_last_scan()
        
        elif choice == '6':
            print("\n[*] Goodbye!")
            break
        
        else:
            print("[-] Invalid option")


if __name__ == '__main__':
    main()
