# ปวีณ์สุดา ทิพยนาสา 653380137-5 sec.1

import pytest
from fastapi.testclient import TestClient
from main import app, User, Book, Borrowlist, get_db

# Fixture to create a test client with a database session
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Test for creating a borrow list
@pytest.mark.parametrize(
    "username, fullname, title, firstauthor, isbn",
    [
        ("test_username1", "test_fullname1", "test_title1", "test_Au1", "12345"),
        ("test_username2", "test_fullname2", "test_title2", "test_Au2", "12222"),
        ("test_USR_emptyFull", "", "test_title3", "test_Au3", "12345"),
        ("", "test_FUllname_emptyUSR", "test_title4", "test_Au4", "54321"),
        ("", "", "", "", "")
    ]
)
def test_create_borrowlist(client, db_session, username, fullname, title, firstauthor, isbn):
    # Create a user and a book
    user = User(username=username, fullname=fullname)
    book = Book(title=title, firstauthor=firstauthor, isbn=isbn)
    db_session.add(user)
    db_session.add(book)
    db_session.commit()

    # Create a borrowing record
    response = client.post(f"/borrowlist/?user_id={user.id}&book_id={book.id}")
    assert response.status_code == 200

    # Verify the borrowing record in the database
    borrowlist = db_session.query(Borrowlist).filter_by(user_id=user.id, book_id=book.id).first()
    assert borrowlist is not None

# Test for retrieving a borrow list
@pytest.mark.parametrize(
    "username, fullname, title, firstauthor, isbn",
    [
        ("test_username1", "test_fullname1", "test_title1", "test_Au1", "12345"),
        ("test_username2", "test_fullname2", "test_title2", "test_Au2", "12222"),
        ("test_USR_emptyFull", "", "test_title3", "test_Au3", "12345"),
        ("", "test_FUllname_emptyUSR", "test_title4", "test_Au4", "54321"),
        ("", "", "", "", "")
    ]
)
def test_get_borrowlist(client, db_session, username, fullname, title, firstauthor, isbn):
    # Create a user and a book
    user = User(username=username, fullname=fullname)
    book = Book(title=title, firstauthor=firstauthor, isbn=isbn)
    db_session.add(user)
    db_session.add(book)
    db_session.commit()

    # Create a borrowing record
    borrowlist = Borrowlist(user_id=user.id, book_id=book.id)
    db_session.add(borrowlist)
    db_session.commit()

    # Retrieve the borrow list
    response = client.get(f"/borrowlist/{user.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == user.id
    assert response.json()[0]["book_id"] == book.id
