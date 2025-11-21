#!/bin/bash
# Script to convert Java to Windows EXE

echo "========================================="
echo "Java to EXE Converter (3 Methods)"
echo "========================================="

# Check if JAR exists
if [ ! -f "test.jar" ]; then
    echo "[*] Compiling Java file..."
    javac test.java
    jar cfe test.jar test test.class
    echo "[+] Created test.jar"
fi

echo ""
echo "Choose conversion method:"
echo "1. jpackage (native Windows .exe with bundled JRE)"
echo "2. Launch4j wrapper (requires manual download)"
echo "3. Simple JAR wrapper script"
read -p "Select (1-3): " choice

case $choice in
    1)
        echo ""
        echo "[*] Using jpackage (creates native Windows installer)..."
        echo "[!] Note: This creates a Windows installer, not a single .exe"
        
        jpackage --input . \
                 --name test \
                 --main-jar test.jar \
                 --main-class test \
                 --type exe \
                 --dest output
        
        if [ -d "output" ]; then
            echo "[+] SUCCESS! Check the 'output' directory"
            ls -lh output/
        else
            echo "[-] jpackage failed. You may need to install additional tools."
        fi
        ;;
    2)
        echo ""
        echo "[*] Download Launch4j from: https://launch4j.sourceforge.net/"
        echo "[*] Creating configuration file..."
        
        cat > launch4j_config.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<launch4jConfig>
  <dontWrapJar>false</dontWrapJar>
  <headerType>console</headerType>
  <jar>test.jar</jar>
  <outfile>test.exe</outfile>
  <errTitle>Error</errTitle>
  <jre>
    <minVersion>1.8.0</minVersion>
  </jre>
</launch4jConfig>
EOF
        echo "[+] Created launch4j_config.xml"
        echo "[!] Run Launch4j on Windows and load this config file"
        ;;
    3)
        echo ""
        echo "[*] Creating JAR wrapper executable..."
        
        cat > test.sh << 'EOF'
#!/bin/bash
java -jar test.jar "$@"
EOF
        chmod +x test.sh
        
        cat > test.bat << 'EOF'
@echo off
java -jar test.jar %*
EOF
        
        echo "[+] Created wrapper scripts:"
        echo "    - test.sh (Linux/Mac)"
        echo "    - test.bat (Windows)"
        ;;
    *)
        echo "[-] Invalid choice"
        ;;
esac

echo ""
echo "========================================="
echo "Files created:"
ls -lh test.* 2>/dev/null | grep -v ".class"
echo "========================================="
