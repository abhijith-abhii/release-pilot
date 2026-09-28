import pytest
from core import run_agent
@pytest.fixture(autouse=True)
def isolated(tmp_path,monkeypatch):monkeypatch.setenv('PILOT_RUNS',str(tmp_path))
def test_pass_and_idempotency():
 r=run_agent('1.0.0');assert r['status']=='ready_for_review';assert r['trace'][1]['detail']['exit_code']==0
 assert run_agent('1.0.0')['reused']
def test_failure_blocks_draft():
 r=run_agent('1.0.0','failing');assert r['status']=='blocked';assert len(r['trace'])==2
@pytest.mark.parametrize('v',['bad','1.0','1.0.0; rm -rf /'])
def test_invalid_version(v):
 with pytest.raises(ValueError):run_agent(v)

from core import summary_supported
def test_unsupported_model_summary_withheld():
 changes=[{'description':'Reject negative prices.'}]
 assert not summary_supported('Remove customer accounts.',changes)
 assert summary_supported('Reject negative prices.',changes)
