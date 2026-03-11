#!/usr/bin/env python3
"""
뉴스 브리핑 수집기 - 9개 한국어/영어 소스 지원
사용법: python3 fetch_news.py --source <소스키|카테고리> [옵션]
"""
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# rss_parser.py 경로 설정
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from rss_parser import fetch_rss_feed

# ============================================================
# 소스 정의
# ============================================================
SOURCES = {
    "ai_news": {
        "name": "AI News",
        "url": "https://www.artificialintelligence-news.com",
        "rss": "https://www.artificialintelligence-news.com/feed/",
        "lang": "en",
        "category": ["ai", "general"],
    },
    "miilk_ai": {
        "name": "더밀크 AI",
        "url": "https://www.themiilk.com/topics/ai",
        "rss": "https://www.themiilk.com/feed",
        "lang": "ko",
        "category": ["ai", "general"],
    },
    "aitimes_kr": {
        "name": "AI타임스(한국)",
        "url": "https://www.aitimes.kr",
        "rss": "https://www.aitimes.kr/rss/allArticle.xml",
        "lang": "ko",
        "category": ["ai", "hr", "general"],
    },
    "aitimes_com": {
        "name": "AI Times",
        "url": "https://www.aitimes.com",
        "rss": "https://www.aitimes.com/rss/",
        "lang": "en",
        "category": ["ai", "hr", "general"],
    },
    "geek_news": {
        "name": "GeekNews(긱뉴스)",
        "url": "https://news.hada.io",
        "rss": "https://news.hada.io/rss",
        "lang": "ko",
        "category": ["general"],
    },
    "ttimes": {
        "name": "T타임스",
        "url": "https://www.ttimes.co.kr",
        "rss": "https://www.ttimes.co.kr/rss/allArticle.xml",
        "lang": "ko",
        "category": ["hr", "general"],
    },
    "mk_ai": {
        "name": "매일경제 AI",
        "url": "https://www.mk.co.kr/news/it/ai",
        "rss": "https://www.mk.co.kr/rss/50200011/",
        "lang": "ko",
        "category": ["ai", "hr", "general"],
    },
    "tech_review": {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com",
        "rss": "https://www.technologyreview.com/feed/",
        "lang": "en",
        "category": ["ai", "hr", "general"],
    },
    "ai_magazine": {
        "name": "AI Magazine",
        "url": "https://aimagazine.com",
        "rss": "https://aimagazine.com/feed/",
        "lang": "en",
        "category": ["ai", "hr", "general"],
    },
    # ── 원본 AI 뉴스레터 소스 ──────────────────────────────────
    "hackernews": {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com",
        "rss": "https://hnrss.org/frontpage",
        "lang": "en",
        "category": ["ai", "general"],
    },
    "huggingface": {
        "name": "HuggingFace Papers",
        "url": "https://huggingface.co/papers",
        "rss": "https://huggingface.co/papers.rss",
        "lang": "en",
        "category": ["ai", "general"],
    },
    "bensbites": {
        "name": "Ben's Bites",
        "url": "https://www.bensbites.com",
        "rss": "https://www.bensbites.com/feed",
        "lang": "en",
        "category": ["ai", "hr", "general"],
    },
    "latentspace": {
        "name": "Latent Space",
        "url": "https://latent.space",
        "rss": "https://latent.space/feed",
        "lang": "en",
        "category": ["ai", "general"],
    },
    "interconnects": {
        "name": "Interconnects",
        "url": "https://www.interconnects.ai",
        "rss": "https://www.interconnects.ai/feed",
        "lang": "en",
        "category": ["ai", "general"],
    },
    "oneusefulthing": {
        "name": "One Useful Thing",
        "url": "https://www.oneusefulthing.org",
        "rss": "https://www.oneusefulthing.org/feed",
        "lang": "en",
        "category": ["ai", "hr", "general"],
    },
    "chinai": {
        "name": "ChinAI Newsletter",
        "url": "https://chinai.substack.com",
        "rss": "https://chinai.substack.com/feed",
        "lang": "en",
        "category": ["ai", "general"],
    },
    "memia": {
        "name": "Memia",
        "url": "https://memia.substack.com",
        "rss": "https://memia.substack.com/feed",
        "lang": "en",
        "category": ["ai", "general"],
    },
    "ai2roi": {
        "name": "AI to ROI",
        "url": "https://ai2roi.substack.com",
        "rss": "https://ai2roi.substack.com/feed",
        "lang": "en",
        "category": ["ai", "hr", "general"],
    },
    "kdnuggets": {
        "name": "KDnuggets",
        "url": "https://www.kdnuggets.com",
        "rss": "https://www.kdnuggets.com/feed",
        "lang": "en",
        "category": ["ai", "general"],
    },
}

