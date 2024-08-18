# ปวีณ์สุดา ทิพยนาสา 653380137-5 sec.1
import pytest
from main import Book

@pytest.mark.parametrize(
    "title, firstauthor, isbn",
    [
        ("test_title1", "test_Au1", "12345"),
        ("test_title2", "test_Au2", "12222"),
        ("test_title3", "test_Au3", "12345"),
        ("", "test_Au4", "54321"),
        ("test_title5", " ", "11111"),
        ("test_title6", "test_Au6", ""),
        ("", "", "")
    ]
)
def test_add_book(db_session, title, firstauthor, isbn):
    new_book = Book(title=title, firstauthor=firstauthor, isbn=isbn)
    db_session.add(new_book)
    db_session.commit()
    
    book = db_session.query(Book).filter_by(title=title).first()
    assert book is not None
    assert book.title == title
    assert book.firstauthor == firstauthor
    assert book.isbn == isbn

@pytest.mark.parametrize(
    "title, firstauthor, isbn",
    [
        ("test_title1", "test_Au1", "12345"),
        ("test_title2", "test_Au2", "12222"),
        ("test_title3", "test_Au3", "12345"),
        ("", "test_Au4", "54321"),
        ("test_title5", " ", "11111"),
        ("test_title6", "test_Au6", ""),
        ("", "", "")
    ]
)
def test_delete_book(db_session, title, firstauthor, isbn):
    book = Book(title=title, firstauthor=firstauthor, isbn=isbn)
    db_session.add(book)
    db_session.commit()

    db_session.delete(book)
    db_session.commit()
    
    deleted_book = db_session.query(Book).filter_by(title=title).first()
    assert deleted_book is None
