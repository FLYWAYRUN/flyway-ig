# -*- coding: utf-8 -*-
"""Token helper for Instagram API with Instagram Login (graph.instagram.com).

  python3 auth.py long   <SHORT_LIVED_TOKEN>   # 1h token -> 60-day token
  python3 auth.py refresh <LONG_LIVED_TOKEN>   # extend another 60 days
  python3 auth.py me      <TOKEN>              # print your IG user id
"""
import sys, json, urllib.parse, urllib.request, os

HOST = 'https://graph.instagram.com'

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())

def long_lived(short):
    secret = os.environ.get('IG_APP_SECRET')
    if not secret:
        sys.exit('set IG_APP_SECRET first\n  = Instagram > API setup with Instagram login > Instagram app secret\n  (NOT the Facebook app secret under App settings > Basic)')
    q = urllib.parse.urlencode({'grant_type':'ig_exchange_token',
                                'client_secret':secret, 'access_token':short})
    return get(f'{HOST}/access_token?{q}')

def refresh(long):
    q = urllib.parse.urlencode({'grant_type':'ig_refresh_token','access_token':long})
    return get(f'{HOST}/refresh_access_token?{q}')

def me(token):
    q = urllib.parse.urlencode({'fields':'user_id,username','access_token':token})
    return get(f'{HOST}/me?{q}')

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    cmd, tok = sys.argv[1], sys.argv[2]
    print(json.dumps({'long':long_lived,'refresh':refresh,'me':me}[cmd](tok), indent=2))
