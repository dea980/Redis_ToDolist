# Redis 기반 할 일 목록 애플리케이션

## 프로젝트 개요
이 프로젝트는 Redis를 데이터베이스로 사용하는 실시간 할 일 목록과 채팅 기능을 제공하는 풀스택 애플리케이션입니다. (오로지 구현 및 공부 목적입니다)

## 시스템 아키텍처

### 기술 스택
- **프론트엔드**: React
- **백엔드**: FastAPI
- **데이터베이스**: Redis
- **실시간 통신**: WebSocket

### 작동 원리

#### 1. 데이터 저장 구조
- **Redis 키-값 구조**
  - 할 일 목록: `todo:{id}` → 할 일 내용
  - 채팅 메시지: `chat:{room_id}:{timestamp}` → 메시지 데이터
  - Redis의 키-값 저장 방식을 활용하여 빠른 데이터 접근 가능

#### 2. 실시간 통신 메커니즘
- **WebSocket 연결**
  - 클라이언트-서버 간 지속적인 양방향 통신
  - 할 일 목록 변경사항 실시간 동기화
  - 채팅 메시지 즉시 전달
  
- **이벤트 기반 통신**
  - 데이터 변경 시 자동 업데이트
  - 연결 상태 모니터링
  - 자동 재연결 메커니즘

#### 3. 상태 관리
- **프론트엔드**
  - React useState를 통한 로컬 상태 관리
  - WebSocket 연결 상태 관리
  - 사용자 입력 및 UI 상태 처리

- **백엔드**
  - Redis 연결 관리
  - WebSocket 클라이언트 관리
  - 에러 처리 및 복구

## 주요 기능 설명

### 1. 할 일 목록 기능

#### 작동 원리
1. **할 일 추가**
   - 사용자 입력 → 프론트엔드 유효성 검사
   - API 요청 → 백엔드에서 Redis에 저장
   - WebSocket을 통해 모든 클라이언트에 업데이트 전파

2. **할 일 수정**
   - 수정 모드 활성화 → 입력 필드 전환
   - 변경사항 저장 → Redis 데이터 업데이트
   - 실시간 동기화로 모든 사용자에게 반영

3. **할 일 삭제**
   - 삭제 요청 → Redis에서 데이터 제거
   - WebSocket을 통한 실시간 목록 업데이트

### 2. 채팅 기능

#### 작동 원리
1. **채팅방 시스템**
   - 룸 ID 기반 채팅방 분리
   - 각 방별 독립적인 WebSocket 연결
   - Redis를 통한 메시지 영구 저장

2. **메시지 전송 과정**
   - 사용자 입력 → WebSocket으로 서버 전송
   - 서버에서 Redis에 저장
   - 같은 방의 모든 사용자에게 브로드캐스트

3. **메시지 동기화**
   - 최근 50개 메시지 유지
   - 새 연결 시 히스토리 로드
   - 실시간 메시지 동기화

## 데이터 흐름

### 1. 할 일 목록 데이터 흐름
```
사용자 입력 → React 컴포넌트 
→ FastAPI 엔드포인트 
→ Redis 저장 
→ WebSocket 브로드캐스트 
→ 모든 클라이언트 업데이트
```

### 2. 채팅 데이터 흐름
```
메시지 입력 → WebSocket 전송 
→ Redis 저장 
→ 룸 멤버들에게 브로드캐스트 
→ UI 업데이트
```

## 성능 최적화

### 1. Redis 활용
- 인메모리 데이터베이스로 빠른 읽기/쓰기
- 키-값 구조로 효율적인 데이터 접근
- 실시간 데이터 처리에 최적화

### 2. WebSocket 최적화
- 연결 유지로 오버헤드 감소
- 효율적인 실시간 데이터 전송
- 자동 재연결로 안정성 확보

### 3. 프론트엔드 최적화
- 조건부 렌더링으로 성능 향상
- 메시지 캐싱으로 불필요한 요청 감소
- 효율적인 상태 관리

## 에러 처리

### 1. 네트워크 에러
- WebSocket 연결 끊김 감지
- 자동 재연결 메커니즘
- 사용자에게 상태 알림

### 2. 데이터 유효성
- 입력 데이터 검증
- 중복 처리 방지
- 에러 상태 표시

### 3. Redis 연결
- 연결 실패 처리
- 재시도 메커니즘
- 데이터 정합성 유지

## 보안 고려사항

### 1. 데이터 보안
- 입력 데이터 검증
- XSS 공격 방지
- SQL 인젝션 방지 (Redis 사용으로 자연스럽게 해결)

### 2. 통신 보안
- WebSocket 연결 보안
- CORS 설정
- 에러 메시지 보안

## 확장성

### 1. 수평적 확장
- Redis 클러스터 지원
- 멀티 서버 구성 가능
- 로드 밸런싱 준비

### 2. 기능 확장
- 새로운 기능 추가 용이
- 모듈화된 구조
- 유연한 아키텍처
