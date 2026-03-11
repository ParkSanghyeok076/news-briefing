---
name: news-briefing
description: Use when user says "뉴스 브리핑" to display an interactive menu for fetching Korean and English AI/tech/HR news from 9 curated sources and generating briefings in Korean across 3 categories (종합뉴스, AI, HR)
allowed-tools:
  - Bash
  - Read
  - Write
---

# 뉴스 브리핑 스킬

## 개요

9개 한국어/영어 AI·테크 뉴스 소스에서 뉴스를 수집해 **한국어** 브리핑을 생성합니다.

**4단계 공통 워크플로:**
1. **수집** — `python3 scripts/fetch_news.py --source <소스>` 로 JSON 데이터 수집
2. **생성** — 카테고리 지침(`instructions/`)에 따라 마크다운 보고서 작성
3. **저장** — `report/YYYY-MM-DD-category.md` 파일로 저장 (Write 툴 사용)
4. **GitHub push** — 아래 명령으로 자동 push

```bash
cd ~/.claude/skills/news-briefing
git add report/
git commit -m "report: YYYY-MM-DD category 브리핑"
git push origin main
```

## 트리거

사용자가 **"뉴스 브리핑"** 이라고 하면 `templates.md` 의 대화형 메뉴를 표시합니다.

## 소스 목록 (21개)

### 내가 지정한 한국어/영어 소스 (9개)
| 소스 키 | 이름 | 언어 | 카테고리 |
|---------|------|------|----------|
| `ai_news` | AI News | 영어 | AI, 종합 |
| `miilk_ai` | 더밀크 AI | 한국어 | AI, 종합 |
| `aitimes_kr` | AI타임스(한국) | 한국어 | AI, HR, 종합 |
| `aitimes_com` | AI Times | 영어 | AI, HR, 종합 |
| `geek_news` | GeekNews/긱뉴스 | 한국어 | 종합 |
| `ttimes` | T타임스 | 한국어 | HR, 종합 |
| `mk_ai` | 매일경제 AI | 한국어 | AI, HR, 종합 |
| `tech_review` | MIT Technology Review | 영어 | AI, HR, 종합 |
| `ai_magazine` | AI Magazine | 영어 | AI, HR, 종합 |

### 원본 AI 뉴스레터 소스 (10개)
| 소스 키 | 이름 | 언어 | 카테고리 |
|---------|------|------|----------|
| `hackernews` | Hacker News | 영어 | AI, 종합 |
| `huggingface` | HuggingFace Papers | 영어 | AI, 종합 |
| `bensbites` | Ben's Bites | 영어 | AI, HR, 종합 |
| `latentspace` | Latent Space | 영어 | AI, 종합 |
| `interconnects` | Interconnects | 영어 | AI, 종합 |
| `oneusefulthing` | One Useful Thing | 영어 | AI, HR, 종합 |
| `chinai` | ChinAI Newsletter | 영어 | AI, 종합 |
| `memia` | Memia | 영어 | AI, 종합 |
| `ai2roi` | AI to ROI | 영어 | AI, HR, 종합 |
| `kdnuggets` | KDnuggets | 영어 | AI, 종합 |

## 브리핑 카테고리

| 카테고리 | 지침 파일 |
|----------|-----------|
| 종합뉴스 (general) | `instructions/briefing_general.md` |
| AI | `instructions/briefing_ai.md` |
| HR | `instructions/briefing_hr.md` |

## 스크립트 실행 위치

스킬 디렉토리 기준으로 실행:
```bash
cd ~/.claude/skills/news-briefing
python3 scripts/fetch_news.py --source general
```

## 보고서 파일명 규칙

`report/YYYY-MM-DD-<category>.md`

예시:
- `report/2026-03-11-ai.md`
- `report/2026-03-11-general.md`
- `report/2026-03-11-hr.md`

## GitHub

- **저장소**: https://github.com/ParkSanghyeok076/news-briefing
- **브리핑 생성 후 항상 push** — `report/` 폴더에 저장된 .md 파일을 자동 commit·push
- **스킬 파일 변경 시**: 변경사항도 commit·push

## 규칙

- **출력 언어**: 한국어 (영어 기사도 한국어로 요약)
- **데이터 진실성**: 수집된 JSON 데이터만 사용, 기사 조작·생성 금지
- **시간 필드**: 필수 포함
- **결과 부족 시**: 5개 미만이면 범위 넓혀 재수집 후 ⚠️ 표시
