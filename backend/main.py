#!/usr/bin/env python3
"""
ResumeForge Backend - Main Entry Point
Consolidated from app.py, run_app.py, and simple_server.py

Usage:
    python -m backend.main                 # Start with default config
    python -m backend.main --port 8000     # Custom port
    python -m backend.main --debug         # Enable debug mode
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.api import create_app
from backend.config import settings


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="ResumeForge Backend API Server"
    )
    parser.add_argument(
        "--host",
        default=settings.flask.host,
        help=f"Host to bind to (default: {settings.flask.host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.flask.port,
        help=f"Port to bind to (default: {settings.flask.port})",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=settings.flask.debug,
        help="Enable debug mode",
    )
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode",
    )
    return parser.parse_args()


def print_startup_info(host: str, port: int, debug: bool):
    """Print startup information"""
    print("=" * 70)
    print("🚀 ResumeForge Backend API v2.0.0")
    print("=" * 70)
    print(f"📡 Server:       http://{host}:{port}")
    print(f"🔧 Debug mode:   {'enabled' if debug else 'disabled'}")
    print(f"🤖 AI Provider:  {settings.ai.provider}")
    print(f"📊 Model:        {settings.ai.openai_model if settings.ai.provider == 'openai' else settings.ai.local_model_name}")
    print(f"📄 PDF Export:   {'enabled' if settings.pdf_export_enabled else 'disabled'}")
    print("=" * 70)
    print("\n📋 Available Endpoints:")
    print(f"   GET  http://{host}:{port}/api/health")
    print(f"   POST http://{host}:{port}/api/optimize")
    print(f"   POST http://{host}:{port}/api/parse-resume")
    print(f"   POST http://{host}:{port}/api/validate-resume")
    print(f"   GET  http://{host}:{port}/api/sample-resume")
    if settings.pdf_export_enabled:
        print(f"   POST http://{host}:{port}/api/export-pdf")
    print("\n✨ Ready to optimize resumes!\n")


def main():
    """Main entry point"""
    args = parse_args()

    # Determine debug mode
    if args.no_debug:
        debug = False
    else:
        debug = args.debug

    # Create Flask app
    app = create_app()

    if app is None:
        print("❌ Failed to create application. Flask not available.")
        print("   Install with: pip install Flask Flask-CORS")
        sys.exit(1)

    # Print startup info
    print_startup_info(args.host, args.port, debug)

    # Run the server
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=debug,
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
