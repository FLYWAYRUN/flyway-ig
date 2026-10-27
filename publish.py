# -*- coding: utf-8 -*-
"""Publish anything in schedule.json whose time has come.

env:
  IG_USER_ID        numeric id from `python3 auth.py me <token>`
  IG_ACCESS_TOKEN   long-lived token
  ASSET_BASE_URL    e.g. https://<user>.github.io/flyway-ig
  DRY_RUN           set to 1 to print what would post and stop
"""
import os, json, time, datetime, urllib.parse, urllib.request, urllib.error

HOST  = 'https://graph.instagram.com'
HERE  = os.path.dirname(os.path.abspath(__file__))
SCHED = os.path.join(HERE, 'schedule.json')
KST   = datetime.timezone(datetime.timedelta(hours=9))

UID    = os.environ.get('IG_USER_ID', '') or 'me'
TOKEN  = os.environ.get('IG_ACCESS_TOKEN', '')
BASE   = os.environ.get('ASSET_BASE_URL', '').rstrip('/')
DRY    = os.environ.get('DRY_RUN') == '1'

def _call(path, params):
    data = urllib.parse.urlencode(params).encode()
    req  = urllib.request.Request(f'{HOST}/{path}', data=data, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

def post(suffix, params):
    """POST /{uid}/{suffix}. Falls back to /me/{suffix} if the id is rejected,
    so a wrong IG_USER_ID does not cost you a failed run."""
    try:
        return _call(f'{UID}/{suffix}', params)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        retryable = e.code in (400, 404) and (
            'does not exist' in body or 'Unsupported' in body or 'nonexisting' in body)
        if not retryable:
            raise SystemExit(f'API error {e.code}: {body[:500]}')
        print(f'   id {UID} rejected, retrying as /me/')
        try:
            return _call(f'me/{suffix}', params)
        except urllib.error.HTTPError as e2:
            raise SystemExit(f'API error {e2.code}: {e2.read().decode()[:500]}')

def due(row, now):
    if row['status'] != 'ready' or not row['when']:
        return False
    t = datetime.datetime.strptime(row['when'], '%Y-%m-%d %H:%M').replace(tzinfo=KST)
    return t <= now

def main():
    rows = json.load(open(SCHED, encoding='utf-8'))
    now  = datetime.datetime.now(KST)
    todo = [r for r in rows if due(r, now)]
    if not todo:
        print('nothing due at', now.strftime('%Y-%m-%d %H:%M KST')); return
    if not DRY and not (UID and TOKEN and BASE):
        raise SystemExit('missing IG_USER_ID / IG_ACCESS_TOKEN / ASSET_BASE_URL')

    for r in todo:
        img = f"{BASE}/img/{r['id']}.png"
        print(f"→ {r['id']}  {r['when']}  {img}")
        if DRY:
            print('   [dry run]'); continue
        c = post(f'{UID}/media', {'image_url': img, 'caption': r['caption'],
                                  'access_token': TOKEN})
        time.sleep(5)                       # let Meta fetch and process the image
        p = post(f'{UID}/media_publish', {'creation_id': c['id'], 'access_token': TOKEN})
        r['status'], r['media_id'] = 'posted', p.get('id','')
        print('   published', p.get('id'))
        json.dump(rows, open(SCHED,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
        time.sleep(3)
    print('done:', len(todo), 'post(s)')

if __name__ == '__main__':
    main()
