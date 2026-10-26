import io
from app import create_app
from database import query_db, execute_db

def test_full_lifecycle():
    app = create_app()
    client = app.test_client()

    with app.app_context():
        # 1. Clean up old test data if exists
        execute_db("DELETE FROM resources WHERE title = 'Test Mid-Term Paper 2026 - Algorithms'")

        # 2. Student uploads paper
        with client.session_transaction() as sess:
            sess['user_id'] = 4
            sess['username'] = 'student1'
            sess['full_name'] = 'Aarav Patel'
            sess['role'] = 'student'

        data = {
            'title': 'Test Mid-Term Paper 2026 - Algorithms',
            'description': 'Student uploaded trial document for verification',
            'resource_type': 'Question Paper',
            'department_id': '1',
            'semester': '3',
            'subject_id': '1',
            'academic_year': '2025-2026',
            'exam_type': 'Mid-Term 1',
            'tags': 'algorithms, test',
            'file': (io.BytesIO(b'%PDF-1.4 sample content'), 'test_paper.pdf')
        }

        res = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
        assert res.status_code == 200
        print("[TEST 1/3] Student file upload POST -> 200 OK")

        # 3. Check DB for pending status
        res_db = query_db("SELECT id, status FROM resources WHERE title = 'Test Mid-Term Paper 2026 - Algorithms'", one=True)
        assert res_db is not None
        assert res_db['status'] == 'pending'
        test_id = res_db['id']
        print(f"[TEST 2/3] Resource ID {test_id} verified in DB with status = 'pending'")

        # 4. Admin approves
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['full_name'] = 'System Administrator'
            sess['role'] = 'admin'

        res_appr = client.post(f'/admin/approve/{test_id}', follow_redirects=True)
        assert res_appr.status_code == 200

        # 5. Check DB for approved status
        res_db_after = query_db("SELECT status FROM resources WHERE id = ?", (test_id,), one=True)
        assert res_db_after['status'] == 'approved'
        print(f"[TEST 3/3] Resource ID {test_id} successfully approved and status = 'approved'")

        # Clean up test row
        execute_db("DELETE FROM resources WHERE id = ?", (test_id,))

        print("\n========================================================")
        print(" ALL END-TO-END WORKFLOW TESTS VERIFIED SUCCESSFULLY!   ")
        print("========================================================")

if __name__ == '__main__':
    test_full_lifecycle()
