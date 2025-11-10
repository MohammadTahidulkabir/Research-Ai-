#!/bin/bash

echo "========================================"
echo "AI Research Agent - Installation"
echo "========================================"
echo ""

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Installation complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Add your OPENAI_API_KEY to .env"
echo "3. Run: python test_agent.py"
echo ""
