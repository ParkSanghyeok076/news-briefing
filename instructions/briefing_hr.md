# 👥 HR·AI at Workplace 브리핑 지침

## 입력
`python3 scripts/fetch_news.py --source hr` 로 수집한 JSON 객체
- 소스: aitimes_kr, aitimes_com, ttimes, mk_ai, ai_magazine, tech_review

## 출력 목표
- **10~15개 항목**
- AI가 업무·조직·인력에 미치는 영향 중심 분석
- 저장: `reports/YYYY-MM-DD/hr_HHMMSS.md`

---

## 섹션 구조

### 1. 🤝 AI·업무 자동화 (4~5개)
AI 도구 도입 사례, 업무 프로세스 변화, 생산성 영향

### 2. 👔 조직·인력 변화 (3~5개)
채용 트렌드, 직무 변화, 교육·리스킬링, AI 인재 확보

### 3. 📊 경영·전략 (3~5개)
기업의 AI 전환 전략, ROI, 조직 구조 변화

---

## 항목 형식 (5줄)

```
**[제목](링크)**
출처: {source_name} | 시간: {time}

요약: {핵심 내용 2~3문장, 한국어}
HR 시사점: {HR 담당자/조직 관리자 관점에서의 실무적 함의}
```

---

## 보고서 헤더 형식

```markdown
# 👥 HR·AI at Workplace 브리핑
**{YYYY년 MM월 DD일}** | HR 관련 6개 소스 | 총 {N}건

---
```

---

## 필터링 기준

**포함 우선 키워드:**
- AI workplace, 자동화, automation, 직무, 채용, 인력, workforce
- talent, 조직, 경영, management, 교육, training, reskilling
- 생산성, productivity, 직원, employee, 리더십

**제외 기준:**
- 순수 AI 기술 논문 (HR 관련성 없음)
- 코딩/개발 튜토리얼
- 단순 제품 스펙 발표

---

## 규칙

- **언어**: 영어 기사 모두 한국어로 번역·요약
- **HR 시사점 필수**: 모든 항목에 실무적 함의 포함
- **관련성 필터**: HR/비즈니스 관련성 낮은 기사 제외
- **최소 10개 항목**: 부족 시 `--keyword "AI,자동화,인력"` 으로 재수집
- **국내 동향 우선**: 한국어 소스 기사를 섹션 상단에 배치
