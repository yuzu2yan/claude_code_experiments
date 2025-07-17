# Installation Guide for JavaFX Todo App

## Prerequisites

### Java 17 Installation

The application requires Java 17 or higher. Here are several ways to install it:

#### Option 1: Using Homebrew (Recommended for macOS)

```bash
# Install OpenJDK 17
brew install openjdk@17

# Create symlink for system Java
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

# Add to PATH (add this to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"

# Verify installation
java -version
```

#### Option 2: Using SDKMAN (Cross-platform)

```bash
# Install SDKMAN
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install Java 17
sdk install java 17.0.9-tem

# Verify installation
java -version
```

#### Option 3: Direct Download

1. **Oracle JDK 17** (requires Oracle account):
   - Visit: https://www.oracle.com/java/technologies/downloads/#java17
   - Download the installer for your OS
   - Run the installer

2. **Adoptium OpenJDK 17** (recommended, no account required):
   - Visit: https://adoptium.net/temurin/releases/?version=17
   - Download the installer for your OS
   - Run the installer

### Maven Installation (Optional)

If you want to use Maven instead of the provided run script:

#### Using Homebrew (macOS)
```bash
brew install maven
```

#### Manual Installation
```bash
# Download Maven
curl -O https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz

# Extract
tar -xzvf apache-maven-3.9.6-bin.tar.gz

# Move to /opt
sudo mv apache-maven-3.9.6 /opt/maven

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH=/opt/maven/bin:$PATH

# Verify installation
mvn -version
```

## Running the Application

After installing Java 17:

### Method 1: Using the Run Script
```bash
cd javafx-todo-app
./run.sh
```

### Method 2: Using Maven (if installed)
```bash
cd javafx-todo-app
mvn clean javafx:run
```

## Troubleshooting

### "Java not found" error
- Make sure Java is in your PATH
- Try restarting your terminal after installation
- Run `echo $PATH` to verify Java's bin directory is included

### "Java version too old" error
- Check current version: `java -version`
- If you have multiple Java versions, use jenv or update-alternatives to switch

### macOS specific issues
- If you get permission errors, make sure to use `sudo` for the symlink command
- On Apple Silicon Macs, make sure to download the ARM64 version of Java

### Script permission denied
```bash
chmod +x run.sh
```