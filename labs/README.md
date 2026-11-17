# أسس إدارة البيانات: المختبرات

اثنا عشر مختبرًا لمقرر أكاديمية سدايا **LDS-DMG-101**، مدة كل منها 35 دقيقة في جلسة من 70 دقيقة. المختبرات صفحات
إرشادية بالعربية: الهدف، والملفات، وخطوات بدقائقها، وأسئلة تحقق، وتمرين إضافي ✱، وملاحظات للمدرب. يعمل المشارك في
جدول بيانات أو أداة رسم أو ورقة، ولا يكتب كودًا.

كل المختبرات في جهة واحدة: **هيئة مَعين للخدمات العامة**، جهة عامة افتراضية، وكلها على برنامج إعانة دعم الأسرة. كل
الأسماء والأرقام وأرقام الهوية والجوالات وهمية.

## ما يحتاجه المشارك

- جدول بيانات: LibreOffice Calc أو Microsoft Excel، مع الفرز والتصفية والدالة COUNTIFS.
- أداة رسم في المختبر 2.3: draw.io أو Excalidraw، أو ورقة وقلم.
- لا حساب ولا تثبيت آخر، ولا يُنزَّل أي نموذج. لا يحتاج أي مختبر مساعد ذكاء اصطناعي ليكتمل؛ المختبر 2.1 دون أي مساعد،
  والمسودات التي يراجعها جاهزة في ملف.
- يدخل المساعدَ ما كتبته بكلماتك: سؤال عن مفهوم، أو مسودة تعريف، أو سطر من خطتك. لا تدخله صفوف الجداول ولا المقابلات ولا الملاحظات ولا وثائق الحزمة: ما لم يُصنَّف «عامًا» لا يدخل أي أداة ذكاء اصطناعي توليدي، عامة كانت أو معتمدة.

## نقطة البداية والحل

كل مختبر يبدأ من ملفات جاهزة في `files/` ولا يعتمد على مختبر آخر في اليوم نفسه. مختبرات اليومين الثاني والثالث التي
تحتاج سجل الأصول تبدأ من السجل المرجعي `files/register_start.xlsx`، لا من سجل المشارك.

| المختبر | الصفحة | يبدأ من | الحل المرجعي |
|---|---|---|---|
| 1.1 | `D1_1_lifecycle.html` | `lifecycle_events.xlsx`، `case_brief.txt` | `solutions/D1_1_lifecycle.md` |
| 1.2 | `D1_2_domains.html` | `domain_map.xlsx`، `governance_charter.txt` | `solutions/D1_2_domains.md` |
| 1.3 | `D1_3_decisions.html` | `decisions.xlsx`، `governance_charter.txt` | `solutions/D1_3_decisions.md` |
| 1.4 | `D1_4_asset_register.html` | `system_extracts.xlsx`، `owner_interviews.txt`، `asset_register_template.xlsx` | `solutions/D1_4_asset_register.md` |
| 2.1 | `D2_1_glossary.html` | `glossary_notes.txt`، `glossary_workbook.xlsx`، `drafted_entries.xlsx` | `solutions/D2_1_glossary.md` |
| 2.2 | `D2_2_active_beneficiary.html` | `families.xlsx`، `definitions_note.txt` | `solutions/D2_2_active_beneficiary.md` |
| 2.3 | `D2_3_lineage.html` | `lineage/` (أربعة ملفات)، `families.xlsx` | `solutions/D2_3_lineage.md` |
| 2.4 | `D2_4_catalogue.html` | `catalogue_fields.xlsx`، `register_start.xlsx`، `system_extracts.xlsx` | `solutions/D2_4_catalogue.md` |
| 3.1 | `D3_1_classify.html` | `register_start.xlsx`، `classification_guide.txt` | `solutions/D3_1_classify.md` |
| 3.2 | `D3_2_profile.html` | `quality_tables.xlsx`، `classification_guide.txt` | `solutions/D3_2_profile.md` |
| 3.3 | `D3_3_requests.html` | `requests.txt`، `governance_charter.txt`، `classification_guide.txt` | `solutions/D3_3_requests.md` |
| 3.4 | `D3_4_maturity.html` | `scoring_guide.xlsx`، `evidence/` (عشرون وثيقة) | `solutions/D3_4_maturity.md` |

