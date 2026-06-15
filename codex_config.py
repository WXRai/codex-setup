# -*- coding: utf-8 -*-
"""
Codex CLI Third-Party API Config Tool
=====================================
Usage:
    Interactive:  python codex_config.py
    Parameters:   python codex_config.py -u https://api.x.com -k sk-xxx
    Show config:  python codex_config.py --show
    Clear config: python codex_config.py --clear
"""

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path

SCRIPT_VERSION = "3.0"
PROVIDER_NAME = "custom"


def get_codex_dir():
    """Get ~/.codex/ directory path"""
    return Path.home() / ".codex"


def get_config_path():
    return get_codex_dir() / "config.toml"


def get_auth_path():
    return get_codex_dir() / "auth.json"


def backup_file(path):
    """Backup file with .backup suffix"""
    if path.exists():
        backup = Path(str(path) + ".backup")
        shutil.copy2(path, backup)
        print("  [OK] Backup: {}".format(backup.name))
        return True
    return False


def generate_config_toml(base_url):
    """Generate config.toml content using official format"""
    # Ensure /v1 suffix for most providers
    if not base_url.endswith("/v1") and not base_url.endswith("/v1/"):
        # Only add /v1 if it looks like an API endpoint (not localhost without port)
        base_url = base_url.rstrip("/") + "/v1"
    
    content = '''model = "gpt-4o"
model_provider = "{provider}"

[model_providers.{provider}]
name = "Custom Provider"
base_url = "{url}"
wire_api = "responses"
requires_openai_auth = true
'''.format(provider=PROVIDER_NAME, url=base_url)
    
    return content


def write_config_toml(content):
    """Write config.toml to disk"""
    get_codex_dir().mkdir(parents=True, exist_ok=True)
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def read_auth():
    """Read auth.json"""
    path = get_auth_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def write_auth(api_key):
    """Write API key to auth.json"""
    get_codex_dir().mkdir(parents=True, exist_ok=True)
    path = get_auth_path()
    auth = read_auth()
    auth["OPENAI_API_KEY"] = api_key
    with open(path, "w", encoding="utf-8") as f:
        json.dump(auth, f, indent=2, ensure_ascii=False)
    return path


def validate_inputs(url, key):
    """Validate and fix user inputs"""
    if not key or not key.strip():
        print("[ERROR] API Key is required")
        return None
    if not url or not url.strip():
        print("[ERROR] URL is required")
        return None
    
    key = key.strip()
    url = url.strip()
    
    # Auto-add protocol
    if not url.startswith(("http://", "https://")):
        print("[INFO] Auto-added https://")
        url = "https://" + url
    
    url = url.rstrip("/")
    
    return url, key


def pause(msg="\nPress Enter to exit..."):
    try:
        input(msg)
    except (KeyboardInterrupt, EOFError):
        pass


def setup(url, key):
    """Main setup flow"""
    print("")
    print("=" * 60)
    print("  Codex CLI Third-Party API Config Tool v{}".format(SCRIPT_VERSION))
    print("=" * 60)
    print("")
    
    # Get inputs
    if url:
        base_url = url
        print("URL: {}".format(base_url))
    else:
        base_url = input("Enter API Base URL (例: azapi.com.cn): ").strip()
    
    if key:
        api_key = key
        masked = "****" + key[-4:] if len(key) > 4 else "****"
        print("Key: {}".format(masked))
    else:
        api_key = input("Enter API Key: ").strip()
    
    # Validate
    result = validate_inputs(base_url, api_key)
    if not result:
        pause("\nPress Enter to exit...")
        sys.exit(1)
    base_url, api_key = result
    
    print("")
    print("-" * 50)
    print("Writing configuration...")
    
    # Backup old files
    backup_file(get_config_path())
    backup_file(get_auth_path())
    
    # 1. Write config.toml
    try:
        toml_content = generate_config_toml(base_url)
        config_path = write_config_toml(toml_content)
        print("  [OK] config.toml: {}".format(config_path))
    except Exception as e:
        print("  [FAIL] config.toml: {}".format(e))
        pause("\nPress Enter to exit...")
        sys.exit(1)
    
    # 2. Write auth.json
    try:
        auth_path = write_auth(api_key)
        print("  [OK] auth.json:   {}".format(auth_path))
    except Exception as e:
        print("  [FAIL] auth.json: {}".format(e))
    
    # 3. Set env var for current session
    os.environ["OPENAI_API_KEY"] = api_key
    print("  [OK] Environment variable set")
    
    # Show result
    masked_key = "****" + api_key[-4:] if len(api_key) > 4 else "****"
    
    print("")
    print("=" * 60)
    print("  Configuration Complete!")
    print("=" * 60)
    print("")
    print("Summary:")
    print("  Base URL: {}".format(base_url))
    print("  API Key:  {}".format(masked_key))
    print("")
    print("Config files:")
    print("  {}".format(get_config_path()))
    print("  {}".format(get_auth_path()))
    print("")
    
    # Show generated config.toml content
    print("Generated config.toml:")
    print("-" * 40)
    print(toml_content)
    print("-" * 40)
    
    print("Test commands:")
    print("  codex --version")
    print("  codex")
    print("")


def show():
    """Show current configuration"""
    print("")
    print("Config dir: {}".format(get_codex_dir()))
    print("")
    
    # Show config.toml
    print("--- config.toml ---")
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print("Read error: {}".format(e))
    else:
        print("(not found)")
    
    print("")
    
    # Show auth.json (masked)
    print("--- auth.json ---")
    auth_path = get_auth_path()
    if auth_path.exists():
        try:
            auth = read_auth()
            masked = {}
            for k, v in auth.items():
                s = str(v)
                masked[k] = "****" + s[-4:] if len(s) > 4 else "****"
            print(json.dumps(masked, indent=2))
        except Exception as e:
            print("Read error: {}".format(e))
    else:
        print("(not found)")
    print("")


def clear():
    """Clear all configuration"""
    print("")
    
    # Remove config.toml
    config_path = get_config_path()
    if config_path.exists():
        backup_file(config_path)
        config_path.unlink()
        print("[OK] Removed config.toml")
    
    # Remove auth.json
    auth_path = get_auth_path()
    if auth_path.exists():
        backup_file(auth_path)
        auth_path.unlink()
        print("[OK] Removed auth.json")
    
    # Unset env var
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    print("")
    print("All configuration cleared.")
    print("")


def main():
    parser = argparse.ArgumentParser(
        description="Codex CLI Third-Party API Config Tool",
    )
    parser.add_argument("-u", "--url", help="API Base URL (without https://)")
    parser.add_argument("-k", "--key", help="API Key")
    parser.add_argument("--show", action="store_true", help="Show current config")
    parser.add_argument("--clear", action="store_true", help="Clear all config")
    parser.add_argument("--version", action="version", version="v{}".format(SCRIPT_VERSION))
    
    args = parser.parse_args()
    
    interactive = not (args.show or args.clear or args.url or args.key)
    
    try:
        if args.show:
            show()
        elif args.clear:
            clear()
        else:
            setup(url=args.url, key=args.key)
    except KeyboardInterrupt:
        print("\n\nCancelled")
    except Exception as e:
        print("\n[ERROR] {}".format(e))
        import traceback
        traceback.print_exc()
        if interactive:
            pause("\nPress Enter to exit...")
        sys.exit(1)
    
    if interactive:
        pause("\nDone! Press Enter to exit...")


if __name__ == "__main__":
    main()
