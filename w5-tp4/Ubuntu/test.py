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

# Run the functions
if __name__ == "__main__":
    print("=" * 70)
    print("THIRD-PARTY APPLICATIONS (MANUALLY INSTALLED)")
    print("=" * 70)
    
    # List only manually installed packages (third-party)
    manual = count_manual_packages()
    
    if manual is not None:
        print(f"\n✅ Total third-party applications found: {manual}\n")
    
    # List manually installed packages
    print("-" * 70)
    print("THIRD-PARTY APPLICATIONS:")
    print("-" * 70)
    manual_list = list_manual_packages()
    if manual_list:
        for i, package in enumerate(manual_list, 1):
            print(f"{i}. {package}")
    else:
        print("No third-party applications found.")
