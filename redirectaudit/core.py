from dataclasses import dataclass
from urllib.parse import urlparse
@dataclass(frozen=True)
class Hop:
    url:str
    status:int
    location:str|None=None
def validate_url(url):
    p=urlparse(url)
    if p.scheme not in {"http","https"} or not p.netloc: raise ValueError("URL must be absolute http/https.")
def analyze(hops):
    redirects=sum(h.status in {301,302,303,307,308} for h in hops)
    loop=bool(hops and hops[-1].status==0)
    final=None if loop or not hops else hops[-1].status
    return {"redirect_count":redirects,"loop_detected":loop,"final_status":final,
            "too_many_redirects":redirects>=5,
            "healthy":bool(hops) and not loop and redirects<5 and final is not None and final<400}
