#!/bin/bash
#
# filename:   /home/al/projects/AddressBook_v2/install.sh
#
# A robust installer for the AddressBook Flask application.
# It is self-aware of its location and can be run from anywhere.

# --- Style and Color Definitions ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# --- Helper functions ---
info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# --- Find the script's own directory ---
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
info "Running installer from: $SCRIPT_DIR"

# --- Main Installation Logic ---
info "Step 1: Checking for essential tools (python3, pip)..."
if ! command -v python3 &> /dev/null || ! command -v pip &> /dev/null; then
    error "Python 3 and/or pip are not found. They are required to continue."
    warn "On Debian/Ubuntu, you can install them with: sudo apt install python3 python3-pip"
    exit 1
fi
info "Essential tools found."

# --- Step 2: Create and install Python dependencies ---
info "Step 2: Creating and installing Python packages from requirements.txt..."
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"

# Create the requirements file if it doesn't exist
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    info "requirements.txt not found. Creating it now."
    cat > "$REQUIREMENTS_FILE" << EOL
# Python dependencies for the AddressBook app
Flask
PyMySQL
Werkzeug
EOL
fi

python3 -m pip install -r "$REQUIREMENTS_FILE"
if [ $? -ne 0 ]; then
    error "Failed to install Python packages. Please check the pip output above."
    exit 1
fi
info "Python packages installed successfully."

# --- Step 3: Final Instructions ---
info "Step 3: Final manual setup required."
echo
warn "This application requires a MySQL database named 'addressbook'."
warn "Please ensure the database exists and that your credentials in"
warn "/home/$USER/py/config.py are correct for this database."
warn "You must also import the schema using the 'addressbook_schema_v2.sql' file."
warn "Example: mysql --defaults-file=/home/$USER/.my.cnf addressbook < ${SCRIPT_DIR}/addressbook_schema_v2.sql"
echo
info "Installation complete!"
info "You can now run the development server with: python3 ${SCRIPT_DIR}/app.py"
echo
