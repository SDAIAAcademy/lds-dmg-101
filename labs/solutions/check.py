# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Run the reference solution of every lab against the course files and check it.

    uv run labs/solutions/check.py            # all labs
    uv run labs/solutions/check.py 2.2 3.2    # some labs

Every lab of this course is done in a spreadsheet, a diagram or a written decision; none calls a
model. This script does what the reference solution does on the files (counts, filters, rule
checks, cross-references to the charter and the guides) and checks the answer keys in
solutions/reference/ against the files, so a key that the files do not support fails here. It
prints the numbers the debrief slides quote and PASS per lab. Nothing is written to disk.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
FILES = HERE.parent / "files"
REF = HERE / "reference"
LABS: dict = {}


def lab(lab_id):
    def wrap(fn):
        LABS[lab_id] = fn
        return fn
    return wrap


def ref(name):
    return json.loads((REF / name).read_text(encoding="utf-8"))


def text(rel):
    return (FILES / rel).read_text(encoding="utf-8")


def rows(rel, sheet):
    ws = openpyxl.load_workbook(FILES / rel, read_only=True)[sheet]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it]


def as_date(v):
    if v is None or v == "":
        return None
    return v.date() if isinstance(v, datetime) else v


def charter_lines():
    """Role name -> the text of its section in the charter."""
    out, cur = {}, None
    for line in text("governance_charter.txt").splitlines():
        m = re.match(r"2\.\d+ (.+)$", line.strip())
        if m:
            cur = re.sub(r" \(.*\)$", "", m.group(1))
            out[cur] = ""
        elif cur:
            out[cur] += line.strip() + " "  # one line per role, so an artefact split over two lines is still found
    return out


@lab("1.1")
def lab_1_1():
    key = ref("lab_1_1.json")
    file_rows = rows("lifecycle_events.xlsx", "الأحداث")
    assert len(key) == len(file_rows) == 12
    assert [r["الحدث في ملف الأسرة"] for r in file_rows] == [k["event"] for k in key]
    stages = Counter(k["stage"] for k in key)
    assert set(stages) == {"الإنشاء والجمع", "التخزين", "الاستخدام", "المشاركة والنشر", "الأرشفة", "الإتلاف"}, stages
    kinds = Counter(k["kind"] for k in key)
    # every governance event is a decision (approve, decide, define), every management event is an action
    for k in key:
        decision = any(w in k["event"] for w in ("اعتماد", "موافقة", "تحديد"))
        assert decision == (k["kind"] == "حوكمة"), k
    print(f"  12 events, every stage used; governance {kinds['حوكمة']}, management {kinds['إدارة']}")


@lab("1.2")
def lab_1_2():
    key = ref("lab_1_2.json")
    ch = charter_lines()
    assert len(key) == 14
    for k in key:
        assert k["role"] in ch, k["role"]
        assert k["artefact"] in ch[k["role"]], (k["artefact"], k["role"])
    lists = rows("domain_map.xlsx", "القوائم")
    artefacts = [r["مخرجات العمل (فيها ثلاثة لا تخص مجالًا بعينه)"] for r in lists]
    assert len(artefacts) == 17 and len(set(k["artefact"] for k in key)) == 14
    extra = sorted(set(artefacts) - {k["artefact"] for k in key})
    roles = Counter(k["role"] for k in key)
    print(f"  14 domains mapped; artefacts not tied to one domain: {', '.join(extra)}")
    print("  roles used:", ", ".join(f"{r} {n}" for r, n in roles.most_common()))


@lab("1.3")
def lab_1_3():
    key = ref("lab_1_3.json")
    ch = charter_lines()
    file_rows = rows("decisions.xlsx", "القرارات")
    assert len(key) == len(file_rows) == 10
    roles = {k["role"] for k in key}
    assert roles == set(ch), set(ch) ^ roles  # all nine roles are used
    print(f"  10 decisions, {len(roles)} roles, each role found in the charter; pass mark 8 of 10")


