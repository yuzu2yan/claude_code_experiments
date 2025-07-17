#!/bin/bash

# JavaFX Todo App Runner Script
# This script helps run the JavaFX application without Maven

echo "JavaFX Todo App Runner"
echo "====================="

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed!"
    echo ""
    echo "Please install Java 17 or higher:"
    echo ""
    echo "Option 1 - Using Homebrew (recommended for macOS):"
    echo "  brew install openjdk@17"
    echo "  sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk"
    echo ""
    echo "Option 2 - Download from Oracle:"
    echo "  Visit: https://www.oracle.com/java/technologies/downloads/#java17"
    echo ""
    echo "Option 3 - Download from Adoptium (OpenJDK):"
    echo "  Visit: https://adoptium.net/temurin/releases/?version=17"
    exit 1
fi

# Check Java version
JAVA_VERSION_OUTPUT=$(java -version 2>&1)
echo "Detected Java: $JAVA_VERSION_OUTPUT" | head -n 1

# Extract version number (works for both 1.8.x and 17.x formats)
if [[ $JAVA_VERSION_OUTPUT =~ \"([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
    MAJOR=${BASH_REMATCH[1]}
    MINOR=${BASH_REMATCH[2]}
    if [[ $MAJOR -eq 1 ]]; then
        JAVA_VERSION=$MINOR
    else
        JAVA_VERSION=$MAJOR
    fi
elif [[ $JAVA_VERSION_OUTPUT =~ \"([0-9]+)\" ]]; then
    JAVA_VERSION=${BASH_REMATCH[1]}
else
    echo "Warning: Could not determine Java version. Proceeding anyway..."
    JAVA_VERSION=17
fi

if [[ "$JAVA_VERSION" -lt 17 ]]; then
    echo "Error: Java 17 or higher is required. Current version: $JAVA_VERSION"
    echo ""
    echo "Please upgrade Java using one of the methods above."
    exit 1
fi

echo "Java version check: OK (Java $JAVA_VERSION)"

# Create directories if they don't exist
mkdir -p lib
mkdir -p out

# Download JavaFX if not present
JAVAFX_VERSION="21"
JAVAFX_DIR="lib/javafx-${JAVAFX_VERSION}"

if [ ! -d "$JAVAFX_DIR" ]; then
    echo "JavaFX not found. Downloading JavaFX ${JAVAFX_VERSION}..."
    
    # Detect OS
    OS=$(uname -s)
    ARCH=$(uname -m)
    
    if [[ "$OS" == "Darwin" ]]; then
        if [[ "$ARCH" == "arm64" ]]; then
            JAVAFX_PLATFORM="osx-aarch64"
        else
            JAVAFX_PLATFORM="osx-x64"
        fi
    elif [[ "$OS" == "Linux" ]]; then
        JAVAFX_PLATFORM="linux-x64"
    else
        echo "Unsupported OS: $OS"
        exit 1
    fi
    
    JAVAFX_URL="https://download2.gluonhq.com/openjfx/${JAVAFX_VERSION}/openjfx-${JAVAFX_VERSION}_${JAVAFX_PLATFORM}_bin-sdk.zip"
    
    echo "Downloading from: $JAVAFX_URL"
    curl -L -o lib/javafx.zip "$JAVAFX_URL"
    
    echo "Extracting JavaFX..."
    unzip -q lib/javafx.zip -d lib/
    
    # Find the extracted directory (could be javafx-sdk-21 or javafx-21)
    EXTRACTED_DIR=$(find lib -maxdepth 1 -type d -name "javafx*${JAVAFX_VERSION}*" | head -n 1)
    
    if [ -n "$EXTRACTED_DIR" ]; then
        mv "$EXTRACTED_DIR" "$JAVAFX_DIR"
    else
        echo "Error: Could not find extracted JavaFX directory"
        exit 1
    fi
    
    rm lib/javafx.zip
    
    echo "JavaFX downloaded successfully!"
fi

# Compile the application
echo "Compiling the application..."

# Find all Java files
JAVA_FILES=$(find src/main/java -name "*.java" -type f)

# Compile with JavaFX
javac --module-path "$JAVAFX_DIR/lib" \
      --add-modules javafx.controls,javafx.fxml \
      -d out \
      -sourcepath src/main/java \
      $JAVA_FILES

if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

echo "Compilation successful!"

# Copy resources
echo "Copying resources..."
cp -r src/main/resources/* out/ 2>/dev/null || true

# Run the application
echo "Starting the application..."
echo ""

java --module-path "$JAVAFX_DIR/lib" \
     --add-modules javafx.controls,javafx.fxml \
     -cp out \
     com.example.todoapp.EnhancedTodoApp