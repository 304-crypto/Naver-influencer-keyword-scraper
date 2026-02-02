# Render 배포 가이드

## 🚀 Render로 FastAPI 배포하기

### 1. GitHub에 코드 올리기

먼저 코드를 GitHub에 올려야 합니다:

```bash
cd c:\Users\USER\Desktop\app-test\naver_infl

# Git 초기화 (아직 안 했다면)
git init
git add .
git commit -m "Initial commit"

# GitHub repository 생성 후
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

### 2. Render 계정 생성

1. [Render.com](https://render.com) 접속
2. "Get Started for Free" 클릭
3. GitHub 계정으로 로그인

### 3. 새 Web Service 생성

1. Dashboard에서 **"New +"** 버튼 클릭
2. **"Web Service"** 선택
3. GitHub repository 연결
   - "Connect GitHub" 클릭
   - 방금 올린 repository 선택

### 4. 배포 설정

다음 정보를 입력하세요:

| 항목 | 값 |
|------|-----|
| **Name** | `naver-influencer-api` (원하는 이름) |
| **Region** | `Singapore` (한국과 가까움) |
| **Branch** | `main` |
| **Root Directory** | (비워두기) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn backend.app:app --host 0.0.0.0 --port $PORT` |

### 5. 플랜 선택

- **Free** 플랜 선택 (무료)
  - 750시간/월 무료
  - 15분 비활성 시 슬립 모드
  - 첫 요청 시 콜드 스타트 (느림)

### 6. 배포 시작

- **"Create Web Service"** 클릭
- 자동으로 배포 시작 (3-5분 소요)
- 배포 로그 실시간 확인 가능

### 7. 배포 완료

배포가 완료되면:
- URL: `https://your-app-name.onrender.com`
- API 문서: `https://your-app-name.onrender.com/docs`

## 📡 API 사용 예시

배포 후 이렇게 사용할 수 있습니다:

```bash
# 카테고리 목록
curl https://your-app-name.onrender.com/api/categories

# 키워드 조회
curl "https://your-app-name.onrender.com/api/keywords?categoryId=123"

# 키워드 텍스트
curl "https://your-app-name.onrender.com/api/keywords.txt?categoryId=123&format=tsv"
```

## ⚠️ 주의사항

### Free 플랜 제한사항

1. **슬립 모드**: 15분 비활성 시 자동 슬립
   - 첫 요청 시 30초~1분 소요 (콜드 스타트)
   - 이후 요청은 정상 속도

2. **월 750시간 제한**
   - 24/7 실행 시 한 달에 720시간
   - 충분히 사용 가능

3. **메모리 제한**: 512MB
   - 이 프로젝트는 충분함

### 성능 최적화 팁

**슬립 방지 (선택사항):**
- [UptimeRobot](https://uptimerobot.com) 같은 서비스로 5분마다 핑
- 하지만 750시간 제한 주의

## 🔧 환경 변수 설정 (필요시)

Render Dashboard에서:
1. 배포된 서비스 클릭
2. **"Environment"** 탭
3. 환경 변수 추가 가능

## 📊 배포 상태 확인

- **Logs**: 실시간 로그 확인
- **Metrics**: CPU, 메모리 사용량
- **Events**: 배포 이력

## 🔄 업데이트 방법

코드 수정 후:

```bash
git add .
git commit -m "Update message"
git push
```

Render가 자동으로 재배포합니다! (Auto-Deploy 기본 활성화)

## 💰 비용

- **Free 플랜**: $0/월
- **Starter 플랜**: $7/월 (슬립 없음, 더 빠름)

## 🎯 배포 완료 체크리스트

- [ ] GitHub에 코드 푸시
- [ ] Render 계정 생성
- [ ] Web Service 생성
- [ ] 배포 설정 입력
- [ ] 배포 완료 대기
- [ ] API 테스트 (`/docs` 접속)
- [ ] 실제 API 호출 테스트

---

**문제 발생 시:**
- Render 로그 확인
- `requirements.txt` 확인
- Start Command 확인: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
