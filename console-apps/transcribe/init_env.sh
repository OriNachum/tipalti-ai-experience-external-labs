
    #!/bin/bash
    # Bash script to initialize Python virtual environment and install packages from requirements.txt

    # Create virtual environment
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
    fi

    # Activate the virtual environment
    echo "Activating virtual environment..."\

    source .venv/bin/activate
    # Install requirements
    pip install -r requirements.txt
