# **ElasticSearch 개요**

---

**Nosql 기반의 Document 지향 Open source database**

- 실시간 분석으로 빠른 검색, 집계 수행. Full-text search
    - 질의에 사용되는 query 및 query의 결과 모두 JSON 형식으로 return
- HTTP 프로토콜로 접근 가능한 RESTful API 지원
    - Create: POST
    - Read: GET
    - Update: PUT
    - Delete: DELETE
- multitenancy
    - 데이터들 간 별도의 커넥션 없이 분산되어 저장됨
- 역인덱스 방식으로 데이터 저장
- 데이터 업데이트 및 삭제에 비용 소모 o
- Query DSL

**git repo:**

https://github.com/elastic

## ElasticSearch data structure

---

1. **인덱스(Index)**: 데이터베이스, 문서의 모음을 유지하는 논리적 네임스페이스. 인덱싱 과정을 거친 결과물
    1. **인덱싱(Indexing)**: 데이터를 검색될 수 있는 구조로 변경하기 위해 문서를 검색어 토큰으로 변환해 저장하는 과정
        1. **검색**: 인덱스에 들어있는 검색어 토큰들을 포함하는 문서를 찾아가는 과정
           ![스크린샷 2024-05-22 오전 8 33 56](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/6b169660-e325-4ce1-9e13-1da63513b0d4)
            
          
            
2. **문서(Document):** **행**, 인덱스에 저장되는 기본 정보 단위. JSON 형식으로 표현
3. **필드(Filed):** **열**, 문서의 각 항목. 데이터의 특정 속성을 포함.
4. **샤드(Shard):** 인덱스의 부분집합. 확장성을 위해 여러 샤드로 분할됨. 각 샤드는 노드에서 호스팅 될 수 있음
5. **레플리카(Replica):** 샤드의 복사본 
    1. 같은 샤드와 레플리카는 동일한 데이터를 담고 있으며 반드시 서로 다른 노드에 저장이 됨
6. **노드(Node):** 클러스터의 단일 인스턴스. 
    1. **노드의 역할: master, data, ingest, ml**
        1. master: 모든 클러스터에는 1개의 마스터 노드 존재. 인덱스의 메타 데이터와 클러스터의 상태 정보를 관리하는 역할 수행
        2. data: 노드가 데이터를 저장하도록 설정
        3. ingest: indexing 시 데이터 전처리 작업 ingest pipeline 설정 
        4. ml: 노드의 머신러닝 작업 수행 설정
7. **클러스터(Cluster):** 하나 이상의 노드로 구성된 것으로. 색인 및 검색 기능 제공
    1. 클러스터 명이 같으면 같은 클러스터로 묶이고, 다르면 같은 물리적 장비 및 같은 네트워크 상이더라도 서로 다른 클러스터 명으로 바인딩 됨
8. **매핑(Mapping):** 인덱스에 저장된 문서들의 필드가 어떻게 저장되고 색인되는지 정의. ↔ RDBMS의 스키마
<img width="750" alt="스크린샷 2024-05-17 오후 4 27 43" src="https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/3c8e852e-c80b-46e6-b511-0b10ef7fc3c4">

![스크린샷 2024-05-20 오전 11 07 25](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/9765775f-69e0-4eab-a088-2c47d3fef877)

```

 Cluster
    │
    │
    │
		├── Node
		│		  │
		│		  ├── Index
		│			│		├── Document
		│			│		│      ├── Filed
		│			│		│      ├── Filed
		│			│		├── Document
		│			│		├── Document
		│			├── Index
		│			│		├── Document
		│			│		│      ├── Filed
		│			│		│      ├── Filed
		│			│		├── Document
		│			│		├── Document
		│			│
		│			├──Index
		│					├── Document
		│					│      ├── Filed
		│					│      ├── Filed
		│					├── Document
		│					├── Document
		│
		├── Node
		│			│
		│		  ├── Index
		│			│		├── Document
		│			│		│      ├── Filed
		│			│		│      ├── Filed
		│			│		├── Document
		│			│		├── Document
		│			├── Index
		│			│		├── Document
		│			│		│      ├── Filed
		│			│		│      ├── Filed
		│			│		├── Document
		│			│		├── Document
		│			│
		│			├──Index
		│					├── Document
		│					│      ├── Filed
		│					│      ├── Filed
		│					├── Document
		│					├── Document
		.         .
		.         .
		.         .

```

