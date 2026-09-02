"""End-to-End User Document Processing Workflow Test."""
import io

def test_e2e_document_upload_and_list(client, user_token):
    # 1. Upload sample text document
    file_content = b"INVOICE #9981\nSubtotal: $500.00\nTax: $50.00\nTotal: $550.00\nPayment Terms: Wire"
    files = [("files", ("invoice_e2e.txt", io.BytesIO(file_content), "text/plain"))]
    
    upload_res = client.post(
        "/api/v1/documents/upload",
        headers={"Authorization": f"Bearer {user_token}"},
        files=files
    )
    assert upload_res.status_code == 200
    docs = upload_res.json()
    assert len(docs) == 1
    doc_id = docs[0]["id"]

    # 2. List documents
    list_res = client.get("/api/v1/documents/", headers={"Authorization": f"Bearer {user_token}"})
    assert list_res.status_code == 200
    user_docs = list_res.json()
    assert any(d["id"] == doc_id for d in user_docs)

    # 3. Retrieve document details
    detail_res = client.get(f"/api/v1/documents/{doc_id}", headers={"Authorization": f"Bearer {user_token}"})
    assert detail_res.status_code == 200
    assert detail_res.json()["title"] == "Invoice E2E"
