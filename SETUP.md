# FLYWAY · 인스타 자동화 세팅

브라우저만으로 끝난다. 터미널은 안 써도 된다.

---

# A. 토큰 받기

## A-1. 계정 연결

좌측 메뉴 **Instagram → API setup with Instagram login**
→ `1. 액세스 토큰 생성` 의 **계정 추가** 클릭
→ 팝업에서 @flyway.run 로그인 → 권한 승인

**확인:** 그 자리에 @flyway.run이 목록으로 뜬다.

## A-2. Instagram 앱 시크릿 복사

같은 화면 중단 `Instagram 앱 시크릿 코드` → **표시** → 복사.

> App settings → Basic 의 시크릿이 **아니다.** 그건 페이스북 로그인용.

## A-3. 단기 토큰 복사

A-1에서 계정이 붙으면 그 줄에 **액세스 토큰 생성**(또는 Generate token) 버튼이 생긴다.
눌러서 나온 토큰 복사. 유효기간 1시간이라 바로 A-4로 간다.

## A-4. 60일 토큰으로 교환

아래 주소의 대괄호 두 개를 바꿔서 **브라우저 주소창에 붙여넣기**.

```
https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=[A-2시크릿]&access_token=[A-3단기토큰]
```

**확인:** 이런 JSON이 보인다.
```json
{"access_token":"IGAAR...","token_type":"bearer","expires_in":5183944}
```
`access_token` 값을 복사해둔다. **이게 60일짜리고 앞으로 계속 쓴다.**

## A-5. user_id 확인

```
https://graph.instagram.com/me?fields=user_id,username&access_token=[A-4의60일토큰]
```

**확인:**
```json
{"user_id":"17841400000000000","username":"flyway.run"}
```
`user_id` 복사. 17841로 시작하는 긴 숫자다.

> 끝나면 브라우저 방문기록에서 이 두 줄 지워라. 시크릿이 들어 있다.

**A 완료 시점에 손에 있어야 할 것 2개**
- 60일 액세스 토큰
- user_id

---

# B. 이미지 호스팅 (GitHub)

인스타 API는 파일 업로드를 안 받는다. 공개 URL에서 이미지를 가져간다.
그래서 이미지를 올려둘 곳이 필요하고, GitHub Pages가 공짜다.

## B-1. 계정
github.com 가입 또는 로그인.

## B-2. 레포 생성
우측 상단 **+ → New repository**
- Repository name: `flyway-ig`
- **Public** 선택 (중요. Private면 이미지를 못 가져간다)
- **Create repository**

## B-3. 파일 올리기
**uploading an existing file** 링크 클릭.

zip을 풀면 `flyway` 폴더가 나온다.
**그 폴더를 통째로 끌지 말고, 폴더 안의 내용물을 전부 선택해서** 드래그한다.

```
O  content.py, tpl.py, docs, .github ...   ← 내용물
X  flyway/                                  ← 폴더째
```

**Commit changes** 클릭.

**확인:** 레포 최상단에 `content.py`, `docs`, `README.md`가 보인다.

## B-4. Actions 권한
**Settings → Actions → General** → 맨 아래 `Workflow permissions`
→ **Read and write permissions** 선택 → Save.

## B-5. Pages 켜기
**Settings → Pages**
- Source: `Deploy from a branch`
- Branch: `main` / 폴더 `/docs`
- **Save**

## B-6. 확인
1~2분 뒤 접속.
```
https://[깃허브아이디].github.io/flyway-ig/
```
**확인:** 12장이 격자로 보인다. 안 보이면 더 기다렸다 새로고침.

이 주소를 복사해둔다. **끝에 슬래시 없이.**

---

# C. 연결

**Settings → Secrets and variables → Actions**

## C-1. Secrets 탭
**New repository secret** 두 번.

| Name | Secret |
|---|---|
| `IG_USER_ID` | A-5의 user_id |
| `IG_ACCESS_TOKEN` | A-4의 60일 토큰 |

## C-2. Variables 탭
**New repository variable** 한 번.

| Name | Value |
|---|---|
| `ASSET_BASE_URL` | `https://[아이디].github.io/flyway-ig` |

---

# D. 첫 발행

## D-1. 빈 테스트
**Actions 탭 → publish → Run workflow** → `dry run` **체크** → 실행.

로그에 `nothing due` 가 나오면 정상이다. 예약된 게 아직 없다.

## D-2. 1번 포스트 예약
레포에서 `schedule.json` 열고 연필 아이콘 클릭.
첫 줄을 이렇게 고친다. 시각은 한국 시간, 지금보다 **몇 분 뒤**로.

```json
{
  "id": "01",
  "when": "2026-10-27 21:00",
  "status": "ready",
```

**Commit changes.**

## D-3. 발행
**Actions → publish → Run workflow** → dry run **체크 해제** → 실행.

**확인:** 로그에 `published` 와 숫자 id가 찍히고, @flyway.run에 1번 포스트가 올라와 있다.

이후로는 매시 정각에 자동으로 돌면서 때가 된 `ready` 건을 올린다.

---

# E. 운영

## 나머지 11장 예약
`schedule.json`에서 각 줄의 `when`에 시각, `status`를 `ready`로.
화/금 저녁 7시 같은 식으로 깔아두면 된다.

| status | 뜻 |
|---|---|
| `draft` | 대기. 안 올라감 |
| `ready` | 예약됨 |
| `posted` | 발행 완료 |

## 새 포스트
`content.py`에 dict 하나 추가 → commit
→ `render` 워크플로가 PNG를 만들고 `schedule.json`에 줄을 추가한다
→ `when` + `ready` 지정

## 토큰 갱신 (50일마다)
```
https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=[현재토큰]
```
나온 새 토큰을 `IG_ACCESS_TOKEN` Secret에 덮어쓴다. 캘린더에 알림 걸어둬라.

---

# 제약

| 항목 | 수치 |
|---|---|
| 24시간 발행 한도 | 50~100건 |
| 이미지 | 공개 URL 필수 |
| 토큰 수명 | 60일, 갱신 가능 |
| 앱 모드 | **개발 그대로.** 라이브 전환 불필요 |
| 자동화 금지 | 댓글·DM·팔로우 |