## ElasticSearch 문법

---

- GET
- POST
- PUT
- DELETE

# Elasticsearch 설치

---

**Download**

---

- **Elasticsearch**: 분석 엔진, Kibana와 상호작용
- **Kibana**: Elasticsearch data를 시각화하고 탐색하는 웹 기반 인터페이스. Elasticsearch와 상호작용
- **~~PostGresql**: open source DB. Data ETL~~
- **~~Logstash**: data pipeline~~

## ElasticSearch

---

1. 아래의 링크에서 OS에 맞는 버전의 Elasticsearch를 다운로드
    - download link:
        
        [Elasticsearch: 공식 분산형 검색 및 분석 엔진 | Elastic](https://www.elastic.co/kr/elasticsearch)
        
        
2. 다운로드 받은 후, 경로로 이동해 `unzip` 후 아래 코드 실행
    1. `./bin/elasticsearch`
    2. `./bin/elasticsearch -d
    # 백그라운드 실행`
        
        ```
        ./bin/elasticsearch -d
        # 백그라운드 실행
        ```
        
    
    - 게이트키퍼 오류 시(mac OS)
        - 게이트키퍼 비활성화 코드
    
    ```
    sudo spctl --master-disable
    ```
    
3. 실행 시 아래의 화면이 출력된다
![스크린샷 2024-05-17 오후 2 18 18 (1)](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/1b893f22-3f03-4bc3-8eac-a3c9eba505b9)
![***login_info, enrollment token, http figer print. 이 세 가지 정보는 따로 저장 必***]



1. **user, password**: Elasticsearch를 관리하는 기본 사용자인 'elastic'의 비밀번호가 설정됨. **따로 기록해두는 것** 권장.
    
    ```
    user: "elastic", password: "LGV8u_-JCULST=mx8+c3"
    # user는 elastic 고정. password는 최초로 발급받은 password 사용
    ```
    
2. 이 비밀번호는 `**bin/elasticsearch-reset-password -u elastic**` 명령어를 통해 재발급 가능, **`bin/elasticsearch-reset-password interative -u elastic`** 명령어로 비밀번호 재설정 가능(mac에서는 되지 않음)
3. **HTTP CA 인증서 SHA-256 지문**: 클러스터의 보안 통신을 위한 인증서의 지문. 이는 클라이언트와 서버 간 통신의 보안을 확인하는 데 사용될 수 있음.
4. **Kibana enrollment token**: Kibana 구성할 때 위에서 제공된 등록 토큰을 입력해야 함. 이 토큰은 30분 동안 유효.
5. **다른 노드가 이 클러스터에 참여하도록 구성**: 클러스터에 새로운 노드를 추가하려면, 기존 노드에서 새로운 등록 토큰을 생성하고, 새 노드에서는 이 토큰을 사용하여 **Elasticsearch**를 시작

4. 로컬 접속 후 응답 확인

**Elasticsearch**가 사용하는 `port=9200`. [https://localhost:9200](https://localhost:9200/) 접속

![스크린샷 2024-05-17 오후 2 41 33](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/5124ce4a-46b0-4aca-a756-1eff7ad0f0bd)

```
	{
  "name": "2eey10ucBookPro.kornet",
  "cluster_name": "elasticsearch",
  "cluster_uuid": "1hKMoPwCTPyba1sJWth2Ow",
  "version": {
    "number": "8.13.4",
    "build_flavor": "default",
    "build_type": "tar",
    "build_hash": "da95df118650b55a500dcc181889ac35c6d8da7c",
    "build_date": "2024-05-06T22:04:45.107454559Z",
    "build_snapshot": false,
    "lucene_version": "9.10.0",
    "minimum_wire_compatibility_version": "7.17.0",
    "minimum_index_compatibility_version": "7.0.0"
  },
  "tagline": "You Know, for Search"
}
```

## Kibana

---

1. 아래의 링크에서 다운로드
    
    [Download Kibana Free | Get Started Now](https://www.elastic.co/kr/downloads/kibana)
    

    
2. 다운로드 받은 후, 경로로 이동해 `unzip` 후 `bin/kibana` 실행
    - CLI를 새 창으로 더 열고 실행하는 것을 추천

![스크린샷 2024-05-17 오후 2 20 20 (1)](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/2d3df000-09d1-4c23-8d79-10db7c8c797c)

 3.  **Kibana**가 사용하는 port=5601. [https://localhost:5601](https://localhost:5601/) 접속

![스크린샷 2024-05-17 오후 2 20 27](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/f7b488b1-42da-4b6f-8eda-dc78c4fbd863)

1. Elasticsearch 설치 시 출력됐던 ***enrollment token을 붙여넣기***

![스크린샷 2024-05-17 오후 2 21 09](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/21ed1657-a172-4f46-ab6e-c17e90ed3bd1)

5. token 입력 시 확인 코드 입력 창이 뜬다. 동시에, 터미널에서 출력된 6자리 코드 입력

![스크린샷 2024-05-17 오후 2 21 29 (1)](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/17dadcf7-626a-434b-bbc3-186b2c0e9e90)

1. 로그인 창이 나타나면, Elasticsearch의 login info를 동일하게 입력 후 login

![스크린샷 2024-05-17 오후 2 55 51](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/484644a0-9688-4b01-94d1-c46e4548cadc)

![스크린샷 2024-05-17 오후 2 56 59](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/7ded17c2-bed0-40c3-92eb-85ecff7b2559)

7. 이후 data 추가 및 dataview 추가해서, Elastic engine을 Kibana로 모니터링하면 된다.

# ElasticSearch CRUD

---

**RestFul**: REST API → HTTP Method를 통해 Resource 별 고유 URL로 자원 처리

- 고유 URL: http://<`host`>:<`port`>/<`index`>/**_doc**/<`document_id`>
    - ex) https://192.168.1.43:9200/test/_doc/1
    - _doc은 document_type의 고정자

## CRUD

---

### 입력(PUT)

---

*데이터 입력* ↔ CREATE

**Request**

```
PUT test/_doc/1
{
"name": "YR LEE",
"message": "Hello World"
}
```

Response

```
{
  "_index": "test",
  "_id": "1",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```

최초 입력시 → `"result" : "created”`, 재입력 시 → `"result" : "updated”`

- 동일 URL에 다른 내용을 다시 입력 시 기존 document 사라지고 새로운 도큐먼트로 덮어 씌워지게 됨.
    - 덮어씌워짐 방지를 위해서, `PUT test/_doc/1/_create` 로 설정 할 수 있음. 이때 document id에 이미 데이터 존재 시 입력오류 출력되게끔

### 조회(GET)

---

*데이터 조회* ↔ READ

**request**

```
GET test/_doc/1
```

**response**

```
{
  "_index": "test",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "name": "YR LEE",
    "message": "Hello World"
  }
}
```

document의 내용은 `_source` 항목에 있음

### 수정(POST) ↔ UPDATE

---

*데이터 수정* 

**request**

```
POST test/_doc
{
  "name": "YR LEE",
  "message": "Hello World"
}
```

**response**

```
{
  "_index": "test",
  "_id": "UPTyno8BTlXDeQjR-Bkx",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 9,
  "_primary_term": 1
}
```

PUT과 유사하게, 데이터 입력으로도 사용 가능. PUT과의 차이점은, document 입력 시 <`index`>/_doc까지만 입력하면, document_id가 자동으로 생성됨

document 수정을 위해 매번 PUT으로 기존 document내용을 다시 입력할 수 있지만, 비효율적임. 이에 `_update` 명령을 통해 수정하고자 하는 field의 내용만 수정할 수 있음. 업데이트 할 내용에 `doc` 지정자를 사용

**request**

```
POST test/_update/1
{
  "doc": {
  "message": "foo World"
}
}
```

**response**

```
{
  "_index": "test",
  "_id": "1",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 11,
  "_primary_term": 1
}
```

### 삭제(DELETE) ↔ DELETE

---

*데이터 삭제*

**request**

```
DELETE test/_doc/1 
# document 단위 삭제

DELETE test
# 해당 index 전체 삭제

```

**response**

```
{
  "_index": "test",
  "_id": "1",
  "_version": 9,
  "result": "deleted",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 8,
  "_primary_term": 1
}
```

이후 GET Method로 삭제된 index 및 document 내용을 조회하려하면 document를 못 찾았다는 message를 return 받음.

## Postman

---

API test tool

![스크린샷 2024-05-22 오후 3 42 37](https://github.com/2eey10/elasticsearch-vector-crud/assets/133326837/15483978-01fb-43ce-b6d6-02e03529cffc)

Ref:

https://esbook.kimjmin.net/01-overview/1.1-elastic-stack/1.1.1-elasticsearch


