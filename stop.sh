kill -9 $(lsof -t -i:9008) >/dev/null 2>&1

echo "Stop server..."