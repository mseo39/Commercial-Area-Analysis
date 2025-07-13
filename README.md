# 상권분석 빅데이터 시스템 (2023.09 ~ 2023.10)

> 개인 프로젝트 | Full-Stack 개발 | MongoDB, Django REST Framework, Celery, Docker, RabbitMQ
> 

## 🧠 프로젝트 개요

- 전세계를 대상으로 하는 상권분석 서비스를 가정
- 기존 상권분석 서비스에서는 **지도로 원하는 지역을 클릭해도 행정구역을 다시 선택해야 하는 불편함**
- 또한 **상권 관련 데이터는 대용량이기 때문에, 단일 서버 환경에서는 처리 효율에 한계** 존재

이 문제를 해결하기 위해:

- **사용자 UI를 직관적으로 개선**
- **MongoDB 기반 수평 확장형 분산 데이터베이스 도입**
- **Celery를 활용한 비동기 분산 작업 시스템 구축**

## 🔧 기술 스택 및 아키텍처

| 영역 | 사용 기술 |
| --- | --- |
| Backend | Python 3.9, Django REST Framework, Celery |
| DB | MongoDB, MySQL |
| Infra | Docker, RabbitMQ, Flower |
| 기타 | REST API, Linux 기반 환경 |

### 📦 시스템 구성도

- 전체 흐름
<img width="627" height="285" alt="image" src="https://github.com/user-attachments/assets/bd2bb3fc-a6bc-40e7-baa7-0f09175b56cf" />

- Docker에서의 분산 시스템 구성
<img width="574" height="448" alt="image" src="https://github.com/user-attachments/assets/ba24fe02-972d-49eb-84e1-8b44d17047c7" />

- Docker에서의 분산 데이터베이스 구성
<img width="805" height="348" alt="image" src="https://github.com/user-attachments/assets/e6b2ced9-0cb8-4dce-964f-e9ca169d80fc" />

---

## 🚀 주요 기능 요약

### ✅ 파일 업로드

- 국가 및 도시 정보와 함께 분석 데이터 업로드
- 대용량 파일 처리: Celery 비동기 큐 사용

> ⏱️ 성능 비교
> 
> 
> 기존: 3188.03초 → 개선: 1851.39초 (⏬ **41.98% 시간 단축**)
> → Celery를 이용해 세 개의 파일을 병렬 작업으로 나눠 처리함으로써, 전체 처리 시간을 **약 42% 단축**했습니다.
<img width="1071" height="462" alt="image" src="https://github.com/user-attachments/assets/11c1a1be-8f37-400a-86f3-25963ff74a92" />

---

### ✅ 상권 영역 데이터 조회

- 지도 기반 UI로 원하는 행정동 클릭
- Hover 시 상권명/코드 정보 표시
- 분석 요청 시 REST API로 서버 통신
- 매출, 인구 등 데이터를 그래프로 시각화
<img width="986" height="640" alt="image" src="https://github.com/user-attachments/assets/9f77ff52-f3ad-41ba-9dec-06b811e4afab" />

---

## 📚 프로젝트를 통해 배운 점

- **수평 확장의 개념**과 MongoDB 샤딩 구조에 대한 실습 경험
- **Celery 기반의 비동기 작업 처리 구조** 설계
- **Docker를 활용한 컨테이너 환경에서의 분산 시스템 구성** 실습

---

## ⚙️ 실행환경 및 버전 정보

```
Python==3.9.6
Django==4.1.7
MongoDB==7.0.2
Celery==5.3.4
Mysql==8.1.0
RabbitMQ==3.12.6
Flower==2.0.1
```

---

## 📎 기타 자료

- 

---

## 👀 마무리

이 프로젝트는 상권 분석보다는 **분산 시스템 설계 및 대용량 데이터 처리**에 초점을 맞췄습니다.

단순한 기능 구현을 넘어서 **실제 환경에서의 병목문제**를 해결해본 경험이 핵심입니다.
