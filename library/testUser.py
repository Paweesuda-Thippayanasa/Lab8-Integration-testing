# ปวีณ์สุดา ทิพยนาสา 653380137-5 sec.1
import pytest
from main import User

@pytest.mark.parametrize(
    "username, fullname",
    [
        ("test_username1", "test_fullname1"),
        ("test_username2", "test_fullname2"),
        ("test_USR_emptyFull", ""),
        ("", "test_FUllname_emptyUSR"),
        ("", "")
    ]
)
def test_add_user(db_session, username, fullname):
    new_user = User(username=username, fullname=fullname)
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User).filter_by(username=username).first()
    assert user is not None
    assert user.username == username
    assert user.fullname == fullname
    

@pytest.mark.parametrize(
    "username, fullname",
    [
        ("test_username1", "test_fullname1"),
        ("test_username2", "test_fullname2"),
        ("test_USR_emptyFull", ""),
        ("", "test_FUllname_emptyUSR"),
        ("", "")
    ]
)
def test_delete_user(db_session, username, fullname):
    user = User(username=username, fullname=fullname)
    db_session.add(user)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    deleted_user = db_session.query(User).filter_by(username=username).first()
    assert deleted_user is None
