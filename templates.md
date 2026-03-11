# 📰 뉴스 브리핑 메뉴

사용자가 **"뉴스 브리핑"** 이라고 하면 아래 메뉴를 표시하세요.

---

## 표시할 메뉴

```
📰 뉴스 브리핑 메뉴
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☕ 일일 브리핑
  1. 종합뉴스    전체 소스 모아보기
  2. AI 브리핑   AI 전문 소스 심층 분석
  3. HR 브리핑   AI·직장 변화 관련 소스

📡 내가 지정한 한국어/영어 소스
  4. AI News               (영어)
  5. 더밀크 AI             (한국어)
  6. AI타임스 kr           (한국어)
  7. AI Times              (영어)
  8. GeekNews / 긱뉴스     (한국어)
  9. T타임스               (한국어)
 10. 매일경제 AI           (한국어)
 11. MIT Technology Review (영어)
 12. AI Magazine           (영어)

📧 AI 뉴스레터 (원본 소스)
 13. Hacker News           (영어)
 14. HuggingFace Papers    (영어)
 15. Ben's Bites           (영어)
 16. Latent Space          (영어)
 17. Interconnects         (영어)
 18. One Useful Thing      (영어)
 19. ChinAI Newsletter     (영어)
 20. Memia                 (영어)
 21. AI to ROI             (영어)
 22. KDnuggets             (영어)

🔍 키워드 검색
 23. 전체 소스에서 키워드 검색
 24. AI 소스에서 키워드 검색
 25. HR 소스에서 키워드 검색

📅 날짜 지정 (선택사항)
  번호 선택 후 날짜 범위를 추가할 수 있습니다:
  • 오늘만        → "--days 1" 추가
  • 최근 3일      → "--days 3" 추가
  • 최근 1주일    → "--days 7" 추가
  • 날짜 직접 지정 → "--date-from 2026-03-01 --date-to 2026-03-11"

번호를 입력하거나, 소스를 쉼표로 조합하세요
예: "2 오늘만" / "13,15,17" / "AI 에이전트" / "3 이번 주"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 날짜 지정 처리 방법

| 사용자 입력 | 날짜 플래그 |
|------------|-----------|
| "오늘만", "오늘 기사", "today" | `--days 1` |
| "이번 주", "최근 1주일", "this week" | `--days 7` |
| "최근 3일", "3일치" | `--days 3` |
| "2026-03-01부터" | `--date-from 2026-03-01` |
| "2026-03-01 ~ 2026-03-05" | `--date-from 2026-03-01 --date-to 2026-03-05` |

---

## 명령어 매핑

| 번호 | fetch 명령어 | 브리핑 지침 |
|------|-------------|------------|
| 1 | `python3 scripts/fetch_news.py --source general [날짜]` | `instructions/briefing_general.md` |
| 2 | `python3 scripts/fetch_news.py --source ai [날짜]` | `instructions/briefing_ai.md` |
| 3 | `python3 scripts/fetch_news.py --source hr [날짜]` | `instructions/briefing_hr.md` |
| 4 | `python3 scripts/fetch_news.py --source ai_news --no-save [날짜]` | 단순 목록 |
| 5 | `python3 scripts/fetch_news.py --source miilk_ai --no-save [날짜]` | 단순 목록 |
| 6 | `python3 scripts/fetch_news.py --source aitimes_kr --no-save [날짜]` | 단순 목록 |
| 7 | `python3 scripts/fetch_news.py --source aitimes_com --no-save [날짜]` | 단순 목록 |
| 8 | `python3 scripts/fetch_news.py --source geek_news --no-save [날짜]` | 단순 목록 |
| 9 | `python3 scripts/fetch_news.py --source ttimes --no-save [날짜]` | 단순 목록 |
| 10 | `python3 scripts/fetch_news.py --source mk_ai --no-save [날짜]` | 단순 목록 |
| 11 | `python3 scripts/fetch_news.py --source tech_review --no-save [날짜]` | 단순 목록 |
| 12 | `python3 scripts/fetch_news.py --source ai_magazine --no-save [날짜]` | 단순 목록 |
| 13 | `python3 scripts/fetch_news.py --source hackernews --no-save [날짜]` | 단순 목록 |
| 14 | `python3 scripts/fetch_news.py --source huggingface --no-save [날짜]` | 단순 목록 |
| 15 | `python3 scripts/fetch_news.py --source bensbites --no-save [날짜]` | 단순 목록 |
| 16 | `python3 scripts/fetch_news.py --source latentspace --no-save [날짜]` | 단순 목록 |
| 17 | `python3 scripts/fetch_news.py --source interconnects --no-save [날짜]` | 단순 목록 |
| 18 | `python3 scripts/fetch_news.py --source oneusefulthing --no-save [날짜]` | 단순 목록 |
| 19 | `python3 scripts/fetch_news.py --source chinai --no-save [날짜]` | 단순 목록 |
| 20 | `python3 scripts/fetch_news.py --source memia --no-save [날짜]` | 단순 목록 |
| 21 | `python3 scripts/fetch_news.py --source ai2roi --no-save [날짜]` | 단순 목록 |
| 22 | `python3 scripts/fetch_news.py --source kdnuggets --no-save [날짜]` | 단순 목록 |
| 23 | `python3 scripts/fetch_news.py --source general --keyword "<키워드>" [날짜]` | 단순 목록 |
| 24 | `python3 scripts/fetch_news.py --source ai --keyword "<키워드>" [날짜]` | 단순 목록 |
| 25 | `python3 scripts/fetch_news.py --source hr --keyword "<키워드>" [날짜]` | 단순 목록 |

---

## 실행 위치

```bash
cd ~/.claude/skills/news-briefing
python3 scripts/fetch_news.py --source ai --days 1
```

보고서 저장: `~/.claude/skills/news-briefing/reports/YYYY-MM-DD/`
