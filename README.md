# FLYWAY

인스타 콘텐츠 생성 + 발행 자동화. 세팅은 `SETUP.md`.

```bash
pip install playwright && playwright install chromium
python3 render.py                      # content.py -> docs/img/*.png
DRY_RUN=1 python3 publish.py           # 뭐가 나갈지 확인만
python3 publish.py                     # 실제 발행
```

| 파일 | 역할 |
|---|---|
| `content.py` | 포스트 데이터. **여기만 고치면 된다** |
| `svgs.py` | 코스 지도·고도 그래픽 |
| `tpl.py` | 템플릿 4종 statement / stat / compare / route |
| `fonts.css` | Anton + Bebas 임베드 |
| `render.py` | HTML → PNG 1080×1350 |
| `schedule.json` | 발행 캘린더 |
| `publish.py` | Instagram Graph API 발행 |
| `auth.py` | 토큰 교환·갱신 |
| `docs/` | GitHub Pages. 이미지 공개 URL |
