#!/usr/bin/env python
"""
Entry point for running the STIX Generator application.
"""

import os
import uvicorn
from stix_generator.app import create_app
from asgiref.wsgi import WsgiToAsgi

print("Starting STIX Generator application...")

# Create the Flask app
app = create_app()
asgi_app = WsgiToAsgi(app)

# Run with Uvicorn if executed directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    # Run with uvicorn using our WSGI app wrapped in ASGI adapter
    uvicorn.run(
        asgi_app,
        host="0.0.0.0",
        port=port
    ) 