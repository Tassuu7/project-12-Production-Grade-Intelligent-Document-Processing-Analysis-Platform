# RESTful API Reference Specification

Comprehensive technical documentation for all Nexus DocIntel REST endpoints.

## POST `/api/v1/auth/register`
**Description**: Register New User Account

**Request Parameters / Body**:
`email, username, full_name, password`

**Response**:
`UserResponse object with created ID and timestamps`

### Example Curl Command
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"sample": "data"}'
```
---

## POST `/api/v1/auth/login`
**Description**: User & Admin Authentication

**Request Parameters / Body**:
`username_or_email, password`

**Response**:
`JWT access_token, refresh_token, and user profile`

### Example Curl Command
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"sample": "data"}'
```
---

## GET `/api/v1/auth/me`
**Description**: Retrieve Current User Profile

**Request Parameters / Body**:
`None (Bearer Token in Authorization header)`

**Response**:
`Authenticated UserResponse object`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" -H "Authorization: Bearer <TOKEN>"
```
---

## POST `/api/v1/documents/upload`
**Description**: Upload Multi-Format Documents

**Request Parameters / Body**:
`Multipart form data with files array (PDF, DOCX, TXT, CSV, XLSX)`

**Response**:
`Array of created DocumentResponse records`

### Example Curl Command
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"sample": "data"}'
```
---

## GET `/api/v1/documents/`
**Description**: List User Documents

**Request Parameters / Body**:
`Optional pagination parameters (page, limit, sort_by)`

**Response**:
`Array of DocumentResponse items`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/documents/" -H "Authorization: Bearer <TOKEN>"
```
---

## GET `/api/v1/documents/{id}`
**Description**: Get Document Details

**Request Parameters / Body**:
`document_id path parameter`

**Response**:
`Full DocumentDetailResponse with summary, keywords, topics, tables`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/documents/{id}" -H "Authorization: Bearer <TOKEN>"
```
---

## GET `/api/v1/documents/{id}/download`
**Description**: Download Original Document File

**Request Parameters / Body**:
`document_id path parameter`

**Response**:
`Binary stream with appropriate MIME type header`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/documents/{id}/download" -H "Authorization: Bearer <TOKEN>"
```
---

## POST `/api/v1/documents/{id}/reprocess`
**Description**: Trigger Document Re-Analysis

**Request Parameters / Body**:
`document_id path parameter`

**Response**:
`Job confirmation and enqueued job ID`

### Example Curl Command
```bash
curl -X POST "http://localhost:8000/api/v1/documents/{id}/reprocess" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"sample": "data"}'
```
---

## GET `/api/v1/search/`
**Description**: Faceted Full-Text Search

**Request Parameters / Body**:
`q (query string), category, file_type, page, limit`

**Response**:
`SearchResponse with highlighted snippets and facet counts`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/search/" -H "Authorization: Bearer <TOKEN>"
```
---

## GET `/api/v1/reports/document/{id}`
**Description**: Generate Analysis Report Export

**Request Parameters / Body**:
`document_id path parameter, format (html, pdf, json, csv)`

**Response**:
`Formatted standalone report document`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/reports/document/{id}" -H "Authorization: Bearer <TOKEN>"
```
---

## GET `/api/v1/admin/stats`
**Description**: System Health & User Telemetry

**Request Parameters / Body**:
`None (Admin Bearer Token required)`

**Response**:
`Global platform metrics and processing counts`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/admin/stats" -H "Authorization: Bearer <TOKEN>"
```
---

## GET `/api/v1/health/`
**Description**: Liveness & Queue Health Check

**Request Parameters / Body**:
`None`

**Response**:
`Health status of database and background worker pool`

### Example Curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/health/" -H "Authorization: Bearer <TOKEN>"
```
---
