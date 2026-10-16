#!/usr/bin/env bash
# Copies the fixture project into the empty eval workspace.
set -euo pipefail
cp -R "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/fixture/." .
rm -f expect.yaml
git init -q && git add -A && git -c user.email=eval@example.com -c user.name=eval commit -qm "fixture"