# 카테고리 → 소스 매핑
CATEGORY_SOURCES = {
    "general": list(SOURCES.keys()),
    "ai": [
        "ai_news", "miilk_ai", "aitimes_kr", "aitimes_com", "tech_review", "ai_magazine",
        "hackernews", "huggingface", "bensbites", "latentspace",
        "interconnects", "oneusefulthing", "memia", "ai2roi", "kdnuggets",
    ],
    "hr": [
        "aitimes_kr", "aitimes_com", "ttimes", "mk_ai", "ai_magazine", "tech_review",
        "bensbites", "oneusefulthing", "ai2roi",
    ],
}


# ============================================================
# 수집 함수
# ============================================================
def parse_item_date(time_str: str):
    """RSS 날짜 문자열 → timezone-aware datetime (파싱 실패 시 None)"""
    if not time_str:
        return None
    # RFC 2822 (RSS 표준): "Mon, 01 Jan 2024 00:00:00 +0000"
    try:
        return parsedate_to_datetime(time_str)
    except Exception:
        pass
    # ISO 8601
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(time_str[:19], fmt[:len(fmt)])
            return dt.replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


def filter_by_date(items: list, days: int = None,
                   date_from: str = None, date_to: str = None) -> list:
    """날짜 범위로 항목 필터링 (날짜 파싱 불가 항목은 유지)"""
    if not days and not date_from and not date_to:
        return items

    now = datetime.now(tz=timezone.utc)

    if days is not None:
        dt_from = now - timedelta(days=days)
        dt_to = now
    else:
        dt_from = datetime.strptime(date_from, "%Y-%m-%d").replace(tzinfo=timezone.utc) if date_from else None
        dt_to = (datetime.strptime(date_to, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                 + timedelta(days=1)) if date_to else now

    filtered = []
    for item in items:
        dt = parse_item_date(item.get("time", ""))
        if dt is None:
            # 날짜 파싱 불가 → 포함 유지 (⚠️ 표시)
            item["_date_unknown"] = True
            filtered.append(item)
            continue
        in_range = True
        if dt_from and dt < dt_from:
            in_range = False
        if dt_to and dt > dt_to:
            in_range = False
        if in_range:
            filtered.append(item)
    return filtered


def fetch_source(source_key: str, limit: int = 5, keyword: str = None,
                 days: int = None, date_from: str = None, date_to: str = None) -> dict:
    """단일 소스에서 뉴스 수집"""
    source = SOURCES.get(source_key)
    if not source:
        return {"source": source_key, "items": [], "error": "알 수 없는 소스"}

    try:
        # 날짜 필터 적용 시 더 많이 가져온 뒤 필터링
        fetch_limit = limit * 3 if (days or date_from or date_to) else limit * 2
        items = fetch_rss_feed(source["rss"], source["name"], limit=fetch_limit)

        # 날짜 필터링
        if days or date_from or date_to:
            items = filter_by_date(items, days=days, date_from=date_from, date_to=date_to)

        # 키워드 필터링
        if keyword and items:
            kw_list = [k.strip().lower() for k in keyword.split(",")]
            filtered = [
                item for item in items
                if any(kw in f"{item.get('title','')} {item.get('summary','')}".lower()
                       for kw in kw_list)
            ]
            if filtered:
                items = filtered
            else:
                for item in items:
                    item["_keyword_miss"] = True

        return {
            "source": source_key,
            "source_name": source["name"],
            "lang": source["lang"],
            "items": items[:limit],
        }
    except Exception as e:
        return {"source": source_key, "items": [], "error": str(e)}


def fetch_multiple(source_keys: list, limit: int = 5, keyword: str = None,
                   days: int = None, date_from: str = None, date_to: str = None) -> dict:
    """여러 소스 병렬 수집"""
    result = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(fetch_source, key, limit, keyword, days, date_from, date_to): key
            for key in source_keys
        }
        for future in as_completed(futures):
            key = futures[future]
            try:
                result[key] = future.result()
            except Exception as e:
                result[key] = {"source": key, "items": [], "error": str(e)}
    return result


