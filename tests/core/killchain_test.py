"""Tests for Yeti vocabs"""
import pytest

from yeti.core.model.settings.killchains import KillChains
from yeti.core.model.settings.setting import Setting

@pytest.mark.usefixtures('clean_db', 'populate_settings')
def test_create_killchain_setting():
    """Tests that killchain settings can be fetched"""
    kc = Setting.get_or_create(name='my_killchain', type='killchain')
    assert isinstance(kc, KillChains)
    kc_ = KillChains.get(kc.id)
    assert kc_ is not None
    assert kc.id == kc_.id
    assert kc_.name == 'my_killchain'