@lab("1.4")
def lab_1_4():
    key = ref("lab_1_4.json")
    found = [r["اسم الجدول أو المجلد"] for r in rows("system_extracts.xlsx", "ما وجده المسح")]
    interviews = text("owner_interviews.txt")
    for t in key["not_assets"]:
        assert t in found and t in interviews, t
    assets = [t for t in found if t not in key["not_assets"]]
    assert sorted(assets) == sorted(key["assets"]) and len(assets) == 15, assets
    reg = rows("register_start.xlsx", "سجل الأصول")
    assert len(reg) == 15
    for r in reg:
        for col in ("المالك", "المصدر (النظام والجدول)", "الحساسية", "الاستخدام"):
            assert r[col], (r["رقم الأصل"], col)
    disputed = [r["رقم الأصل"] for r in reg if "قيد التأكيد" in (r["ملاحظات"] or "")]
    sens = Counter(r["الحساسية"] for r in reg)
    print(f"  {len(found)} items scanned, {len(key['not_assets'])} not assets, 15 registered; owner, source, sensitivity, use all filled")
    print("  disputed owner:", ", ".join(disputed), "| sensitivity:", dict(sens))


@lab("2.1")
def lab_2_1():
    key = ref("lab_2_1.json")
    notes = text("glossary_notes.txt")
    drafted = rows("drafted_entries.xlsx", "مدخلات صاغها مساعد")
    assert len(key["checklist"]) == 8 and len(drafted) == 5
    mine = rows("glossary_workbook.xlsx", "مدخلاتي")
    assert len(mine) == 5
    for d, k in zip(drafted, key["drafted"]):
        assert d["المصطلح"] == k["term"]
        draft = d["التعريف كما صاغه المساعد"]
        if k["error"] == "الحد الأعلى":
            assert "5,000" in draft and "3,000" in notes
        elif k["error"] == "قيد مخترع":
            assert "أقل من 18" in draft and "من أي عمر" in notes
        elif k["error"] == "تعريف دائري":
            assert draft.split()[0] in k["term"], draft  # the definition opens with the term itself
        elif k["error"] == "مالك خاطئ":
            assert "مدير برنامج" in draft and "تحققت منه الإدارة المالية" in notes
        elif k["error"] == "خلط بين مفهومين":
            assert "الرعاية المنزلية" in draft and "خدمة أخرى" in notes
    print(f"  5 entries written by hand + 5 drafted entries corrected = {len(mine) + len(drafted)} entries; 5 planted errors confirmed against the notes")


@lab("2.2")
def lab_2_2():
    key = ref("lab_2_2.json")
    fam = rows("families.xlsx", "الأسر")
    start = date.fromisoformat(key["window_start"])
    paid = {f["family_id"] for f in fam if as_date(f["تاريخ آخر صرف"]) and as_date(f["تاريخ آخر صرف"]) >= start}
    approved = {f["family_id"] for f in fam if f["حالة الطلب"] == "مقبول"}
    status = {f["family_id"]: f["حالة الطلب"] for f in fam}
    a_not_b = Counter(status[i] for i in paid - approved)
    b_not_a = approved - paid
    new = sum(1 for f in fam if f["family_id"] in b_not_a and not f["تاريخ آخر صرف"])
    held = len(b_not_a) - new
    assert len(fam) == 600
    assert len(paid) == key["count_paid_definition"] and len(approved) == key["count_status_definition"]
    assert a_not_b["موقوف"] == key["suspended_paid"] and a_not_b["مغلق"] == key["closed_paid"]
    assert new == key["approved_new_unpaid"] and held == key["approved_held"]
    print(f"  paid in the last three months: {len(paid)} | status approved: {len(approved)} | both: {len(paid & approved)}")
    print(f"  paid but not approved: {sum(a_not_b.values())} (suspended {a_not_b['موقوف']}, closed {a_not_b['مغلق']})")
    print(f"  approved but not paid: {len(b_not_a)} (approved in September, no payment yet {new}; payment held since before July {held})")


