#!/bin/zsh
# ⏹️  Stop 24/7 Agent Service
# ਸੇਵਾ ਬੰਦ ਕਰਨ ਲਈ

cd /Users/gurpreetdhillon/Nam-toon-studio

echo "⏹️  Stopping 24/7 Agent Service..."

PID_FILE="agent_service.pid"

if [ -f "$PID_FILE" ]; then
    SERVICE_PID=$(cat $PID_FILE)
    
    # Check if process is running
    if ps -p $SERVICE_PID > /dev/null 2>&1; then
        echo "🔍 Found service running (PID: $SERVICE_PID)"
        echo "⏹️  Stopping..."
        
        # Send interrupt signal (graceful shutdown)
        kill -INT $SERVICE_PID
        
        # Wait a bit
        sleep 2
        
        # Check if still running
        if ps -p $SERVICE_PID > /dev/null 2>&1; then
            echo "⚠️  Service still running, force stopping..."
            kill -9 $SERVICE_PID
        fi
        
        echo "✅ Service stopped!"
        
        # Remove PID file
        rm -f $PID_FILE
    else
        echo "⚠️  Service not running (PID: $SERVICE_PID not found)"
        rm -f $PID_FILE
    fi
else
    echo "⚠️  No PID file found - checking for running processes..."
    
    # Find by name
    PIDS=$(ps aux | grep "CONTINUOUS_AGENT_SERVICE_24x7.py" | grep -v grep | awk '{print $2}')
    
    if [ -n "$PIDS" ]; then
        echo "🔍 Found running service(s):"
        echo "$PIDS"
        echo "⏹️  Stopping all..."
        
        for pid in $PIDS; do
            kill -INT $pid 2>/dev/null || kill -9 $pid 2>/dev/null
        done
        
        echo "✅ All services stopped!"
    else
        echo "✅ No service running"
    fi
fi

echo ""
echo "📊 Check status: cat agent_service_status.json"
echo "📝 Check logs: tail -50 24x7_agent_service.log"
echo "📄 Check reports: ls -lt night_report_*.txt | head -1"
