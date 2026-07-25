# Iraqi Arabic Sales Dialogue Dataset

**A large-scale conversational dataset in Iraqi (Baghdadi) Arabic, centered on buying, selling, and negotiation.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
![Conversations](https://img.shields.io/badge/conversations-210k-blue)
![Unique patterns](https://img.shields.io/badge/unique%20patterns-110k-orange)
![Language](https://img.shields.io/badge/language-Iraqi%20Arabic-green)

> 🇮🇶 **النسخة العربية** متوفرة بالكامل [بالأسفل](#النسخة-العربية) — Arabic version available in full below.

---

## Overview

Iraqi Arabic is severely under-represented in NLP resources. Most Arabic datasets cover Modern Standard Arabic (MSA) or Egyptian/Levantine dialects, leaving Iraqi speakers poorly served by conversational models.

This dataset provides **110,168 unique synthetic dialogue patterns, template-expanded to 210,832 conversations**, in colloquial Iraqi Arabic across **20 topical categories**. The focus is deliberately on **commercial dialogue** — price inquiry, haggling, discounts, warranty, installments, and closing a sale — plus everyday and social conversation that gives models the cultural context those exchanges assume.

The data is **synthetically generated**, not transcribed from real speakers. Both the surface count and the underlying pattern count are reported above and broken down [per category below](#diversity-and-repetition), so you can judge the effective size for yourself rather than take a headline number on trust.

**What makes it distinct:**

- **Dialect-authentic, not transliterated MSA.** Vocabulary and syntax are Iraqi throughout (`شلونك` not `كيف حالك`, `بيش` not `بكم`, `أكو` not `يوجد`).
- **Commerce-focused.** Roughly 80% of the data is seller–customer negotiation, a domain absent from general Arabic corpora.
- **Chat-ready format.** Native `role`/`content` message lists — loadable directly into any instruction-tuning pipeline.
- **Grounded variants included.** Later versions add catalog-conditioned examples that teach a model to quote only from supplied facts rather than hallucinating prices.

---

## Quick Start

```python
import json

# Load a category file
with open("iraqi_training_data/iraqi_train_01_electronics.json", encoding="utf-8") as f:
    data = json.load(f)

print(len(data))          # 10000
print(data[0]["messages"])
```

With 🤗 `datasets`:

```python
from datasets import load_dataset

ds = load_dataset("json", data_files="data/iraqi_train_v8_part*.jsonl", split="train")
```

---

## Data Format

Each conversation is a JSON object with a `messages` list:

```json
{
  "id": "elec_0001",
  "category": "sales_electronics",
  "dialect": "iraqi_arabic",
  "messages": [
    { "role": "user",      "content": "السلام عليكم" },
    { "role": "assistant", "content": "وعليكم السلام، هلا وغلا! كيف أكدر أساعدك؟" },
    { "role": "user",      "content": "أريد موبايل سامسونج S24، عندكم؟" },
    { "role": "assistant", "content": "إي أكو، سامسونج S24 جديد وبالكرتون. سعره 750,000 دينار. كاميرا 50 ميگاپيكسل وذاكرة 256 گيگا" }
  ]
}
```

Grounded examples additionally carry a `system` message holding an explicit product catalog, training the model to quote from it verbatim instead of inventing prices.

---

## Dataset Structure

### Category files — `iraqi_training_data/`

Curated corpus, 10,000 conversations per category.

| File | Topic | Conversations |
|------|-------|--------------:|
| `iraqi_train_01_electronics.json` | Electronics (phones, laptops, TVs) | 10,000 |
| `iraqi_train_02_food.json` | Groceries and produce | 10,000 |
| `iraqi_train_03_clothes.json` | Clothing and footwear | 10,000 |
| `iraqi_train_04_cars.json` | Cars | 10,000 |
| `iraqi_train_04_cars_plus_scraped.json` | Cars, augmented with listing data | 10,832 |
| `iraqi_train_05_realestate.json` | Real estate — sale and rent | 10,000 |
| `iraqi_train_06_furniture.json` | Furniture and appliances | 10,000 |
| `iraqi_train_07_services.json` | Services (repair, installation) | 10,000 |
| `iraqi_train_08_daily.json` | Everyday conversation | 10,000 |
| `iraqi_train_09_social.json` | Family and social | 10,000 |
| `iraqi_train_10_mixed.json` | Mixed | 10,000 |
| `iraqi_train_11_health.json` | Health and pharmacy | 10,000 |
| `iraqi_train_12_education.json` | Education | 10,000 |
| `iraqi_train_13_government.json` | Government services | 10,000 |
| `iraqi_train_14_restaurant.json` | Restaurants and food service | 10,000 |
| `iraqi_train_15_transport.json` | Transport | 10,000 |
| `iraqi_train_16_sports.json` | Sports and leisure | 10,000 |
| `iraqi_train_17_family.json` | Family | 10,000 |
| `iraqi_train_18_occasions.json` | Occasions and holidays | 10,000 |
| `iraqi_train_19_neighborhood.json` | Neighborhood life | 10,000 |
| `iraqi_train_20_work.json` | Work and profession | 10,000 |
| **Total** | | **210,832** |

### Training splits — `data/`

Versioned, deduplicated JSONL splits prepared for fine-tuning. Each version applies targeted quality fixes over the last; **v8 is the current recommended split.**

| Split | Lines |
|-------|------:|
| `iraqi_train_v8_part01–03.jsonl` | 75,998 |
| `iraqi_val_v8.jsonl` | 15,480 |

Earlier versions (`v4`–`v7`) are retained for reproducibility. Supplementary sets cover grounded catalog answers, clarification behavior, structured extraction, and greetings/small-talk.

### Supporting files

| Path | Contents |
|------|----------|
| `word.json` | 930 dialect terms across 50 semantic categories |
| `scripts/` | Generation, validation, and split-preparation scripts |
| `scraped_data/` | Raw marketplace listings used to ground car pricing |
| `IRAQI_DIALECT_REFERENCE.md` | Extended dialect notes |

---

## Dialect Reference

Core substitutions that distinguish Iraqi Arabic from MSA and other dialects:

| MSA / Levantine | Iraqi | Meaning |
|-----------------|-------|---------|
| كيف حالك | شلونك | how are you |
| ماذا / ما | شنو | what |
| بكم / كم | بيش / شكد | how much |
| متى | شوكت | when |
| يمكن / تستطيع | تكدر / أكدر | can / able to |
| نعم | إي / إي والله | yes |
| كثير | هواي | a lot |
| الآن | هسه | now |
| يوجد | أكو | there is |
| لا يوجد | ما أكو | there isn't |
| النقود | الفلوس | money |
| كل شيء | كلشي | everything |

**Commercial expressions:**

| Meaning | Iraqi |
|---------|-------|
| What's the price? | بيش / شكد السعر |
| Give me a discount | نزل علي / ما تعطيني تخفيض |
| That's expensive | هذا غالي هواي / مو معقول |
| Final price | هذا آخر سعر / هذا سعر نار |
| I'll think about it | بفكر وأرجع / راح أتصل |

**Forms of address:** حجي / حاجي (sir), باجي (sister), أبو + son's name, أم + son's name, عمو (uncle).

---

## Coverage

**Baghdad districts:** Karrada, Mansour, Jadriya, Kadhimiya, Adhamiyah, Harthiya, Arasat, Saydiya, Dora, Zafaraniya, Karkh, Shula, Sha'ab.

**Cities:** Mosul, Basra, Najaf, Karbala, Kut, Diwaniyah, Samawah, Amarah, Ramadi, Tikrit, Hillah, Kirkuk.

**Prices** are denominated in **Iraqi Dinar (IQD)**, occasionally cross-referenced to USD, within realistic market ranges:

| Category | Range (IQD) |
|----------|-------------|
| Mobile phone | 130,000 – 1,200,000 |
| Laptop | 520,000 – 1,500,000 |
| Television | 450,000 – 1,200,000 |
| Car | 18,000,000 – 110,000,000 |
| House / apartment | 90,000,000 – 900,000,000 |
| Furniture | 90,000 – 3,000,000 |
| Services | 10,000 – 500,000 |

**Sales scenarios covered:** product inquiry, price question, haggling, price rejection, product comparison, warranty, installment plans, bulk pricing, delivery, returns, closing.

---

<a name="diversity-and-repetition"></a>

## Diversity and Repetition

Because the corpus is template-generated, raw conversation count overstates its effective size. Two measurements, both reproducible from the files in this repo:

- **Exact duplicates** — identical message sequences: **170,053 unique / 210,832 total (1.24×)**.
- **Unique patterns** — message sequences after normalizing numbers, prices, and Latin product names to placeholders, so two conversations differing only in a price collapse to one: **110,168 unique / 210,832 total (1.9×)**.

The pattern count is the more honest measure of variety, and the one quoted at the top of this README.

Repetition is uneven across categories. The commerce categories that form the core of the dataset are the most varied; the later general-topic categories are the most templated:

| Category | Conversations | Unique patterns | Repetition |
|----------|--------------:|----------------:|-----------:|
| Mixed | 10,000 | 8,691 | 1.2× |
| Services | 10,000 | 8,075 | 1.2× |
| Electronics | 10,000 | 7,847 | 1.3× |
| Clothes | 10,000 | 7,832 | 1.3× |
| Food | 10,000 | 7,812 | 1.3× |
| Daily | 10,000 | 7,118 | 1.4× |
| Social | 10,000 | 7,011 | 1.4× |
| Education | 10,000 | 6,234 | 1.6× |
| Health | 10,000 | 6,099 | 1.6× |
| Furniture | 10,000 | 5,175 | 1.9× |
| Work | 10,000 | 5,158 | 1.9× |
| Occasions | 10,000 | 4,680 | 2.1× |
| Neighborhood | 10,000 | 4,603 | 2.2× |
| Cars | 10,000 | 4,133 | 2.4× |
| Cars + scraped | 10,832 | 4,032 | 2.7× |
| Real estate | 10,000 | 3,856 | 2.6× |
| Transport | 10,000 | 3,855 | 2.6× |
| Restaurant | 10,000 | 3,591 | 2.8× |
| Sports | 10,000 | 3,141 | 3.2× |
| Family | 10,000 | 3,014 | 3.3× |
| Government | 10,000 | 2,810 | 3.6× |
| **Total** | **210,832** | **110,168** | **1.9×** |

If uniform variety matters more to you than volume, deduplicate on the normalized pattern or subsample the high-repetition categories.

---

## Intended Uses

- Fine-tuning conversational LLMs for Iraqi Arabic (this corpus was used to tune Gemma via LoRA)
- Building retail chatbots for Iraqi electronics, automotive, and real-estate businesses
- Arabic dialect NLP research and dialect-identification work
- Studying sales and negotiation discourse in Iraqi culture

---

## Limitations and Biases

Please read before using in research:

- **Synthetically generated.** Conversations are produced from templates and generation scripts seeded with curated dialect vocabulary — not transcribed from real speakers. They reflect plausible market dialogue, not verified natural speech, and lack the disfluencies of genuine conversation.
- **Template repetition.** 210,832 conversations expand from 110,168 unique patterns (1.9× average). Repetition is uneven — government, family, and sports categories repeat 3.2–3.6×, while mixed, services, and electronics stay near 1.2×. See [Diversity and Repetition](#diversity-and-repetition) and weight or subsample accordingly.
- **Baghdadi-weighted.** Baghdad dialect dominates; southern and northern Iraqi varieties are under-covered.
- **Prices are time-bound.** Figures reflect market conditions around 2025–2026 and will age.
- **Not safety-filtered for deployment.** No adversarial, toxicity, or refusal training is included. A model tuned on this alone will imitate a salesperson, including on questions it should decline.
- **Overfitting risk.** The narrow stylistic range can cause catastrophic forgetting of a base model's general abilities. Mixing in general instruction data is strongly recommended — see `AA.md`.

---

## License

Released under the **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)** license.

You are free to share and adapt the material, including commercially, provided you give appropriate credit.

```bibtex
@misc{iraqi_arabic_sales_dialogue_2026,
  title  = {Iraqi Arabic Sales Dialogue Dataset},
  author = {Ameer Wisam},
  year   = {2026},
  url    = {https://github.com/ameer20042005/iraqi-arabic-sales-dialogue-dataset}
}
```

### Vocabulary attribution

The 930-term dialect vocabulary in `word.json` was compiled with reference to [Mo3jam's Iraqi dialect section](https://ar.mo3jam.com/dialect/Iraqi) and manually reviewed to remove Gulf and Levantine terms. Individual dialect words are not themselves copyrightable, and no definitions or entry text were reproduced from the source.

---
---

<a name="النسخة-العربية"></a>

# مجموعة بيانات محادثات البيع باللهجة العراقية

**مجموعة بيانات محادثات واسعة باللهجة العراقية البغدادية، متخصصة بالبيع والشراء والتفاوض.**

---

## نظرة عامة

اللهجة العراقية ممثّلة تمثيلاً ضعيفاً جداً في موارد معالجة اللغة الطبيعية. أغلب البيانات العربية تغطي الفصحى أو اللهجتين المصرية والشامية، ما يترك المتحدثين بالعراقية بخدمة رديئة من النماذج الحوارية.

توفّر هذي المجموعة **110,168 نمط حوار صناعي فريد، موسّعة بالقوالب إلى 210,832 محادثة**، باللهجة العراقية الشعبية موزعة على **20 تصنيفاً**، مع تركيز مقصود على **حوار البيع** — السؤال عن السعر، التفاوض، الخصم، الضمان، التقسيط، وإغلاق الصفقة — إضافة لمحادثات يومية واجتماعية تعطي النموذج السياق الثقافي اللي تفترضه تلك الحوارات.

البيانات **مولّدة صناعياً**، مو منقولة من متحدثين حقيقيين. الرقمان — السطحي والأنماط الأساسية — مذكوران أعلاه ومفصّلان [حسب التصنيف بالأسفل](#التنوع-والتكرار)، حتى تحكم بنفسك على الحجم الفعلي بدل ما تعتمد على رقم عنوان.

**ما يميزها:**

- **لهجة أصيلة، مو فصحى محوّلة.** المفردات والتراكيب عراقية بالكامل (`شلونك` مو `كيف حالك`، `بيش` مو `بكم`، `أكو` مو `يوجد`).
- **متخصصة بالتجارة.** حوالي 80% من البيانات تفاوض بين بائع وزبون، وهو مجال غائب عن المدوّنات العربية العامة.
- **جاهزة كصيغة محادثة.** قوائم رسائل `role`/`content` أصلية — تنحمّل مباشرة بأي مسار تدريب تعليمات.
- **تتضمن أمثلة مقيّدة بكتالوج.** الإصدارات المتأخرة تضيف أمثلة مشروطة بكتالوج تعلّم النموذج ينقل الأسعار من المعطيات فقط بدل ما يختلقها.

---

## البدء السريع

```python
import json

with open("iraqi_training_data/iraqi_train_01_electronics.json", encoding="utf-8") as f:
    data = json.load(f)

print(len(data))          # 10000
print(data[0]["messages"])
```

---

## صيغة البيانات

كل محادثة كائن JSON يحتوي قائمة `messages`:

```json
{
  "id": "elec_0001",
  "category": "sales_electronics",
  "dialect": "iraqi_arabic",
  "messages": [
    { "role": "user",      "content": "السلام عليكم" },
    { "role": "assistant", "content": "وعليكم السلام، هلا وغلا! كيف أكدر أساعدك؟" },
    { "role": "user",      "content": "أريد موبايل سامسونج S24، عندكم؟" },
    { "role": "assistant", "content": "إي أكو، سامسونج S24 جديد وبالكرتون. سعره 750,000 دينار. كاميرا 50 ميگاپيكسل وذاكرة 256 گيگا" }
  ]
}
```

الأمثلة المقيّدة تحمل إضافة لذلك رسالة `system` فيها كتالوج منتجات صريح، تدرّب النموذج ينقل منه حرفياً بدل اختلاق الأسعار.

---

## هيكل المجموعة

### ملفات التصنيفات — `iraqi_training_data/`

مدوّنة منسّقة، 10,000 محادثة لكل تصنيف.

| الملف | الموضوع | المحادثات |
|-------|---------|----------:|
| `iraqi_train_01_electronics.json` | الإلكترونيات (موبايل، لابتوب، تلفزيون) | 10,000 |
| `iraqi_train_02_food.json` | المواد الغذائية والخضار | 10,000 |
| `iraqi_train_03_clothes.json` | الملابس والأحذية | 10,000 |
| `iraqi_train_04_cars.json` | السيارات | 10,000 |
| `iraqi_train_04_cars_plus_scraped.json` | السيارات، مدعّمة ببيانات إعلانات | 10,832 |
| `iraqi_train_05_realestate.json` | العقارات — بيع وإيجار | 10,000 |
| `iraqi_train_06_furniture.json` | الأثاث والأجهزة المنزلية | 10,000 |
| `iraqi_train_07_services.json` | الخدمات (تصليح، تركيب) | 10,000 |
| `iraqi_train_08_daily.json` | محادثات يومية | 10,000 |
| `iraqi_train_09_social.json` | عائلية واجتماعية | 10,000 |
| `iraqi_train_10_mixed.json` | مزيج | 10,000 |
| `iraqi_train_11_health.json` | الصحة والصيدلية | 10,000 |
| `iraqi_train_12_education.json` | التعليم | 10,000 |
| `iraqi_train_13_government.json` | الخدمات الحكومية | 10,000 |
| `iraqi_train_14_restaurant.json` | المطاعم | 10,000 |
| `iraqi_train_15_transport.json` | النقل والمواصلات | 10,000 |
| `iraqi_train_16_sports.json` | الرياضة والترفيه | 10,000 |
| `iraqi_train_17_family.json` | العائلة | 10,000 |
| `iraqi_train_18_occasions.json` | المناسبات والأعياد | 10,000 |
| `iraqi_train_19_neighborhood.json` | حياة المحلة | 10,000 |
| `iraqi_train_20_work.json` | العمل والمهنة | 10,000 |
| **المجموع** | | **210,832** |

### تقسيمات التدريب — `data/`

تقسيمات JSONL مُصدَّرة ومنقّاة من التكرار، جاهزة للـ fine-tuning. كل إصدار يطبّق إصلاحات جودة على سابقه، و**v8 هو التقسيم الموصى به حالياً.**

| التقسيم | الأسطر |
|---------|-------:|
| `iraqi_train_v8_part01–03.jsonl` | 75,998 |
| `iraqi_val_v8.jsonl` | 15,480 |

الإصدارات الأقدم (`v4`–`v7`) محفوظة لإمكانية إعادة الإنتاج. المجموعات المكمّلة تغطي الإجابات المقيّدة بكتالوج، وسلوك الاستيضاح، والاستخراج المهيكل، والتحيات.

### ملفات مساندة

| المسار | المحتوى |
|--------|---------|
| `word.json` | 930 مفردة لهجية على 50 تصنيف دلالي |
| `scripts/` | سكربتات التوليد والتحقق وتحضير التقسيمات |
| `scraped_data/` | إعلانات سوق خام استُخدمت لتثبيت أسعار السيارات |
| `IRAQI_DIALECT_REFERENCE.md` | ملاحظات موسّعة عن اللهجة |

---

## مرجع اللهجة

أبرز الاستبدالات اللي تميّز العراقية عن الفصحى وباقي اللهجات:

| الفصحى / الشامي | العراقي |
|-----------------|---------|
| كيف حالك | شلونك |
| ما أخبارك | شخبارك |
| ماذا / ما | شنو |
| بكم / كم | بيش / شكد |
| متى | شوكت |
| يمكن / تستطيع | تكدر / أكدر |
| نعم | إي / إي والله |
| موافق | ماشي |
| كثير | هواي |
| الآن | هسه |
| يوجد | أكو |
| لا يوجد | ما أكو |
| جاء / جاءت | اجه / اجت |
| معطل / مكسور | عطلان / خربان |
| النقود | الفلوس |
| كل شيء | كلشي |

**تعابير البيع والشراء:**

| المعنى | العراقي |
|--------|---------|
| كم السعر؟ | بيش / شكد السعر |
| أعطني خصم | نزل علي / ما تعطيني تخفيض |
| هذا غالي | هذا غالي هواي / مو معقول |
| آخر سعر | هذا آخر سعر / هذا سعر نار |
| فكر بعدين | بفكر وأرجع / راح أتصل |

**ألقاب المناداة:** حجي / حاجي، باجي، أبو + اسم الولد، أم + اسم الولد، عمو، أستاذ.

---

## التغطية

**أحياء بغداد:** الكرادة، المنصور، الجادرية، الكاظمية، الأعظمية، الحارثية، العرصات، المعلف، السيدية، الدورة، الزعفرانية، الكرخ، الشعلة، الشعب، حي بابل، حي الرشيد.

**المدن:** الموصل، البصرة، النجف، كربلاء، الكوت، الديوانية، السماوة، عمارة، الرمادي، تكريت، الحلة، كركوك.

**الأسواق والمراجع:** سوق الأمين وشارع الأبيض للإلكترونيات، الطابو الرسمي بالعقارات، معارض السيارات، والأكل العراقي (مسگوف، دولمة، قوزي، باچة، قيمة، تشريب، بريانية).

**الأسعار** بالدينار العراقي (IQD) مع إشارة أحياناً للدولار، ضمن نطاقات سوقية واقعية:

| النوع | النطاق (دينار) |
|-------|---------------|
| موبايل | 130,000 – 1,200,000 |
| لابتوب | 520,000 – 1,500,000 |
| تلفزيون | 450,000 – 1,200,000 |
| سيارة | 18,000,000 – 110,000,000 |
| بيت/شقة | 90,000,000 – 900,000,000 |
| أثاث | 90,000 – 3,000,000 |
| خدمات | 10,000 – 500,000 |

**سيناريوهات البيع المغطّاة:** الاستفسار عن المنتج، السؤال عن السعر، التفاوض والخصم، رفض السعر، مقارنة المنتجات، الضمان، التقسيط، الشراء بالجملة، التوصيل، الإرجاع، إغلاق الصفقة.

---

<a name="التنوع-والتكرار"></a>

## التنوّع والتكرار

بما إن المدوّنة مولّدة بقوالب، فإن عدد المحادثات الخام يبالغ بحجمها الفعلي. قياسان، وكلاهما قابل لإعادة الإنتاج من ملفات المستودع:

- **التكرار الحرفي** — تسلسلات رسائل متطابقة: **170,053 فريدة / 210,832 إجمالاً (1.24×)**.
- **الأنماط الفريدة** — تسلسلات الرسائل بعد تحييد الأرقام والأسعار وأسماء المنتجات اللاتينية، بحيث محادثتان تختلفان بالسعر فقط تنطبقان على نمط واحد: **110,168 فريدة / 210,832 إجمالاً (1.9×)**.

عدد الأنماط هو المقياس الأنزه للتنوّع، وهو المذكور بأعلى هذا الملف.

التكرار متفاوت بين التصنيفات. تصنيفات التجارة اللي تشكّل نواة المجموعة هي الأكثر تنوعاً، وتصنيفات المواضيع العامة المتأخرة هي الأكثر قولبة:

| التصنيف | المحادثات | الأنماط الفريدة | التكرار |
|---------|----------:|----------------:|--------:|
| المختلط | 10,000 | 8,691 | 1.2× |
| الخدمات | 10,000 | 8,075 | 1.2× |
| الإلكترونيات | 10,000 | 7,847 | 1.3× |
| الملابس | 10,000 | 7,832 | 1.3× |
| الغذاء | 10,000 | 7,812 | 1.3× |
| اليومية | 10,000 | 7,118 | 1.4× |
| الاجتماعية | 10,000 | 7,011 | 1.4× |
| التعليم | 10,000 | 6,234 | 1.6× |
| الصحة | 10,000 | 6,099 | 1.6× |
| الأثاث | 10,000 | 5,175 | 1.9× |
| العمل | 10,000 | 5,158 | 1.9× |
| المناسبات | 10,000 | 4,680 | 2.1× |
| المحلة | 10,000 | 4,603 | 2.2× |
| السيارات | 10,000 | 4,133 | 2.4× |
| السيارات + المسحوبة | 10,832 | 4,032 | 2.7× |
| العقارات | 10,000 | 3,856 | 2.6× |
| النقل | 10,000 | 3,855 | 2.6× |
| المطاعم | 10,000 | 3,591 | 2.8× |
| الرياضة | 10,000 | 3,141 | 3.2× |
| العائلة | 10,000 | 3,014 | 3.3× |
| الحكومية | 10,000 | 2,810 | 3.6× |
| **المجموع** | **210,832** | **110,168** | **1.9×** |

إذا كان انتظام التنوّع أهم عندك من الحجم، احذف التكرار على أساس النمط المحيَّد أو خذ عينة أصغر من التصنيفات عالية التكرار.

---

## الاستخدامات المقترحة

- تدريب نماذج حوارية على اللهجة العراقية (استُخدمت هذي المدوّنة لتدريب Gemma بتقنية LoRA)
- بناء chatbot لمحلات الإلكترونيات والسيارات والعقارات العراقية
- أبحاث معالجة اللهجات العربية وتمييز اللهجات
- دراسة خطاب البيع والتفاوض بالثقافة العراقية

---

## الحدود والتحيّزات

يُرجى قراءتها قبل الاستخدام البحثي:

- **مولّدة صناعياً.** المحادثات منتجة من قوالب وسكربتات توليد مغذّاة بمفردات لهجية منسّقة — مو منقولة من متحدثين حقيقيين. تعكس حواراً سوقياً معقولاً، لكنها مو كلاماً طبيعياً موثّقاً، وتفتقر لتعثرات الحديث الحقيقي.
- **تكرار القوالب.** الـ210,832 محادثة موسّعة من 110,168 نمطاً فريداً (1.9× بالمتوسط). التكرار متفاوت — التصنيفات الحكومية والعائلة والرياضة تتكرر 3.2–3.6×، بينما المختلط والخدمات والإلكترونيات قريبة من 1.2×. راجع [التنوّع والتكرار](#التنوع-والتكرار) ووازِن أو خذ عينات وفقاً لذلك.
- **مائلة للبغدادية.** لهجة بغداد هي الغالبة، والتغطية ضعيفة للهجات الجنوب والشمال.
- **الأسعار مرتبطة بزمنها.** الأرقام تعكس ظروف السوق حوالي 2025–2026 وراح تتقادم.
- **غير مفلترة للنشر.** ما بيها تدريب على الرفض أو مقاومة المدخلات العدائية. النموذج المدرَّب عليها لوحدها راح يقلّد بائعاً، حتى بالأسئلة اللي المفروض يرفضها.
- **خطر فرط التخصيص.** ضيق النطاق الأسلوبي يسبب نسياناً كارثياً لقدرات النموذج الأساسي العامة. يُنصح بشدة بخلط بيانات تعليمات عامة — راجع `AA.md`.

---

## الترخيص

منشورة برخصة **[المشاع الإبداعي — نسب المُصنَّف 4.0 دولي (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.ar)**.

لك حرية المشاركة والاقتباس والتعديل، بما في ذلك الاستخدام التجاري، شرط الإشارة المناسبة للمصدر.

### إسناد المفردات

المفردات الـ930 في `word.json` جُمعت بالرجوع إلى [قسم اللهجة العراقية في موقع معجم](https://ar.mo3jam.com/dialect/Iraqi) ورُوجعت يدوياً لحذف الكلمات الخليجية والشامية. المفردات المفردة بحد ذاتها غير خاضعة لحقوق التأليف، ولم يُنسخ أي تعريف أو نص مدخلات من المصدر.
