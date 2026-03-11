# 뉴스 브리핑 스킬 - 작업 이력

## 프로젝트 개요

**목적**: AI/테크/HR 분야 한국어·영어 뉴스를 자동 수집·요약하는 Claude Code 스킬

**GitHub**: https://github.com/ParkSanghyeok076/news-briefing

**원본 참조**: https://github.com/cclank/news-aggregator-skill (MIT License)

**트리거**: Claude Code에서 `뉴스 브리핑` 입력 → 대화형 메뉴 표시

---

## 기획 의도

1. **한국어 출력**: 원본 스킬이 간체중국어 출력 → 한국어로 전환
2. **소스 현지화**: 중국 소스 제거, 한국어/영어 AI 특화 소스로 교체
3. **직접 지정 소스 추가**: AI타임스, 더밀크, 긱뉴스 등 한국 독자적 소스 통합
4. **원본 AI 뉴스레터 유지**: Ben's Bites, Latent Space, HuggingFace Papers 등 유지
5. **날짜 필터**: 오늘/이번 주/기간 지정 필터 추가
6. **GitHub 연동**: 생성된 브리핑 리포트를 `report/` 폴더에 자동 push

---

## 소스 구성 (19개)

### 직접 지정 한국어/영어 소스 (9개)

| 소스 키 | 사이트 | 언어 |
|---------|--------|------|
| `ai_news` | artificialintelligence-news.com | 영어 |
| `miilk_ai` | themiilk.com/topics/ai | 한국어 |
| `aitimes_kr` | aitimes.kr | 한국어 |
| `aitimes_com` | aitimes.com | 영어 |
| `geek_news` | news.hada.io (긱뉴스) | 한국어 |
| `ttimes` | ttimes.co.kr (T타임스) | 한국어 |
| `mk_ai` | mk.co.kr/news/it/ai | 한국어 |
| `tech_review` | technologyreview.com | 영어 |
| `ai_magazine` | aimagazine.com | 영어 |

### 원본 AI 뉴스레터 소스 (10개)

| 소스 키 | 사이트 | 언어 |
|---------|--------|------|
| `hackernews` | news.ycombinator.com | 영어 |
| `huggingface` | huggingface.co/papers | 영어 |
| `bensbites` | bensbites.com | 영어 |
| `latentspace` | latent.space | 영어 |
| `interconnects` | interconnects.ai | 영어 |
| `oneusefulthing` | oneusefulthing.org | 영어 |
| `chinai` | chinai.substack.com | 영어 |
| `memia` | memia.substack.com | 영어 |
| `ai2roi` | ai2roi.substack.com | 영어 |
| `kdnuggets` | kdnuggets.com | 영어 |

---

## 브리핑 카테고리

| 카테고리 | 소스 수 | 지침 파일 |
|----------|--------|-----------|
| 종합뉴스 (general) | 19개 전체 | instructions/briefing_general.md |
| AI | 15개 | instructions/briefing_ai.md |
| HR (AI at workplace) | 9개 | instructions/briefing_hr.md |

---

## 파일 구조

```
news-briefing/
├── SKILL.md                      # Claude Code 스킬 정의 (트리거·워크플로)
├── WORK_LOG.md                   # 이 파일
├── requirements.txt              # Python 의존성
├── templates.md                  # 25개 옵션 대화형 메뉴
├── scripts/
│   ├── fetch_news.py             # 뉴스 수집 메인 스크립트
│   └── rss_parser.py             # RSS/Atom 피드 파서
├── instructions/
│   ├── briefing_general.md       # 종합뉴스 브리핑 지침
│   ├── briefing_ai.md            # AI 브리핑 지침
│   └── briefing_hr.md            # HR 브리핑 지침
└── report/                       # 생성된 브리핑 리포트 (GitHub push)
    └── YYYY-MM-DD-category.md
```

---

## 작업 이력

### 2026-03-11 — 초기 구축

**작업자**: Claude Code (Sonnet 4.6)

**주요 작업:**

1. **원본 스킬 분석**
   - `cclank/news-aggregator-skill` 구조 분석
   - SKILL.md, fetch_news.py, 6개 브리핑 지침 파악
   - 원본: 간체중국어 출력, 중국 소스 위주, `如意如意` 트리거

2. **한국어 버전 재구성**
   - 트리거: `如意如意` → `뉴스 브리핑`
   - 출력 언어: 간체중국어 → 한국어
   - 소스: 중국 위주 28개 → 한국/영어 19개로 재편

3. **날짜 필터 기능 추가**
   - `--days N`: 최근 N일 기사만 (1=오늘, 7=이번주)
   - `--date-from / --date-to`: 날짜 범위 직접 지정
   - RFC 2822 / ISO 8601 날짜 파싱 지원

4. **GitHub 연동 설정**
   - 저장소: ParkSanghyeok076/news-briefing
   - 브리핑 생성 시 `report/` 폴더에 자동 push

---

## 사용법

```bash
# 트리거: Claude Code에서
뉴스 브리핑

# 직접 실행
cd ~/.claude/skills/news-briefing
python3 scripts/fetch_news.py --source ai --days 1
python3 scripts/fetch_news.py --source hr --days 7
python3 scripts/fetch_news.py --list-sources
```
