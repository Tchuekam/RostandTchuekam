#!/bin/sh
set -e

# Railway provides PORT env var — default to 8642 if not set
RAIL_PORT="${PORT:-8642}"

echo "=== Hermes Agent starting on Railway ==="
echo "PORT=$RAIL_PORT"
echo "HERMES_HOME=$HERMES_HOME"

# Start gateway with API server enabled on Railway's PORT
export API_SERVER_HOST="0.0.0.0"
export API_SERVER_PORT="$RAIL_PORT"

# If no API_SERVER_KEY is set, generate a random one and print it
if [ -z "$API_SERVER_KEY" ]; then
    export API_SERVER_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
    echo "Generated API_SERVER_KEY=$API_SERVER_KEY"
    echo "(Set this as a Railway env var to keep it stable across deploys)"
fi

exec hermes gateway run