def save_result(data: dict, label: str = "general") -> str:
    """reports/YYYY-MM-DD/ 에 JSON 저장"""
    today = datetime.now().strftime("%Y-%m-%d")
    # 스킬 루트 기준 reports 폴더
    reports_dir = Path(__file__).parent.parent / "reports" / today
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%H%M%S")
    safe_label = label.replace(",", "_")[:30]
    filename = reports_dir / f"{safe_label}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(filename)


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="뉴스 브리핑 수집기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
카테고리:
  general  전체 9개 소스 (종합뉴스)
  ai       AI 전문 6개 소스
  hr       HR/직장 AI 6개 소스

예시:
  python3 fetch_news.py --source ai
  python3 fetch_news.py --source aitimes_kr,geek_news --limit 10
  python3 fetch_news.py --source general --keyword "생성AI,LLM"
        """,
    )
    parser.add_argument(
        "--source", "-s", default="general",
        help="소스 키(쉼표 구분) 또는 카테고리: general|ai|hr (기본: general)"
    )
    parser.add_argument(
        "--keyword", "-k", default=None,
        help="키워드 필터 (쉼표 구분, 예: AI,LLM,자동화)"
    )
    parser.add_argument(
        "--limit", "-l", type=int, default=5,
        help="소스당 최대 항목 수 (기본: 5)"
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="파일 저장 없이 stdout 출력만"
    )
    parser.add_argument(
        "--list-sources", action="store_true",
        help="사용 가능한 소스 목록 출력"
    )
    # 날짜 필터 옵션
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--days", type=int, default=None,
        help="최근 N일 기사만 포함 (예: --days 1 = 오늘, --days 7 = 최근 1주일)"
    )
    date_group.add_argument(
        "--date-from", default=None, metavar="YYYY-MM-DD",
        help="시작 날짜 (예: --date-from 2026-03-01)"
    )
    parser.add_argument(
        "--date-to", default=None, metavar="YYYY-MM-DD",
        help="종료 날짜 (--date-from 과 함께 사용, 예: --date-to 2026-03-11)"
    )
    args = parser.parse_args()

    # 소스 목록 출력
    if args.list_sources:
        print("\n=== 소스 목록 ===")
        for key, src in SOURCES.items():
            cats = ", ".join(src["category"])
            print(f"  {key:15} | {src['name']:25} | {src['lang']} | [{cats}]")
        print("\n=== 카테고리 ===")
        for cat, keys in CATEGORY_SOURCES.items():
            print(f"  {cat:10} : {', '.join(keys)}")
        return

    # 소스 결정
    source_arg = args.source.lower().strip()
    if source_arg in CATEGORY_SOURCES:
        source_keys = CATEGORY_SOURCES[source_arg]
    else:
        source_keys = [s.strip() for s in source_arg.split(",")]
        invalid = [k for k in source_keys if k not in SOURCES]
        if invalid:
            print(f"[경고] 알 수 없는 소스: {', '.join(invalid)}", file=sys.stderr)
            source_keys = [k for k in source_keys if k in SOURCES]

    if not source_keys:
        print("[오류] 수집할 소스가 없습니다.", file=sys.stderr)
        sys.exit(1)

    # 날짜 필터 요약 메시지
    date_desc = ""
    if args.days == 1:
        date_desc = " [오늘 기사만]"
    elif args.days == 7:
        date_desc = " [최근 1주일]"
    elif args.days:
        date_desc = f" [최근 {args.days}일]"
    elif args.date_from or args.date_to:
        date_desc = f" [{args.date_from or '?'} ~ {args.date_to or '오늘'}]"

    print(f"[수집 시작] 소스: {', '.join(source_keys)}{date_desc}", file=sys.stderr)

    data = fetch_multiple(
        source_keys,
        limit=args.limit,
        keyword=args.keyword,
        days=args.days,
        date_from=args.date_from,
        date_to=args.date_to,
    )

    total_items = sum(len(v.get("items", [])) for v in data.values())
    warning_low = total_items < 5

    output = {
        "fetched_at": datetime.now().isoformat(),
        "category": source_arg,
        "date_filter": {
            "days": args.days,
            "date_from": args.date_from,
            "date_to": args.date_to,
        },
        "sources_requested": source_keys,
        "total_items": total_items,
        "warning_low_results": warning_low,
        "data": data,
    }

    if warning_low:
        print(f"[⚠️ 경고] 수집 항목이 {total_items}개로 부족합니다.", file=sys.stderr)

    if not args.no_save:
        saved_path = save_result(output, source_arg)
        print(f"[저장 완료] {saved_path}", file=sys.stderr)

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
