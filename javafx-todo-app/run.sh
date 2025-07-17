#!/bin/bash

# JavaFX Todo App Runner Script
# This script helps run the JavaFX application without Maven

echo "JavaFX Todo App Runner"
echo "====================="

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed. Please install Java 17 or higher."
    exit 1
fi

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | cut -d'.' -f1)
if [[ "$JAVA_VERSION" -lt 17 ]]; then
    echo "Error: Java 17 or higher is required. Current version: $JAVA_VERSION"
    exit 1
fi

echo "Java version check: OK"

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
    mv lib/javafx-${JAVAFX_VERSION} "$JAVAFX_DIR"
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