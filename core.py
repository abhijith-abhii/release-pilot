"""A bounded state-machine agent with real tools, branching and an audit trail."""
from pathlib import Path
import subprocess,sys,json,hashlib,re,os,time
ROOT=Path(__file__).parent

def run_agent(version,scenario='passing',engine='rules'):
 if not re.fullmatch(r'\d+\.\d+\.\d+',version):raise ValueError('Use major.minor.patch version format')
 if scenario not in ['passing','failing']:raise ValueError('Unknown scenario')

 if engine not in ['rules','local-llm']:raise ValueError('Unsupported engine')
 workspace=ROOT/'examples'/scenario;runroot=Path(os.environ.get('PILOT_RUNS',ROOT/'var/runs'));runroot.mkdir(parents=True,exist_ok=True)
 files=sorted(workspace.glob('*.py'));digest=hashlib.sha256(b''.join(f.name.encode()+f.read_bytes() for f in files)+(workspace/'changes.json').read_bytes()+version.encode()+engine.encode()+Path(__file__).read_bytes()).hexdigest()[:16];output=runroot/(digest+'.json')
 if output.exists():return json.loads(output.read_text())|{'reused':True}
 trace=[]
 def record(tool,status,detail):trace.append({'step':len(trace)+1,'tool':tool,'status':status,'detail':detail})
 # Policies and observations determine the next tool; no arbitrary shell commands.
 unsafe=[f.name for f in files if re.search(r'(?:ghp_|sk_live_)[A-Za-z0-9]{16,}',f.read_text())]
 record('inspect_workspace','failed' if unsafe else 'passed',{'files':[f.name for f in files],'suspected_secrets':unsafe})
 if unsafe:status='blocked'
 else:
  start=time.monotonic()
  try:r=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(workspace),'-v'],cwd=workspace,text=True,capture_output=True,timeout=20)
  except subprocess.TimeoutExpired:r=None
  record('run_tests','passed' if r and r.returncode==0 else 'failed',{'exit_code':r.returncode if r else None,'seconds':round(time.monotonic()-start,4),'output':(r.stdout+r.stderr)[-10000:] if r else 'Timed out'})
  if not r or r.returncode:status='blocked'
  else:
   changes=json.loads((workspace/'changes.json').read_text())
   if not isinstance(changes,list) or any(set(x)!={'type','description'} for x in changes):raise ValueError('Invalid change manifest')
   draft='# Release '+version+'\n\n'+''.join('- '+x['type']+': '+x['description']+'\n' for x in changes)

   if engine=='local-llm':
    summary=summarize_changes(changes);supported=summary_supported(summary,changes);draft+='\n## Model-generated summary (review required)\n\n'+(summary if supported else 'Model summary withheld: unsupported wording. Use the verified change list above.')+'\n';record('summarize_changes','passed' if supported else 'withheld',{'model':'google/flan-t5-small','raw_output':summary,'lexical_support_check':supported})
   (runroot/(digest+'.md')).write_text(draft);record('write_review_draft','passed',{'artifact':digest+'.md','text':draft});status='ready_for_review'
 report={'run_id':digest,'version':version,'scenario':scenario,'status':status,'trace':trace,'reused':False,'planner':'policy-constrained state-machine agent','summary_engine':engine,'published':False}
 temp=output.with_suffix('.tmp');temp.write_text(json.dumps(report,indent=2));temp.replace(output);return report

def analyze(p):
 r=run_agent(p.get('version','1.1.0'),p.get('scenario','passing'),p.get('engine','rules'))
 return dict(metrics={'Status':r['status'],'Tools executed':len(r['trace']),'Cached run':r['reused']},rows=[dict(step=x['step'],tool=x['tool'],status=x['status']) for x in r['trace']],answer=r['trace'][-1]['detail'].get('text','No release draft produced; inspect failed checks.'),details=r,notice='Actual local tool execution. Rules enforce tool order and block failed tests. Local-llm mode generates a review summary; rules mode uses only the change manifest. Nothing is published.')

from functools import lru_cache
@lru_cache(maxsize=1)
def load_model():
 from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
 import torch
 torch.set_num_threads(4);source=os.environ.get('PILOT_MODEL',str(ROOT/'var/model'))
 if not Path(source).exists():raise ValueError('Model missing. Run python download_model.py or select rules mode.')
 return AutoTokenizer.from_pretrained(source),AutoModelForSeq2SeqLM.from_pretrained(source).eval()
def summarize_changes(changes):
 import torch
 tokenizer,model=load_model();prompt='Summarize the following software changes in one sentence: '+ ' '.join(x['description'] for x in changes)
 x=tokenizer(prompt,return_tensors='pt',truncation=True,max_length=384)
 with torch.no_grad():return tokenizer.decode(model.generate(**x,max_new_tokens=60)[0],skip_special_tokens=True)

def summary_supported(summary,changes):
 words=lambda t:set(re.findall(r'[a-z]+',t.lower()))
 stop={'a','an','the','and','or','to','of','for','in','on','with','is','are','be','this','that','it','by','as','from','can','now','will','has','have'}
 source=words(' '.join(x['description'] for x in changes))
 claimed=words(summary)-stop
 return bool(claimed) and len(claimed-source)==0
