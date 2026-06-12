"""
ADAM SMASHER — Discord Webhook Server
Receives webhook events from Discord and stores messages for the HTML panel

This server allows the HTML Discord panel to receive Discord messages
without needing the bot to be running 24/7.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [WEBHOOK] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# ===== CONFIGURATION =====
DATA_DIR = Path(__file__).parent
MESSAGES_FILE = DATA_DIR / 'messages.json'
ALERTS_FILE = DATA_DIR / 'alerts.json'
CONFIG_FILE = DATA_DIR / 'webhook_config.json'

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-webhook-secret-here')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '5000'))

# Initialize files
MESSAGES_FILE.touch(exist_ok=True)
ALERTS_FILE.touch(exist_ok=True)
CONFIG_FILE.touch(exist_ok=True)

# ===== HELPER FUNCTIONS =====

def load_messages() -> List[Dict]:
    """Load messages from JSON file"""
    messages = []
    if MESSAGES_FILE.exists():
        try:
            with open(MESSAGES_FILE, 'r') as f:
                for line in f:
                    if line.strip():
                        messages.append(json.loads(line))
        except Exception as e:
            logger.error(f'Error loading messages: {e}')
    return messages


def save_message(message: Dict) -> None:
    """Save a message to JSON file"""
    try:
        with open(MESSAGES_FILE, 'a') as f:
            f.write(json.dumps(message, default=str) + '\n')
    except Exception as e:
        logger.error(f'Error saving message: {e}')


def load_config() -> Dict:
    """Load webhook configuration"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'discord_webhook_url': '',
        'channels': [],
        'alert_threshold_usdzar': 18.50,
        'alert_threshold_rubzar': 0.01,
        'enabled': True
    }


def save_config(config: Dict) -> None:
    """Save webhook configuration"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


# ===== HTML TEMPLATE =====

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADAM SMASHER — Webhook Server</title>
    <style>
        :root {
            --bg-dark: #0a0a0f;
            --bg-card: #13131a;
            --accent: #8b5cf6;
            --accent-light: #a78bfa;
            --success: #22c55e;
            --warning: #eab308;
            --error: #ef4444;
            --text: #e4e4e7;
            --text-muted: #71717a;
        }
        
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            color: var(--accent);
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            color: var(--text-muted);
            margin-bottom: 2rem;
        }
        
        .card {
            background: var(--bg-card);
            border: 1px solid rgba(139, 92, 246, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .card h2 {
            color: var(--accent);
            margin-top: 0;
            font-size: 1.2rem;
        }
        
        .status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid var(--success);
            border-radius: 20px;
            color: var(--success);
        }
        
        .status.error {
            background: rgba(239, 68, 68, 0.2);
            border-color: var(--error);
            color: var(--error);
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: currentColor;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat {
            text-align: center;
            padding: 15px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-light);
        }
        
        .stat-label {
            color: var(--text-muted);
            font-size: 0.85rem;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            color: var(--text-muted);
        }
        
        input, textarea {
            width: 100%;
            padding: 10px 12px;
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 6px;
            color: var(--text);
            font-size: 0.95rem;
            box-sizing: border-box;
        }
        
        input:focus, textarea:focus {
            outline: none;
            border-color: var(--accent);
        }
        
        button {
            padding: 10px 20px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }
        
        button:hover {
            background: var(--accent-light);
        }
        
        .btn-success {
            background: var(--success);
        }
        
        .btn-success:hover {
            background: #16a34a;
        }
        
        .logs {
            max-height: 400px;
            overflow-y: auto;
            background: rgba(0,0,0,0.4);
            border-radius: 6px;
            padding: 10px;
        }
        
        .log-entry {
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 0.85rem;
        }
        
        .log-entry:last-child {
            border-bottom: none;
        }
        
        .log-time {
            color: var(--text-muted);
            margin-right: 10px;
        }
        
        .log-type {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-right: 10px;
        }
        
        .log-type.event { background: rgba(59, 130, 246, 0.3); }
        .log-type.message { background: rgba(139, 92, 246, 0.3); }
        .log-type.alert { background: rgba(234, 179, 8, 0.3); }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
        
        code {
            background: rgba(0,0,0,0.4);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 ADAM SMASHER Webhook Server</h1>
        <p class="subtitle">Discord integration endpoint for the Global Markets OS</p>
        
        <div class="card">
            <h2>📡 Server Status</h2>
            <div class="status" id="status">
                <span class="status-dot"></span>
                <span>Online</span>
            </div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="msg-count">{{ stats.messages }}</div>
                    <div class="stat-label">Messages</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="event-count">{{ stats.events }}</div>
                    <div class="stat-label">Events</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="uptime">{{ stats.uptime }}</div>
                    <div class="stat-label">Uptime</div>
                </div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>⚙️ Configuration</h2>
                <form id="config-form">
                    <div class="form-group">
                        <label>Discord Webhook URL</label>
                        <input type="text" id="webhook-url" value="{{ config.discord_webhook_url }}" placeholder="https://discord.com/api/webhooks/...">
                    </div>
                    <div class="form-group">
                        <label>USD/ZAR Alert Threshold</label>
                        <input type="number" step="0.01" id="threshold-usdzar" value="{{ config.alert_threshold_usdzar }}">
                    </div>
                    <div class="form-group">
                        <label>RUB/ZAR Move Threshold (%)</label>
                        <input type="number" step="0.1" id="threshold-rubzar" value="{{ config.alert_threshold_rubzar }}">
                    </div>
                    <button type="submit" class="btn-success">Save Configuration</button>
                </form>
            </div>
            
            <div class="card">
                <h2>📋 Recent Activity</h2>
                <div class="logs" id="logs">
                    {% for log in logs %}
                    <div class="log-entry">
                        <span class="log-time">{{ log.time }}</span>
                        <span class="log-type {{ log.type }}">{{ log.type }}</span>
                        {{ log.message }}
                    </div>
                    {% endfor %}
                    {% if not logs %}
                    <div class="log-entry" style="color: var(--text-muted); text-align: center;">
                        No activity yet. Send a webhook request to see logs.
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>🔗 Endpoints</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);"><code>POST /webhook</code></td>
                    <td style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);">Receive Discord webhook events</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);"><code>GET /messages</code></td>
                    <td style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);">Get all stored messages</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);"><code>GET /config</code></td>
                    <td style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);">Get webhook configuration</td>
                </tr>
                <tr>
                    <td style="padding: 10px;"><code>GET /status</code></td>
                    <td style="padding: 10px;">Server health check</td>
                </tr>
            </table>
        </div>
    </div>
    
    <script>
        // Auto-refresh stats
        async function refreshStats() {
            try {
                const res = await fetch('/status');
                const data = await res.json();
                document.getElementById('msg-count').textContent = data.message_count;
                document.getElementById('event-count').textContent = data.event_count;
            } catch (e) {
                console.error('Failed to refresh stats:', e);
            }
        }
        
        setInterval(refreshStats, 5000);
        
        // Handle config form
        document.getElementById('config-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                discord_webhook_url: document.getElementById('webhook-url').value,
                alert_threshold_usdzar: parseFloat(document.getElementById('threshold-usdzar').value),
                alert_threshold_rubzar: parseFloat(document.getElementById('threshold-rubzar').value)
            };
            
            await fetch('/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            alert('Configuration saved!');
        });
    </script>
</body>
</html>
"""


