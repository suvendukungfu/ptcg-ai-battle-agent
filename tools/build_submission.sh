#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_ARCHIVE="${PROJECT_ROOT}/submission.tar.gz"
TEMP_BUILD_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "${TEMP_BUILD_DIR}"
}
trap cleanup EXIT

echo "=================================================="
echo "    KAGGLE PTCG AGENT SUBMISSION BUILDER        "
echo "=================================================="
echo "Project Root : ${PROJECT_ROOT}"
echo "Staging Temp : ${TEMP_BUILD_DIR}"
echo "Target Tarball: ${OUTPUT_ARCHIVE}"
echo "--------------------------------------------------"

# 1. Copy required files to clean staging directory
echo "==> Staging essential files..."
cp "${PROJECT_ROOT}/main.py" "${TEMP_BUILD_DIR}/main.py"
cp "${PROJECT_ROOT}/deck.csv" "${TEMP_BUILD_DIR}/deck.csv"
cp -r "${PROJECT_ROOT}/src" "${TEMP_BUILD_DIR}/src"
cp -r "${PROJECT_ROOT}/agent" "${TEMP_BUILD_DIR}/agent"

if [ -d "${PROJECT_ROOT}/cg" ]; then
    cp -r "${PROJECT_ROOT}/cg" "${TEMP_BUILD_DIR}/cg"
fi

# 2. Validate deck count
echo "==> Validating deck.csv structure..."
DECK_COUNT=$(grep -v '^[[:space:]]*$' "${TEMP_BUILD_DIR}/deck.csv" | wc -l | tr -d ' ')
if [ "${DECK_COUNT}" -ne 60 ]; then
    echo "ERROR: deck.csv must contain exactly 60 cards, found ${DECK_COUNT}!"
    exit 1
fi
echo "  [OK] deck.csv contains exactly 60 valid card IDs."

# 3. Validate standalone imports
echo "==> Validating standalone imports in isolated environment..."
(
    cd "${TEMP_BUILD_DIR}"
    /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -c "
import main
deck = main.load_and_validate_deck()
assert len(deck) == 60, f'Expected 60 cards, got {len(deck)}'
t0_action = main.agent({'select': None})
assert len(t0_action) == 60, f'Expected 60 card action in turn 0, got {len(t0_action)}'
print('  [OK] Standalone import and Turn 0 initialization verified.')
"
)

# 4. Run pre-packaging isolated smoke test
echo "==> Running pre-packaging isolated smoke test simulation..."
(
    cd "${TEMP_BUILD_DIR}"
    /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -c "
from kaggle_environments import make
from kaggle_environments.envs.cabt import cabt
import main

env = make('cabt', debug=True)
env.run([main.agent, cabt.random_agent])

assert len(env.steps) > 0, 'No steps recorded in smoke test'
final_step = env.steps[-1]
assert final_step[0].status != 'INVALID', f'Agent produced INVALID status: {final_step[0].status}'
print(f'  [OK] Smoke test match completed cleanly in {len(env.steps)} steps (Status: {final_step[0].status}).')
"
)

# 5. Clean any runtime cache artifacts before final packaging
echo "==> Purging cache artifacts from staging..."
find "${TEMP_BUILD_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "${TEMP_BUILD_DIR}" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find "${TEMP_BUILD_DIR}" -type f -name ".DS_Store" -delete 2>/dev/null || true
find "${TEMP_BUILD_DIR}" -type f -name "*.pyc" -delete 2>/dev/null || true

# 6. Create submission archive at root level
echo "==> Packaging submission.tar.gz..."
rm -f "${OUTPUT_ARCHIVE}"
(
    cd "${TEMP_BUILD_DIR}"
    tar -czvf "${OUTPUT_ARCHIVE}" ./*
)

# 7. Verify archive size and constraints
echo "--------------------------------------------------"
ARCHIVE_SIZE_BYTES=$(wc -c < "${OUTPUT_ARCHIVE}" | tr -d ' ')
ARCHIVE_SIZE_MB=$(echo "scale=2; ${ARCHIVE_SIZE_BYTES} / 1048576" | bc)
MAX_ALLOWED_MB=197.7

echo "Archive Size: ${ARCHIVE_SIZE_MB} MiB (${ARCHIVE_SIZE_BYTES} bytes)"
if (( $(echo "${ARCHIVE_SIZE_MB} > ${MAX_ALLOWED_MB}" | bc -l) )); then
    echo "ERROR: Archive exceeds maximum allowed size of ${MAX_ALLOWED_MB} MiB!"
    exit 1
fi
echo "  [OK] Size is well within Kaggle competition limits (< ${MAX_ALLOWED_MB} MiB)."

# 8. Print archive contents
echo "==> Archive Table of Contents:"
tar -tzvf "${OUTPUT_ARCHIVE}"

echo "=================================================="
echo "SUCCESS: submission.tar.gz is built & certified!"
echo "Location: ${OUTPUT_ARCHIVE}"
echo "=================================================="
