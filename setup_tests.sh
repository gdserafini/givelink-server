#!/bin/sh

set -e

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

. .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

echo "Tests environment successfully configured."
echo "Run the tests with 'task test'."