@lab("2.3")
def lab_2_3():
    key = ref("lab_2_3.json")
    report = text("lineage/report_excerpt.txt")
    note = text("lineage/analyst_note.txt")
    interview = text("lineage/systems_interview.txt")
    pub = int(re.search(r"النشطة في نهاية الربع: (\d+)", report).group(1))
    removed = int(re.search(r"كانت (\d+) أسرة", note).group(1))
    approved = sum(1 for f in rows("families.xlsx", "الأسر") if f["حالة الطلب"] == "مقبول")
    assert pub == key["published"] == approved - removed and removed == key["removed"]
    for name in ("stg_families", "monthly_beneficiary_summary", "published_quarterly_indicators"):
        assert name in interview
    assert len(key["nodes"]) == 8 and len(key["transformations"]) == 2
    print(f"  8 stations, 2 transformations, 3 copies; published {pub} = approved {approved} - {removed} removed by hand")


@lab("2.4")
def lab_2_4():
    key = ref("lab_2_4.json")
    fields = [r["الحقل"] for r in rows("catalogue_fields.xlsx", "حقول الكتالوج")]
    assert fields == [k["field"] for k in key] and len(fields) == 14
    types = Counter(k["type"] for k in key)
    auto = [k["field"] for k in key if k["filled_by"] == "آلي"]
    # what a tool harvests is never business metadata
    assert all(k["type"] != "أعمال" for k in key if k["filled_by"] == "آلي")
    print(f"  14 fields: business {types['أعمال']}, technical {types['فني']}, operational {types['تشغيلي']}; harvested {len(auto)}, by a person {14 - len(auto)}")


def level_from_guide(r):
    """The case's provisional rules (classification_guide.txt), applied to a register row."""
    s, notes, name = r["الحساسية"], r["ملاحظات"] or "", r["اسم الأصل"]
    if s in ("شخصية ومالية", "شخصية وصحية"):
        return "سري"
    if s == "شخصية":
        return "مقيد"
    if "مرجعية" in notes or "منشورة" in name:
        return "عام"
    return "مقيد"


@lab("3.1")
def lab_3_1():
    key = ref("lab_3_1.json")
    guide = text("classification_guide.txt")
    for w in ("سري للغاية", "سري", "مقيد", "عام", "أعلى مستوى"):
        assert w in guide
    reg = rows("register_start.xlsx", "سجل الأصول")
    got = {r["رقم الأصل"]: level_from_guide(r) for r in reg}
    diff = {a: (got[a], key[a][0]) for a in key if got[a] != key[a][0]}
    assert not diff, diff
    print("  15 assets:", dict(Counter(v[0] for v in key.values())), "| A-15 takes the highest level of its contents")


