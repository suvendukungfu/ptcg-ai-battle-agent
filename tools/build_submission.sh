#!/usr/bin/env bash
set -e

# Base directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

echo "=================================================="
echo "      PTCG AI BATTLE SUBMISSION PACKAGER         "
echo "=================================================="

BUILD_DIR="$BASE_DIR/build_submission_tmp"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 1. Copy required submission files into isolated staging directory
echo "[1/5] Staging production submission files..."
cp "$BASE_DIR/main.py" "$BUILD_DIR/"
cp "$BASE_DIR/deck.csv" "$BUILD_DIR/"
cp -r "$BASE_DIR/agent" "$BUILD_DIR/"
if [ -d "$BASE_DIR/data" ]; then
    mkdir -p "$BUILD_DIR/data"
    cp -r "$BASE_DIR/data"/* "$BUILD_DIR/data/" 2>/dev/null || true
fi
if [ -d "$BASE_DIR/src" ]; then
    mkdir -p "$BUILD_DIR/src"
    cp -r "$BASE_DIR/src"/* "$BUILD_DIR/src/" 2>/dev/null || true
fi

# 2. Validate Deck File
echo "[2/5] Validating deck.csv format (exactly 60 integer cards)..."
DECK_COUNT=$(grep -v '^$' "$BUILD_DIR/deck.csv" | tr ',' '\n' | grep -v '^$' | wc -l | tr -d ' ')
if [ "$DECK_COUNT" -ne 60 ]; then
    echo "ERROR: deck.csv contains $DECK_COUNT cards (must be exactly 60)!"
    rm -rf "$BUILD_DIR"
    exit 1
fi
echo "      Deck validation: PASS (60 cards verified)"

# 3. Validate Imports & Smoke Test
echo "[3/5] Running isolated Python import and smoke tests..."
PYTHON_BIN="$BASE_DIR/.venv/bin/python"
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

"$PYTHON_BIN" - <<EOF
import os
import sys

sys.path.insert(0, "$BUILD_DIR")
import main

# Test Turn 0
deck = main.agent({"select": None, "current": None})
assert isinstance(deck, list) and len(deck) == 60, "Turn 0 must return 60-card deck"

# Test Turn 1 Legal Selection
test_obs = {
    "remainingOverageTime": 600.0,
    "select": {
        "type": 0,
        "minCount": 1,
        "maxCount": 1,
        "option": [{"type": 14}]
    },
    "current": {
        "yourIndex": 0,
        "turn": 1,
        "players": [
            {"active": [{"id": 723, "hp": 350, "energies": [3, 3]}], "prize": [1, 2]},
            {"active": [{"id": 721, "hp": 100}], "prize": [1, 2, 3]}
        ]
    }
}
action = main.agent(test_obs)
assert isinstance(action, list) and len(action) == 1, "Agent must return valid action list"
print("      Agent import: PASS")
print("      Smoke test: PASS")
EOF

# 4. Package Tarball
echo "[4/5] Building submission.tar.gz..."
OUTPUT_TAR="$BASE_DIR/submission.tar.gz"
rm -f "$OUTPUT_TAR"

cd "$BUILD_DIR"
tar --exclude='*.pyc' --exclude='__pycache__' --exclude='.DS_Store' -czf "$OUTPUT_TAR" ./*
cd "$BASE_DIR"
rm -rf "$BUILD_DIR"

# 5. Validate Archive Size & Integrity
FILE_SIZE_BYTES=$(wc -c < "$OUTPUT_TAR" | tr -d ' ')
FILE_SIZE_MIB=$(awk "BEGIN {printf \"%.2f\", $FILE_SIZE_BYTES / (1024 * 1024)}")
MAX_SIZE_MIB="197.7"

echo "[5/5] Checking submission archive size constraints..."
if (( $(echo "$FILE_SIZE_MIB > 197.7" | bc -l 2>/dev/null || echo 0) )); then
    echo "ERROR: submission.tar.gz is $FILE_SIZE_MIB MiB (exceeds 197.7 MiB limit)!"
    exit 1
fi

FILE_COUNT=$(tar -ztvf "$OUTPUT_TAR" | wc -l | tr -d ' ')

echo ""
echo "=================================================="
echo "              Submission READY                    "
echo "=================================================="
echo "Archive Path   : $OUTPUT_TAR"
echo "Size           : $FILE_SIZE_MIB MiB (Limit: $MAX_SIZE_MIB MiB)"
echo "Files Included : $FILE_COUNT"
echo "Agent import   : PASS"
echo "Deck validation: PASS"
echo "Smoke test     : PASS"
echo "=================================================="
