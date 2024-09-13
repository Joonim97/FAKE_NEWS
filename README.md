# API 문서

## 1. User Accounts (Authentication)

### 1.1. 회원 가입
- Endpoint: `POST` `/api/accounts`
- 설명: 새로운 사용자 등록.
- Request (JSON):
  <pre>
  {
    "username": "RYU",
    "password": "ryu12345",
    "email": "ryu@example.com",
    "name": "Ryu",
    "nickname": "YesYesMe",
    "birthday": "1990-01-01",
    "gender": "M",
    "introduction": "Yes Yes Me."
  }
  </pre>

- Response (JSON):
  <pre>
  {
    "id": 1,
    "username": "RYU",
    "email": "ryu@example.com",
    "name": "Ryu",
    "nickname": "YesYesMe",
    "birthday": "1990-01-01",
    "gender": "M",
    "introduction": "Yes Yes Me."
  }
  </pre>

### 1.2. 로그인
- Endpoint: `POST` `/api/accounts/login`
- 설명: 사용자 로그인 후 Access Token과 Refresh Token 발급.
- Request (JSON):
  <pre>
  {
    "username": "RYU",
    "password": "ryu12345"
  }
  </pre>

- Response (JSON):
  <pre>
  {
      "refresh": "eyJh...U4 (refresh token)",
      "access": "eyJh...DU (access token)"
  }
  </pre>

### 1.3. 프로필 조회
- Endpoint: `GET` `/api/accounts/<사용자 이름 (username)>/`
- 설명: 현재 로그인한 사용자 프로필 조회.
- Headers: `Authorization: Bearer <your_access_token>`
- Response (JSON):
  <pre>
  {
      "id": 2,
      "last_login": null,
      "is_superuser": false,
      "first_name": "",
      "last_name": "",
      "is_staff": false,
      "is_active": true,
      "date_joined": "2024-09-13T05:31:54.955457Z",
      "username": "ryu",
      "email": "ryu@example.com",
      "password": "해싱된 비밀번호",
      "name": "",
      "nickname": "yesyesme",
      "birthday": "1990-01-01",
      "gender": "M",
      "introduction": "No No You",
      "groups": [],
      "user_permissions": []
  }
  </pre>

---

## 2. Articles CRUD

### 2.1. 전체 기사 조회
- Endpoint: `GET` `/api/articles`
- 설명: 모든 기사 조회.
- Response (JSON):
  <pre>
  [
    {
      "id": 1,
      "title": "가짜뉴스",
      "description": "가짜뉴스내용",
      "isFake": "FAKE",
      "user": "RYU",
      "comments": []
    }
  ]
  </pre>

### 2.2. 기사 작성
- Endpoint: `POST` `/api/articles`
- 설명: 새로운 기사 생성. isFake가 'REAL'일 경우 서버 종료.
- Request (JSON):
  <pre>
  {
    "title": "가짜뉴스",
    "description": "가짜뉴스내용",
    "isFake": "FAKE"
  }
  </pre>

- Response (JSON):
  <pre>
  {
    "id": 1,
    "title": "가짜뉴스",
    "description": "가짜뉴스내용",
    "isFake": "FAKE",
    "user": "RYU",
    "comments": []
  }
  </pre>

### 2.3. 특정 기사 조회
- Endpoint: `GET` `/api/articles/{article_id}`
- 설명: 특정 기사 조회.
- Response (JSON):
  <pre>
  {
    "id": 1,
    "title": "가짜뉴스",
    "description": "가짜뉴스내용",
    "isFake": "FAKE",
    "user": "RYU",
    "comments": []
  }
  </pre>

### 2.4. 특정 기사 수정
- Endpoint: `PUT` `/api/articles/{article_id}`
- 설명: 특정 기사 수정.
- Request (JSON):
  <pre>
  {
    "title": "업데이트된 가짜뉴스",
    "description": "업데이트된 가짜뉴스내용",
    "isFake": "FAKE"
  }
  </pre>

- Response (JSON):
  <pre>
  {
    "id": 1,
    "title": "업데이트된 가짜뉴스",
    "description": "업데이트된 가짜뉴스내용",
    "isFake": "FAKE",
    "user": "RYU",
    "comments": []
  }
  </pre>

### 2.5. 특정 기사 삭제
- Endpoint: `DELETE` `/api/articles/{article_id}`
- 설명: 특정 기사 삭제.
- Response: <pre>204 No Content</pre>

---

## 3. Comments CRUD

### 3.1. 특정 기사 댓글 조회
- Endpoint: `GET` `/api/articles/{article_id}/comments`
- 설명: 특정 기사에 달린 모든 댓글 조회.
- Response (JSON):
  <pre>
  [
    {
      "id": 1,
      "user": "RYU",
      "article": 1,
      "text": "이 기사는 흥미롭네요.",
      "created_at": "2024-09-13T10:00:00Z"
    }
  ]
  </pre>

### 3.2. 특정 기사 댓글 작성
- Endpoint: `POST` `/api/articles/{article_id}/comments`
- 설명: 특정 기사에 댓글 작성.
- Request (JSON):
  <pre>
  {
    "text": "이 기사는 흥미롭네요."
  }
  </pre>

- Response (JSON):
  <pre>
  {
    "id": 1,
    "user": "RYU",
    "article": 1,
    "text": "이 기사는 흥미롭네요.",
    "created_at": "2024-09-13T10:00:00Z"
  }
  </pre>

### 3.3. 특정 댓글 수정
- Endpoint: `PUT` `/api/articles/{article_id}/comments/{comment_id}`
- 설명: 특정 댓글 수정.
- Request (JSON):
  <pre>
  {
    "text": "업데이트된 댓글"
  }
  </pre>

- Response (JSON):
  <pre>
  {
    "id": 1,
    "user": "RYU",
    "article": 1,
    "text": "업데이트된 댓글",
    "created_at": "2024-09-13T10:00:00Z"
  }
  </pre>

### 3.4. 특정 댓글 삭제
- Endpoint: `DELETE` `/api/articles/{article_id}/comments/{comment_id}`
- 설명: 특정 댓글 삭제.
- Response: <pre>204 No Content</pre>

---


