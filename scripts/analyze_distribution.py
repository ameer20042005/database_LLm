# -*- coding: utf-8 -*-
"""تحليل توزيع وتنوع بيانات التدريب — يعيد إنتاج منطق الخلية 6 محلياً."""
import glob, json, math, os, re, sys, io, hashlib
from collections import Counter, defaultdict
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUT = {}

def load(files):
    return pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)

v8  = sorted(glob.glob(os.path.join(D, "iraqi_train_v8_part*.jsonl")))
v9  = sorted(glob.glob(os.path.join(D, "iraqi_v9_generated*.jsonl")))
v10 = sorted(glob.glob(os.path.join(D, "iraqi_v10_*.jsonl")))
v11 = sorted(glob.glob(os.path.join(D, "iraqi_v11_gaps.jsonl")))
v12 = sorted(glob.glob(os.path.join(D, "iraqi_v12_order.jsonl")))
v13 = sorted(glob.glob(os.path.join(D, "iraqi_v13_scope.jsonl")))
val_files = [os.path.join(D, "iraqi_val_v8.jsonl"),
             os.path.join(D, "iraqi_val_v13.jsonl")]

FILE_GROUPS = {"v8": v8, "v9": v9, "v10": v10, "v11": v11, "v12": v12,
               "v13": v13}
raw_by_group = {}
for g, fs in FILE_GROUPS.items():
    r = load(fs)
    if "category" not in r.columns: r["category"] = "?"
    r["batch"] = g
    raw_by_group[g] = r
val_df = load(val_files)

TARGET_PER_STEP, EFFECTIVE_BATCH, TARGET_GENERAL_RATIO = 0.10, 32, 0.15
BOOST = {("v11","gap6_anti_sycophancy"):2.4, ("v12","ord1_marker_positive"):1.3,
         ("v12","ord2_marker_withheld"):2.0, ("v12","ord4_submit_refusal"):1.5}
WEIGHT_CAP = {("v10","items_dual_form"):12}
MAX_WEIGHT = 8          # لا BASE_GROUP: كل الفئات تمر بالموازِن

_sizes = {(g,c):n for g,r in raw_by_group.items()
          for c,n in r["category"].value_counts().items()}
W = {k:1 for k in _sizes}
for _ in range(80):
    iraqi = sum(_sizes[k]*W[k] for k in _sizes)
    steps = (iraqi/(1-TARGET_GENERAL_RATIO))/EFFECTIVE_BATCH
    ch=False
    for k,n in _sizes.items():
        want = math.ceil(TARGET_PER_STEP*steps*BOOST.get(k,1)/n)
        want = min(max(want,1), WEIGHT_CAP.get(k,MAX_WEIGHT))
        if W[k]!=want: W[k]=want; ch=True
    if not ch: break

parts, rows_log = [], []
for g,r in raw_by_group.items():
    r=r.copy(); r["_w"]=[W.get((g,c),1) for c in r["category"]]
    rep=r.loc[r.index.repeat(r["_w"])].reset_index(drop=True)
    parts.append(rep); rows_log.append((g,len(r),len(rep)))
train_df = pd.concat(parts, ignore_index=True)

# تلوث
key=lambda m: json.dumps(m, ensure_ascii=False, sort_keys=True)
vk=set(val_df["messages"].apply(key))
leak=train_df["messages"].apply(key).isin(vk)
n_leak=int(leak.sum())
train_df=train_df[~leak].reset_index(drop=True)

P=print
P("="*78); P("١) حجم الملفات الخام مقابل ما يدخل التدريب فعلاً"); P("="*78)
all_files = sorted(glob.glob(os.path.join(D,"*.jsonl")))
used = set(v8+v9+v10+v11+v12+v13+val_files)
tot_lines_all = 0
P(f"{'الملف':<38}{'أسطر':>9}  مستخدم؟")
for f in all_files:
    n=sum(1 for _ in open(f,encoding='utf-8')); tot_lines_all+=n
    P(f"{os.path.basename(f):<38}{n:>9,}  {'✅' if f in used else '—'}")
P(f"{'المجموع بمجلد data/':<38}{tot_lines_all:>9,}")
P(f"\nالمستخدم فعلاً: تدريب خام {sum(len(r) for r in raw_by_group.values()):,} + تقييم {len(val_df):,}")

P(); P("="*78); P("٢) الدفعات بعد الترجيح"); P("="*78)
tot=len(train_df)
steps=(tot/(1-TARGET_GENERAL_RATIO))/EFFECTIVE_BATCH
P(f"{'الدفعة':<7}{'خام':>9}{'بعد الترجيح':>14}{'%':>9}{'تضخيم':>9}")
for g,nr,nrep in rows_log:
    P(f"{g:<7}{nr:>9,}{nrep:>14,}{100*nrep/tot:>8.2f}%{nrep/nr:>8.1f}×")
P(f"{'مجموع':<7}{sum(r[1] for r in rows_log):>9,}{tot:>14,}{100:>8.2f}%")
P(f"خطوات تقديرية ≈ {steps:,.0f} (بعد إضافة Aya {TARGET_GENERAL_RATIO:.0%})")
P(f"تلوث train/val محذوف: {n_leak:,}")