# ===== ROUTES =====

@app.route('/')
def index():
    """Dashboard page"""
    messages = load_messages()
    config = load_config()
    
    # Calculate stats
    events = [m for m in messages if m.get('type') != 'message' or not m.get('content')]
    message_count = len(messages)
    
    # Recent logs (last 20)
    logs = []
    for msg in messages[-20:]:
        logs.append({
            'time': msg.get('timestamp', '')[:19],
            'type': 'message' if msg.get('content') else 'event',
            'message': msg.get('content', msg.get('event_type', 'Unknown event'))[:100]
        })
    
    return render_template_string(HTML_TEMPLATE, 
        stats={
            'messages': message_count,
            'events': len(events),
            'uptime': 'Active'
        },
        config=config,
        logs=logs
    )


@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive webhook events from Discord"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Add timestamp
        data['received_at'] = datetime.utcnow().isoformat()
        
        # Determine event type
        if data.get('type') == 1:  # Discord ping
            return jsonify({'type': 1})  # Pong
        
        # Store the event
        save_message(data)
        
        logger.info(f'Received webhook: {data.get("event_type", "unknown")}')
        
        return jsonify({'status': 'ok', 'received': True})
    except Exception as e:
        logger.error(f'Webhook error: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/messages', methods=['GET'])
def get_messages():
    """Get all stored messages"""
    limit = request.args.get('limit', 100, type=int)
    messages = load_messages()
    return jsonify(messages[-limit:])


@app.route('/messages/recent', methods=['GET'])
def get_recent_messages():
    """Get recent messages (last 20)"""
    messages = load_messages()
    return jsonify(messages[-20:])


@app.route('/config', methods=['GET'])
def get_config():
    """Get webhook configuration"""
    return jsonify(load_config())


@app.route('/config', methods=['POST'])
def update_config():
    """Update webhook configuration"""
    try:
        data = request.json
        config = load_config()
        config.update(data)
        save_config(config)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    """Server health check"""
    messages = load_messages()
    return jsonify({
        'status': 'online',
        'message_count': len(messages),
        'event_count': len([m for m in messages if not m.get('content')]),
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/clear', methods=['POST'])
def clear_messages():
    """Clear all stored messages"""
    try:
        with open(MESSAGES_FILE, 'w') as f:
            f.write('')
        return jsonify({'status': 'ok', 'cleared': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== CORS SUPPORT =====
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response


# ===== RUN =====
if __name__ == '__main__':
    print('='*60)
    print('ADAM SMASHER Webhook Server')
    print('='*60)
    print(f'Port: {WEBHOOK_PORT}')
    print(f'Messages file: {MESSAGES_FILE}')
    print(f'Dashboard: http://localhost:{WEBHOOK_PORT}')
    print('='*60)
    
    app.run(host='0.0.0.0', port=WEBHOOK_PORT, debug=False)