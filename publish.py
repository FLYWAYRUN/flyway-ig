# -*- coding: utf-8 -*-
import os, json, time, datetime, urllib.parse, urllib.request, urllib.error

HOST  = 'https://graph.instagram.com'
HERE  = os.path.dirname(os.path.abspath(__file__))
SCHED = os.path.join(HERE, 'schedule.json')
KST   = datetime.timezone(datetime.timedelta(hours=9))

UID   = os.environ.get('IG_USER_ID', '') or 'me'
TOKEN = os.environ.get('IG_ACCESS_TOKEN', '')
BASE  = os.environ.get('ASSET_BASE_URL', '').rstrip('/')
DRY   = os.environ.get('DRY_RUN') == '1'

CANDIDATES = ['v23.0/{u}', '{u}', 'v23.0/me', 'me', 'v21.0/{u}', 'v18.0/{u}']
PATH = None

def _call(path, params):
    data = urllib.parse.urlencode(params).encode()
    req  = urllib.request.Request(f'{HOST}/{path}', data=data, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

def post(suffix, params):
    global PATH
    if PATH:
        try:
            return _call(f'{PATH}/{suffix}', params)
        except urllib.error.HTTPError as e:
            raise SystemExit(f'API error {e.code}: {e.read().decode()[:400]}')
    errs = []
    for cand in CANDIDATES:
        base = cand.format(u=UID)
        try:
            out = _call(f'{base}/{suffix}', params)
            PATH = base
            print(f'   path OK -> {base}/')
            return out
        except urllib.error.HTTPError as e:
            errs.append(f'     {base:16} {e.code}  {e.read().decode()[:150]}')
    raise SystemExit('every path shape failed:\n' + '\n'.join(errs))

def due(row, now):
    if row.get('status') != 'ready' or not row.get('when'):
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
        c = post('media', {'image_url': img, 'caption': r['caption'],
                           'access_token': TOKEN})
        time.sleep(5)
        p = post('media_publish', {'creation_id': c['id'], 'access_token': TOKEN})
        r['status'], r['media_id'] = 'posted', p.get('id', '')
        print('   published', p.get('id'))
        json.dump(rows, open(SCHED, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        time.sleep(3)
    print('done:', len(todo), 'post(s)')

if __name__ == '__main__':
    main()