P(); P("="*78); P("٣) توزيع الفئات — خام / مرجّح / حصة لكل خطوة"); P("="*78)
for g in FILE_GROUPS:
    r=raw_by_group[g]
    P(f"\n▌{g}  ({len(r):,} خام)")
    vc=r["category"].value_counts()
    for c,n in vc.items():
        w=W.get((g,c),1); share=n*w/steps
        flags=[]
        if (g,c) in BOOST: flags.append("معزّزة")
        if (g,c) in WEIGHT_CAP: flags.append("مسقوفة")
        if share<0.08: flags.append("تحت العتبة")
        P(f"   {c:<34}{n:>7,} ×{w:<3}= {n*w:>7,}  {share:>6.3f}/خطوة  {' '.join(flags)}")

P(); P("="*78); P("٤) توزيع فئات التقييم (val_v8)"); P("="*78)
if "category" in val_df.columns:
    vc=val_df["category"].value_counts()
    for c,n in vc.items(): P(f"   {c:<40}{n:>7,}  {100*n/len(val_df):>6.2f}%")
    P(f"   {'المجموع':<40}{len(val_df):>7,}")
    # تطابق فئات التدريب/التقييم
    tr_cats=set(train_df["category"].unique()); v_cats=set(vc.index)
    P(f"\n   فئات بالتدريب غير مقيَّمة: {len(tr_cats-v_cats)}")
    for c in sorted(tr_cats-v_cats): P(f"      - {c}")
    P(f"   فئات بالتقييم غير مدرَّبة: {sorted(v_cats-tr_cats)}")

P(); P("="*78); P("٥) بنية المحادثة: الأدوار والأطوال"); P("="*78)
def stats(df,label):
    turns=[]; sysn=0; ulen=[]; alen=[]; achars=[]
    for m in df["messages"]:
        turns.append(len(m))
        if m and m[0].get("role")=="system": sysn+=1
        for t in m:
            if t["role"]=="user": ulen.append(len(t["content"].split()))
            elif t["role"]=="assistant":
                alen.append(len(t["content"].split())); achars.append(len(t["content"]))
    s=pd.Series(turns)
    P(f"\n▌{label}  (n={len(df):,})")
    P(f"   أدوار/محادثة: متوسط {s.mean():.2f} | وسيط {s.median():.0f} | "
      f"p10 {s.quantile(.10):.0f} | p90 {s.quantile(.90):.0f} | أقصى {s.max()}")
    P(f"   فيها system: {sysn:,} ({100*sysn/len(df):.1f}%)")
    P(f"   طول رد المستخدم (كلمات):  متوسط {pd.Series(ulen).mean():.1f} | وسيط {pd.Series(ulen).median():.0f}")
    P(f"   طول رد المساعد (كلمات):   متوسط {pd.Series(alen).mean():.1f} | وسيط {pd.Series(alen).median():.0f} | p95 {pd.Series(alen).quantile(.95):.0f}")
    P(f"   طول رد المساعد (حروف):    متوسط {pd.Series(achars).mean():.1f} | p95 {pd.Series(achars).quantile(.95):.0f}")
    return Counter(turns)
tc_raw = pd.concat([raw_by_group[g] for g in FILE_GROUPS], ignore_index=True)
stats(tc_raw,"التدريب (خام، قبل الترجيح)")
stats(train_df,"التدريب (بعد الترجيح)")
stats(val_df,"التقييم")

P(); P("="*78); P("٦) التنوع المعجمي والتكرار"); P("="*78)
def diversity(df,label,sample=None):
    d = df.sample(min(sample or len(df), len(df)), random_state=0) if sample else df
    users=[]; asst=[]
    for m in d["messages"]:
        for t in m:
            (users if t["role"]=="user" else asst if t["role"]=="assistant" else []).append(t["content"])
    def tt(xs):
        toks=[w for x in xs for w in re.findall(r'[\w\u0600-\u06FF]+',x)]
        return len(set(toks)), len(toks)
    uu,ut=tt(users); au,at=tt(asst)
    P(f"\n▌{label}")
    P(f"   مفردات فريدة (المستخدم): {uu:,} من {ut:,} توكن  → TTR {uu/max(ut,1):.4f}")
    P(f"   مفردات فريدة (المساعد):  {au:,} من {at:,} توكن  → TTR {au/max(at,1):.4f}")
    cu=Counter(users); ca=Counter(asst)
    P(f"   ردود مستخدم فريدة: {len(cu):,}/{len(users):,} ({100*len(cu)/max(len(users),1):.1f}%)")
    P(f"   ردود مساعد فريدة:  {len(ca):,}/{len(asst):,} ({100*len(ca)/max(len(asst),1):.1f}%)")
    P("   أكثر 8 ردود مساعد تكراراً:")
    for s,n in ca.most_common(8):
        P(f"      {n:>6,}×  {s[:60]}")
    return ca
diversity(tc_raw,"التدريب الخام")
diversity(val_df,"التقييم")

