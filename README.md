# AIFFEL 과제

## Create Question

- **URL**
    
    /questions
    
- **Method:**
    
    `POST`
    
- **Request Body**
    
    `title=[varchar]`
    `content=[varchar]`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 201 </br>
    **Content:** `{  
        "title": "4번 질문",
        "content": "4번 질문 내용",
        "user": "muk",
        "created_at": "2021-12-17"}`
- **Error Response:**
    - **Code:** 400 KEYERROR </br>
    **Content:** `{ MESSAGE:"KEY_ERROR" }`
    
    OR
    
    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }`
 ---
    
 ## Revise Question

- **URL**
    
    /questions/:id
    
- **Method:**
    
    `PUT`
    
- **URL Params**
    
    **Required:**
    
    `id=[integer]`
    
- **Request Body**
    
    `title=[varchar]`
    `content=[varchar]`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions/4" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 201 </br>
    **Content:** `{ MESSAGE:"SUCCESS" }` 
     
- **Error Response:**
    - **Code:** 404 NOT FOUND </br>
    **Content:** `{ MESSAGE:"QUESTION_DOES_NOT_EXIST" }`
    
    OR
    
    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }` or `{ MESSAGE:"NOT_MATCHED_USER" }` 
---
## DELETE Question

- **URL**
    
    /questions/:id
    
- **Method:**
    
    `DELETE`
    
- **URL Params**
    
    **Required:**
    
    `id=[integer]`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions/4" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 204 </br>
    **Content:** `{ MESSAGE:"DELETE" }` 
     
- **Error Response:**
    - **Code:** 404 NOT FOUND </br>
    **Content:** `{ MESSAGE:"QUESTION_DOES_NOT_EXIST" }`
    
    OR
    
    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }` or `{ MESSAGE:"NOT_MATCHED_USER" }` 
---

## Create Comment

- **URL**
    
    /questions/:id/comments
    
- **Method:**
    
    `POST`
    
- **Request Body**
    
    `content=[varchar]`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions/4/comments" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 201 </br>
    **Content:** `{ MESSAGE:"CREATE" }`
    
- **Error Response:**
    - **Code:** 400 KEYERROR </br>
    **Content:** `{ MESSAGE:"KEY_ERROR" }` or `{ MESSAGE:"EMPTY_CONTENT" }`
    
    OR
    
    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }`
 ---

## Show Comment

- **URL**
    
    /questions/:id/comments
    
- **Method:**
    
    `GET`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions/4/comments" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 200 </br>
    **Content:**
       `[{
            "content": "댓글(1)"
        },
        {
            "content": "댓글(2)"
        },
        {
            "content": "댓글(3)"
        }]`
    
- **Error Response:**
    - **Code:** 400 KEYERROR or EMPTY </br>
    **Content:** `{ MESSAGE:"KEY_ERROR" }` or `{ MESSAGE:"EMPTY_CONTENT" }`
    
    OR
    
    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }`
    
      OR
    
    - **Code:** 404 Page not found </br>
    **Content:** `{ "No Question matches the given query" }`
 ---
 
 ## Show Question  

- **URL**
    
    /questions/list
    
- **Method:**
    
    `GET`
    
- **URL Params**
    
    **Required:**
    
    `title=[varchar]` or `content=[varchar]`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions/list?title=1번" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 200 </br>
    **Content:**
      `[
        {
            "title": "1번 질문",
            "content": "1번 질문 내용",
            "user": "muk",
            "created_at": "2021-12-16"
        },
        {
            "title": "1번 질문(수정)",
            "content": "1번 질문 내용(수정)",
            "user": "muk",
            "created_at": "2021-12-17"
        }
      ]`
    
- **Error Response:**

    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }`
   
 ---
 
 ## Like or Like_Cancel

- **URL**
    
    /questions/like
    
- **Method:**
    
    `POST`
    
- **Request Body**
    
    `question_id=[integer]`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions/like" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 201 </br>
    **Content:** `{ MESSAGE:"LIKE" }` or `{ MESSAGE:"LIKE_CANCEL" }` 
    
- **Error Response:**
    - **Code:** 400 KEYERROR </br>
    **Content:** `{ MESSAGE:"KEY_ERROR" }`
    
    OR
    
    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }`
    
    - **Code:** 404 Not Found</br>
    **Content:** `{ MESSAGE:"QUESTION_DOES_NOT_EXIST" }`
 ---

## Show Most Like_Question

- **URL**
    
    /questions/like
    
- **Method:**
    
    `GET`
    
- **URL Params**
    
    **Required:**
    
    `year=[integer]`
    `month=[integer]`
    
- **Request Header:**
    
    Authorization: {access token]
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/questions/like?year=2021&month=12" \
          -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc"
    ```
    
- **Success Response:**
    - **Code:** 200 </br>
    **Content:**
      `[
        {
            "title": "1번 질문",
            "content": "1번 질문 내용",
            "user": "muk",
            "like_count": 1,
            "created_at": "2021-12-16"
        }
       ]`
    
- **Error Response:**

    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"INVALID_USER" }` or `{ MESSAGE:"INVALID_TOKEN" }`
   
 ---
 
## Sign_up

- **URL**
    
    /users/signup
    
- **Method:**
    
    `POST`
    
- **Request Body**
    
    `user_id=[varchar]`
    `password=[varchar]`
    
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/users/signup"
    ```
    
- **Success Response:**
    - **Code:** 201 </br>
    **Content:** `{ MESSAGE:"SUCCESS" }` 
    
- **Error Response:**
    - **Code:** 400 KEYERROR, EMPTY, DUPLICATION </br>
    **Content:** `{ MESSAGE:"KEY_ERROR" }` or `{ MESSAGE:"EMPTY_VALUE_ERROR" }` or `{ MESSAGE:"DUPLICATION_ERROR" }`
 ---
 
## Sign_in

- **URL**
    
    /users/signin
    
- **Method:**
    
    `POST`
    
- **Request Body**
    
    `user_id=[varchar]`
    `password=[varchar]`
    
    
- **Sample Call:**
    
    ```bash
    curl  -XGET "http://127.0.0.1:8000/users/signin"
    ```
    
- **Success Response:**
    - **Code:** 201 </br>
    **Content:** `{ MESSAGE:"SUCCESS", ACCESS_TOKEN:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.VrcoibekRYNzk_VJ8wAeMGVUKE8uvP7-gO0yQEALTtc" }` 
    
- **Error Response:**
    - **Code:** 400 KEYERROR, EMPTY </br>
    **Content:** `{ MESSAGE:"KEY_ERROR" }` or `{ MESSAGE:"EMPTY_VALUE_ERROR" }`
    
    - **Code:** 401 UNAUTHORIZED </br>
    **Content:** `{ MESSAGE:"USER_DOES_NOT_EXIST" }` or `{ MESSAGE:"INVALID_PASSWORD" }`
 ---
