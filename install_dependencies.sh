#!/bin/bash

# Install Poppler
install_poppler() {
    if ! command -v pdftoppm &> /dev/null; then
        echo "Poppler is not installed. Installing..."
        
        # Install Poppler
        sudo apt-get update
        sudo apt-get install -y poppler-utils  # For Ubuntu/Debian-based systems
        
        # Check if installation was successful
        if [ $? -eq 0 ]; then
            echo "Poppler installed successfully."
        else
            echo "Failed to install Poppler. Please install it manually."
            exit 1
        fi
    else
        echo "Poppler is already installed."
    fi
}

# Install Tesseract OCR
install_tesseract() {
    if ! command -v tesseract &> /dev/null; then
        echo "Tesseract OCR is not installed. Installing..."
        
        # Install Tesseract OCR
        sudo apt-get install -y tesseract-ocr
        
        # Check if installation was successful
        if [ $? -eq 0 ]; then
            echo "Tesseract OCR installed successfully."
        else
            echo "Failed to install Tesseract OCR. Please install it manually."
            exit 1
        fi
    else
        echo "Tesseract OCR is already installed."
    fi
}

# Main function
main() {
    install_poppler
    install_tesseract
}

# Execute main function
main
