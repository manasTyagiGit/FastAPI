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

## Default value fixture
@pytest.fixture
def init_default_bank_account() :
    return BankAccount()

# Parameterised Fixture
@pytest.fixture
def bank_account() :
    return BankAccount(120)

def test_init_bank_account(bank_account) :
    assert bank_account.balance == 120

def test_default_init_bank_account(init_default_bank_account) :
    assert init_default_bank_account.balance == 0

@pytest.mark.parametrize ("withdrawn, bal", [
    (69, 51), (120, 0)
])
def test_withdraw(bank_account, withdrawn, bal) :
    bank_account.withdraw(withdrawn)
    assert bank_account.balance == bal

@pytest.mark.parametrize ("dep, bal", [
    (81, 201), (22, 142)
])
def test_deposit(bank_account, dep, bal):
    bank_account.deposit(dep)
    assert bank_account.balance == bal

@pytest.mark.parametrize ("times, bal", [
    (1, 132), (2, 145), (5, 193)
])
def test_interest(bank_account, times, bal):

    for i in range (0, times) :
        bank_account.collect_interest()

    assert int(bank_account.balance) == bal

@pytest.mark.parametrize ("deposited, withdrawn, remaining", [
    (100, 100, 0), (120, 50, 70), (212, 75, 137)
])
def test_transaction(init_default_bank_account, deposited, withdrawn, remaining) :
    init_default_bank_account.deposit(deposited)
    init_default_bank_account.withdraw(withdrawn)

    assert init_default_bank_account.balance == remaining
