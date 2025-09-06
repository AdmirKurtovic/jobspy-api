#!/usr/bin/env python3
"""
Railway startup script
"""

import os
import sys

# Set default port if not provided
if 'PORT' not in os.environ:
    os.environ['PORT'] = '8000'

# Import and run the app
from railway_app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Railway app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
