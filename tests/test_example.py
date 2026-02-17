from app.example import add, multiply

def test_add() :
    print ("Testing add function")
    assert add(8, 5) == 13

def test_multiply() :
    print ("Testing multiply function")
    assert multiply(8, 5) == 40