P(); P("="*78); P("٧) تكرار المحادثات (نسخ متطابقة)"); P("="*78)
for label,df in [("خام",tc_raw),("مرجّح",train_df),("تقييم",val_df)]:
    k=df["messages"].apply(key)
    d=len(k)-k.nunique()
    P(f"   {label:<8} محادثات {len(k):>8,} | فريدة {k.nunique():>8,} | مكررة {d:>8,} ({100*d/len(k):.2f}%)")

P(); P("="*78); P("٨) علامات وظيفية حرجة"); P("="*78)
MARKERS = {"[ORDER_READY]":"علامة جاهزية الطلب", "[TOOL_CALL]":"استدعاء أداة",
           "[TOOL_RESULT]":"نتيجة أداة", "```json":"كتلة JSON",
           '"order"':"مخطط طلب", '"items"':"مخطط عناصر", "status":"وسيط status",
           '"all"':"وسيط all", "order_id":"وسيط order_id", "phone":"وسيط phone"}
def mk(df,label):
    txt_a=defaultdict(int); txt_u=defaultdict(int)
    for m in df["messages"]:
        blob_a=" ".join(t["content"] for t in m if t["role"]=="assistant")
        blob_o=" ".join(t["content"] for t in m if t["role"]!="assistant")
        for tok in MARKERS:
            if tok in blob_a: txt_a[tok]+=1
            if tok in blob_o: txt_u[tok]+=1
    P(f"\n▌{label} (n={len(df):,})")
    P(f"   {'العلامة':<16}{'بردود المساعد':>16}{'%':>9}{'بغير المساعد':>16}")
    for tok,desc in MARKERS.items():
        P(f"   {tok:<16}{txt_a[tok]:>16,}{100*txt_a[tok]/len(df):>8.3f}%{txt_u[tok]:>16,}   {desc}")
mk(tc_raw,"التدريب الخام")
mk(train_df,"التدريب المرجّح")
mk(val_df,"التقييم")

P(); P("="*78); P("٩) نسبة العلامة سالب:موجب بـv12"); P("="*78)
v12t=train_df.loc[train_df["batch"]=="v12","category"]
pos=int((v12t=="ord1_marker_positive").sum())
neg=int(v12t.isin(["ord2_marker_withheld","ord3_confirm_gate","ord4_submit_refusal"]).sum())
r12=raw_by_group["v12"]["category"]
rpos=int((r12=="ord1_marker_positive").sum())
rneg=int(r12.isin(["ord2_marker_withheld","ord3_confirm_gate","ord4_submit_refusal"]).sum())
P(f"   خام:    سالب {rneg:,} : موجب {rpos:,} = 1:{rneg/max(rpos,1):.2f}")
P(f"   مرجّح:  سالب {neg:,} : موجب {pos:,} = 1:{neg/max(pos,1):.2f}   (النطاق المقبول 2.5–5.0)")

P(); P("="*78); P("١٠) تغطية اللهجة العراقية"); P("="*78)
IRAQI = ["شلون","شنو","هواي","اكو","ماكو","گاعد","هسه","زين","چا","وياك","عدنا","خوش",
         "شگد","ليش","وين","تره","يمعود","دزلي","اشوف","بس","هاي","هاذ","يمّه","عمي",
         "مو","جان","لك","ابو","خالة","تكدر","اريد","صاير","شوكت"]
GULF_MSA_MARK=["ماذا","كيف حالك","الآن","نعم","لماذا","أين","جداً"]
def dial(df,label):
    hits=Counter(); n_iraqi=0
    for m in df["messages"]:
        blob=" ".join(t["content"] for t in m)
        h=[w for w in IRAQI if w in blob]
        for w in h: hits[w]+=1
        if h: n_iraqi+=1
    P(f"\n▌{label} — محادثات فيها ≥1 علامة عراقية: {n_iraqi:,}/{len(df):,} ({100*n_iraqi/len(df):.1f}%)")
    P("   أكثر 15 علامة:")
    for w,n in hits.most_common(15): P(f"      {w:<10}{n:>8,}  ({100*n/len(df):>5.1f}%)")
dial(tc_raw,"التدريب الخام"); dial(val_df,"التقييم")

P(); P("="*78); P("١١) الفئات: التركّز (Gini/هيرفندال) والذيل"); P("="*78)
def conc(vc,label):
    p=(vc/vc.sum()).values
    hhi=float((p**2).sum())
    ent=float(-(p*pd.np.log(p)).sum()) if hasattr(pd,'np') else float(-sum(x*math.log(x) for x in p))
    P(f"   {label:<24} فئات {len(vc):>4} | HHI {hhi:.4f} | إنتروبيا {ent:.3f} / أقصى {math.log(len(vc)):.3f} "
      f"| تكافؤ {ent/math.log(len(vc)):.3f} | أكبر فئة {100*p[0]:.2f}%")
conc(tc_raw["category"].value_counts(),"التدريب الخام")
conc(train_df["category"].value_counts(),"التدريب المرجّح")
conc(val_df["category"].value_counts(),"التقييم")
P("\n   ذيل التدريب الخام (أصغر 12 فئة):")
for c,n in tc_raw["category"].value_counts().tail(12).items():
    P(f"      {c:<36}{n:>6,}")