@lab("3.2")
def lab_3_2():
    key = ref("lab_3_2.json")
    regions = ["RYD", "MKH", "MDN", "QSM", "EST", "ASR", "TBK", "HAL", "JZN", "JOF"]
    fam = rows("quality_tables.xlsx", "families_sample")
    pay = rows("quality_tables.xlsx", "payments_q3")
    vis = rows("quality_tables.xlsx", "eligibility_visits")
    ok_id = sum(1 for f in fam if re.fullmatch(r"[12]\d{9}", str(f["رقم الهوية (اصطناعي)"] or "")))
    mob = [f["الجوال (اصطناعي)"] for f in fam if f["الجوال (اصطناعي)"]]
    ok_mob = sum(1 for m in mob if re.fullmatch(r"05\d{8}", str(m)))
    ok_reg = sum(1 for f in fam if f["رمز المنطقة"] in regions)
    dates = [as_date(p["تاريخ الصرف"]) for p in pay if p["تاريخ الصرف"]]
    ok_amt = sum(1 for p in pay if 0 < p["المبلغ (ريال)"] <= 3000)
    zero_neg = sum(1 for p in pay if p["المبلغ (ريال)"] <= 0)
    outs = [v["النتيجة"] for v in vis if v["النتيجة"]]
    ok_out = sum(1 for o in outs if o in ("مؤهل", "غير مؤهل", "يحتاج مستندات"))
    ok_vdate = sum(1 for v in vis if as_date(v["تاريخ الزيارة"]) <= date(2026, 9, 30))
    k = key
    assert (len(fam), len(mob), ok_mob, ok_id, ok_reg) == (200, k["families_sample"]["mobile_complete"], k["families_sample"]["mobile_valid_of_filled"], k["families_sample"]["id_valid"], k["families_sample"]["region_valid"])
    assert (len(pay), len(dates), ok_amt) == (300, k["payments_q3"]["date_complete"], k["payments_q3"]["amount_valid"])
    assert all(date(2026, 7, 1) <= d <= date(2026, 9, 30) for d in dates)
    assert (len(vis), len(outs), ok_out, ok_vdate) == (150, k["eligibility_visits"]["outcome_complete"], k["eligibility_visits"]["outcome_valid_of_filled"], k["eligibility_visits"]["date_valid"])
    pct = lambda a, b: f"{100 * a / b:.1f}%"
    print(f"  families_sample: mobile complete {len(mob)}/200 = {pct(len(mob), 200)}; ID valid {ok_id}/200 = {pct(ok_id, 200)}; region valid {ok_reg}/200 = {pct(ok_reg, 200)}")
    print(f"  payments_q3: date complete {len(dates)}/300 = {pct(len(dates), 300)}; amount valid {ok_amt}/300 = {pct(ok_amt, 300)} (zero or negative {zero_neg}, above the cap {300 - ok_amt - zero_neg})")
    print(f"  eligibility_visits: outcome complete {len(outs)}/150 = {pct(len(outs), 150)}; outcome valid {ok_out}/{len(outs)} = {pct(ok_out, len(outs))}; date valid {ok_vdate}/150")
    print(f"  levels: families_sample {k['families_sample']['level']}, payments_q3 {k['payments_q3']['level']}, eligibility_visits {k['eligibility_visits']['level']}")


@lab("3.3")
def lab_3_3():
    key = ref("lab_3_3.json")
    req = text("requests.txt")
    assert len(re.findall(r"^الطلب \d", req, re.M)) == 6 == len(key)
    ch = charter_lines()
    for k in key:
        assert k["n"] == 5 or any(r in k["route"] for r in ch), k  # request 5 stays with the employee and her manager
    print("  6 decisions:", ", ".join(f"{k['n']} {k['decision']}" for k in key))


@lab("3.4")
def lab_3_4():
    key = ref("lab_3_4.json")
    docs = sorted(p.stem for p in (FILES / "evidence").glob("E*.txt"))
    assert docs == key["documents"] and len(docs) == 20
    guide = openpyxl.load_workbook(FILES / "scoring_guide.xlsx", read_only=True)
    levels = [r[0] for r in guide["المقياس"].iter_rows(min_row=2, values_only=True)]
    assert levels == [0, 1, 2, 3, 4, 5] == key["levels"]
    for area, s in key["scores"].items():
        assert s["evidence"] and all(e in docs for e in s["evidence"]), area
        assert not set(s["evidence"]) & set(key["traps"]), area  # no score rests on a trap
        bodies = " ".join(text(f"evidence/{e}.txt") for e in s["evidence"])
        if s["score"] >= 3:
            assert "مسودة" not in bodies.split("\n", 2)[-1] or "معتمد" in bodies, area
    print("  20 documents, 6 levels;", ", ".join(f"{a} {s['score']} ({'+'.join(s['evidence'])})" for a, s in key["scores"].items()))
    print("  not evidence:", ", ".join(f"{d} {w}" for d, w in key["traps"].items()))


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # Arabic output on any console code page
    wanted = argv or list(LABS)
    failed = 0
    for lab_id in wanted:
        print(f"Lab {lab_id}")
        try:
            LABS[lab_id]()
            print("  PASS")
        except AssertionError as e:
            failed += 1
            print("  FAIL", e)
    print(f"{len(wanted) - failed} of {len(wanted)} labs pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
