# Bounded File Navigation (실험적 스킬)

[English README](README.md)

대규모 코드베이스나 여러 프로젝트를 탐색할 때, 검색 결과 전체나 대용량 파일을 에이전트의 대화 컨텍스트에 한 번에 쏟아붓지 않고 **필요한 범위만 좁혀서 읽도록 돕는 에이전트 스킬과 파이썬 CLI**입니다.

이 도구는 **탐색 보조 도구**일 뿐이며, 자체적으로 토큰 절감이나 정확도 유지를 보증하지 않습니다. 검색 결과의 줄 수는 제한되지만, 정답 판정에 필요한 원본 파일 읽기는 제한해서는 안 됩니다. 에이전트는 결론을 내리거나 코드를 수정하기 전에 관련된 원본 근거를 충분히 확인해야 합니다.

## 설치 및 실행 방법

### 1. 터미널에서 직접 실행 (의존성 없음, Python 3.9+)

별도 패키지 설치 없이 `git clone` 후 바로 사용할 수 있습니다.

```sh
git clone https://github.com/nakim81/bounded-file-navigation.git
cd bounded-file-navigation

# 1) 파일 경로 탐색 (기본 12개까지)
python3 scripts/nav.py /경로/프로젝트 'manifest'

# 2) 파일 내용 검색 (일치하는 줄 요약 출력)
python3 scripts/nav.py /경로/프로젝트 'parse_manifest' --mode lines

# 3) 특정 하위 폴더만 더 좁혀서 검색 (최대 25개)
python3 scripts/nav.py /경로/프로젝트/src 'parse_manifest' --mode lines --limit 25
```

### 2. 표준 Agent Skills 생태계 (`skills.sh` / Claude Code, Codex, Cursor 등)

공용 skills CLI를 통해 한 줄로 등록할 수 있습니다.

```sh
# 사용 가능한 스킬 확인
npx skills add nakim81/bounded-file-navigation --list

# 전역(Global) 스킬로 설치
npx skills add nakim81/bounded-file-navigation -g -y

# 특정 에이전트 지정 설치 (예: claude-code, cursor)
npx skills add nakim81/bounded-file-navigation -g --agent claude-code -y
```

### 3. Hermes Agent에서 설치

Hermes CLI를 통해 원격 URL에서 바로 설치할 수 있습니다.

```sh
hermes skills install https://raw.githubusercontent.com/nakim81/bounded-file-navigation/main/SKILL.md --name bounded-file-navigation --yes
```

### 4. 에이전트가 다른 환경에서 즉석으로 사용하게 하는 프롬프트 (Prompt Hook)

에이전트에게 사전 설치된 스킬이 없을 때는, 프로젝트 지침(`AGENTS.md`, `CLAUDE.md`, `.hermes.md`)에 다음 원칙을 포함해 두는 것만으로도 동일한 절차를 유도할 수 있습니다.

```markdown
## Bounded File Navigation Rule
- 전체 디렉터리(`~` 등)를 대상으로 broad grep/find를 실행해 컨텍스트를 채우지 마십시오.
- 파일명 목록이나 일치하는 줄(line)만 먼저 제한된 건수(10~20건)로 확인하십시오.
- 검색 결과가 잘렸다면(TRUNCATED) 끝난 것이 아니라 범위가 넓다는 뜻이므로 하위 경로를 좁히거나 쿼리를 구체화하십시오.
- 섣불리 파일이 없다고 판단하지 말고, 관련 핵심 파일의 특정 줄 범위만 읽어서 최종 근거를 교차 검증하십시오.
```

## 효과 측정과 검증 기준

토큰을 아꼈다는 주장이 성립하려면 **정확도가 떨어지지 않아야** 합니다. 실제 작업에 적용할 때는 아래 기준을 함께 비교해야 합니다.

1. **정확도:** 올바른 원본 파일과 최신 근거를 정확히 찾아냈는가? (누락된 근거는 없는가?)
2. **실제 토큰 소비량:** 도구 출력뿐 아니라 스킬 프롬프트, 재시도 호출을 포함한 총 입력 토큰이 실제로 줄었는가?
3. **탐색 시간 및 호출 수:** 정답에 도달하기까지 걸린 호출 횟수와 대기 시간.
4. **한계 상황 인식:** 대용량 파일(1MB 초과 제외), 숨김 폴더, 제외 확장자, 정렬 순서로 인해 뒤쪽 매칭이 잘린 경우를 에이전트가 인지하고 범위를 좁혔는가?

## 라이선스

MIT. 자세한 내용은 [LICENSE](LICENSE)를 참고하십시오.