## تشغيل الحلول

```bash
uv run labs/solutions/check.py            # كل المختبرات
uv run labs/solutions/check.py 2.2 3.2    # بعضها
```

ملف واحد يعلن اعتمادياته ويحتاج [uv](https://docs.astral.sh/uv/). يعيد حساب كل مفتاح من الملفات (الأعداد، والقياسات،
والمطابقة مع الميثاق والأدلة)، ويطبع الأرقام التي تقتبسها شرائح ما بعد المختبر و`PASS` لكل مختبر، ولا يكتب شيئًا على
القرص. لا يستدعي أي نموذج: كل المختبرات عمل بشري على جدول بيانات أو مخطط أو قرار مكتوب. المسودات الخمس التي يراجعها
المشارك في المختبر 2.1 مكتوبة سلفًا وفيها أخطاء مزروعة، فلا تحتاج نموذجًا.

## الملفات

| الملف | ما هو | المزروع فيه |
|---|---|---|
| `case_brief.txt`، `governance_charter.txt` | موجز الحالة، وميثاق الحوكمة بأدواره التسعة | سطر «يُساءل عن» لكل دور |
| `lifecycle_events.xlsx` | اثنا عشر حدثًا من ملف أسرة | خمسة قرارات حوكمة وسبعة أعمال إدارة |
| `domain_map.xlsx` | المجالات الخمسة عشر وسبعة عشر مخرجًا | ثلاثة مخرجات لا تخص مجالًا بعينه |
| `decisions.xlsx` | عشرة قرارات عن البيانات | قراران يُخلط فيهما بين الاعتماد والتنفيذ |
| `system_extracts.xlsx`، `owner_interviews.txt` | مسح آلي من 18 عنصرًا ومقابلات الملاك | ثلاثة ليست أصولًا، وأصل يدّعيه مديران |
| `glossary_notes.txt`، `drafted_entries.xlsx` | ملاحظات المصطلحات وخمس مسودات | خطأ واحد في كل مسودة |
| `families.xlsx`، `definitions_note.txt` | 600 أسرة بلا أسماء، والتعريفان | 30 أسرة صُرف لها وليست «مقبول»، و37 «مقبول» بلا صرف |
| `lineage/` | النموذج والمقابلة ورسالة المحللة ومقتطف التقرير | حذف يدوي غير موثق لاثنتي عشرة أسرة |
| `catalogue_fields.xlsx`، `register_start.xlsx` | أربعة عشر حقلًا، والسجل المرجعي | أصل بلا مشرف من جهة الأعمال ومالكه «قيد التأكيد» |
| `classification_guide.txt` | دليل التصنيف المبدئي للحالة | ملخص مجمّع بخلايا صغيرة، وملف مركّب |
| `quality_tables.xlsx` | ثلاثة جداول وورقة القواعد | جوالات ناقصة، ومبالغ صفر أو فوق الحد، وزيارات في المستقبل |
| `requests.txt` | ستة طلبات على مكتب البيانات | غرض جديد داخل الهيئة نفسها، وطلب لصق ملاحظات في مساعد عام |
| `scoring_guide.xlsx`، `evidence/` | مقياس الحالة بستة مستويات، وعشرون وثيقة | ست وثائق ليست أدلة |

مقياس المستويات الستة في `scoring_guide.xlsx` دليل تقدير خاص بهذه الحالة، كتب لهذا المقرر، ولا يُنسب إلى أي مؤشر وطني.

## إعادة توليد الملفات

```bash
uv run labs/_tools/prepare_files.py
node labs/_tools/write_solutions.mjs
```

الأول يولد كل ملفات `files/` ومفاتيح `solutions/reference/` ببذرة ثابتة، فيعطي البايتات نفسها في كل تشغيل. والثاني يكتب
الحلول المرجعية من المفاتيح.
