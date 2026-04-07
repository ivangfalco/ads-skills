#!/usr/bin/env python3
"""
Meta Ad Scheduler - Automatically pause ads at scheduled times.

Use case: Webinar ads that need to be paused at a specific date/time
without touching other ads in the same ad set.

Commands:
    add   - Schedule an ad to be paused at a specific time
    list  - Show all scheduled pauses (pending + completed)
    run   - Execute pending pauses (called by cron every 12h)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_VERSION = 'v22.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'
CONFIG_FILE = Path(__file__).parent / 'scheduled_pauses.json'


def load_config():
    """Load scheduled pauses from JSON config."""
    if not CONFIG_FILE.exists():
        return []
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(entries):
    """Save scheduled pauses to JSON config."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(entries, f, indent=2)


def pause_ad(ad_id, token):
    """Pause a single ad via Meta API. Returns (success, message)."""
    url = f'{BASE_URL}/{ad_id}'
    resp = requests.post(url, data={
        'status': 'PAUSED',
        'access_token': token,
    })
    data = resp.json()

    if 'error' in data:
        return False, data['error'].get('message', str(data['error']))

    if data.get('success'):
        return True, 'Paused successfully'

    return False, f'Unexpected response: {data}'


def cmd_add(args):
    """Schedule an ad to be paused at a specific time."""
    try:
        pause_at = datetime.strptime(args.pause_at, '%Y-%m-%d %H:%M')
    except ValueError:
        print('Error: --pause-at must be in format "YYYY-MM-DD HH:MM"')
        sys.exit(1)

    entries = load_config()

    for entry in entries:
        if entry['ad_id'] == args.ad_id and entry['status'] == 'pending':
            print(f'Warning: Ad {args.ad_id} already has a pending pause scheduled for {entry["pause_at"]}')
            print('Skipping. Remove the existing entry first if you want to reschedule.')
            return

    entry = {
        'ad_id': args.ad_id,
        'name': args.name,
        'pause_at': pause_at.isoformat(),
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'paused_at': None,
    }

    entries.append(entry)
    save_config(entries)

    print(f'Scheduled pause:')
    print(f'  Ad ID:    {args.ad_id}')
    print(f'  Name:     {args.name}')
    print(f'  Pause at: {pause_at.strftime("%Y-%m-%d %H:%M")}')


def cmd_list(args):
    """List all scheduled pauses."""
    entries = load_config()

    if not entries:
        print('No scheduled pauses.')
        return

    pending = [e for e in entries if e['status'] == 'pending']
    done = [e for e in entries if e['status'] == 'done']
    failed = [e for e in entries if e['status'] == 'failed']

    if pending:
        print(f'PENDING ({len(pending)}):')
        for e in pending:
            print(f'  - {e["name"]} (ID: {e["ad_id"]}) - pauses at {e["pause_at"]}')
        print()

    if done:
        print(f'COMPLETED ({len(done)}):')
        for e in done:
            print(f'  - {e["name"]} (ID: {e["ad_id"]}) - paused at {e["paused_at"]}')
        print()

    if failed:
        print(f'FAILED ({len(failed)}):')
        for e in failed:
            print(f'  - {e["name"]} (ID: {e["ad_id"]}) - error: {e.get("error", "unknown")}')
        print()


def cmd_run(args):
    """Execute pending pauses due within the next 12 hours (or already past)."""
    token = os.getenv('META_ACCESS_TOKEN')
    if not token:
        print('Error: META_ACCESS_TOKEN not found in .env')
        sys.exit(1)

    entries = load_config()
    now = datetime.now()
    lookahead = now + timedelta(hours=12)
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    pending = [e for e in entries if e['status'] == 'pending']
    if not pending:
        print(f'[{timestamp}] No pending pauses.')
        return

    due = [e for e in pending if datetime.fromisoformat(e['pause_at']) <= lookahead]
    if not due:
        print(f'[{timestamp}] {len(pending)} pending, none due within next 12h.')
        return

    print(f'[{timestamp}] {len(due)} ad(s) due for pausing (now through {lookahead.strftime("%Y-%m-%d %H:%M")}):')

    for entry in due:
        ad_id = entry['ad_id']
        name = entry['name']

        success, message = pause_ad(ad_id, token)

        if success:
            entry['status'] = 'done'
            entry['paused_at'] = now.isoformat()
            print(f'  OK: {name} (ID: {ad_id}) - paused')
        else:
            entry['status'] = 'failed'
            entry['error'] = message
            entry['failed_at'] = now.isoformat()
            print(f'  FAIL: {name} (ID: {ad_id}) - {message}')

    save_config(entries)
    print(f'Done. Updated {len(due)} entries.')


def main():
    parser = argparse.ArgumentParser(
        description='Meta Ad Scheduler - pause ads at scheduled times'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add', help='Schedule an ad to be paused')
    add_parser.add_argument('--ad-id', required=True, help='Meta ad ID')
    add_parser.add_argument('--pause-at', required=True, help='When to pause (YYYY-MM-DD HH:MM)')
    add_parser.add_argument('--name', required=True, help='Ad name (for display/logging)')

    subparsers.add_parser('list', help='List all scheduled pauses')
    subparsers.add_parser('run', help='Execute pending pauses (for cron)')

    args = parser.parse_args()

    if args.command == 'add':
        cmd_add(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'run':
        cmd_run(args)


if __name__ == '__main__':
    main()
