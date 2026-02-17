import pytest
from app.example import add, multiply, BankAccount

@pytest.mark.parametrize("a, b, res", [
    (2, 3, 5), (5, 5, 10), (-1, -1, -2)
])
def test_add(a, b, res) :
    print ("Testing add function")
    assert add(a, b) == res


@pytest.mark.parametrize ("a, b, res", [
    (1, 1, 1), (1, 2, 2), (0, 0, 0),
    (-1, -1, 1), (-1, 0, 0)
])
def test_multiply(a, b, res) :
    print ("Testing multiply function")
    assert multiply(a, b) == res


### Tests for class BankAccount ###

def test_init_bank_account() :
    bank_account = BankAccount(120)
    assert bank_account.balance == 120

def test_default_init_bank_account() :
    bank_account = BankAccount()
    assert bank_account.balance == 0

def test_withdraw() :
    bank_account = BankAccount(120)
    bank_account.withdraw(69)
    assert bank_account.balance == 51

def test_deposit():
    bank_account = BankAccount(120)
    bank_account.deposit(81)
    assert bank_account.balance == 201

def test_interest():
    bank_account = BankAccount(120)
    bank_account.collect_interest()

    assert int(bank_account.balance) == 132