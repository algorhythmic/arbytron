import pytest
from services.position import PortfolioManager, Position

@pytest.fixture
def manager():
    return PortfolioManager()

def test_record_buy_and_avg_cost(manager):
    # initial buy
    manager.record_fill('e1', 'Yes', size=10, price=0.5, side='BUY')
    pos = manager.positions[('e1', 'Yes')]
    assert pos.quantity == 10
    assert pos.avg_cost == pytest.approx(0.5)
    # additional buy
    manager.record_fill('e1', 'Yes', size=10, price=0.7, side='BUY')
    pos = manager.positions[('e1', 'Yes')]
    assert pos.quantity == 20
    # avg_cost = (0.5*10 + 0.7*10) / 20 = 0.6
    assert pos.avg_cost == pytest.approx((0.5*10 + 0.7*10) / 20)

def test_record_sell(manager):
    # initial buy then sell
    manager.record_fill('e2', 'No', size=5, price=0.4, side='BUY')
    manager.record_fill('e2', 'No', size=2, price=0.0, side='SELL')
    pos = manager.positions[('e2', 'No')]
    assert pos.quantity == 3
    # avg_cost remains unchanged on sell
    assert pos.avg_cost == pytest.approx(0.4)

def test_compute_pnls_and_get_exits(manager):
    # set up positions
    manager.record_fill('e3', 'Yes', size=5, price=0.2, side='BUY')
    manager.record_fill('e3', 'No', size=5, price=0.3, side='BUY')
    latest_prices = {('e3', 'Yes'): 0.6, ('e3', 'No'): 0.1}
    pnls = manager.compute_pnls(latest_prices)
    # Yes: (0.6-0.2)*5=2.0, No: (0.1-0.3)*5=-1.0
    assert pnls[('e3', 'Yes')] == pytest.approx((0.6-0.2)*5)
    assert pnls[('e3', 'No')] == pytest.approx((0.1-0.3)*5)
    # get exits threshold=1.0, should only include Yes
    exits = manager.get_exits(latest_prices, threshold=1.0)
    assert len(exits) == 1
    assert isinstance(exits[0], Position)
    assert exits[0].outcome == 'Yes'
