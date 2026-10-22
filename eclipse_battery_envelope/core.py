from .common import number,unique_ids

def interval(x,low,high):
    a,b=x;number(a,low,high);number(b,a,high);return a,b

def run(data):
    cap=number(data['capacity_wh'],1e-9,1e12);reserve=number(data.get('reserve_wh',0),0,cap)
    lo,hi=interval(data['initial_wh'],0,cap);charge=number(data.get('charge_efficiency',1),1e-9,1);discharge=number(data.get('discharge_efficiency',1),1e-9,1)
    segs=data['segments']
    if len(segs)>10000:raise ValueError('size')
    unique_ids(segs);time=0;trace=[];first=0 if lo<reserve else None;unmet=0
    for s in segs:
        dt=number(s['duration_hours'],0,1e9);gl,gh=interval(s['generation_w'],0,1e12);ll,lh=interval(s['load_w'],0,1e12)
        # Declared bus model: generation passes charge efficiency, load passes discharge efficiency.
        worst=gl*charge-lh/discharge;best=gh*charge-ll/discharge
        before_lo=lo;rawlo=lo+worst*dt;rawhi=hi+best*dt
        if first is None and min(lo,rawlo)<reserve:
            first=time if lo<reserve else time+(lo-reserve)/(-worst)
        deficit=max(0,-rawlo);unmet+=deficit
        lo=min(cap,max(0,rawlo));hi=min(cap,max(0,rawhi))
        trace.append({'id':s['id'],'start_hours':time,'end_hours':time+dt,'charge_wh':[lo,hi],'worst_case_unserved_wh':deficit,'possible_curtailment_wh':max(0,rawhi-cap),'guaranteed_curtailment_wh':max(0,rawlo-cap),'minimum_worst_case_wh':min(before_lo,rawlo)})
        time+=dt
    return {'charge_wh':[lo,hi],'first_worst_case_reserve_crossing_hours':first,'guaranteed_reserve':first is None,'worst_case_unserved_wh':unmet,'trace':trace,'model':'independent rectangular piecewise-constant generation/load bounds; clamped battery; no dynamics'}
