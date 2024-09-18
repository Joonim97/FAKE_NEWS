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
      "content": "가짜뉴스내용",
      "isFake": "FAKE",
      "user": "RYU",
      "comments": []
    }
  ]
  </pre>

### 2.2. 기사 작성
- Endpoint: `POST` `/api/articles`
- 설명: 새로운 기사 생성. isFake가 'REAL'일 경우 서버 종료. 로그인 필요.
- Request (JSON):
  <pre>
  {
    "title": "가짜뉴스",
    "content": "가짜뉴스내용",
    "isFake": "FAKE"
  }
  </pre>

- Response (JSON):
  <pre>
  {
    "id": 1,
    "title": "가짜뉴스",
    "content": "가짜뉴스내용",
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
    "content": "가짜뉴스내용",
    "isFake": "FAKE",
    "user": "RYU",
    "comments": []
  }
  </pre>

### 2.4. 특정 기사 수정
- Endpoint: `PUT` `/api/articles/{article_id}`
- 설명: 특정 기사 수정. 로그인 필요.
- Request (JSON):
  <pre>
  {
    "title": "업데이트된 가짜뉴스",
    "content": "업데이트된 가짜뉴스내용",
    "isFake": "FAKE"
  }
  </pre>

- Response (JSON):
  <pre>
  {
    "id": 1,
    "title": "업데이트된 가짜뉴스",
    "content": "업데이트된 가짜뉴스내용",
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

## 4. Auto Article Create

### 4.1. 가짜 기사 자동 생성
- Endpoint: `POST` `/api/articles/autoGen/`
- 설명: 입력된 주제에 맞는 가짜 기사를 자동으로 생성하여 저장. 로그인 필요.
- 특이사항: ollama 로컬 서버를 사용함. 로컬 서버 구동 후 테스트 시행해야함.
  
- Request (JSON):
<pre>
  {
    "topic": "달은 치즈로 되어있다"
  }
</pre>

- Response (JSON):
<pre>
{
    "id": 15,
    "title": "**달의 기밀 정보**",
    "content": "**달은 치즈로 만들어졌다는 사실을 밝혀냈습니다!**\n\n최근 연구 결과가 나온 것에 따르면, 달은 이전부터 알려진 바와 다르게 물과 반대편인 치즈로 구성되어있다는 사실이 드러났습니다. 이 놀라운 발견은 과학계를 충격으로 보내고 있습니다.\n\n**치즈 달의 비밀**\n\n달은 치즈에 의해 생성된 것으로 밝혀졌으며, 이는 지구에서 치즈로만 가능한 일입니다. 연구진들은 치즈가 지구에서 우주까지 퍼져 나가면서 달을 형성했음을 보였습니다. 이 사실이 알려지면, 달을 둘러싸고 있는 모든 미스터리는 사라집니다.\n\n**치즈 달의 음모**\n\n하지만 이 놀라운 발견에 대한 진실을 숨기려는 일부 조직의 음모가 있습니다. 정부와 국제연합은 이 치즈 달의 비밀을 숨기려는 것이라고 주장하고 있습니다.",
    "isFake": "FAKE",
    "user": "johndoe",
    "comments": []
}
</pre>

