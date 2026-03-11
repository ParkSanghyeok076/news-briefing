"""
RSS/Atom 피드 파서 - BeautifulSoup 기반
원본: cclank/news-aggregator-skill (MIT License)
"""
import sys
import requests
from bs4 import BeautifulSoup
import urllib3
import re
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def clean_text(text):
    if not text:
        return ""
    return text.strip()


def parse_rss_content(content, source_name, limit=5):
    """RSS/Atom 컨텐츠 파싱 → 항목 리스트 반환"""
    try:
        soup = BeautifulSoup(content, 'html.parser')
        items = []
        entries = soup.find_all(['item', 'entry'])

        for entry in entries:
            # 제목
            title_tag = entry.find('title')
            if not title_tag:
                continue
            title = clean_text(title_tag.get_text())

            # 링크
            link = ""
            link_tag = entry.find('link')
            if link_tag:
                if link_tag.has_attr('href'):
                    link = link_tag['href']
                elif link_tag.get_text(strip=True):
                    link = link_tag.get_text(strip=True)
                if not link:
                    link = str(link_tag.next_sibling).strip()
            if not link:
                guid = entry.find('guid')
                if guid and guid.get_text(strip=True).startswith('http'):
                    link = guid.get_text(strip=True)

            # 시간
            pub = entry.find(['pubdate', 'published', 'updated', 'dc:date'])
            time_str = clean_text(pub.get_text()) if pub else ""

            # 요약
            content_encoded = entry.find('content:encoded')
            description = entry.find('description')
            summary_tag = entry.find('summary')
            content_tag = entry.find('content')

            raw_summary = ""
            if content_encoded:
                raw_summary = content_encoded.get_text()
            elif description:
                raw_summary = description.get_text()
            elif summary_tag:
                raw_summary = summary_tag.get_text()
            elif content_tag:
                raw_summary = content_tag.get_text()

            soup_desc = BeautifulSoup(raw_summary, 'html.parser')
            clean_summary = soup_desc.get_text(separator=' ', strip=True)
            if len(clean_summary) > 300:
                clean_summary = clean_summary[:300] + "..."

            # 반응 수 (있을 경우)
            heat = ""
            comments = entry.find('slash:comments')
            if comments:
                heat = f"{comments.get_text(strip=True)} comments"

            items.append({
                "source": source_name,
                "title": title,
                "url": link,
                "time": time_str,
                "heat": heat,
                "summary": clean_summary,
            })
            if len(items) >= limit:
                break

        return items
    except Exception as e:
        print(f"[파싱 오류] {source_name}: {e}", file=sys.stderr)
        return []


def fetch_rss_feed(url, source_name, limit=5):
    """RSS/Atom 피드 수집"""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,image/avif,image/webp,*/*;q=0.8"
            ),
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.encoding = response.apparent_encoding or 'utf-8'
        return parse_rss_content(response.content, source_name, limit)
    except Exception as e:
        print(f"[수집 오류] {source_name} ({url}): {e}", file=sys.stderr)
        return []
