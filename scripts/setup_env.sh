#!/bin/bash
# Survey Analysis Kit - Environment Setup
# Run this once to install all dependencies

echo "=== Setting up Survey Analysis Kit for Kiro CLI ==="
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found: $(python3 --version)"
else
    echo "❌ Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found"
else
    echo "❌ pip3 not found. Please install pip first."
    exit 1
fi

# Install packages
echo ""
echo "Installing required Python packages..."
pip3 install pyreadstat pandas numpy scipy openpyxl python-pptx matplotlib seaborn

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All packages installed successfully!"
else
    echo ""
    echo "⚠️  Some packages may have failed. Try installing individually:"
    echo "    pip3 install pyreadstat"
    echo "    pip3 install pandas numpy scipy"
    echo "    pip3 install openpyxl python-pptx"
    echo "    pip3 install matplotlib seaborn"
fi

# Check Kiro CLI
echo ""
if command -v kiro &> /dev/null || command -v kiro-cli &> /dev/null; then
    echo "✅ Kiro CLI found"
else
    echo "⚠️  Kiro CLI not found in PATH. Make sure it's installed."
    echo "    See: https://kiro.dev/docs/cli/"
fi

# Create output directories
mkdir -p outputs scripts

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Drop your .sav file in the data/ folder"
echo "  2. cd to this directory"
echo "  3. Run: kiro"
echo "  4. Or: kiro-cli chat --agent survey-analyst"
echo ""
echo "Then tell Kiro:"
echo '  "Read .kiro/skills/spss/SKILL.md and analyze the SPSS file in data/"'
echo ""
