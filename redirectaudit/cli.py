import argparse,json
from urllib.request import Request,build_opener,HTTPRedirectHandler
from urllib.error import HTTPError,URLError
from urllib.parse import urljoin
from .core import Hop,analyze,validate_url
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl): return None
def inspect(url,max_hops=10,timeout=5):
    validate_url(url)
    if not 1<=max_hops<=30: raise ValueError("max_hops must be between 1 and 30")
    opener=build_opener(NoRedirect()); out=[]; current=url; seen=set()
    for _ in range(max_hops):
        if current in seen: out.append(Hop(current,0,"redirect-loop")); return out
        seen.add(current); req=Request(current,headers={"User-Agent":"RedirectAudit/0.1"})
        try:
            res=opener.open(req,timeout=timeout); status=res.status; loc=res.headers.get("Location"); res.close()
        except HTTPError as e: status=e.code; loc=e.headers.get("Location")
        except URLError as e: raise RuntimeError(str(e.reason))
        out.append(Hop(current,status,loc))
        if status not in {301,302,303,307,308} or not loc:return out
        current=urljoin(current,loc)
    return out
def main(argv=None):
    p=argparse.ArgumentParser(description="Audit an HTTP redirect chain.");p.add_argument("url");p.add_argument("--json",action="store_true");p.add_argument("--max-hops",type=int,default=10);a=p.parse_args(argv)
    try:hops=inspect(a.url,a.max_hops)
    except (ValueError,RuntimeError) as e:p.error(str(e))
    result=analyze(hops); payload={"result":result,"hops":[h.__dict__ for h in hops]}
    if a.json:print(json.dumps(payload,indent=2))
    else:
        for i,h in enumerate(hops,1):print(i,h.status,h.url,("-> "+h.location) if h.location else "")
        print("Healthy:",result["healthy"])
    return 0 if result["healthy"] else 2
if __name__=="__main__":raise SystemExit(main())
