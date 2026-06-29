#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iraqi Arabic Dialect LLM Training Data Generator - Part 2
ملفات 11-20: مجالات جديدة كلياً
"""

import json, random, os


# ============================================================
# LOAD WORD BANK
# ============================================================
def _load_words():
    path = os.path.join(os.path.dirname(__file__), "word.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {cat["category"]: [i["word"] for i in cat["items"]] for cat in data}

_W = _load_words()
def _cat(name): return _W.get(name, [])
def pick(lst): return random.choice(lst)

# ============================================================
# SHARED BANKS
# ============================================================
MALE   = ["أبو علي","أبو أحمد","حجي كريم","عمو صالح","أستاذ حيدر","أبو حسين",
          "حجي جاسم","أبو محمد","عمو رضا","أبو يوسف","أبو ليث","حجي فلاح",
          "أبو مصطفى","أبو رعد","عمو خليل","أبو كرار","حجي وداد","أبو بلال"]
FEMALE = ["أم علي","باجي فاطمة","أم أحمد","حجية أم حسين","باجي زينب",
          "أم جعفر","باجي رهام","أم يوسف","باجي نور","أم ليث","باجي علا",
          "أم سعد","باجي ريم","أم تقي","باجي ياسمين"]
ALL_NAMES = MALE + FEMALE

GREET = ["السلام عليكم","هلو","مرحبا","هلا","صباح الخير","مساء الخير","سلام"]
GREET_R = ["وعليكم السلام، هلا وغلا","هلا بيك، تفضل","مرحبتين، شنو أكدر أساعدك",
           "أهلاً وسهلاً","هلا هلا، تفضل يا عمو","صباح النور، كيف أكدر أساعدك"]

CONFIRM  = _cat("الردود")
REJECT   = _cat("الرفض")
PRAISE   = _cat("المدح")
SYMPATHY = _cat("التعاطف والمواساة")
EMOTIONS = _cat("المشاعر")
DAILY    = _cat("كلمات يومية شائعة")
HOME     = _cat("البيت والمنزل")
FOOD_W   = _cat("الطعام والشراب")
HEALTH_W = _cat("الصحة والمرض")
WORK_W   = _cat("العمل والمهنة")
STUDY_W  = _cat("التعليم والدراسة")
TRANS_W  = _cat("المواصلات")
PLACE_W  = _cat("الأماكن")
RELIGION = _cat("الدين والمناسبات")
FAMILY_W = _cat("العلاقات والعائلة")
PROBLEMS = _cat("المشاكل والشكاوى")
WEATHER  = _cat("الطقس")
SPORT_W  = _cat("الرياضة والترفيه")
YOUTH    = _cat("كلمات الشباب")
QUESTIONS= _cat("السؤال")
TIME_W   = _cat("الوقت")

CLOSE = ["الله يوفقك","مشكور، تسلم","بالتوفيق إن شاء الله","يزاك الله خير",
         "الله يخليك","تسلم وتغنم","ما قصرت","شكراً جزيلاً"]
DISC_YES = ["ماشي، على خاطرك","تمام، نتفق","حاضر","إي زين، اتفقنا"]
DISC_NO  = ["والله ما أكدر، هذا آخر سعر","سعر ثابت مو ممكن أغيره","هذا سعر التكلفة"]

def vp(p, lo=0.93, hi=1.07):
    return f"{int(p * random.uniform(lo, hi) / 1000)*1000:,}"

def g(): return pick(GREET)
def gr(): return pick(GREET_R)
def cl(): return pick(CLOSE)
def sy(): return pick(SYMPATHY) if SYMPATHY else "الله يوفقك"
def hw(): return pick(HOME) if HOME else "بيت"
def fw(): return pick(FOOD_W) if FOOD_W else "أكلة"
def hlw(): return pick(HEALTH_W) if HEALTH_W else "دواء"
def rw(): return pick(RELIGION) if RELIGION else "إن شاء الله"

# ============================================================
# FILE 11 - HEALTH & MEDICAL
# ============================================================
DOCTORS   = ["دكتور علي","دكتور حسن","دكتورة سارة","دكتور أحمد","دكتورة نور","دكتور كريم"]
CLINICS   = ["عيادة الرازي","مستشفى ابن سينا","مركز الصحي","مستشفى اليرموك",
             "عيادة الشفاء","مستشفى الكندي"]
DISEASES  = ["ضغط عالي","سكر","ألم بالظهر","زكام وحرارة","وجع رأس","مشكلة بالمعدة",
             "ألم بالركبة","حساسية","مشكلة بالقلب","صداع مزمن"]
MEDS      = ["حبوب ضغط","إنسولين","مسكنات","مضاد حيوي","فيتامينات","حبوب سكر"]

def gen_health(i):
    doc   = pick(DOCTORS)
    doc2  = pick(DOCTORS)
    clin  = pick(CLINICS)
    clin2 = pick(CLINICS)
    dis   = pick(DISEASES)
    dis2  = pick(DISEASES)
    med   = pick(MEDS)
    med2  = pick(MEDS)
    nm    = pick(ALL_NAMES)
    _gr   = pick(GREET)
    _age  = pick(["طفل صغير","3 سنين","5 سنين","7 سنين","10 سنين","12 سنة"])
    _day  = pick(["باچر","بعد باچر","اليوم بعد العصر","نهاية الأسبوع","باچر الصبح"])
    _hour = pick(["8 الصبح","9 الصبح","10 الصبح","11 الصبح","3 العصر","4 العصر","5 العصر"])
    _dur  = pick(["من أمس","من يومين","من أسبوع","من الليلة الماضية","من شوية","من ثلاثة أيام"])
    _temp = pick(["37.8","38.0","38.5","39.0","39.2","38.7"])
    _days_course = pick(["5 أيام","7 أيام","10 أيام","أسبوعين"])
    _xray_type = pick(["أشعة صدر","أشعة على الظهر","أشعة على الركبة","سونار","MRI","CT scan"])
    _test_price = pick([15000,20000,25000,30000,35000,40000])
    _pkg_price  = pick([60000,80000,100000,120000,150000])
    _ins_ind    = pick([400000,500000,600000,700000,800000])
    _ins_fam    = pick([1000000,1200000,1500000,1800000])
    _sym  = pick(["حرارة ووجع رأس","غثيان وتعب","كحة وضيق بالصدر","وجع معدة","دوخة وارتجاف","طفح جلدي"])
    _wait = pick(["شخصين","3 أشخاص","4 أشخاص","5 أشخاص","شخص واحد"])
    _floor_num = pick(["الطابق الأول","الطابق الثاني","الطابق الأرضي","الطابق الثالث"])
    _ksh_price = pick([20000,25000,30000,35000,40000])
    _elder_age = pick(["60","65","70","75","80"])
    _jnrc_price = pick([6000,8000,10000,12000])
    tpl   = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد أحجز موعد عند {doc}"},
            {"role":"assistant","content":f"{gr()}. {doc} متاح {_day}. شنو شكوتك؟"},
            {"role":"user","content":f"عندي {dis} {_dur}"},
            {"role":"assistant","content":f"ماشي، سجلت اسمك. الموعد الساعة {_hour}"},
            {"role":"user","content":"الكشف بيش؟"},
            {"role":"assistant","content":f"كشف {doc} بـ{vp(_ksh_price)} دينار"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"عندي {dis} {_dur}، شتنصحني؟"},
            {"role":"assistant","content":f"لازم تروح دكتور. روح {clin} قريب منك"},
            {"role":"user","content":"ما أحب روح المستشفى"},
            {"role":"assistant","content":f"تره {dis} ما يتهاون فيها. الدكتور {doc} متاح {_day}"},
            {"role":"user","content":"ماشي، إن شاء الله أروح"},
            {"role":"assistant","content":"الله يشفيك ويعافيك"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"هلو، أريد {med} بدون روشيتة، أكو؟"},
            {"role":"assistant","content":"والله أخوي بعض الأدوية ما نكدر نبيعها بدون روشيتة"},
            {"role":"user","content":"بس أنا دايماً آخذها"},
            {"role":"assistant","content":f"هالمرة جيب روشيتة {doc} لو سمحت"},
            {"role":"user","content":"زين، بروح الدكتور"},
            {"role":"assistant","content":f"صح، {sy()}"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"ولدي {_age} عنده حرارة {_dur}، شسوي؟"},
            {"role":"assistant","content":"كم درجة الحرارة؟"},
            {"role":"user","content":f"{_temp}"},
            {"role":"assistant","content":f"حرارة {_temp} متوسطة. أعطيه {med} وماي هواي. لو ارتفعت روح الطوارئ"},
            {"role":"user","content":f"وإذا ما نزلت {_day}؟"},
            {"role":"assistant","content":f"روح {clin} الصبح وما تأخر"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"{_gr}، عندي موعد عند {doc} بس أريد أغيره"},
            {"role":"assistant","content":"ماشي، شوكت يناسبك؟"},
            {"role":"user","content":f"{_day}"},
            {"role":"assistant","content":f"{_day} {doc} عنده وقت الساعة {_hour}"},
            {"role":"user","content":"ممتاز، غيره لو سمحت"},
            {"role":"assistant","content":"تم التغيير، الله يشفيك"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"أريد أسأل، {_xray_type} تحتاج موعد مسبق؟"},
            {"role":"assistant","content":f"إي، لازم حجز لـ{_xray_type}. شنو المشكلة؟"},
            {"role":"user","content":f"عندي {dis} {_dur}"},
            {"role":"assistant","content":f"عندنا موعد {_day}. بكم تكدر تجي؟"},
            {"role":"user","content":"الصبح"},
            {"role":"assistant","content":f"تمام، سجلتك الساعة {_hour}. السعر {vp(_test_price)} دينار"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"دكتور {doc}، عندي {dis} من {_dur} ما تحسنت"},
            {"role":"assistant","content":"وينك تراجعت؟"},
            {"role":"user","content":"ما راجعت، كنت آخذ دواء من الصيدلية"},
            {"role":"assistant","content":"هذا غلط يا حجي، لازم تراجع دكتور. خليني أفحصك"},
            {"role":"user","content":"طيب دكتور، شنو عندي؟"},
            {"role":"assistant","content":f"تحتاج تحاليل أول. روشيتة وتجي {_day} بالنتيجة"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"الصيدلية عندكم بـ{clin}؟"},
            {"role":"assistant","content":f"إي، بـ{_floor_num}"},
            {"role":"user","content":f"أريد أعرف سعر {med}"},
            {"role":"assistant","content":f"{med} بـ{vp(_test_price)} دينار للعلبة"},
            {"role":"user","content":"عندكم البديل الأرخص؟"},
            {"role":"assistant","content":f"إي، عندنا جنيريك بنفس التأثير بـ{vp(_jnrc_price)} دينار"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":"أريد أسأل عن تأمين صحي"},
            {"role":"assistant","content":"أهلاً، شنو نوع التأمين اللي تريده؟"},
            {"role":"user","content":"تأمين يغطي العمليات والمستشفى"},
            {"role":"assistant","content":f"عندنا باكج شامل بـ{vp(_ins_ind)} دينار بالسنة. يغطي الطوارئ والعمليات والأدوية"},
            {"role":"user","content":"وتأمين العائلة؟"},
            {"role":"assistant","content":f"للعائلة كلها {vp(_ins_fam)} دينار بالسنة. يشمل {_wait}"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"والله أنا {pick(EMOTIONS) if EMOTIONS else 'تعبان'} من كثر المراجعات"},
            {"role":"assistant","content":f"{sy()}. شنو عندك بالضبط؟"},
            {"role":"user","content":f"عندي {dis} و{dis2} ومريت على ثلاث دكاترة ما حلوا"},
            {"role":"assistant","content":"هذا مؤسف. لازم تروح متخصص. وينك مراجعت؟"},
            {"role":"user","content":"بالحكومي"},
            {"role":"assistant","content":f"جرب {clin2} الخاص، الدكاترة أحسن وما فيه زحمة"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"شلونك {doc}؟"},
            {"role":"assistant","content":"الحمد لله بخير. شنو عندك؟"},
            {"role":"user","content":f"أريد فحص دوري شامل، عمري {pick(['30','35','40','45','50'])} سنة"},
            {"role":"assistant","content":f"أحسن شي. تحتاج تحاليل دم وبول و{_xray_type}"},
            {"role":"user","content":"كم يكلف كل هذا؟"},
            {"role":"assistant","content":f"التحاليل الشاملة بـ{vp(_pkg_price)} دينار. نتيجة خلال {pick(['ساعة','ساعتين','3 ساعات'])}"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"ما عندي بطاقة صحية، أكدر أراجع {clin}؟"},
            {"role":"assistant","content":"إي تكدر، بس بسعر بدون تأمين"},
            {"role":"user","content":"كم يكلف؟"},
            {"role":"assistant","content":f"كشف عادي {vp(_ksh_price)} دينار بدون بطاقة"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"تفضل، ملأ استمارة بالاستقبال {_floor_num} أول"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"ولدي عنده مشكلة بالأسنان، في دكتور أسنان بـ{clin}؟"},
            {"role":"assistant","content":f"إي عندنا عيادة أسنان بـ{_floor_num}"},
            {"role":"user","content":f"عمره {_age}، يقبلون أطفال؟"},
            {"role":"assistant","content":"إي طبعاً، عندنا دكتور متخصص بأسنان الأطفال"},
            {"role":"user","content":"الموعد شوكت؟"},
            {"role":"assistant","content":f"{_day}، الساعة {_hour}"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"أريد أسأل، عندي {dis}، أيش آكل وأيش أترك؟"},
            {"role":"assistant","content":f"لازم تقلل السكريات والنشويات. و{med} لازم تأخذه بانتظام"},
            {"role":"user","content":"يعني الرز والخبز؟"},
            {"role":"assistant","content":"تقليل مو تقطيع. نص حصة وزد الخضار. وروح دكتور تغذية"},
            {"role":"user","content":"في دكتور تغذية هنا؟"},
            {"role":"assistant","content":f"إي، موعده {_day} الساعة {_hour}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"هلو، عندي {dis} {_dur} وما أعرف شسوي"},
            {"role":"assistant","content":"شنو الأعراض بالتفصيل؟"},
            {"role":"user","content":f"{_sym}"},
            {"role":"assistant","content":f"يشبه {dis}. خذ {med} وارتاح يوم كامل"},
            {"role":"user","content":f"لو ما تحسنت {_day}؟"},
            {"role":"assistant","content":f"روح {clin} وما تتهاون"},
        ]
    elif tpl == 16:
        _col1 = pick(["الصفراء","الزرقاء","الكبسولات","الكبيرة"])
        _col2 = pick(["البيضاء","الحمراء","السائل","الصغيرة"])
        msgs = [
            {"role":"user","content":f"دكتور {doc}، هالأدوية {med}، متى آخذها؟"},
            {"role":"assistant","content":f"حبوب {_col1} بعد الأكل، و{_col2} قبل النوم"},
            {"role":"user","content":"وإذا نسيت حبة؟"},
            {"role":"assistant","content":"خذها لما تتذكر، بس لا تاخذ ضعفها"},
            {"role":"user","content":"كم يوم أكمل الكورس؟"},
            {"role":"assistant","content":f"{_days_course} كاملة، حتى لو تحسنت"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"والدي عمره {_elder_age} سنة وعنده {dis} و{dis2}، شنو تنصحني؟"},
            {"role":"assistant","content":"لازم متابعة منتظمة. فحص الضغط يومياً والسكر أسبوعياً"},
            {"role":"user","content":"الأدوية ما ينساها؟"},
            {"role":"assistant","content":"اشتري له منبه للأدوية أو علبة أيام الأسبوع"},
            {"role":"user","content":"وأكله؟"},
            {"role":"assistant","content":f"قلل الملح للضغط والسكر للسكري. وراجع {doc} كل {pick(['شهر','شهرين','3 أشهر'])}"},
        ]
    elif tpl == 18:
        _injury = pick(["جرح بالإيد","جرح بالرجل","حرق بسيط","كدمة","جرح بالوجه"])
        msgs = [
            {"role":"user","content":f"في طوارئ بـ{clin} ولا لازم أروح المستشفى؟"},
            {"role":"assistant","content":"عندنا طوارئ بسيطة. شنو المشكلة؟"},
            {"role":"user","content":f"{_injury}، محتاج خياطة"},
            {"role":"assistant","content":f"تعال هسه، نشوف {_injury}. إذا عميق نحيلك للجراحة"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"تفضل بالطوارئ على {pick(['اليمين','اليسار','الطابق الثاني'])}"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"شلونك {doc}، أجيت أشكرك، تحسنت كلش من {dis}"},
            {"role":"assistant","content":"الله يشفيك ويعافيك، هذا واجبنا"},
            {"role":"user","content":f"الأدوية {med} كملتها، لازم أكمل؟"},
            {"role":"assistant","content":f"إي، لا تقطع الأدوية بدون مراجعة، تعال بعد {pick(['أسبوع','أسبوعين','شهر'])}"},
            {"role":"user","content":"إن شاء الله دكتور"},
            {"role":"assistant","content":"دوم بصحة وعافية"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"دكتور {doc}، أريد أسألك عن {dis}، خطيرة؟"},
            {"role":"assistant","content":f"{dis} تحتاج متابعة، بس ما هي خطيرة لو اتعالجت"},
            {"role":"user","content":f"خذت {med} من أسبوع بدون وصفة"},
            {"role":"assistant","content":"هذا مو زين، الأدوية لازم تكون بوصفة طبية"},
            {"role":"user","content":"شسوي هلأ؟"},
            {"role":"assistant","content":f"تعال للعيادة {_day} وأكشفك بشكل صحيح"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"مرحبا، أبي مريض بـ{dis}، وين أقدر أجيب {med} بالجملة؟"},
            {"role":"assistant","content":"جملة الأدوية تحتاج وصفة دكتور وترخيص"},
            {"role":"user","content":"بس محتاجين كمية كبيرة"},
            {"role":"assistant","content":f"روح {clin} وتكلم الدكتور، يعطيك وصفة لكمية أكبر"},
            {"role":"user","content":"والسعر يفرق؟"},
            {"role":"assistant","content":f"بالجملة {vp(_jnrc_price*3)} للكرتون. توفير كبير"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"السلام عليكم، ولدي {nm} عنده حساسية من {med}"},
            {"role":"assistant","content":f"مهم جداً تعرف هذا الشي. شنو الأعراض لما يأخذه؟"},
            {"role":"user","content":f"{_sym}"},
            {"role":"assistant","content":f"هذي أعراض حساسية دوائية. لازم تسجله بسجل الحساسية عند {doc}"},
            {"role":"user","content":"وشنو البديل؟"},
            {"role":"assistant","content":f"الدكتور يوصف {med2} بدله، لا تخاف"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"هلو، سمعت {clin2} أحسن من {clin}، صحيح؟"},
            {"role":"assistant","content":"كل عيادة عندها مميزاتها. شنو تبي تراجع؟"},
            {"role":"user","content":f"عندي {dis}"},
            {"role":"assistant","content":f"لهذا الشي {doc} بـ{clin} متخصص. هو الأفضل"},
            {"role":"user","content":"ماشي، بحجز عنده"},
            {"role":"assistant","content":f"الحجز بالتلفون أو تجي هسه، {_day} عنده وقت"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":"أريد أعرف عن فحص السكر الدوري، مهم؟"},
            {"role":"assistant","content":"مهم جداً، خصوصاً لو عندك تاريخ عائلي بالسكر"},
            {"role":"user","content":"كيف أعرف إذا عندي سكر؟"},
            {"role":"assistant","content":f"أبسط طريقة فحص دم صيام. يكلف {vp(_test_price)} دينار"},
            {"role":"user","content":"وإذا الفحص طلع عالي؟"},
            {"role":"assistant","content":f"راجع {doc} ويفسرلك النتيجة ويعطيك خطة علاج"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"دكتور، عندي وجع بالظهر {_dur}، شسوي؟"},
            {"role":"assistant","content":"هل الوجع مستمر ولا يجي ويروح؟"},
            {"role":"user","content":"مستمر ويشتد بالليل"},
            {"role":"assistant","content":f"هذا يحتاج {_xray_type}. بكتبلك طلب"},
            {"role":"user","content":"وإذا الأشعة طلعت سليمة؟"},
            {"role":"assistant","content":f"نعمل تحليل دم إضافي. لا تقلق نوصل للسبب"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أحجز عند {doc2} بدل {doc}"},
            {"role":"assistant","content":f"{doc2} عنده دوام {_day}. شنو السبب؟"},
            {"role":"user","content":f"راجعت {doc} مرتين وما تحسنت"},
            {"role":"assistant","content":f"نفهمك، {doc2} متخصص بـ{dis}، ممكن يساعدك أكثر"},
            {"role":"user","content":"ماشي، سجلني عنده"},
            {"role":"assistant","content":f"تم، الموعد {_day} الساعة {_hour}"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":"أريد أعرف، لو أجيت بدون موعد تقبلونني؟"},
            {"role":"assistant","content":f"في عيادة الطوارئ إي، بس للدكاترة المتخصصين لازم موعد"},
            {"role":"user","content":"عندي شي مستعجل"},
            {"role":"assistant","content":"شنو المشكلة، أنا أشوف إذا أكو إلغاء موعد اليوم"},
            {"role":"user","content":f"عندي {_sym}"},
            {"role":"assistant","content":f"هذا يحتاج اهتمام. تعال هسه و{doc} يشوفك بين المواعيد"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"ابنتي حامل وتشكي من {_sym}، شنو أسوي؟"},
            {"role":"assistant","content":"الحمل وقت حساس. هذي الأعراض شنو مدتها؟"},
            {"role":"user","content":f"{_dur}"},
            {"role":"assistant","content":f"لازم تراجع دكتورة نساء هسه. لا تتأخر"},
            {"role":"user","content":"في دكتورة بـ{clin}؟"},
            {"role":"assistant","content":f"إي، {doc} متخصصة. موعدها {_day}"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":"هلو، أريد نتيجة تحاليلي، اسمي {nm}"},
            {"role":"assistant","content":"تفضل، شوكت سويتها؟"},
            {"role":"user","content":f"{_dur}"},
            {"role":"assistant","content":"تفضل بالمختبر، شارك هويتك والإيصال"},
            {"role":"user","content":"النتيجة جاهزة؟"},
            {"role":"assistant","content":f"إي جاهزة، والدكتور {doc} يفسرها {_day}"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد أعرف ساعات دوام {clin}"},
            {"role":"assistant","content":"الدوام من 8 الصبح للساعة 8 بالليل بدون انقطاع"},
            {"role":"user","content":"حتى الجمعة؟"},
            {"role":"assistant","content":"الجمعة من 10 الصبح لـ4 العصر"},
            {"role":"user","content":f"وهل {doc} موجود كل أيام؟"},
            {"role":"assistant","content":f"{doc} موجود يومياً ما عدا {pick(['الثلاثاء','الأربعاء','الخميس'])}"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"دكتور، أخذت {med} و{med2} مع بعض، مشكلة؟"},
            {"role":"assistant","content":"بعض الأدوية ما تنحط مع بعض. شنو الجرعة؟"},
            {"role":"user","content":"ما أدري، المكتوب على العلبة"},
            {"role":"assistant","content":f"كفي آخذ {med2} حتى أشوفك. تعال {_day}"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":"الله يسلمك، لا تهاون بالأدوية"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"أريد أعرف، سعر عملية {dis} كم؟"},
            {"role":"assistant","content":f"عملية {dis} تختلف حسب الوضع والمستشفى"},
            {"role":"user","content":"تقريباً؟"},
            {"role":"assistant","content":f"بين {vp(_ins_ind)} وـ{vp(_ins_fam)} حسب التعقيد"},
            {"role":"user","content":"والتأمين يغطي؟"},
            {"role":"assistant","content":"لو عندك تأمين شامل يغطي أغلبها. راجع شركة التأمين"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"مرحبا، عندي فحص دم باچر، أكل شي؟"},
            {"role":"assistant","content":"إذا فحص صيام لازم ما تاكل 8 ساعات قبله"},
            {"role":"user","content":"وماي أشرب؟"},
            {"role":"assistant","content":"ماي عادي مسموح، ما تشرب شاي أو قهوة"},
            {"role":"user","content":"وإذا فطرت بالغلط؟"},
            {"role":"assistant","content":f"تأجل الفحص ليوم ثاني. لا تجي وأنت غير صايم"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"هلو، أبي عنده {dis} وما يريد ياكل أدوية، شسوي؟"},
            {"role":"assistant","content":"هذا موقف صعب. شنو سبب رفضه؟"},
            {"role":"user","content":"يقول ما يثق بالأطباء"},
            {"role":"assistant","content":f"جرب تاخذه لـ{doc}، أسلوبه هادي ويفهم الكبار"},
            {"role":"user","content":"وإذا رفض؟"},
            {"role":"assistant","content":f"ربما مع {dis} تتفاقم ويضطر يراجع. لا تضغط عليه، اقنعه بهدوء"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"دكتور، شلون أحسن علاج لـ{dis}؟"},
            {"role":"assistant","content":f"العلاج يختلف حسب مرحلة {dis}. لازم أفحصك أول"},
            {"role":"user","content":"تقريباً؟"},
            {"role":"assistant","content":f"الغالب {med} مع نظام غذائي وراحة كافية"},
            {"role":"user","content":"كم مدة العلاج؟"},
            {"role":"assistant","content":f"بين {_days_course} وأشهر حسب التحسن. متابعة ضرورية"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":f"هلو، سمعت {dis} معدية، صح؟"},
            {"role":"assistant","content":f"يختلف، بعض {dis} معدي وبعضه مو معدي"},
            {"role":"user","content":"كيف أحمي عيالي؟"},
            {"role":"assistant","content":"نظافة اليدين والتهوية المناسبة بالبيت"},
            {"role":"user","content":"وإذا أحد احتك بالمريض؟"},
            {"role":"assistant","content":f"لو ظهرت أعراض {_sym} عليه، راجع {clin} فوراً"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":f"أريد أعرف، أكو لقاح لـ{dis}؟"},
            {"role":"assistant","content":f"بعض أنواع {dis} عندها لقاح. شنو عمر من تريد تطعمه؟"},
            {"role":"user","content":f"ولدي {_age}"},
            {"role":"assistant","content":f"بهالعمر اللقاحات تكون فعالة. راجع {clin} لجدول التطعيم"},
            {"role":"user","content":"مجاني؟"},
            {"role":"assistant","content":f"اللقاحات الأساسية مجانية، البعض الاختياري بـ{vp(_test_price)} دينار"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"هلو، عندي تقرير طبي وما أفهمه، تقدر تشرحلي؟"},
            {"role":"assistant","content":"طبعاً. شو مكتوب فيه؟"},
            {"role":"user","content":f"مكتوب عندي {dis} ويحتاج {_xray_type}"},
            {"role":"assistant","content":f"{dis} تحتاج {_xray_type} علشان نشوف بالتفصيل. هذا طلب عادي"},
            {"role":"user","content":"مو خطيرة؟"},
            {"role":"assistant","content":f"مو خطيرة لو اتعالجت بالوقت. الدكتور {doc} يفسرها بالكامل"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":f"دكتور، أريد أنزل وزن، كيف؟"},
            {"role":"assistant","content":"الأكل الصحي والرياضة هم الحل الأساسي"},
            {"role":"user","content":"ما عندي وقت للرياضة"},
            {"role":"assistant","content":"حتى مشي 30 دقيقة يوميا يفرق. وقلل الدهون والسكريات"},
            {"role":"user","content":"في أدوية تساعد؟"},
            {"role":"assistant","content":f"في بس بوصفة طبية. تعال {_day} وأشوف وضعك"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"السلام عليكم، ولدي عنده {dis} ومريض من {_dur}"},
            {"role":"assistant","content":f"تعال هسه، لا تتأخر مع {dis}"},
            {"role":"user","content":"الطوارئ مفتوحة؟"},
            {"role":"assistant","content":"إي، الطوارئ 24 ساعة. تعال الحين"},
            {"role":"user","content":"ماشي، جاي هسه"},
            {"role":"assistant","content":f"الله يشفيه، {doc} مناوب الليل"},
        ]
    elif tpl == 41:
        msgs = [
            {"role":"user","content":f"هلو، أسألك، {med} يسبب نعاس؟"},
            {"role":"assistant","content":f"بعض {med} نعم يسبب نعاس. متى تاخذه؟"},
            {"role":"user","content":"الصبح قبل الشغل"},
            {"role":"assistant","content":"حوله للعصر أو قبل النوم. يأثر أقل على نشاطك"},
            {"role":"user","content":"وإذا نسيته؟"},
            {"role":"assistant","content":f"خذه لما تتذكر بس لا تضاعف. الانتظام بـ{_days_course} مهم"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أسأل عن دكتور {pick(['قلب','عيون','أعصاب','عظام','جلدية'])} ممتاز"},
            {"role":"assistant","content":f"عندنا متخصصين في كل هذه المجالات بـ{clin}"},
            {"role":"user","content":"الأغلى دكتور أحسن؟"},
            {"role":"assistant","content":"مو بالضرورة. بعض الدكاترة خبرتهم ممتازة وسعرهم معقول"},
            {"role":"user","content":"تنصحني بأحد؟"},
            {"role":"assistant","content":f"الدكتور {doc} عنده خبرة {pick(['15','20','25'])} سنة. الناس تمدحه"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"هلو، عندي فحص غداً، شو لازم أجيب معي؟"},
            {"role":"assistant","content":"هوية الأحوال، ونتائج تحاليل سابقة لو عندك"},
            {"role":"user","content":"الأشعة القديمة أجيبها؟"},
            {"role":"assistant","content":"إي، مهم تجيبها علشان المقارنة"},
            {"role":"user","content":f"والموعد الساعة {_hour}، صح؟"},
            {"role":"assistant","content":f"إي صح. جي قبل {pick(['10','15','20'])} دقيقة للتسجيل"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"{_gr}، ابنتي تعبانة وعندها {_sym}"},
            {"role":"assistant","content":f"{sy()}. كم عمرها؟"},
            {"role":"user","content":f"{_age}"},
            {"role":"assistant","content":f"بهالعمر لازم تراجع دكتور أطفال. {doc} متاح {_day}"},
            {"role":"user","content":"الكشف كم؟"},
            {"role":"assistant","content":f"كشف الأطفال {vp(_ksh_price)} دينار. يستاهل عافيتها"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"دكتور {doc}، قلت لي أجي بعد شهر، بس تحسنت، لازم أجي؟"},
            {"role":"assistant","content":"إي لازم تجي حتى لو تحسنت. المتابعة مهمة"},
            {"role":"user","content":"ليش إذا أنا بخير؟"},
            {"role":"assistant","content":f"بعض حالات {dis} تتحسن بالظاهر بس الجذر ما اتحل"},
            {"role":"user","content":"ماشي، بحجز"},
            {"role":"assistant","content":f"الله يحفظك. موعدك {_day} الساعة {_hour}"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"هلو، أريد أجيب والدتي للفحص، هي {_elder_age} سنة وما تكدر تمشي"},
            {"role":"assistant","content":"عندنا كراسي متحركة ومرافقين يساعدون"},
            {"role":"user","content":"الموعد ينجز بسرعة؟"},
            {"role":"assistant","content":"لأهل السن والمحتاجين خدمة أولوية، ما راح تنتظرون طويل"},
            {"role":"user","content":"شكراً، الله يجزاكم خير"},
            {"role":"assistant","content":f"هلا وغلا، نوعدك بأحسن خدمة. الموعد {_day}"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"أريد أسأل، لو أحس بـ{_sym} عالطريق، شسوي؟"},
            {"role":"assistant","content":"لو كان الوضع حرج، اتصل إسعاف مباشرة"},
            {"role":"user","content":"رقم الإسعاف؟"},
            {"role":"assistant","content":"115، وروح أقرب طوارئ مو تتأخر"},
            {"role":"user","content":"ماشي، أحفظ الرقم"},
            {"role":"assistant","content":"صح. وخذ معك دايماً بطاقة مكتوب عليها مرضك وأدويتك"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"مرحبا، ابني {nm} عنده امتحانات وضغطه عالي من التعب"},
            {"role":"assistant","content":"الضغط النفسي يأثر على الصحة. شنو أعراضه؟"},
            {"role":"user","content":f"{_sym}"},
            {"role":"assistant","content":"هذي أعراض الإجهاد. راحة وأكل صحي ونوم كافي"},
            {"role":"user","content":"أدوية تساعد؟"},
            {"role":"assistant","content":f"مفيتش حاجة بدون فحص. تعال {_day} نشوفه"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أسألك دكتور، {med} يتداخل مع الأكل؟"},
            {"role":"assistant","content":f"بعض الأدوية مثل {med} أحسن تاخذها مع الأكل علشان ما تأذي المعدة"},
            {"role":"user","content":"وإذا أخذته بدون أكل؟"},
            {"role":"assistant","content":"قد يحس بغثيان. أكل خفيف كافي"},
            {"role":"user","content":"والقهوة؟"},
            {"role":"assistant","content":"ابعد القهوة ساعة على الأقل بعد الدواء"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"هلو، {nm}، ولدي عنده {dis} {_dur}، شوكت {doc} موجود؟"},
            {"role":"assistant","content":f"{doc} يجي بعد {pick(['ساعة','نص ساعة','ساعتين'])}. اكعد بالانتظار"},
            {"role":"user","content":"عنده زحمة؟"},
            {"role":"assistant","content":f"{_wait} قبلك بس"},
            {"role":"user","content":"ماشي، أنتظر"},
            {"role":"assistant","content":"الله يشفي ولدك ويعافيه"},
        ]

    return {"id": f"health_{i:04d}", "category": "healthcare", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 12 - EDUCATION
# ============================================================
SCHOOLS   = ["مدرسة الرصافة","ثانوية المتنبي","مدرسة الكرادة الابتدائية","ثانوية الكرخ"]
UNIS      = ["جامعة بغداد","الجامعة المستنصرية","جامعة النهرين","الجامعة التكنولوجية"]
SUBJECTS  = ["رياضيات","فيزياء","كيمياء","أحياء","عربي","إنجليزي","تاريخ","جغرافية"]
TUTORS    = ["أستاذ سامر","أستاذة رنا","أستاذ علاء","أستاذة دينا","أستاذ حسن"]

def gen_education(i):
    school = pick(SCHOOLS)
    school2= pick(SCHOOLS)
    uni    = pick(UNIS)
    uni2   = pick(UNIS)
    subj   = pick(SUBJECTS)
    subj2  = pick(SUBJECTS)
    tutor  = pick(TUTORS)
    tutor2 = pick(TUTORS)
    _gr    = pick(GREET)
    _grade = pick(["الصف الثاني","الصف الثالث","الصف الخامس","الصف السادس","الأول متوسط","الثالث متوسط","الثاني إعدادي","الثالث إعدادي"])
    _score = pick(["55","60","65","70","75","80","85","90","92","95"])
    _fee   = pick([30000,40000,50000,60000,75000,100000])
    _day   = pick(["باچر","بعد باچر","نهاية الأسبوع","هذا الأسبوع","باچر الصبح"])
    _hour  = pick(["8 الصبح","9 الصبح","10 الصبح","3 العصر","4 العصر","5 العصر","6 المساء"])
    _sessions = pick(["3 مرات بالأسبوع","مرتين بالأسبوع","يومياً","4 مرات بالأسبوع"])
    _dur_course = pick(["شهر","شهرين","3 أشهر","فصل دراسي","سنة"])
    _nm    = pick(ALL_NAMES)
    _spec  = pick(["هندسة","طب","صيدلة","قانون","اقتصاد","حاسبات","تربية","إعلام"])
    _years_gap = pick(["5 سنين","7 سنين","10 سنين","3 سنين","سنتين"])
    _abroad = pick(["تركيا","ماليزيا","أوروبا","كندا","ألمانيا","مصر","الأردن"])
    _level_eng = pick(["بيجنر","مبتدئ","متوسط","متقدم","بزنس إنجليش"])
    tpl    = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد أسجل ولدي بـ{school}"},
            {"role":"assistant","content":f"{gr()}. شنو صف ولدك؟"},
            {"role":"user","content":f"{_grade}"},
            {"role":"assistant","content":f"عندنا أماكن متاحة. تحتاج شهادة الميلاد وهوية الأب وصورتين"},
            {"role":"user","content":"الرسوم كم؟"},
            {"role":"assistant","content":f"التسجيل {vp(_fee)} دينار، والقسط الفصلي {vp(_fee*4)} دينار"},
        ]
    elif tpl == 2:
        hrs_per_week = pick(["ساعتين","ساعة","3 ساعات"])
        loc = pick(["البيت","عنده","أونلاين"])
        msgs = [
            {"role":"user","content":f"أريد أستاذ {subj} لابني {_grade}"},
            {"role":"assistant","content":f"{tutor} متخصص بـ{subj}. كم ساعة بالأسبوع تريد؟"},
            {"role":"user","content":f"{hrs_per_week} بالأسبوع"},
            {"role":"assistant","content":f"الأجر {vp(_fee)} للساعة. {loc} أحسن لك؟"},
            {"role":"user","content":f"{loc} أحسن"},
            {"role":"assistant","content":f"ماشي، أعطيك رقم {tutor} تتفق على المواعيد"},
        ]
    elif tpl == 3:
        _min_score = pick(["65","70","75"])
        _med_score = pick(["90","92","93","94"])
        msgs = [
            {"role":"user","content":f"هلو، أريد أعرف شروط القبول بـ{uni}"},
            {"role":"assistant","content":f"المعدل الأدنى للقبول {_min_score}%، ويختلف حسب الكلية"},
            {"role":"user","content":f"{_spec} يحتاج كام؟"},
            {"role":"assistant","content":f"{_spec} يحتاج {_med_score}% وأعلى في الغالب"},
            {"role":"user","content":f"ولدي معدله {_score}%"},
            {"role":"assistant","content":f"معدل {_score}% يؤهله لـ{pick(['هندسة','إعلام','اقتصاد','قانون','تربية'])} بـ{uni}"},
        ]
    elif tpl == 4:
        _days_review = pick(["3 أيام","أسبوع","5 أيام"])
        msgs = [
            {"role":"user","content":f"أستاذ، ابنتي رسبت بـ{subj}، شسوي؟"},
            {"role":"assistant","content":"لا تنزعل، ممكن تراجع؟"},
            {"role":"user","content":"إي، كيف؟"},
            {"role":"assistant","content":f"تقدم طلب مراجعة ورقة الإجابة خلال {_days_review} من النتيجة"},
            {"role":"user","content":"وإذا ما تغيرت النتيجة؟"},
            {"role":"assistant","content":"تسجل امتحان إكمال، إن شاء الله تنجح"},
        ]
    elif tpl == 5:
        _advantage = pick(["الشهادة أقوى","الرسوم مجانية","الأساتذة أحسن","المختبرات أفضل"])
        msgs = [
            {"role":"user","content":f"ما أعرف أختار بين {uni} الحكومية و{uni2} الأهلية لـ{_spec}، شتنصحني؟"},
            {"role":"assistant","content":f"الحكومية أرخص ومعترف فيها أكثر، الأهلية أسهل قبول بـ{_spec}"},
            {"role":"user","content":"بس الحكومية زحمة"},
            {"role":"assistant","content":f"صح، بس {_advantage} بـ{uni} يستاهل"},
            {"role":"user","content":"والله صح، أحاول الحكومية أول"},
            {"role":"assistant","content":f"إن شاء الله تقبل بـ{uni}"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"الدراسة بـ{uni} كيف؟ أنا ناوي أتقدم بـ{_spec}"},
            {"role":"assistant","content":f"{uni} ممتازة. {_spec} عندهم أساتذة كبار"},
            {"role":"user","content":f"المعدل المطلوب لـ{_spec}؟"},
            {"role":"assistant","content":f"{_spec} يحتاج {_score}% وأعلى"},
            {"role":"user","content":"التقديم متى يبدأ؟"},
            {"role":"assistant","content":"التقديم يبدأ بعد إعلان نتائج السادس، تابع الموقع الرسمي"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"أبني {_grade}، كيف أساعده يذاكر {subj}؟"},
            {"role":"assistant","content":"حدد وقت ثابت للمذاكرة كل يوم بعد العصر"},
            {"role":"user","content":"يتشتت هواي من الموبايل"},
            {"role":"assistant","content":f"بعّد عنه الموبايل وقت المذاكرة. قسّم {subj} على أيام"},
            {"role":"user","content":"وإذا ما فهم؟"},
            {"role":"assistant","content":f"اشرحله بأسلوب بسيط، أو استعن بـ{tutor} كأستاذ خصوصي"},
        ]
    elif tpl == 8:
        _area = pick(["الكرادة","المنصور","الكاظمية","الجادرية","زيونة"])
        msgs = [
            {"role":"user","content":f"في دورات تعليم {pick(['إنجليزي','فرنسي','ألماني'])} قريبة من {_area}؟"},
            {"role":"assistant","content":f"إي، عندنا مراكز بـ{_area} نفسها"},
            {"role":"user","content":"الرسوم كم؟"},
            {"role":"assistant","content":f"بين {vp(100000)} لـ{vp(300000)} دينار بالشهر حسب المستوى"},
            {"role":"user","content":f"مستوى {_level_eng} للكبار أكو؟"},
            {"role":"assistant","content":f"إي، عندنا كورسات {_level_eng} للكبار من الساعة {_hour}"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"أستاذ {tutor}، ابني ما يفهم {subj} أبد"},
            {"role":"assistant","content":f"لا تقلق، {subj} تحتاج أسلوب معين"},
            {"role":"user","content":f"حاولنا أكثر من أستاذ، حتى {tutor2}"},
            {"role":"assistant","content":"كل طالب يتعلم بطريقة مختلفة. أنا أشتغل على الفهم مو الحفظ"},
            {"role":"user","content":"إن شاء الله ينجح معك"},
            {"role":"assistant","content":f"إن شاء الله، أعطيه {pick(['شهر','أسبوعين','3 أسابيع'])} وتشوف الفرق"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"الواجبات {subj} كلش كثيرة، ابني {_grade} يتعب"},
            {"role":"assistant","content":"إي والله، المناهج ثقيلة هالأيام"},
            {"role":"user","content":"كيف يخلص الواجبات بسرعة؟"},
            {"role":"assistant","content":f"الأهم يخلص {subj} أول وهو مرتاح، بعدين باقي المواد"},
            {"role":"user","content":"وإذا ما فهم الواجب؟"},
            {"role":"assistant","content":f"يخبر {tutor} بالصبح، الأستاذ يشرحله قبل الحصة"},
        ]
    elif tpl == 11:
        _last_school = pick(["الابتدائية","المتوسطة","الإعدادية","الصف السادس"])
        _near_area   = pick(["قريب من البيت","بالكرادة","بالمنصور","بالكاظمية","قريب"])
        msgs = [
            {"role":"user","content":f"أريد أكمل دراستي، وقفت عند {_last_school} من {_years_gap}"},
            {"role":"assistant","content":"ماكو مشكلة، تكدر تكمل بتعليم الكبار"},
            {"role":"user","content":"كيف أسجل؟"},
            {"role":"assistant","content":f"في مراكز تعليم الكبار {_near_area} تابعة للوزارة"},
            {"role":"user","content":"مجانية؟"},
            {"role":"assistant","content":f"إي مجانية كلش، نقدر نسجلك هسه للفصل {pick(['الأول','الثاني','القادم'])}"},
        ]
    elif tpl == 12:
        _abroad_city = pick(["إسطنبول","أنقرة","كوالالمبور","برلين","تورنتو","القاهرة","عمّان"])
        msgs = [
            {"role":"user","content":f"ابنتي تبي تدرس {_spec} بـ{_abroad}، شتنصحني؟"},
            {"role":"assistant","content":f"{_abroad} عندها جامعات ممتازة بـ{_spec}. شنو ميزانيتكم؟"},
            {"role":"user","content":f"معقول، ما نقدر نصرف هواي"},
            {"role":"assistant","content":f"{_abroad_city} أسعارها معقولة مقارنة بأوروبا"},
            {"role":"user","content":"الشهادة معترف فيها بالعراق؟"},
            {"role":"assistant","content":f"إي، بس تحتاج معادلة من وزارة التعليم بعد الرجوع من {_abroad}"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"هلو، أسألك، {tutor} يدرس {subj} و{subj2}؟"},
            {"role":"assistant","content":f"{tutor} متخصص بـ{subj}. لـ{subj2} عندنا {tutor2}"},
            {"role":"user","content":"والسعر؟"},
            {"role":"assistant","content":f"{tutor} بـ{vp(_fee)} للساعة. {tutor2} بـ{vp(_fee)} كذلك"},
            {"role":"user","content":"والجدول؟"},
            {"role":"assistant","content":f"{_sessions}. المواعيد تتفق معهم"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"هلو، ابني {_grade} ومعدله {_score}%، يكفي للجامعة؟"},
            {"role":"assistant","content":f"معدل {_score}% ممتاز. يقدر يتقدم لـ{_spec}"},
            {"role":"user","content":f"يحلم بـ{pick(['طب','هندسة','صيدلة'])}"},
            {"role":"assistant","content":f"لهذا يحتاج {pick(['90%','92%','95%'])} وأعلى. لازم يركز أكثر"},
            {"role":"user","content":"أستاذ خصوصي يفيد؟"},
            {"role":"assistant","content":f"إي كثير. {tutor} ممتاز لـ{subj}، جرب معه"},
        ]
    elif tpl == 15:
        _wait_time = pick(["شهر","شهرين","3 أشهر","الفصل الثاني"])
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أسجل ولدي بـ{school} للـ{_grade} بس قائمة انتظار؟"},
            {"role":"assistant","content":f"إي، هالسنة الطلبات كثيرة بـ{school}"},
            {"role":"user","content":"كم وقت الانتظار؟"},
            {"role":"assistant","content":f"من {_wait_time} تقريباً"},
            {"role":"user","content":f"أسجل بـ{school2} ريثما؟"},
            {"role":"assistant","content":f"فكرة ممتازة، {school2} قريبة وعندها مكان. وبعدين تنقل لما يجي دورك بـ{school}"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أستاذ {tutor}، كيف تشرح {subj} بطريقة مبسطة للأطفال؟"},
            {"role":"assistant","content":f"{subj} أحسن أشرحها بالأمثلة من الحياة اليومية"},
            {"role":"user","content":"ابني ما يحب المادة أصلاً"},
            {"role":"assistant","content":"هذي مشكلة نفسية مو علمية. لازم نحببه بالمادة أول"},
            {"role":"user","content":"كيف؟"},
            {"role":"assistant","content":f"ألعاب تعليمية وقصص. أعطيني {pick(['أسبوعين','شهر'])} وتشوف"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"هلو، أريد معلومات عن كلية {_spec} بـ{uni}"},
            {"role":"assistant","content":f"كلية {_spec} عندها {pick(['4','5','6'])} سنوات دراسية"},
            {"role":"user","content":"التوظيف بعد التخرج؟"},
            {"role":"assistant","content":f"خريجي {_spec} عندهم فرص ممتازة بالقطاع {pick(['الحكومي','الخاص','كليهما'])}"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"للحكومية مجانية. الأهلية بـ{vp(_fee*5)} بالفصل"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"ابني ينسى كل شي يحفظه بـ{subj}، شسوي؟"},
            {"role":"assistant","content":"هذي مشكلة الحفظ بدون فهم. لازم تغير الأسلوب"},
            {"role":"user","content":"يعني؟"},
            {"role":"assistant","content":"بدل الحفظ الحرفي، يفهم الفكرة ويشرحها بكلامه"},
            {"role":"user","content":"وإذا ما ينجح؟"},
            {"role":"assistant","content":f"{tutor} يستخدم خرائط ذهنية. جرب معه {_sessions}"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"مرحبا، ابنتي تحب {subj} وتريد تكمل بيها بالجامعة"},
            {"role":"assistant","content":f"ممتاز، {subj} تخصص واعد"},
            {"role":"user","content":f"وين أحسن جامعة لـ{subj}؟"},
            {"role":"assistant","content":f"{uni} من أفضل الجامعات لـ{subj} بالعراق"},
            {"role":"user","content":"المعدل المطلوب؟"},
            {"role":"assistant","content":f"{_score}% فأكثر للقبول"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"هلو، أريد كتب {subj} للسنة الدراسية الجديدة"},
            {"role":"assistant","content":f"كتب {subj} متوفرة. أي صف؟"},
            {"role":"user","content":f"{_grade}"},
            {"role":"assistant","content":f"مجموعة {_grade} بـ{vp(_fee)} الكل"},
            {"role":"user","content":"وين أجيها؟"},
            {"role":"assistant","content":"مكتبة {school} أو المكتبات المركزية بالكرادة"},
        ]
    elif tpl == 21:
        _transfer_reason = pick(["انتقلنا للسكن بمنطقة ثانية","المدرسة بعيدة عن بيتنا الجديد","ظروف عائلية","قرب من العمل"])
        _transfer_time = pick(["أسبوع","أسبوعين","3 أيام عمل"])
        msgs = [
            {"role":"user","content":f"السلام عليكم، أريد أغير ولدي {_grade} من {school} لـ{school2}"},
            {"role":"assistant","content":"النقل ممكن. شنو السبب؟"},
            {"role":"user","content":f"{_transfer_reason}"},
            {"role":"assistant","content":f"هذا سبب مقبول. تحتاج وثيقة السكن الجديد وكشف درجات {_grade}"},
            {"role":"user","content":"المدة؟"},
            {"role":"assistant","content":f"{_transfer_time} تقريباً لإكمال الإجراءات"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"أريد دورة مكثفة لـ{subj} قبل الامتحانات"},
            {"role":"assistant","content":f"أكو دورة مكثفة {subj} تبدأ {_day}"},
            {"role":"user","content":"كم ساعة؟"},
            {"role":"assistant","content":f"3 ساعات يومياً لمدة {_dur_course}"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"{vp(_fee*2)} دينار للدورة كاملة"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"أستاذ، شنو الفرق بين {subj} و{subj2}؟"},
            {"role":"assistant","content":f"{subj} يعتمد على النظريات، و{subj2} أكثر تطبيقي"},
            {"role":"user","content":f"أيش أفيد للمستقبل؟"},
            {"role":"assistant","content":f"يعتمد على اهتماماتك. لو تحب التطبيق خذ {subj2}"},
            {"role":"user","content":"ماشي، فكر"},
            {"role":"assistant","content":f"والطريقتين ممتازتين، {tutor} يقدر ينصحك أكثر"},
        ]
    elif tpl == 24:
        _ill_days = pick(["يومين","3 أيام","أسبوع"])
        _exam_type = pick(["النهائي","الفصلي","المرحلي","الشهري"])
        msgs = [
            {"role":"user","content":f"هلو، ابني ما راح يگدر يحضر امتحان {subj} {_exam_type} لأنه مريض من {_ill_days}"},
            {"role":"assistant","content":"لازم تجيب تقرير طبي رسمي من {pick(['مستشفى حكومي','طبيب معترف به','عيادة مرخصة'])}"},
            {"role":"user","content":"وبعدين؟"},
            {"role":"assistant","content":f"نقدمه لإدارة {school} ويكون له امتحان بديل"},
            {"role":"user","content":"متى الامتحان البديل؟"},
            {"role":"assistant","content":f"خلال {pick(['أسبوع','أسبوعين','10 أيام'])} من انتهاء مرضه"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"مرحبا، في منح دراسية لـ{uni}؟"},
            {"role":"assistant","content":"إي، عندنا منح للطلاب المتميزين"},
            {"role":"user","content":"الشروط؟"},
            {"role":"assistant","content":f"معدل {_score}% فأكثر ونشاط لا صفي"},
            {"role":"user","content":"كيف أقدم؟"},
            {"role":"assistant","content":f"ملأ الاستمارة {_day} قبل نهاية الشهر"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"هلو، أريد أعرف منهج {subj} للسنة الجديدة اتغير؟"},
            {"role":"assistant","content":f"إي، منهج {subj} اتحدث بعض الفصول"},
            {"role":"user","content":"الكتب نفسها؟"},
            {"role":"assistant","content":f"الكتب اتغيرت لـ{_grade}. لازم تشتري الإصدار الجديد"},
            {"role":"user","content":"وين يباع؟"},
            {"role":"assistant","content":"مكتبة الوزارة أو المكتبات المرخصة"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"أستاذ {tutor}، بني يصير أستاذ {subj} مثلك؟"},
            {"role":"assistant","content":f"التعليم مهنة جميلة. يحتاج دراسة {_spec} أو تربية"},
            {"role":"user","content":f"كام سنة الدراسة؟"},
            {"role":"assistant","content":f"4 سنوات للبكالوريوس، وبعدين يكمل تدريبه"},
            {"role":"user","content":"والراتب؟"},
            {"role":"assistant","content":"ما هو كبير بالحكومي، بس بالخاص والدروس الخصوصية يعيش حلو"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"هلو، ابنتي تدرس بـ{school} وشكاوى من المناهج"},
            {"role":"assistant","content":"شنو المشكلة بالتحديد؟"},
            {"role":"user","content":f"المنهج {subj} طويل وما يكملونه"},
            {"role":"assistant","content":"هذا شكوى كثير من الأهالي. الأستاذ يختار المهم"},
            {"role":"user","content":"وإذا طلع بالامتحان شي ما درسوه؟"},
            {"role":"assistant","content":f"الامتحانات من مادة الكتاب فقط. لا تخاف"},
        ]
    elif tpl == 29:
        _job_type = pick(["شغل نص وقت","شغل بالمساء","شغل الأسبوع","شغل فريلانس"])
        _study_level = pick(["الجامعة","المتوسطة","الإعدادية","الثانوية"])
        msgs = [
            {"role":"user","content":f"مرحبا، ابني {_grade} بـ{_study_level} يبي يشتغل وهو يدرس، ممكن؟"},
            {"role":"assistant","content":"ممكن بس صعب. الدراسة تحتاج تركيز"},
            {"role":"user","content":f"{_job_type} بس"},
            {"role":"assistant","content":f"{_job_type} ممكن، بس لازم ينظم وقته ولا يهمل {subj}"},
            {"role":"user","content":"وإذا أثر على معدله؟"},
            {"role":"assistant","content":"الأولوية للدراسة. شغل الإجازة الصيفية أفضل بكثير"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"هلو، دروس {tutor} الخصوصية أونلاين أو بالحضور؟"},
            {"role":"assistant","content":f"{tutor} يعطي الاثنين. أيش تفضل؟"},
            {"role":"user","content":"أونلاين أسهل لنا"},
            {"role":"assistant","content":f"تمام، {_sessions} أونلاين. نفس السعر {vp(_fee)} بالساعة"},
            {"role":"user","content":"البرنامج المستخدم؟"},
            {"role":"assistant","content":f"زوم أو گوگل ميت. ابنك عنده كمبيوتر؟"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"أريد أسأل، {uni} أو {uni2}، أيش أفضل لـ{_spec}؟"},
            {"role":"assistant","content":f"{uni} أقدم وعندها مختبرات أحسن لـ{_spec}"},
            {"role":"user","content":f"بس {uni2} أقرب للبيت"},
            {"role":"assistant","content":"القرب مهم. بس الجودة أهم على المدى البعيد"},
            {"role":"user","content":"ماشي، أفكر"},
            {"role":"assistant","content":f"زر الجامعتين أول قبل ما تقرر"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"هلو، أريد أعرف نتيجة ابني بـ{school}"},
            {"role":"assistant","content":"اسم الطالب؟"},
            {"role":"user","content":f"{_nm}"},
            {"role":"assistant","content":f"تفضل بالسكرتارية الساعة {_hour}، معك هويتك"},
            {"role":"user","content":"ما أقدر أجي، أكدر أتصل؟"},
            {"role":"assistant","content":"النتائج مو تنعطى بالتلفون. لازم حضور أو وكيل رسمي"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"أستاذ، كيف أحضر ولدي للامتحان النهائي بـ{subj}؟"},
            {"role":"assistant","content":"ابدأ مبكر، لا تنتظر آخر أسبوع"},
            {"role":"user","content":"مو فاهم من وين يبدأ"},
            {"role":"assistant","content":"راجع الملاحظات من الأول، حدد الفصول المهمة"},
            {"role":"user","content":"وإذا فيه فصل صعب؟"},
            {"role":"assistant","content":f"خصص له وقت أكثر، أو تعال نشرحه مع {tutor}"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أسأل عن التسجيل ببرنامج الدراسات العليا بـ{uni}"},
            {"role":"assistant","content":"الدراسات العليا تحتاج بكالوريوس بمعدل لا يقل عن 70%"},
            {"role":"user","content":"معدلي 75%"},
            {"role":"assistant","content":"أهل. شنو التخصص اللي تريد؟"},
            {"role":"user","content":f"{_spec}"},
            {"role":"assistant","content":f"عندنا ماجستير {_spec}. التقديم يبدأ {_day}"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"هلو، ابني يبي يكمل دراسته بـ{_abroad}، شتقول؟"},
            {"role":"assistant","content":f"{_abroad} عندها جامعات ممتازة. شنو تخصصه؟"},
            {"role":"user","content":f"{_spec}"},
            {"role":"assistant","content":f"لـ{_spec} بـ{_abroad} شهرة عالمية. بس يحتاج اللغة"},
            {"role":"user","content":"اللغة كم يستغرق يتعلمها؟"},
            {"role":"assistant","content":f"من {pick(['6 أشهر','سنة','سنتين'])} حسب مستواه الحالي"},
        ]
    elif tpl == 36:
        _shy_grade = pick(["الابتدائية","المتوسطة","الإعدادية"])
        _shy_subject = pick(["العربي","الإنجليزي","العلوم","الرياضيات"])
        msgs = [
            {"role":"user","content":f"أستاذ {tutor}، ابنتي ذكية بـ{_shy_subject} بس خجولة بالفصل بـ{_shy_grade}"},
            {"role":"assistant","content":"الخجل طبيعي بهالمرحلة، بس نقدر نساعدها"},
            {"role":"user","content":"ما تجاوب بالفصل حتى وهي تعرف الجواب"},
            {"role":"assistant","content":f"نحاول أساليب تشاركية تريحها. أنا أشجعها بدروس {_shy_subject} الخصوصية أول"},
            {"role":"user","content":"كيف تبني ثقتها؟"},
            {"role":"assistant","content":f"مشاريع جماعية وعروض صغيرة بـ{_shy_subject} تبني ثقتها بنفسها تدريجياً"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":f"هلو، أريد أسجل بدورة {subj} بس عمري {pick(['35','40','45','50'])} سنة"},
            {"role":"assistant","content":"ما في عمر للتعلم. تفضل بالسجيل"},
            {"role":"user","content":"الأستاذ يقبل كبار؟"},
            {"role":"assistant","content":f"{tutor} عنده خبرة مع كل الأعمار"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"{vp(_fee)} بالشهر. تبدأ {_day} الساعة {_hour}"},
        ]
    elif tpl == 38:
        _absence_pct = pick(["10%","15%","20%"])
        _absent_days = pick(["3 أيام","5 أيام","أسبوع","أسبوعين"])
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أعرف نظام الحضور والغياب بـ{school} للـ{_grade}"},
            {"role":"assistant","content":f"الغياب المسموح {_absence_pct} من الحصص بالفصل الواحد"},
            {"role":"user","content":"وإذا زاد؟"},
            {"role":"assistant","content":"يحرم من الامتحان إلا بعذر طبي رسمي معتمد"},
            {"role":"user","content":f"ابني غاب {_absent_days} بسبب مرض"},
            {"role":"assistant","content":f"جيب تقرير طبي خلال {pick(['3 أيام','أسبوع'])} وسويه مراجعة لضمان حقه بالامتحان"},
        ]
    elif tpl == 39:
        _fav_sub = pick(["الرياضيات","العلوم","الإنجليزي","التاريخ","الجغرافية"])
        _branch = pick(["علمي","أدبي","مهني","فني"])
        msgs = [
            {"role":"user","content":f"أستاذ، ابني {_grade} يحب {_fav_sub} وما يحب {subj}، أكدر أركز على {_fav_sub} بس؟"},
            {"role":"assistant","content":f"الميول مهمة، بس {subj} لازم يدرسها بالمرحلة الحالية"},
            {"role":"user","content":"يعني ما أكدر؟"},
            {"role":"assistant","content":f"للـ{_grade} كل المواد إجبارية. بس لاحقاً يختار"},
            {"role":"user","content":"وبالثانوية؟"},
            {"role":"assistant","content":f"الثانوية عندها فروع: {_branch} وغيره. {_fav_sub} يحدد الفرع المناسب"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"هلو، أريد أعرف برنامج الدراسة المسائية بـ{uni}"},
            {"role":"assistant","content":"برنامج المسائي يبدأ من 4 العصر للساعة 9"},
            {"role":"user","content":"الشهادة نفسها للصباحي؟"},
            {"role":"assistant","content":"إي، نفس الشهادة ونفس المنهج"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"المسائي أعلى شوية، بـ{vp(_fee*8)} بالفصل"},
        ]
    elif tpl == 41:
        _failed_count = pick(["مادة واحدة","مادتين","3 مواد"])
        _failed_exam = pick(["الفصلي","النهائي","الشهري"])
        msgs = [
            {"role":"user","content":f"سلام، ابني {_grade} راسب {_failed_count} بالامتحان {_failed_exam}، كيف يعوضها؟"},
            {"role":"assistant","content":f"امتحان الإكمال لـ{_failed_count} في نهاية الإجازة الصيفية"},
            {"role":"user","content":"إذا رسب بالإكمال؟"},
            {"role":"assistant","content":f"بالنظام الجديد يمشي للـ{pick(['صف بعده','مرحلة أعلى'])} بمادة مقيدة ويكملها بالموازي"},
            {"role":"user","content":f"وهل يحتاج أستاذ لـ{_failed_count}؟"},
            {"role":"assistant","content":f"إي، {tutor} يقدر يساعده يجهز لامتحان الإكمال بـ{subj}"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"هلو، أريد أعرف إذا {tutor} يقبل طلاب جدد؟"},
            {"role":"assistant","content":f"{tutor} مجدوله ممتلئ الحين"},
            {"role":"user","content":"متى يفتح مكان؟"},
            {"role":"assistant","content":f"بعد {pick(['أسبوعين','شهر','نهاية الفصل'])}"},
            {"role":"user","content":"أسجلني على قائمة الانتظار"},
            {"role":"assistant","content":f"ماشي، سجلتك. نتصل عليك لما يفتح مكان"},
        ]
    elif tpl == 43:
        _family_want = pick(["طب","هندسة","محاسبة","قانون","اقتصاد"])
        msgs = [
            {"role":"user","content":f"أستاذ، ابنتي تريد تدرس {_spec} بـ{uni} بس العيلة تريدها {_family_want}"},
            {"role":"assistant","content":f"هذا موقف صعب. شنو سبب رفض {_spec}؟"},
            {"role":"user","content":f"يقولون سوق {_spec} ما فيه توظيف"},
            {"role":"assistant","content":f"سوق {_spec} واعد. خريجيه بالقطاع الخاص يكسبون أكثر من {_family_want}"},
            {"role":"user","content":"كيف أقنعهم؟"},
            {"role":"assistant","content":f"أرهم إحصائيات التوظيف الحقيقية وراتب متخصصي {_spec} بالسوق الحالي"},
        ]
    elif tpl == 44:
        _exam_start = pick(["نهاية الشهر الرابع","أول الشهر الخامس","منتصف الفصل","آخر الفصل"])
        _prior_notice = pick(["أسبوع","أسبوعين","3 أيام"])
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أعرف أوقات امتحانات {subj} الفصلية للـ{_grade} بـ{school}"},
            {"role":"assistant","content":f"امتحانات {subj} تبدأ {_exam_start} من الفصل"},
            {"role":"user","content":"الجدول متى يطلع؟"},
            {"role":"assistant","content":f"الجدول ينزل على لوحة إعلانات {school} قبل {_prior_notice}"},
            {"role":"user","content":"وإذا فيه تعارض مع امتحان {subj2}؟"},
            {"role":"assistant","content":f"قدم طلب للإدارة قبل {_prior_notice} على الأقل لإعادة الجدولة"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"هلو، ابني خلص {_grade} وعنده إجازة، كيف يستغل وقته؟"},
            {"role":"assistant","content":"دورات صيفية ممتازة. شنو يحب؟"},
            {"role":"user","content":f"يحب {subj} وبرمجة"},
            {"role":"assistant","content":"عندنا دورة برمجة مبتدئين لطلاب الإجازة"},
            {"role":"user","content":"الرسوم وأوقاتها؟"},
            {"role":"assistant","content":f"{vp(_fee*2)} لشهر كامل. {_sessions} الساعة {_hour}"},
        ]
    elif tpl == 46:
        _ch1 = pick(["الأول","الثاني","الثالث"])
        _ch2 = pick(["الرابع","الخامس","السادس"])
        _ch3 = pick(["السابع","الثامن","التاسع"])
        msgs = [
            {"role":"user","content":f"أستاذ {tutor}، يمكن تعطيني ملخص {subj} لامتحان {_grade}؟"},
            {"role":"assistant","content":f"الملخص موجود، بس الفهم أهم. شنو أضعف نقاطك بـ{subj}؟"},
            {"role":"user","content":f"الفصل {_ch2} صعب"},
            {"role":"assistant","content":f"الفصول الأهم بـ{subj}: {_ch1} و{_ch2} و{_ch3}. ركز عليها"},
            {"role":"user","content":"ماشي، وبعدين؟"},
            {"role":"assistant","content":f"راجع أسئلة {subj} القديمة، هي أحسن تدريب قبل الامتحان"},
        ]
    elif tpl == 47:
        _yr_pct = pick(["30%","40%","50%"])
        _final_pct = pick(["60%","70%","50%"])
        _attend_pct = pick(["5%","10%","15%"])
        msgs = [
            {"role":"user","content":f"هلو، أريد أسألك عن نظام التقييم بـ{school} للـ{_grade}"},
            {"role":"assistant","content":f"التقييم: {_yr_pct} أعمال سنة و{_final_pct} امتحان نهائي"},
            {"role":"user","content":"أعمال السنة شتشمل بالـ{_grade}؟"},
            {"role":"assistant","content":f"حضور وواجبات {subj} ومشاريع وامتحانات شهرية"},
            {"role":"user","content":"الحضور كم نقطة؟"},
            {"role":"assistant","content":f"{_attend_pct} من درجة الأعمال السنة. ما تتغيب بدون عذر"},
        ]
    elif tpl == 48:
        _skill = pick(["التفكير المنطقي","التحليل","حل المشكلات","الإبداع","التواصل"])
        _job = pick(["مهندس","طبيب","مبرمج","محاسب","عالم","صحفي"])
        msgs = [
            {"role":"user","content":f"أستاذ {tutor}، ابني {_grade} يقول {subj} ما له فايدة بالحياة"},
            {"role":"assistant","content":f"هذا تفكير كثير من طلاب {_grade}. بس الواقع غير"},
            {"role":"user","content":"وكيف تردون عليه؟"},
            {"role":"assistant","content":f"{subj} تبني {_skill} اللي كل مهنة تحتاجه"},
            {"role":"user","content":"مثل؟"},
            {"role":"assistant","content":f"{_job} يحتاج {_skill} كل يوم. {subj} أساسها"},
        ]
    elif tpl == 49:
        _gpa_req = pick(["85%","80%","90%","75%"])
        _lang_test = pick(["IELTS","TOEFL","ألماني B2","فرنسي B1"])
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أستفسر عن الابتعاث الحكومي لـ{_abroad} بتخصص {_spec}"},
            {"role":"assistant","content":f"ابتعاث {_spec} لـ{_abroad} للمتميزين من خريجي الجامعات الحكومية"},
            {"role":"user","content":"الشروط؟"},
            {"role":"assistant","content":f"معدل تراكمي {_gpa_req} فأكثر + اختبار {_lang_test} + موافقة وزارة التعليم"},
            {"role":"user","content":"الراتب التشغيلي كافي بـ{_abroad}؟"},
            {"role":"assistant","content":f"يعطونك منحة {pick(['800','1000','1200'])} دولار شهرياً. يختلف حسب {_abroad}"},
        ]
    else:
        _fail_reason = pick(["ما يفهم","ما يذاكر","خايف من الامتحان","تشتت"])
        msgs = [
            {"role":"user","content":f"ابني {_grade} راسب بـ{subj}، شنو أسوي؟"},
            {"role":"assistant","content":"لا تضرب وتزعل، هذا يزيد المشكلة"},
            {"role":"user","content":f"بس مو معقول يرسب بـ{subj}"},
            {"role":"assistant","content":"اكعد معه واعرف السبب. مو فاهم ولا مو مذاكر؟"},
            {"role":"user","content":f"يقول {_fail_reason} بـ{subj}"},
            {"role":"assistant","content":f"خذله {tutor} أستاذ خصوصي لـ{subj}، أسلوبه واضح ويفيد"},
        ]

    return {"id": f"edu_{i:04d}", "category": "education", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 13 - GOVERNMENT SERVICES
# ============================================================
DEPTS = ["دائرة الجنسية","دائرة التسجيل العقاري","محكمة البداءة",
         "دائرة المرور","مديرية الجوازات","دائرة الضرائب","دائرة التقاعد"]
DOCS  = ["هوية الأحوال","جواز السفر","شهادة الميلاد","وكالة قانونية",
         "عقد الملكية","بطاقة التقاعد","رخصة القيادة"]

def gen_government(i):
    dept  = pick(DEPTS)
    dept2 = pick(DEPTS)
    doc   = pick(DOCS)
    doc2  = pick(DOCS)
    nm    = pick(ALL_NAMES)
    _gr   = pick(GREET)
    _day  = pick(["باچر","بعد باچر","نهاية الأسبوع","أي يوم","باچر الصبح"])
    _hour = pick(["8 الصبح","9 الصبح","10 الصبح","11 الصبح"])
    _fee  = pick([5000,10000,15000,20000,25000,30000])
    _rush = pick([50000,75000,100000])
    _wait_days = pick(["3 أيام","5 أيام","أسبوع","أسبوعين","10 أيام"])
    _fine = pick([10000,15000,20000,25000])
    _renew_fee = pick([5000,10000,15000])
    _travel_date = pick(["بعد أسبوعين","بعد شهر","بعد 3 أسابيع","الأسبوع القادم"])
    _win_num = pick(["1","2","3","4","الشباك الرئيسي"])
    _doc_type = pick(["شهادة الميلاد","هوية الأحوال","جواز السفر","شهادة الجنسية","وثيقة السكن"])
    _court_dur = pick(["شهر","شهرين","3 أشهر","أسبوعين"])
    _location = pick(["شارع الرشيد","المنصور","الكرادة","الكاظمية","المثنى"])
    _region = pick(["اليمين","اليسار","الطابق الأول","الطابق الثاني","نهاية الممشى"])
    _expire_yrs = pick(["سنة","سنتين","3 سنين","6 أشهر"])
    _car_type = pick(["سيارة تيوتا","سيارة كيا","سيارة هيونداي","سيارة نيسان","سيارة BME"])
    _prop_type = pick(["بيت","قطعة أرض","محل","شقة","بستان"])
    _nbr_name = pick(["جاسم","أبو علي","حسن","صالح","محمود"])
    _insp_time = pick(["أسبوع","أسبوعين","3 أيام"])
    _lost_type = pick(["هويتي","جوازي","رخصتي","شهادة ميلاد"])
    _born_corr = pick(["تصحيح اسمي","تعديل التاريخ","إضافة اللقب","تصحيح اسم الأب"])
    tpl   = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد أجدد {doc}، شنو المطلوب؟"},
            {"role":"assistant","content":f"لتجديد {doc} تحتاج: نسخة من القديم، صورتين، وإيصال دفع الرسوم"},
            {"role":"user","content":"الرسوم كم؟"},
            {"role":"assistant","content":f"{vp(_fee)} دينار، تدفع بالبنك"},
            {"role":"user","content":"كم يستغرق؟"},
            {"role":"assistant","content":f"{_wait_days} عادةً"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"جوازي انتهى، وعندي سفر {_travel_date}"},
            {"role":"assistant","content":"اللحاق ممكن لو قدمت هسه. أكو تعجيل برسوم إضافية"},
            {"role":"user","content":"كم رسوم التعجيل؟"},
            {"role":"assistant","content":f"التعجيل {vp(_rush)} دينار إضافية ويجي خلال {pick(['3 أيام','يومين','5 أيام'])}"},
            {"role":"user","content":"ماشي، أريد التعجيل"},
            {"role":"assistant","content":f"تفضل ملأ الاستمارة وادفع بالشباك رقم {_win_num}"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"أريد أسجل {_car_type} باسمي، كيف؟"},
            {"role":"assistant","content":"تحتاج عقد البيع موثق، هوية البائع والمشتري، وشهادة المعاينة"},
            {"role":"user","content":"المعاينة وين أسويها؟"},
            {"role":"assistant","content":f"مديرية المرور بـ{_location}، لازم تروح هناك أول"},
            {"role":"user","content":"والتسجيل هنا بعدين؟"},
            {"role":"assistant","content":f"إي، بعد ما تجيب المعاينة نكمل التسجيل. يستغرق {_wait_days}"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"رخصة القيادة الخاصة بي انتهت من {_expire_yrs}"},
            {"role":"assistant","content":"في غرامة تأخير. كم مدة انتهت؟"},
            {"role":"user","content":f"{_expire_yrs}"},
            {"role":"assistant","content":f"الغرامة {vp(_fine)} دينار + رسوم التجديد {vp(_renew_fee)} دينار"},
            {"role":"user","content":"أدفع هنا؟"},
            {"role":"assistant","content":f"إي، شباك الدفع على {_region}"},
        ]
    elif tpl == 5:
        _proxy_type = pick(["وكالة عامة","وكالة خاصة","وكالة بيع"])
        msgs = [
            {"role":"user","content":f"أريد أستخرج {_proxy_type} لأخوي"},
            {"role":"assistant","content":f"الوكالة تحتاج كلاكم تحضرون أمام الكاتب العدل"},
            {"role":"user","content":"أخوي بره البلد"},
            {"role":"assistant","content":f"لو برة البلد يصادق عليها بالسفارة العراقية هناك ويرسلها"},
            {"role":"user","content":"كم يستغرق؟"},
            {"role":"assistant","content":f"حسب السفارة، عادةً {_wait_days}"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"أريد {_born_corr} بشهادة الميلاد"},
            {"role":"assistant","content":"هذا يحتاج دعوى قضائية بالمحكمة"},
            {"role":"user","content":"يعني محامي؟"},
            {"role":"assistant","content":"نعم، أو تقدر تراجع المحكمة مباشرة لو الأمر بسيط"},
            {"role":"user","content":"كم المدة؟"},
            {"role":"assistant","content":f"من {_court_dur} حسب الزحمة بالمحكمة"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"{dept2} وين؟"},
            {"role":"assistant","content":f"على {_location}، {pick(['قرب البنك','قبل الجسر بمية متر','قرب السوق','جنب البريد'])}"},
            {"role":"user","content":"ساعات الدوام؟"},
            {"role":"assistant","content":f"من {_hour} لـ2 الضهر، إجازة الجمعة والسبت"},
            {"role":"user","content":f"ماشي، بروح {_day}"},
            {"role":"assistant","content":f"روح بكير، لأن فيه زحمة من الساعة {pick(['9','10','8 ونص'])}"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"أريد أشكو على جاري {_nbr_name} عنده تجاوز على {_prop_type}تي"},
            {"role":"assistant","content":"لازم تقدم شكوى مكتوبة مع صور وشهود"},
            {"role":"user","content":"وبعدين؟"},
            {"role":"assistant","content":f"نبعث لجنة تفتيش خلال {_insp_time}"},
            {"role":"user","content":"وإذا ما حلوا؟"},
            {"role":"assistant","content":"الخطوة الثانية المحكمة، بس نحاول نحلها هنا أول"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"{_lost_type} ضاع، كيف أستخرج بديل؟"},
            {"role":"assistant","content":"تحتاج إفادة من مركز الشرطة بالضياع، وشهادة ميلاد، وصورتين"},
            {"role":"user","content":"ومدة الاستخراج؟"},
            {"role":"assistant","content":f"{_wait_days} تقريباً"},
            {"role":"user","content":"في رسوم؟"},
            {"role":"assistant","content":f"إي، {vp(_fee)} دينار رسوم الاستمارة"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"هلو، أريد أراجع {dept}، فيه دوام اليوم؟"},
            {"role":"assistant","content":f"إي، الدوام من {_hour} للساعة 2"},
            {"role":"user","content":f"اليوم {pick(['خميس','أحد','ثلاثاء','اثنين'])}، مفتوحين؟"},
            {"role":"assistant","content":f"إي، الدوام كامل. الشبابيك تسكر الساعة 2 بالضبط"},
            {"role":"user","content":"ماشي، بروح هسه"},
            {"role":"assistant","content":f"استعجل، البعد بـ{pick(['20 دقيقة','ربع ساعة','10 دقايق'])} من الساعة 2"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"أريد أستخرج {doc} لأول مرة، شنو المطلوب؟"},
            {"role":"assistant","content":f"لاستخراج {doc} لأول مرة تحتاج: شهادة ميلاد، هوية الوالد، وصورتين"},
            {"role":"user","content":"وين الاستمارة؟"},
            {"role":"assistant","content":f"الاستمارة من شباك الاستعلام. الرسوم {vp(_fee)} دينار"},
            {"role":"user","content":"كم يستغرق؟"},
            {"role":"assistant","content":f"{_wait_days}"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد أسأل عن تسجيل {_prop_type} بالدائرة"},
            {"role":"assistant","content":"تحتاج سند الملكية القديم، هوية البائع والمشتري، وتقييم الدائرة"},
            {"role":"user","content":"التقييم كيف؟"},
            {"role":"assistant","content":f"تقدم طلب تقييم، يجي مهندس من الدائرة خلال {_insp_time}"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"حسب قيمة {_prop_type}، بين {vp(_fee*3)} وـ{vp(_fee*10)} تقريباً"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"أريد أسأل، راتب التقاعد الخاص بأبوي، كيف أستلمه؟"},
            {"role":"assistant","content":"هل الوالد توفي؟ الراتب ينتقل للأرملة أو الأولاد"},
            {"role":"user","content":"إي، توفي الشهر الماضي"},
            {"role":"assistant","content":f"العزاء لله. روح {dept} بوثيقة الوفاة وهوية الأحوال"},
            {"role":"user","content":"الإجراءات طويلة؟"},
            {"role":"assistant","content":f"عادةً {_wait_days} للإتمام"},
        ]
    elif tpl == 14:
        _viol_type = pick(["تجاوز الإشارة الحمراء","سرعة زائدة","وقوف ممنوع","عدم ربط حزام الأمان","استخدام الموبايل بالقيادة"])
        _viol_num = pick(["واحدة","اثنتين","ثلاثة","أربعة"])
        msgs = [
            {"role":"user","content":f"عندي {_viol_num} مخالفات مرورية بسبب {_viol_type}، كيف أدفعها؟"},
            {"role":"assistant","content":f"مخالفة {_viol_type} تكدر تدفعها بالشباك أو عبر التطبيق الإلكتروني"},
            {"role":"user","content":"المبلغ الكلي كم؟"},
            {"role":"assistant","content":f"مخالفة {_viol_type} بـ{vp(_fine)} دينار × {_viol_num}"},
            {"role":"user","content":"وإذا ما دفعت؟"},
            {"role":"assistant","content":f"تتراكم الغرامات وممكن يسحبون رخصتك بعد {pick(['3 مخالفات','5 مخالفات','10 مخالفات'])}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"السلام عليكم، أريد أفتح محل تجاري، شنو الإجراءات؟"},
            {"role":"assistant","content":"تحتاج سجل تجاري، رخصة بلدية، وموافقة وزارة التجارة"},
            {"role":"user","content":"وين أبدأ؟"},
            {"role":"assistant","content":f"ابدأ بالبلدية، بعدين السجل التجاري بـ{dept}"},
            {"role":"user","content":"الرسوم الكلية كم؟"},
            {"role":"assistant","content":f"بين {vp(_fee*5)} وـ{vp(_fee*15)} حسب نوع المحل والموقع"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أريد أسأل عن استخراج {_doc_type} للأطفال"},
            {"role":"assistant","content":f"{_doc_type} للأطفال تحتاج: شهادة ميلاد، هوية الوالد، وصورتين للطفل"},
            {"role":"user","content":"في عمر معين؟"},
            {"role":"assistant","content":"لا، من الولادة ممكن. الأحسن تسجله بكير"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"{vp(_fee)} دينار للاستمارة"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد أسأل، {dept} عندها خدمة إلكترونية؟"},
            {"role":"assistant","content":"بعض الخدمات متاحة أونلاين، وبعضها لازم حضور شخصي"},
            {"role":"user","content":f"وين الموقع؟"},
            {"role":"assistant","content":"ابحث عن بوابة الخدمات الحكومية العراقية"},
            {"role":"user","content":f"وإذا ما كمل الموقع؟"},
            {"role":"assistant","content":f"تجي حضورياً لـ{dept}. ساعات الدوام {_hour} للساعة 2"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أراجع {dept} بس ما أعرف الموقع"},
            {"role":"assistant","content":f"{dept} على {_location}، {pick(['جنب المصرف','قرب الساحة','أمام الحديقة'])}"},
            {"role":"user","content":"بالسيارة كم يستغرق من الكرادة؟"},
            {"role":"assistant","content":f"بدون زحمة {pick(['10 دقايق','ربع ساعة','20 دقيقة'])}. بس الزحمة بالصبح شديدة"},
            {"role":"user","content":"هناك پارك سيارات؟"},
            {"role":"assistant","content":f"إي، فيه پارك قريب بـ{vp(2000)} دينار بالساعة"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"هلو، أريد أعرف رسوم استخراج {doc}"},
            {"role":"assistant","content":f"{doc} أنواع: عادي وتعجيل. أيش تريد؟"},
            {"role":"user","content":"العادي كم؟"},
            {"role":"assistant","content":f"العادي {vp(_fee)} دينار ويجي خلال {_wait_days}"},
            {"role":"user","content":"والتعجيل؟"},
            {"role":"assistant","content":f"التعجيل {vp(_rush)} ويجي خلال {pick(['يومين','3 أيام','24 ساعة'])}"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"أريد أستفسر، شنو أكمل الأوراق لتسجيل {_prop_type}؟"},
            {"role":"assistant","content":f"لتسجيل {_prop_type} تحتاج: صك الملكية، هوية مدنية، وتقييم حكومي"},
            {"role":"user","content":"التقييم كم يكلف؟"},
            {"role":"assistant","content":f"التقييم الحكومي {vp(_fee*2)} دينار ويستغرق {_insp_time}"},
            {"role":"user","content":"وإذا كان {_prop_type} موروث؟"},
            {"role":"assistant","content":"تحتاج إضافة وثيقة الوفاة وتقسيم الإرث بقرار المحكمة"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"هلو، ابني يبي يجدد جواز سفره للسفر للدراسة"},
            {"role":"assistant","content":"الجواز يستغرق استخراجه وقت. كم بعده عن السفر؟"},
            {"role":"user","content":f"{_travel_date}"},
            {"role":"assistant","content":f"لو {_travel_date} ممكن تعجيل بـ{vp(_rush)} دينار"},
            {"role":"user","content":"وهل يحتاج موافقة خاصة للطالب؟"},
            {"role":"assistant","content":"لو تحت 18 سنة يحتاج موافقة الوالد الموثقة"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"أريد أستخرج شهادة خلو سوابق"},
            {"role":"assistant","content":"تحتاج هوية الأحوال وصورتين وإيصال دفع الرسوم"},
            {"role":"user","content":"وين أقدم؟"},
            {"role":"assistant","content":f"مركز الشرطة أول، بعدين {dept}"},
            {"role":"user","content":"المدة؟"},
            {"role":"assistant","content":f"{_wait_days}"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"مرحبا {nm}، أريد أسأل عن الحصول على رخصة مهنية"},
            {"role":"assistant","content":"شنو المهنة؟"},
            {"role":"user","content":f"محامي"},
            {"role":"assistant","content":"رخصة المحامي من نقابة المحامين العراقيين. تحتاج شهادة القانون"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"التسجيل بالنقابة {vp(_fee*3)} دينار أول سنة"},
        ]
    elif tpl == 24:
        _passport_error = pick(["الاسم مغلوط","تاريخ الميلاد خاطئ","رقم الهوية غلط","صورة مو وضوح"])
        msgs = [
            {"role":"user","content":f"جوازي فيه غلط بـ{_passport_error}، كيف أصلحه؟"},
            {"role":"assistant","content":f"تصحيح {_passport_error} بالجواز يحتاج طلب رسمي مع المستندات الثبوتية"},
            {"role":"user","content":"مستندات ايش؟"},
            {"role":"assistant","content":f"هوية الأحوال الصحيحة وشهادة الميلاد وصورتين معتمدة من {dept}"},
            {"role":"user","content":"المدة والرسوم؟"},
            {"role":"assistant","content":f"{_wait_days} بعد قبول الطلب. الرسوم {vp(_fee)} دينار"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"هلو، أريد أغير عنواني السكني بالهوية"},
            {"role":"assistant","content":"تحتاج وثيقة السكن الجديد وهويتك القديمة"},
            {"role":"user","content":"وثيقة السكن أيش تكون؟"},
            {"role":"assistant","content":"إيجار موثق أو فاتورة كهرباء بالاسم أو عقد تمليك"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"{vp(_fee)} دينار والمدة {_wait_days}"},
        ]
    elif tpl == 26:
        _marriage_country = pick(["تركيا","ألمانيا","السويد","هولندا","الإمارات","مصر"])
        msgs = [
            {"role":"user","content":f"أريد أسأل عن تسجيل زواج صار بـ{_marriage_country} بالعراق"},
            {"role":"assistant","content":f"الزواج المسجل بـ{_marriage_country} يحتاج توثيق بالسفارة العراقية هناك أولاً"},
            {"role":"user","content":"وبعدين؟"},
            {"role":"assistant","content":f"تقدم الوثيقة المصادق عليها لدائرة {dept} بالعراق"},
            {"role":"user","content":"المدة والرسوم؟"},
            {"role":"assistant","content":f"من {_wait_days} للإتمام. الرسوم {vp(_fee)} دينار"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"أريد أسأل عن استئناف قرار {dept}"},
            {"role":"assistant","content":"الاستئناف يكون أمام المحكمة الإدارية خلال 30 يوم من القرار"},
            {"role":"user","content":"يحتاج محامي؟"},
            {"role":"assistant","content":"يفضل، بس مو إجباري للقضايا البسيطة"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"رسوم الدعوى {vp(_fee*2)} دينار + أتعاب المحامي لو اخترت"},
        ]
    elif tpl == 28:
        _crowd_time = pick(["بالصبح الباكر","بعد الضهر","وسط الأسبوع","يوم الأحد","أول أيام الدوام"])
        _crowd_num = pick(["20 شخص","30 شخص","50 شخص","ناس كثار","طابور طويل"])
        _wait_est = pick(["ساعة","ساعة ونص","30 دقيقة","ساعتين","45 دقيقة"])
        msgs = [
            {"role":"user","content":f"السلام عليكم، جيت لـ{dept} بس الزحمة هائلة، يمكن {_crowd_num} قبلي"},
            {"role":"assistant","content":f"إي والله، {dept} دايماً زحمة {_crowd_time}"},
            {"role":"user","content":"في نظام ترقيم؟"},
            {"role":"assistant","content":f"إي، خذ رقم من الماكينة عند الباب. رقمك يطلع بالشاشة"},
            {"role":"user","content":"كم أنتظر تقريباً؟"},
            {"role":"assistant","content":f"بحساب {_crowd_num} قبلك، تقريباً {_wait_est}. تجي {_crowd_time} أهون"},
        ]
    elif tpl == 29:
        _doc_validity = pick(["10 سنين","5 سنين","3 سنين","سنتين","سنة واحدة"])
        _issue_year = pick(["2018","2019","2020","2021","2022","2023"])
        msgs = [
            {"role":"user","content":f"هلو، أريد أتحقق إذا {doc} الخاص بي، اللي صدر سنة {_issue_year}، لازال صالح"},
            {"role":"assistant","content":f"{doc} عادةً صالح {_doc_validity} من تاريخ الإصدار"},
            {"role":"user","content":"ما معي الأصل هسه، بس عندي صورة"},
            {"role":"assistant","content":f"الصورة ما تكفي للتحقق الرسمي. لازم تجيب الأصل لـ{dept}"},
            {"role":"user","content":"ولو انتهى، كم يستغرق التجديد؟"},
            {"role":"assistant","content":f"تجديد {doc} يستغرق {_wait_days} والرسوم {vp(_fee)} دينار"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"أريد أسأل عن استخراج تصريح عمل لعامل أجنبي"},
            {"role":"assistant","content":"تصريح العمل من وزارة العمل. تحتاج عقد العمل وهوية العامل"},
            {"role":"user","content":"كم وقت يستغرق؟"},
            {"role":"assistant","content":f"{_wait_days} تقريباً بعد اكتمال الأوراق"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"{vp(_fee*4)} دينار سنوياً للتصريح"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"هلو، أريد أستعلم عن طلب مقدم مسبقاً بـ{dept}"},
            {"role":"assistant","content":"اسمك ورقم الطلب؟"},
            {"role":"user","content":f"{nm}، الطلب {pick(['123456','789012','345678','901234'])}"},
            {"role":"assistant","content":"تفضل بشباك الاستعلام، هم يتحققون"},
            {"role":"user","content":"كم يستغرق التحقق؟"},
            {"role":"assistant","content":f"بالسيستم فوري، بالورق ممكن {pick(['يوم','يومين','ربع ساعة'])}"},
        ]
    elif tpl == 32:
        _cert_purpose = pick(["تقديم طلب قرض","فتح حساب مصرفي","التسجيل بالجامعة","طلب وظيفة","التأمين"])
        msgs = [
            {"role":"user","content":f"أريد أستخرج شهادة إقامة لـ{_cert_purpose}"},
            {"role":"assistant","content":f"شهادة الإقامة لـ{_cert_purpose} تجيبها من المحلة، تحتاج هوية الأحوال والمختار"},
            {"role":"user","content":"المختار وين؟"},
            {"role":"assistant","content":f"مختار المحلة موجود بـ{_location}. يفتح أوقات الصبح عادةً"},
            {"role":"user","content":"الرسوم والمدة؟"},
            {"role":"assistant","content":f"رمزية، {vp(2000)} دينار. تجيك في نفس اليوم أو {pick(['يوم','يومين'])}"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"هلو، أريد أعرف رقم {dept} للتواصل"},
            {"role":"assistant","content":f"رقم {dept} الرسمي {pick(['07700000000','07800000000','07900000000'])}"},
            {"role":"user","content":"والإيميل؟"},
            {"role":"assistant","content":"مو كل الدوائر عندها إيميل فعال. الحضور أضمن"},
            {"role":"user","content":"ساعات التواصل؟"},
            {"role":"assistant","content":f"من {_hour} للساعة 2 أيام العمل الرسمية"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"أريد أستفسر عن خدمات {dept} للمغتربين"},
            {"role":"assistant","content":"المغتربون يكدرون ينجزون بعض المعاملات عبر السفارة"},
            {"role":"user","content":"أي معاملات؟"},
            {"role":"assistant","content":f"تجديد {doc}، التوكيلات، وتصديق الوثائق"},
            {"role":"user","content":"الأوقات؟"},
            {"role":"assistant","content":"حسب ساعات السفارة في بلدهم"},
        ]
    elif tpl == 35:
        _inherit_type = pick(["بيت","أرض","محل تجاري","سيارات","أموال بالمصرف","مزرعة"])
        _heirs = pick(["3 أولاد","5 أولاد وبنتين","زوجة وولدين","إخوان وأخوات","أحفاد"])
        msgs = [
            {"role":"user","content":f"مرحبا، أبوي توفي وخلى {_inherit_type}، أريد أسأل عن إجراءات الميراث"},
            {"role":"assistant","content":f"الميراث لـ{_heirs} يحتاج قرار محكمة أولاً لتحديد حصة كل وارث"},
            {"role":"user","content":"وبعد قرار المحكمة؟"},
            {"role":"assistant","content":f"تنقل ملكية {_inherit_type} لـ{dept2} بعد قرار المحكمة الرسمي"},
            {"role":"user","content":"المدة الكلية؟"},
            {"role":"assistant","content":f"من {_court_dur} حسب تعقيد الملف وعدد الورثة"},
        ]
    elif tpl == 36:
        _baby_hosp = pick(["مستشفى اليرموك","مستشفى الكندي","مستشفى ابن البلدي","مركز الولادة","العيادة الأهلية"])
        _baby_days = pick(["3 أيام","أسبوع","10 أيام","أسبوعين"])
        msgs = [
            {"role":"user","content":f"أريد أسجل طفلي المولود من {_baby_days} بـ{_baby_hosp}"},
            {"role":"assistant","content":f"تسجيل المواليد يكون خلال شهر من الولادة. {_baby_hosp} تعطي شهادة ميلاد رسمية؟"},
            {"role":"user","content":"إي، عندي شهادة الولادة من المستشفى"},
            {"role":"assistant","content":f"ممتاز، تحتاج شهادة الولادة من {_baby_hosp}، هوية الأب والأم، وصورتين"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"مجانية لأول {pick(['30 يوم','شهر'])}، بعدها {vp(_fee)} دينار غرامة تأخير"},
        ]
    elif tpl == 37:
        _weapon_type = pick(["مسدس للحماية الشخصية","بندقية للصيد","سلاح ورثته","مسدس للعمل"])
        msgs = [
            {"role":"user","content":f"هلو، أريد أستفسر عن رخصة {_weapon_type}"},
            {"role":"assistant","content":f"رخصة {_weapon_type} من وزارة الداخلية، متطلبات صارمة"},
            {"role":"user","content":"الشروط؟"},
            {"role":"assistant","content":f"لا توجد سوابق جنائية، رسوم {vp(_fee*3)} دينار، وموافقة أمنية"},
            {"role":"user","content":"المدة؟"},
            {"role":"assistant","content":f"من {_wait_days} للتحقق الأمني. بعدين يصدر قرار"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"أريد أسأل، {doc} الالكتروني مقبول بالمعاملات؟"},
            {"role":"assistant","content":"نعم، الوثائق الالكترونية المصدقة مقبولة رسمياً"},
            {"role":"user","content":"كيف أحصل عليه؟"},
            {"role":"assistant","content":"عبر بوابة الحكومة الالكترونية بعد التحقق من الهوية"},
            {"role":"user","content":"في رسوم؟"},
            {"role":"assistant","content":f"{vp(_fee)} دينار رسوم الخدمة الالكترونية"},
        ]
    elif tpl == 39:
        _civil_error = pick(["اسم مغلوط بالهوية","تاريخ ميلاد خاطئ","اسم الأب مغلوط","رقم الملف غلط"])
        msgs = [
            {"role":"user","content":f"أريد أصحح {_civil_error} بالسجل المدني، كيف؟"},
            {"role":"assistant","content":f"تصحيح {_civil_error} يحتاج طلب رسمي مع مستندات إثبات من {dept}"},
            {"role":"user","content":"ما المستندات المطلوبة؟"},
            {"role":"assistant","content":f"شهادات قديمة تثبت الصح، {doc}، وشهادة ميلاد أصلية"},
            {"role":"user","content":"المدة؟"},
            {"role":"assistant","content":f"إذا بسيطة {_wait_days}. إذا محتاجة قرار قضائي {_court_dur}"},
        ]
    elif tpl == 40:
        _nat_origin = pick(["سوري","مصري","أردني","إيراني","تركي","لبناني"])
        _nat_years = pick(["10 سنوات","12 سنة","15 سنة","8 سنوات"])
        msgs = [
            {"role":"user","content":f"السلام عليكم، أريد أعرف إجراءات الحصول على الجنسية العراقية، أنا {_nat_origin} أصلاً"},
            {"role":"assistant","content":f"المواطن {_nat_origin} يكدر يتجنس بالعراق بعد إقامة قانونية متواصلة"},
            {"role":"user","content":"شروط التجنيس؟"},
            {"role":"assistant","content":f"إقامة قانونية {_nat_years} متواصلة، لا توجد سوابق جنائية، وإجادة اللغة العربية"},
            {"role":"user","content":"الرسوم والمدة؟"},
            {"role":"assistant","content":f"الطلب الرسمي {vp(_fee*2)} دينار. القرار من وزارة الداخلية ويستغرق {_court_dur}"},
        ]
    elif tpl == 41:
        _visitor_country = pick(["أوروبا","أمريكا","ماليزيا","تركيا","السويد","ألمانيا","إيران"])
        _visa_cost = pick(["30","50","75","100","120"])
        _visa_dur = pick(["شهر","شهرين","3 أشهر","أسبوعين"])
        msgs = [
            {"role":"user","content":f"هلو، أريد أستفسر عن تأشيرة زيارة لأقاربي من {_visitor_country}"},
            {"role":"assistant","content":f"تأشيرة الزيارة من {_visitor_country} تقدم عبر السفارة العراقية هناك"},
            {"role":"user","content":"كم تكلف؟"},
            {"role":"assistant","content":f"بين {_visa_cost} دولار حسب الجنسية"},
            {"role":"user","content":"ومدة الصلاحية؟"},
            {"role":"assistant","content":f"عادةً {_visa_dur} قابلة للتجديد من {dept}"},
        ]
    elif tpl == 42:
        _complaint_type = pick(["رشوة","تأخير متعمد","وقاحة في الكلام","رفض استقبال معاملة","تمييز بالمعاملة"])
        msgs = [
            {"role":"user","content":f"أريد أشكو على موظف بـ{dept}، عنده {_complaint_type}"},
            {"role":"assistant","content":f"حقك تشكو على {_complaint_type}. الشكاوى عبر مكتب المفتش العام"},
            {"role":"user","content":"كيف أقدم الشكوى؟"},
            {"role":"assistant","content":f"شكوى مكتوبة مع تفاصيل {_complaint_type} والتاريخ والشهود لو أكو"},
            {"role":"user","content":"وبعدين؟"},
            {"role":"assistant","content":f"التحقيق يستغرق {_wait_days}. يكون رد رسمي من {dept}"},
        ]
    elif tpl == 43:
        _work_dept = pick(["الصحة","التعليم","الداخلية","النفط","العدل","المالية"])
        _work_purpose = pick(["السفارة الأجنبية","طلب قرض","تقديم لوظيفة","التسجيل بجامعة"])
        msgs = [
            {"role":"user","content":f"أريد إفادة عمل من وزارة {_work_dept}، كيف؟"},
            {"role":"assistant","content":f"إفادة العمل من دائرتك بوزارة {_work_dept}، تحتاج طلب كتابي"},
            {"role":"user","content":"المدة؟"},
            {"role":"assistant","content":f"من {pick(['يوم','يومين','3 أيام'])} حسب الزحمة"},
            {"role":"user","content":f"تصلح لـ{_work_purpose}؟"},
            {"role":"assistant","content":f"إي لـ{_work_purpose}، بس لازم تكون مصدقة من وزارة الخارجية أيضاً"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"أريد أسأل، انتهت مدة إقامتي الدراسية، شسوي؟"},
            {"role":"assistant","content":"تجديد الإقامة من دائرة الإقامة قبل انتهاء المدة"},
            {"role":"user","content":"انتهت من {_expire_yrs}"},
            {"role":"assistant","content":f"في غرامة تأخير {vp(_fine)} دينار. تعال هسه قبل ما تزيد"},
            {"role":"user","content":"هل أتعرض لمشكلة قانونية؟"},
            {"role":"assistant","content":"لو تأخرت أكثر ممكن. اسرع وأنجز وضعك"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"هلو، أريد أسجل شركة صغيرة، شنو الخطوات؟"},
            {"role":"assistant","content":"تسجيل الشركة يبدأ من وزارة التجارة والصناعة"},
            {"role":"user","content":"ما يحتاج؟"},
            {"role":"assistant","content":"اسم الشركة، عقد التأسيس، هوية الشركاء، ورأس المال"},
            {"role":"user","content":"المدة والرسوم؟"},
            {"role":"assistant","content":f"من {_wait_days} والرسوم {vp(_fee*5)} دينار"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"أريد أسأل عن نقل ملكية {_car_type} من أبوي باسمي"},
            {"role":"assistant","content":"نقل ملكية السيارة يحتاج موافقة الوالد أو وثيقة وفاة"},
            {"role":"user","content":"وثيقة الوفاة؟"},
            {"role":"assistant","content":"إي، أضف إرث معتمد من المحكمة وتعال لنا"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"نقل الملكية {vp(_fee*2)} دينار والإجراءات {_wait_days}"},
        ]
    elif tpl == 47:
        _tax_type = pick(["ضريبة الدخل","ضريبة العقارات","ضريبة المبيعات","ضريبة الأرباح"])
        _tax_amount = pick([100000,200000,300000,500000,750000])
        msgs = [
            {"role":"user","content":f"السلام عليكم، أريد أعرف كيف أدفع {_tax_type} السنوية"},
            {"role":"assistant","content":f"{_tax_type} تدفع في دائرة الضرائب أو المصرف المعتمد"},
            {"role":"user","content":f"المبلغ {vp(_tax_amount)} دينار، هل فيه تسهيلات؟"},
            {"role":"assistant","content":f"إي، أقساط ربعية متاحة للمبالغ فوق {vp(500000)} دينار"},
            {"role":"user","content":"أسوي نفسي ولا أستعين بمحاسب؟"},
            {"role":"assistant","content":f"لو ملف {_tax_type} معقد، المحاسب يوفر عليك وقت وغلطات"},
        ]
    elif tpl == 48:
        _proxy_person = pick(["أخوي","ابن عمي","صاحبي الموثوق","زوجتي","أبوي"])
        _proxy_trans = pick(["استخراج هوية","تجديد جواز","استلام وثيقة","تقديم طلب إقامة","نقل ملكية"])
        msgs = [
            {"role":"user","content":f"مرحبا، أنا مسافر وأريد {_proxy_person} يخلص {_proxy_trans} بـ{dept} بدالي، ممكن؟"},
            {"role":"assistant","content":f"إي ممكن، {_proxy_person} يكدر يخلص {_proxy_trans} بالوكالة"},
            {"role":"user","content":"شنو لازم يكون بالوكالة؟"},
            {"role":"assistant","content":f"الوكالة تكون مكتوب فيها اسم {dept} و{_proxy_trans} تحديداً بشكل صريح"},
            {"role":"user","content":"وكالة عامة تكفي؟"},
            {"role":"assistant","content":f"بعض معاملات {dept} تقبل العامة، بس {_proxy_trans} عادةً تحتاج وكالة خاصة"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أريد أسأل عن خدمات {dept} للمتقاعدين"},
            {"role":"assistant","content":"المتقاعدون عندهم أولوية بالدوائر الحكومية"},
            {"role":"user","content":"فيه شباك مخصص؟"},
            {"role":"assistant","content":f"إي، شباك {_win_num} للمتقاعدين وكبار السن بـ{dept}"},
            {"role":"user","content":"وأيام الدوام؟"},
            {"role":"assistant","content":f"كل أيام الأسبوع ما عدا الجمعة والسبت. من {_hour}"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"هلو، أريد أستفسر عن أوضاع معاملة {doc} المقدمة"},
            {"role":"assistant","content":f"اسمك ورقم الطلب؟"},
            {"role":"user","content":f"{nm}"},
            {"role":"assistant","content":"تفضل بالاستعلام. المعاملة قيد المعالجة"},
            {"role":"user","content":"متى تنجز؟"},
            {"role":"assistant","content":f"خلال {_wait_days} إن شاء الله"},
        ]

    return {"id": f"gov_{i:04d}", "category": "government_services", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 14 - RESTAURANTS & CAFES
# ============================================================
RESTAURANTS = ["مطعم أبو نواس","مطعم الشواية الذهبية","مطعم بغداد للمسقوف",
               "مطعم الكباب العراقي","مطعم الرز والمرق","كافيه الرصافة"]
MEALS = ["كباب","مسقوف","قوزي","دولمة","تشريب","برياني","مضغوط",
         "فطور عراقي","مرق دجاج وتمن","باچة"]
DRINKS= ["شاي","چاي بالحليب","شلغم","ماء","عصير","نسكافيه","قهوة"]

def gen_restaurant(i):
    rest  = pick(RESTAURANTS)
    rest2 = pick(RESTAURANTS)
    meal  = pick(MEALS)
    meal2 = pick(MEALS)
    drink = pick(DRINKS)
    drink2= pick(DRINKS)
    _gr   = pick(GREET)
    _pax  = pick(["شخصين","3 أشخاص","4 أشخاص","5 أشخاص","6 أشخاص","عيلة"])
    _seat = pick(["قرب النافذة","بالباحة الخارجية","بالقاعة الداخلية","قرب الكاشير","زاوية هادية"])
    _price1 = pick([10000,12000,15000,18000,20000,25000])
    _price2 = pick([8000,10000,12000,15000])
    _total  = pick([30000,45000,60000,75000,90000,120000])
    _deposit= pick([50000,75000,100000,150000])
    _wait_min = pick(["15 دقيقة","20 دقيقة","30 دقيقة","نص ساعة"])
    _delivery_time = pick(["30 دقيقة","45 دقيقة","ساعة","20 دقيقة"])
    _delivery_fee = pick([2000,3000,5000])
    _free_delivery = pick([25000,30000,40000,50000])
    _event = pick(["عشاء عائلي","عيد ميلاد","خطوبة","إفطار جماعي","لقاء عمل","عزومة أصحاب"])
    _event_day = pick(["الجمعة المسا","السبت الغداة","الخميس الليل","أي يوم تحدد"])
    _discount = pick([10,15,20])
    _tax_pct = pick([10,12,15])
    _complaint = pick(["الطلب جاء بارد","الطلب غلط","الانتظار طال","الكمية قليلة"])
    _solution = pick(["نغيره فوراً","نعيد الطلب","نعطيك خصم","نضيف حصة مجانية"])
    _table_area = pick(["قاعة هادية بالداخل","الطابق الثاني","الحديقة","الشرفة"])
    _fridge_item = pick(["كاهي وقيمر","پاچة جاهزة","سلطة ومقبلات","فواكه طازجة"])
    _heat = pick(["مكيف باردة كلش","الجو حار داخل","تكييف مو شغال","الحرارة ثقيلة"])
    tpl   = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{_gr}، طاولة لـ{_pax}"},
            {"role":"assistant","content":f"{gr()}. تفضل، عندنا طاولة {_seat}"},
            {"role":"user","content":"شنو تنصحنا من المينيو؟"},
            {"role":"assistant","content":f"اليوم عندنا {meal} طازج وعليه طلب كثير"},
            {"role":"user","content":f"آخذ {_pax} حصص {meal}"},
            {"role":"assistant","content":f"حاضر، وشنو تشربون؟"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"بيش طبق {meal} عندكم؟"},
            {"role":"assistant","content":f"{meal} بـ{vp(_price1)} دينار للشخص"},
            {"role":"user","content":"يشمل خبز وشاي؟"},
            {"role":"assistant","content":f"يشمل خبز، أما {drink} بـ{vp(_price2)} إضافي"},
            {"role":"user","content":"ماشي، آخذ واحد"},
            {"role":"assistant","content":"حاضر يا أخوي، يجيك خلال {_wait_min}"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"أريد أحجز {rest} لـ{_event}، {_pax}"},
            {"role":"assistant","content":"ممكن، أي يوم؟"},
            {"role":"user","content":f"{_event_day}"},
            {"role":"assistant","content":f"{_event_day} مزبوط. تحتاج عربون حجز"},
            {"role":"user","content":"كم العربون؟"},
            {"role":"assistant","content":f"{vp(_deposit)} دينار، يحتسب من الحساب النهائي"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"{_complaint} وأنا انتظرت {_wait_min}"},
            {"role":"assistant","content":f"آسفين جداً. {_solution} هسه"},
            {"role":"user","content":"هذا مو مقبول"},
            {"role":"assistant","content":"نعتذر، عندنا زحمة اليوم. نعطيك {drink} مجاناً"},
            {"role":"user","content":"ماشي بس انتبهوا المرة الجاية"},
            {"role":"assistant","content":"وعد، ما يصير مرة ثانية"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"عندكم توصيل للبيت من {rest}؟"},
            {"role":"assistant","content":"إي، توصيل لجميع مناطق بغداد"},
            {"role":"user","content":"كم يستغرق؟"},
            {"role":"assistant","content":f"{_delivery_time} حسب المنطقة"},
            {"role":"user","content":"رسوم التوصيل؟"},
            {"role":"assistant","content":f"{vp(_delivery_fee)} دينار. مجاني لو الطلب فوق {vp(_free_delivery)} دينار"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"أريد أطلب {meal} و{meal2}"},
            {"role":"assistant","content":f"حاضر. {meal} بـ{vp(_price1)} و{meal2} بـ{vp(_price2)} دينار"},
            {"role":"user","content":"والمجموع؟"},
            {"role":"assistant","content":f"المجموع {vp(_price1+_price2)} دينار"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"يجيك خلال {_wait_min} إن شاء الله"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"أكل {rest} حلو بس الجلسة ضيقة"},
            {"role":"assistant","content":"شكراً على ملاحظتك. نحاول نوسع المكان"},
            {"role":"user","content":"وهالضوضاء ما أكدر أسمع"},
            {"role":"assistant","content":f"عندنا {_table_area}، تريد تنتقل؟"},
            {"role":"user","content":"أيوه، أحسن"},
            {"role":"assistant","content":"تفضل، أنا أودِّيك"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"شنو الفرق بين {meal} عندكم و{meal2}؟"},
            {"role":"assistant","content":f"{meal} مشوي بالفحم، و{meal2} طبخ بيتي تقليدي"},
            {"role":"user","content":"أنا أفضل المشوي"},
            {"role":"assistant","content":f"إذاً {meal} هو اختيارك، ممتاز"},
            {"role":"user","content":f"مع {drink}"},
            {"role":"assistant","content":"حاضر، الطلب جاي"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"أريد فطور عراقي أصيل بـ{rest}، عندكم؟"},
            {"role":"assistant","content":f"إي والله، عندنا {_fridge_item} وبيض وعسل"},
            {"role":"user","content":f"و{drink2}؟"},
            {"role":"assistant","content":f"طبعاً، ما يكمل الفطور بدون {drink2}"},
            {"role":"user","content":"هذا يهبل، آخذ واحد"},
            {"role":"assistant","content":f"بـ{vp(_price2+3000)} دينار. يجي فوراً"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":"الحساب لو سمحت"},
            {"role":"assistant","content":f"المجموع {vp(_total)} دينار"},
            {"role":"user","content":"هذا أكثر مما حسبت"},
            {"role":"assistant","content":f"عندنا ضريبة خدمة {_tax_pct}%، موجودة بالمينيو"},
            {"role":"user","content":"آه ما انتبهت، ماشي"},
            {"role":"assistant","content":"شكراً، نتشرف بزيارتكم دايماً"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"{_heat} بـ{rest}"},
            {"role":"assistant","content":"آسفين، نصلح الموضوع هسه"},
            {"role":"user","content":f"ومنديل ما جاي مع {meal}"},
            {"role":"assistant","content":"هسه أجيبه، معذرة على التقصير"},
            {"role":"user","content":"ماشي بس خدمتكم تحتاج تتحسن"},
            {"role":"assistant","content":"شكراً على ملاحظتك، نعتمد على آراء زبائننا"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"هلو، عندكم {meal} هالأيام؟"},
            {"role":"assistant","content":f"إي والله، {meal} موجود كل يوم بـ{rest}"},
            {"role":"user","content":"طازج؟"},
            {"role":"assistant","content":"كلشي يتحضر من الصبح، طازج 100%"},
            {"role":"user","content":"ماشي، آجي الغداة"},
            {"role":"assistant","content":"حياك، نستنيك"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"عندكم وجبة {meal} بدون {pick(['حار','ملح زيادة','دهن'])}؟"},
            {"role":"assistant","content":"إي، نقدر نعدل الطلب حسب طلبك"},
            {"role":"user","content":"وبدون بصل؟"},
            {"role":"assistant","content":"ماكو مشكلة، نطلب من المطبخ يحذفونه"},
            {"role":"user","content":"شكراً، هذا مناسب"},
            {"role":"assistant","content":"دايماً، الزبون دايماً صاحي"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"أريد أسأل، {rest} مفتوح الجمعة؟"},
            {"role":"assistant","content":"إي، مفتوحين كل الأيام حتى الجمعة"},
            {"role":"user","content":"الساعة كم تفتحون؟"},
            {"role":"assistant","content":f"نفتح الساعة {pick(['10 الصبح','11 الصبح','9 الصبح'])} ونسكر {pick(['11 الليل','منتصف الليل','12 الليل'])}"},
            {"role":"user","content":"وهل فيه حجز مسبق؟"},
            {"role":"assistant","content":"الحجز مو إجباري، بس للجمعة أحسن تحجز"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"شنو أحسن {meal} بالمنطقة؟"},
            {"role":"assistant","content":f"بصراحة، {rest} صاحب أحسن {meal} بالمنطقة"},
            {"role":"user","content":f"أحسن من {rest2}؟"},
            {"role":"assistant","content":f"{rest} يشتغل بالفحم الطبيعي. النكهة مختلفة"},
            {"role":"user","content":"ماشي، بروح أجرب"},
            {"role":"assistant","content":"راح تفرق معك، بالهنا والشفا"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أريد طلب للبيت، عندكم تطبيق؟"},
            {"role":"assistant","content":"إي، طبق علينا أو اتصل مباشر"},
            {"role":"user","content":"رقم التوصيل؟"},
            {"role":"assistant","content":f"اتصل {pick(['07700000000','07800000000','07900000000'])} أو عبر التطبيق"},
            {"role":"user","content":"والحد الأدنى للطلب؟"},
            {"role":"assistant","content":f"{vp(_free_delivery)} دينار للتوصيل المجاني"},
        ]
    elif tpl == 17:
        meals3 = pick(MEALS)
        msgs = [
            {"role":"user","content":f"عندكم باكج غداء للموظفين؟"},
            {"role":"assistant","content":"إي، عندنا عروض يومية للموظفين"},
            {"role":"user","content":"شيشمل؟"},
            {"role":"assistant","content":f"{meal} أو {meals3} مع {drink} وخبز"},
            {"role":"user","content":"السعر؟"},
            {"role":"assistant","content":f"{vp(_price1)} دينار فقط للوجبة الكاملة"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"أحجز للأسبوع القادم لـ{_event}، {_pax}"},
            {"role":"assistant","content":f"أي يوم بالضبط؟"},
            {"role":"user","content":f"{_event_day}"},
            {"role":"assistant","content":f"الأسبوع القادم {_event_day} معاك. وين تفضل تجلس؟"},
            {"role":"user","content":f"{_seat}"},
            {"role":"assistant","content":f"سجلناك. العربون {vp(_deposit)} دينار لتثبيت الحجز"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"أريد قائمة {rest} الكاملة"},
            {"role":"assistant","content":"حاضر، ما تشتهي اليوم؟"},
            {"role":"user","content":f"شنو أحسن شي عندكم؟"},
            {"role":"assistant","content":f"أكثر طلب عندنا {meal}، والناس تمدحه"},
            {"role":"user","content":f"وللحساسية من {pick(['جلوتين','لكتوز','مكسرات'])}؟"},
            {"role":"assistant","content":"عندنا خيارات خالية من المواد الحساسة، اسأل النادل"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"أكلت بـ{rest} وتسمم، شنو تقول؟"},
            {"role":"assistant","content":"والله هذا مؤسف جداً. متأكد من {rest}؟"},
            {"role":"user","content":"إي، بالأمس وكلنا مريضين"},
            {"role":"assistant","content":"آسفين جداً. تعال وأحضر الإيصال نعالج الموضوع"},
            {"role":"user","content":"أريد تعويض"},
            {"role":"assistant","content":"حقك، نحن نتحمل المسؤولية"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"شنو عروض {rest} هالأسبوع؟"},
            {"role":"assistant","content":f"عندنا خصم {_discount}% على {meal} حتى نهاية الأسبوع"},
            {"role":"user","content":"وعروض التوصيل؟"},
            {"role":"assistant","content":f"توصيل مجاني للطلبات فوق {vp(_free_delivery)} دينار هالأسبوع"},
            {"role":"user","content":"ممتاز، بطلب الليلة"},
            {"role":"assistant","content":"حياك، ننتظر طلبك"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"أريد أجرب {rest} للمرة الأولى، شنو تنصح؟"},
            {"role":"assistant","content":f"أهلاً بيك! مشهورين بـ{meal}. أنا أنصحك تجرب"},
            {"role":"user","content":"هل للنباتيين خيارات؟"},
            {"role":"assistant","content":"إي، عندنا مينيو نباتي كامل"},
            {"role":"user","content":f"وللأطفال؟"},
            {"role":"assistant","content":"عندنا وجبات أطفال بحصص مناسبة"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"الحساب لـ{_pax} بـ{rest} كم يجي؟"},
            {"role":"assistant","content":f"بيش كنتوا تأكلون؟"},
            {"role":"user","content":f"{meal} للكل مع {drink}"},
            {"role":"assistant","content":f"تقريباً {vp(_price1*4)} دينار حسب العدد"},
            {"role":"user","content":"وبالبطاقة أدفع؟"},
            {"role":"assistant","content":"إي، كارد وكاش مقبولين"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"عندكم {pick(['وايفاي مجاني','شحن موبايل','ألعاب للأطفال'])} بـ{rest}؟"},
            {"role":"assistant","content":"إي، وايفاي مجاني للزبائن"},
            {"role":"user","content":"وساعة دخول؟"},
            {"role":"assistant","content":"ما في ساعة دخول، اجلس براحتك"},
            {"role":"user","content":"ممتاز، هذا المكان المناسب للشغل"},
            {"role":"assistant","content":"حياك دايماً، الإنترنت سريع"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"أريد أسأل، {meal} عندكم حلال 100%؟"},
            {"role":"assistant","content":"إي طبعاً، كل لحومنا من مصادر حلال معتمدة"},
            {"role":"user","content":"في شهادة؟"},
            {"role":"assistant","content":"إي، شهادة الحلال معلقة بالمدخل تفضل شوفها"},
            {"role":"user","content":"ممتاز، هذا المهم"},
            {"role":"assistant","content":"طبعاً، صحة زبائننا أهم شي"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"أريد أضيف ملاحظة على الطلب، بدون {pick(['ملح','حار','ثوم','بصل'])}"},
            {"role":"assistant","content":"ممكن، شو الطلب؟"},
            {"role":"user","content":f"{meal}"},
            {"role":"assistant","content":f"سجلنا: {meal} بدون {pick(['ملح','حار','ثوم','بصل'])}. أي شي ثاني؟"},
            {"role":"user","content":f"مع {drink} بدون ثلج"},
            {"role":"assistant","content":"ماشي، كل شي متعرف"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"أيش الفرق بين {rest} و{rest2}؟"},
            {"role":"assistant","content":f"{rest} متخصص بـ{meal}، {rest2} بـ{meal2}"},
            {"role":"user","content":"أيش أحسن للعيلة؟"},
            {"role":"assistant","content":f"{rest} عنده قاعات عيلية أكبر وهادية"},
            {"role":"user","content":"والسعر؟"},
            {"role":"assistant","content":f"{rest} شوية أغلى بس الجودة أعلى"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"ترا جيت قبل وطلبي طول وقت، شلون؟"},
            {"role":"assistant","content":f"آسفين جداً. {_complaint} أحياناً بالزحمة"},
            {"role":"user","content":"هذا مو معقول، عندكم زبائن ثانيين جاوا بعدي"},
            {"role":"assistant","content":"هذا غلط منا. نعطيك {pick(['خصم','حصة مجانية','مشروب مجاني'])} تعويضاً"},
            {"role":"user","content":"ماشي، بس هالمرة الأخيرة"},
            {"role":"assistant","content":"ما يتكرر، نعدك"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":f"أريد أطلب ولا أعرف شنو آكل، تنصحني؟"},
            {"role":"assistant","content":"شنو تفضل، مشوي ولا مرق؟"},
            {"role":"user","content":"مشوي"},
            {"role":"assistant","content":f"{meal} ممتاز اليوم، طازج وعليه طلب هواي"},
            {"role":"user","content":"آخذه مع {drink2}"},
            {"role":"assistant","content":f"خيار ممتاز. بـ{vp(_price1+_price2)} دينار الكل"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"عندكم عروض رمضان خاصة بـ{rest}؟"},
            {"role":"assistant","content":"إي، عروض إفطار كاملة رمضان"},
            {"role":"user","content":"شنو تشمل؟"},
            {"role":"assistant","content":f"شوربة و{meal} و{drink} وحلو بـ{vp(_price1*2)} للشخص"},
            {"role":"user","content":"وللعيلة؟"},
            {"role":"assistant","content":f"باكج عيلي {_pax} بـ{vp(_price1*2*4)} دينار"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"شكد يكلف الدجاج المشوي بـ{rest}؟"},
            {"role":"assistant","content":f"دجاجة كاملة مشوية بـ{vp(_price1*2)} دينار"},
            {"role":"user","content":"ونصف دجاجة؟"},
            {"role":"assistant","content":f"نص بـ{vp(_price1)} دينار"},
            {"role":"user","content":"مع صلصة ثوم؟"},
            {"role":"assistant","content":f"مضمنة، وعندنا صلصة {pick(['حارة','خفيفة','مزيجة'])} تختار"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"أريد أحتفل بعيد ميلاد بـ{rest}، تساعدوني؟"},
            {"role":"assistant","content":"طبعاً، تشرفنا! كم عدد المدعوين؟"},
            {"role":"user","content":f"{_pax}"},
            {"role":"assistant","content":f"عندنا باكج احتفالات. شمعة وكيك وبالون مجاناً مع طلب {_pax}"},
            {"role":"user","content":"وهل ممكن جهاز صوت؟"},
            {"role":"assistant","content":"إي، ممكن برسوم رمزية {vp(20000)} دينار"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"الطلب جاي لي ولا لشخص ثاني؟"},
            {"role":"assistant","content":"اسم الطلب؟"},
            {"role":"user","content":f"{pick(ALL_NAMES)}"},
            {"role":"assistant","content":f"إي هذا طلبك. {meal} و{drink}"},
            {"role":"user","content":"ناقص {drink2}"},
            {"role":"assistant","content":"آسفين، هسه أجيبه"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"كيف الجودة بـ{rest} مقارنة بالسابق؟"},
            {"role":"assistant","content":"جودتنا ثابتة بفضل الله. ما تنازلنا عن المواد"},
            {"role":"user","content":"أحياناً أحس النكهة تتغير"},
            {"role":"assistant","content":"ممكن، عندنا طباخين اثنين والنكهة قد تختلف شوية"},
            {"role":"user","content":"أتمنى تثبت الجودة"},
            {"role":"assistant","content":"شكراً، هذا دافعنا نتحسن"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"هلو، مستوى النظافة بـ{rest} كيف؟"},
            {"role":"assistant","content":"نظافتنا من أولويتنا. مفتش الصحة يجي شهرياً"},
            {"role":"user","content":"ماشي، وين الحمامات؟"},
            {"role":"assistant","content":f"بـ{pick(['اليمين','اليسار','الطابق الثاني'])} بجانب المطبخ"},
            {"role":"user","content":"نظيفة؟"},
            {"role":"assistant","content":"نظيفها كل ساعة. تفضل"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":f"عندكم {pick(['سفة','محلبية','بقلاوة','زلابية'])} للحلو؟"},
            {"role":"assistant","content":"إي عندنا حلويات يومية"},
            {"role":"user","content":"طازجة؟"},
            {"role":"assistant","content":"تتحضر كل يوم من الصبح"},
            {"role":"user","content":"آخذ واحدة بعد الغداء"},
            {"role":"assistant","content":f"بـ{vp(5000)} دينار. طيبة إن شاء الله"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":f"أريد طلب للمكتب، {_pax} أشخاص"},
            {"role":"assistant","content":"بيش تريدون؟"},
            {"role":"user","content":f"كل واحد {meal}"},
            {"role":"assistant","content":f"مجموع {_pax} وجبات {meal} بـ{vp(_price1*4)} دينار"},
            {"role":"user","content":"وين نعطيكم العنوان؟"},
            {"role":"assistant","content":"بالتطبيق أو اتصل مباشرة وأعطينا العنوان"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"أريد أسأل، {drink} عندكم مثلج ولا عادي؟"},
            {"role":"assistant","content":f"{drink} عندنا مثلج وطبيعي. تختار؟"},
            {"role":"user","content":"مثلج أحسن"},
            {"role":"assistant","content":"ماشي. مع ليمون؟"},
            {"role":"user","content":"بدون ليمون"},
            {"role":"assistant","content":"حاضر، جاي هسه"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":f"عندكم {meal} هالفصل ولا مو موجود؟"},
            {"role":"assistant","content":f"{meal} موسمي، موجود فقط {pick(['الشتاء','الصيف','رمضان','المواسم'])}"},
            {"role":"user","content":"وشنو البديل؟"},
            {"role":"assistant","content":f"{meal2} موجود طول السنة وقريب منه بالطعم"},
            {"role":"user","content":"ماشي، آخذ البديل"},
            {"role":"assistant","content":"ممتاز، ما تندم"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"هلو، عندكم كوبون خصم لزبائن جدد؟"},
            {"role":"assistant","content":"إي، خصم 10% على أول طلب مع الاشتراك بتطبيقنا"},
            {"role":"user","content":"كيف أشترك؟"},
            {"role":"assistant","content":"حمل التطبيق وسجل برقم هاتفك"},
            {"role":"user","content":"والخصم ينطبق على كل شي؟"},
            {"role":"assistant","content":"كل شي ما عدا الكيك والعروض"},
        ]
    elif tpl == 41:
        msgs = [
            {"role":"user","content":f"أريد أقرأ المراجعات قبل أجي، {rest} كيف؟"},
            {"role":"assistant","content":"مراجعات گوگل 4.5 نجوم و500+ تقييم"},
            {"role":"user","content":"والشكاوى؟"},
            {"role":"assistant","content":"أغلب الشكاوى وقت الزحمة. نحاول نتحسن"},
            {"role":"user","content":"وين تجلسون أحسن؟"},
            {"role":"assistant","content":f"بعيداً عن المطبخ. {_seat} أهدأ"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"أريد أسأل، في بقايا طلبي الأمس عندكم؟"},
            {"role":"assistant","content":"آسفين، ما نحتفظ بطلبات من يوم لثاني"},
            {"role":"user","content":"وما تقدرون ترسلون للبيت اليوم نفسه؟"},
            {"role":"assistant","content":f"إذا طلبت قبل ساعتين من إغلاقنا، ممكن نوصل"},
            {"role":"user","content":"ماشي، بطلب اليوم"},
            {"role":"assistant","content":"حياك، ننتظر طلبك"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"عندكم جلسة خارجية بـ{rest}؟"},
            {"role":"assistant","content":"إي، عندنا حديقة خارجية هادية"},
            {"role":"user","content":"تشتغل بالشتاء؟"},
            {"role":"assistant","content":"الشتاء نحطلها دفايات وتبقى مريحة"},
            {"role":"user","content":"ممتاز، أفضلها"},
            {"role":"assistant","content":"حياك، الجو برة أحلى"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"هلو، هالإيصال صح؟ جاي {vp(_total)} دينار"},
            {"role":"assistant","content":"أشوف... حسبنا {_pax} وجبات صح؟"},
            {"role":"user","content":"إي بس الحساب يبدو كثير"},
            {"role":"assistant","content":f"الضريبة {_tax_pct}% مضافة. هذا يرفع المجموع"},
            {"role":"user","content":"ماشي، هذا الحساب صح"},
            {"role":"assistant","content":"شكراً، نتشرف"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"أريد طلب عند {rest}، الأطفال يأكلون شنو؟"},
            {"role":"assistant","content":"عندنا وجبات أطفال خاصة"},
            {"role":"user","content":"مثل؟"},
            {"role":"assistant","content":f"دجاج صغير أو {pick(['برغر صغير','سمك','نگيت'])} مع بطاطا"},
            {"role":"user","content":"السعر؟"},
            {"role":"assistant","content":f"وجبة الأطفال بـ{vp(_price2)} دينار مع عصير"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"أريد أقارن بين {meal} عندكم وعند {rest2}"},
            {"role":"assistant","content":f"ما قدر أقارن، بس {meal} عندنا بالفحم الطبيعي"},
            {"role":"user","content":"والسعر؟"},
            {"role":"assistant","content":f"عندنا {vp(_price1)} دينار. جرب وحكم بنفسك"},
            {"role":"user","content":"ماشي، بجرب عندكم"},
            {"role":"assistant","content":"حياك، ما تندم"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أعرف كم مدة تحضير {meal} عندكم؟"},
            {"role":"assistant","content":f"{meal} يحتاج {_wait_min} تحضير. يستاهل"},
            {"role":"user","content":"وأنا جوعان هسه"},
            {"role":"assistant","content":f"عندنا {drink} ومقبلات جاهزة ترقدك بالوقت"},
            {"role":"user","content":"ماشي، آخذ مقبلات ريثما"},
            {"role":"assistant","content":"حاضر، جايك فوراً"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"هلو، عندكم أكل صحي أو خيارات دايت؟"},
            {"role":"assistant","content":"إي، عندنا قسم صحي بالمينيو"},
            {"role":"user","content":"مثل؟"},
            {"role":"assistant","content":f"سلطة كبيرة وشوي بدون دهن و{drink} طبيعي"},
            {"role":"user","content":"وبدون ملح؟"},
            {"role":"assistant","content":"ممكن، نقول للمطبخ يحضرونه بدون ملح"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أريد أحجز طاولة خاصة لـ{_event} مهم"},
            {"role":"assistant","content":"أهلاً، عندنا قاعة خاصة للمناسبات"},
            {"role":"user","content":"الأجر؟"},
            {"role":"assistant","content":f"القاعة بـ{vp(_deposit)} دينار بدون أكل، أو مجانية لو الطلب فوق {vp(_deposit*3)} دينار"},
            {"role":"user","content":"ماشي، بنطلب أكثر من الحد"},
            {"role":"assistant","content":"ممتاز، سجلنا الحجز باسمك"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"هلو، عندكم {meal} و{meal2} هالأيام؟"},
            {"role":"assistant","content":f"إي والله، {meal} موجود. {meal2} بيتذبذب"},
            {"role":"user","content":f"آخذ {meal} إذاً"},
            {"role":"assistant","content":"كلشي يتحضر طازج. يجيك خلال {_wait_min}"},
            {"role":"user","content":f"مع {drink}"},
            {"role":"assistant","content":f"حاضر. المجموع {vp(_price1+_price2)} دينار"},
        ]

    return {"id": f"rest_{i:04d}", "category": "restaurant_cafe", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 15 - TRANSPORTATION
# ============================================================
AREAS = ["الكرادة","المنصور","الكاظمية","الأعظمية","الجادرية","النهضة",
         "الزعفرانية","الحارثية","الشعب","العطيفية","الدورة"]
TAXI_NAMES = ["أبو صلاح","أبو وسيم","أبو فهد","أبو طارق","أبو ماجد"]

def gen_transport(i):
    area1  = pick(AREAS)
    area2  = pick(AREAS)
    while area2 == area1: area2 = pick(AREAS)
    taxi   = pick(TAXI_NAMES)
    _gr    = pick(GREET)
    _price1 = pick([5000,6000,7000,8000,9000,10000])
    _price2 = pick([12000,15000,18000,20000,25000])
    _price3 = pick([30000,35000,40000,45000,50000])
    _airport_price = pick([20000,25000,30000,35000])
    _fullday_city  = pick([75000,80000,90000,100000])
    _fullday_out   = pick([140000,150000,175000,200000])
    _moto_price    = pick([25000,30000,35000,40000])
    _bus_price     = pick([750,1000,1500,2000])
    _bus_num       = pick(["1","2","9","15","21","33","77","99"])
    _wait_time     = pick(["5 دقايق","10 دقايق","15 دقيقة","ربع ساعة","20 دقيقة"])
    _extra_time    = pick(["10 دقايق","15 دقيقة","ربع ساعة","20 دقيقة"])
    _flight_hour   = pick(["4 الفجر","5 الصبح","6 الصبح","7 الصبح","8 الصبح"])
    _pickup_hour   = pick(["2 الفجر","3 الفجر","4 الصبح","5 الصبح"])
    _bridge        = pick(["جسر الأئمة","جسر السنك","جسر المعلق","جسر الجمهورية","جسر بغداد"])
    _alt_route     = pick(["الطريق الدوري","الشارع الفرعي","شارع أبو نواس","الخط السريع"])
    _block_reason  = pick(["موكب","تفجير زجاجي","إصلاحات","حادثة","تظاهرة"])
    _stolen_item   = pick(["موبايل وفلوس","حقيبة الظهر","لابتوب","وثائق مهمة","حقيبتي"])
    _fuel_type     = pick(["بنزين","ديزل","بنزين ممتاز"])
    _fuel_price    = pick([750,800,850,900,1000])
    _park_fee      = pick([1000,2000,3000,5000])
    _car_problem   = pick(["إطار مثقوب","الكمبريسر خربان","ما تشتغل البطارية","تسرب زيت","أوفرهيتنج"])
    _trip_city     = pick(["كربلاء","النجف","بابل","الديوانية","سامراء","تكريت","الموصل"])
    _trip_price    = pick([50000,60000,75000,80000,100000])
    _nm            = pick(ALL_NAMES)
    _school_area   = pick(["قريبة","بعيدة نوعاً","بالمنطقة","في المركز"])
    _school_price  = pick([5000,6000,7000,8000])
    _app_name      = pick(["كريم","أوبر","مسافر","زين لفت"])
    _app_wait      = pick(["3 دقايق","5 دقايق","7 دقايق","10 دقايق"])
    _trailer_load  = pick(["أثاث بيت كامل","أجهزة كهربائية","بضاعة محل","مواد بناء"])
    _trailer_price = pick([100000,120000,150000,200000])
    tpl = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"تاكسي، تروح {area1}؟"},
            {"role":"assistant","content":f"إي، ركب يا أخوي"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"{vp(_price1)} دينار"},
            {"role":"user","content":f"غالي شوي، {vp(_price1-1000)} أكدر؟"},
            {"role":"assistant","content":f"{vp(_price1)} وهذا آخر سعر، والله البنزين غلى"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"كيف أروح من {area1} لـ{area2}؟"},
            {"role":"assistant","content":f"تاكسي مباشر أو پاص {_bus_num} يمر على {area2}"},
            {"role":"user","content":"الپاص أسرع ولا التاكسي؟"},
            {"role":"assistant","content":f"التاكسي أسرع بس أغلى بـ{vp(_price1)}. الپاص بـ{vp(_bus_price)} بس فيه وقفات"},
            {"role":"user","content":"وين وقفة الپاص؟"},
            {"role":"assistant","content":f"وقفة پاص {_bus_num} على طرف {area1}، المحطة الرئيسية"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"أريد سيارة مع سائق ليوم كامل، بيش؟"},
            {"role":"assistant","content":f"يوم كامل داخل بغداد {vp(_fullday_city)} دينار"},
            {"role":"user","content":f"وإذا طلعنا برة بغداد، مثلاً {_trip_city}؟"},
            {"role":"assistant","content":f"برة بغداد لـ{_trip_city} {vp(_fullday_out)} دينار + البنزين علينا مشترك"},
            {"role":"user","content":f"ماشي، غداً الصبح من الساعة 8، تجي لـ{area1}؟"},
            {"role":"assistant","content":f"حاضر، أعطيني عنوانك بـ{area1} وأكون هناك"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"أريد أروح مطار بغداد، طياراني الساعة {_flight_hour}"},
            {"role":"assistant","content":f"المطار بـ{_flight_hour} {vp(_airport_price)} دينار"},
            {"role":"user","content":f"تكدر تجيني الساعة {_pickup_hour}؟"},
            {"role":"assistant","content":f"إي بس في إضافة لأنه وقت ما في سيارات بـ{_pickup_hour}"},
            {"role":"user","content":"ماشي، بيش المجموع؟"},
            {"role":"assistant","content":f"المجموع {vp(_airport_price + 10000)} دينار بالإضافة للوقت الباكر"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"الطريق على {area2} مقطوع؟"},
            {"role":"assistant","content":f"إي، فيه {_block_reason} هسه. نروح من {_alt_route}"},
            {"role":"user","content":"يطول كثير؟"},
            {"role":"assistant","content":f"{_extra_time} إضافية تقريباً بسبب {_block_reason}"},
            {"role":"user","content":"ماشي بس استعجل، عندي موعد"},
            {"role":"assistant","content":f"إن شاء الله أحاول من {_alt_route} أسرع شي"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":"موتوسيكل للإيجار عندكم؟"},
            {"role":"assistant","content":f"إي، بيش تريده؟ يوم ولا أكثر؟"},
            {"role":"user","content":"يوم كامل"},
            {"role":"assistant","content":f"يوم كامل {vp(_moto_price)} دينار مع تأمين"},
            {"role":"user","content":"رخصة القيادة مطلوبة؟"},
            {"role":"assistant","content":f"إي لازم رخصة، ورهن هوية لحين الإرجاع"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"الزحمة على {_bridge} مو طبيعية اليوم"},
            {"role":"assistant","content":f"إي والله، من الصبح و{_bridge} واقف بسبب {_block_reason}"},
            {"role":"user","content":"في طريق ثاني نتجنبه؟"},
            {"role":"assistant","content":f"نروح من {_alt_route}، يطول {_extra_time} بس أهون من الوقفة"},
            {"role":"user","content":"يا إلهي، ماشي روح من هناك"},
            {"role":"assistant","content":"حاضر، بس السعر يزيد شوي بسبب الطريق الأطول"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"أجرة الكرام على {area1} كلش غالية هالأيام"},
            {"role":"assistant","content":f"إي والله، {_fuel_type} غلى وهم رفعوا الأسعار"},
            {"role":"user","content":"قبل كانت أرخص بكثير"},
            {"role":"assistant","content":f"صح، {_fuel_type} كان بـ{vp(_fuel_price-200)} والحين بـ{vp(_fuel_price)} للتر"},
            {"role":"user","content":"شنو البديل الأرخص؟"},
            {"role":"assistant","content":f"پاص {_bus_num} يمر على {area1} وبيه بـ{vp(_bus_price)} دينار"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"سرقوا {_stolen_item} من سيارتي بالپاركنگ قرب {area1}"},
            {"role":"assistant","content":f"والله ما زين! متى هذا صار؟"},
            {"role":"user","content":"هسه، الكسر موجود بالنافذة"},
            {"role":"assistant","content":f"روح مركز الشرطة القريب من {area1} وقدم بلاغ فوراً"},
            {"role":"user","content":"يفيد؟"},
            {"role":"assistant","content":"لازم البلاغ للتأمين، وكاميرات الپاركنگ تساعد بالتحقيق"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"{taxi}، تعرف {area2}؟"},
            {"role":"assistant","content":f"إي أعرفها كلش زين"},
            {"role":"user","content":"خذني هناك بسرعة، عندي موعد"},
            {"role":"assistant","content":f"{vp(_price2)} دينار بالزحمة الموجودة"},
            {"role":"user","content":"ماشي زين، استعجل"},
            {"role":"assistant","content":f"حاضر يا أخوي، ناخذ من {_alt_route} أسرع"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"أريد سيارة أجرة تروح {_trip_city}"},
            {"role":"assistant","content":f"سفرة {_trip_city} بـ{vp(_trip_price)} دينار للشخص الواحد"},
            {"role":"user","content":"يكمل أشخاص ثانيين؟"},
            {"role":"assistant","content":f"إي، السيارة تشيل 4 أشخاص. الرحلة {pick(['ساعتين','3 ساعات','4 ساعات'])}"},
            {"role":"user","content":"متى تطلع؟"},
            {"role":"assistant","content":f"أقرب سيارة بعد {_wait_time}"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"أريد تطبيق {_app_name}، كيف أطلب سيارة؟"},
            {"role":"assistant","content":f"{_app_name} سهل، نزّل التطبيق وسجل رقمك"},
            {"role":"user","content":"بعدين؟"},
            {"role":"assistant","content":f"حدد موقعك ووجهتك وراح تظهر الأسعار"},
            {"role":"user","content":"كم وقت الانتظار عادةً؟"},
            {"role":"assistant","content":f"{_app_name} بالمنطقة {_app_wait} عادةً"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"سيارتي عندها {_car_problem}، كيف أوصل لـ{area2}؟"},
            {"role":"assistant","content":f"{_car_problem} مشكلة، لازم تسوي {pick(['كاري','قطر','إصلاح على الطريق'])} أول"},
            {"role":"user","content":"رقم مكانيكي قريب عندك؟"},
            {"role":"assistant","content":f"أبو {pick(['جاسم','وسيم','صالح','علي'])} يجي للموقع، يصلح {_car_problem}"},
            {"role":"user","content":"وبعدين أكمل لـ{area2}؟"},
            {"role":"assistant","content":f"إي بعد الإصلاح تكمل. أو أطلب {_app_name} حالياً"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"چاي أخوي، بيش توديني {area1} من هنا؟"},
            {"role":"assistant","content":f"{area1}؟ بعيدة شوي، {vp(_price2)} دينار"},
            {"role":"user","content":f"ياخي، {vp(_price1)} أكدر؟"},
            {"role":"assistant","content":f"صعبة، البنزين والزحمة. {vp(_price1+1000)} آخر كلام"},
            {"role":"user","content":"ماشي، اركب نروح"},
            {"role":"assistant","content":"أحكيلي العنوان بالضبط بـ{area1}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"أريد أرسل طرد لـ{area2}، في خدمة توصيل؟"},
            {"role":"assistant","content":f"إي، توصيل {area2} موجودة"},
            {"role":"user","content":"كم يكلف؟"},
            {"role":"assistant","content":f"حسب الوزن، من {vp(3000)} للـ{pick(['كيلو','3 كيلو','5 كيلو'])} الأول"},
            {"role":"user","content":"كم يستغرق؟"},
            {"role":"assistant","content":f"توصيل داخل بغداد نفس اليوم أو {pick(['باچر','بعد باچر'])}"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"بنزين الستيشن فاضي هسه؟"},
            {"role":"assistant","content":f"إي، بس فيه طابور طويل"},
            {"role":"user","content":"كم أنتظر تقريباً؟"},
            {"role":"assistant","content":f"بالتقريب {pick(['20 دقيقة','ربع ساعة','نص ساعة','ساعة'])}"},
            {"role":"user","content":"وستيشن ثاني قريب؟"},
            {"role":"assistant","content":f"فيه ستيشن ثاني بـ{area2}، أقل زحمة"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد أروح {area2} وما أعرف الطريق، تساعدني؟"},
            {"role":"assistant","content":f"من {area1} لـ{area2} تمشي على {pick(['الشارع الرئيسي','الطريق الدوري','شارع فلسطين','شارع 14 رمضان'])}"},
            {"role":"user","content":"نزلة وين؟"},
            {"role":"assistant","content":f"بعد {pick(['إشارة المرور الثانية','الجسر','الدوار الكبير','المسجد الكبير'])} تنزل يمين"},
            {"role":"user","content":"شكراً، بالسيارة كم دقيقة؟"},
            {"role":"assistant","content":f"بدون زحمة {pick(['10','15','20'])} دقيقة من {area1}"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"أريد سيارة لنقل {_trailer_load} من {area1} لـ{area2}"},
            {"role":"assistant","content":f"نقل {_trailer_load} يحتاج {pick(['پك أب','سيارة نص طن','تريلة صغيرة'])}"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"نقل {_trailer_load} من {area1} لـ{area2} بـ{vp(_trailer_price)} دينار"},
            {"role":"user","content":"متى تكدر؟"},
            {"role":"assistant","content":f"أكدر {pick(['هسه','الصبح الباكر','بعد الظهر','باچر'])}، أقولك على الموعد"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"طريق {area1} آمن هالأيام؟"},
            {"role":"assistant","content":f"إي، {area1} ما فيها مشاكل"},
            {"role":"user","content":f"سمعت فيه نقطة تفتيش قرب {area2}؟"},
            {"role":"assistant","content":f"إي، نقطة أمنية بس روتينية وتمر سريع"},
            {"role":"user","content":"أجيب هوية معي؟"},
            {"role":"assistant","content":"دايماً أحسن تشيل هويتك بالسفر"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"توصلني {area2} وارجع؟"},
            {"role":"assistant","content":f"إيصال وإرجاع؟ {vp(_price2 * 2)} دينار"},
            {"role":"user","content":"كم أنتظر هناك؟"},
            {"role":"assistant","content":f"إذا {pick(['نص ساعة','ساعة','ساعة ونص'])} الانتظار مجاني"},
            {"role":"user","content":"وإذا أكثر؟"},
            {"role":"assistant","content":f"كل ساعة إضافية {vp(5000)} دينار"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"في پاص يروح {area2} من هنا؟"},
            {"role":"assistant","content":f"إي، پاص {_bus_num} يمر على {area2}"},
            {"role":"user","content":"وقفته وين؟"},
            {"role":"assistant","content":f"الوقفة قرب {pick(['إشارة الشارع','أمام المسجد','السوق','المدرسة'])} بـ{area1}"},
            {"role":"user","content":"الأجرة كم؟"},
            {"role":"assistant","content":f"{vp(_bus_price)} دينار فقط"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"أريد أوصل ولدي للمدرسة بـ{area2}، {_school_area}"},
            {"role":"assistant","content":f"موصلة مدرسة يومية لـ{area2}؟ بكم يوم بالأسبوع؟"},
            {"role":"user","content":"خمسة أيام"},
            {"role":"assistant","content":f"شهري {vp(_school_price * 20)} دينار للذهاب فقط، أو {vp(_school_price * 35)} إياب كمان"},
            {"role":"user","content":"يمر من {area1}؟"},
            {"role":"assistant","content":f"إي، مساره يمر من {area1} ثم {area2} مباشرة"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"شنو أحسن تطبيق للتاكسي بالعراق؟"},
            {"role":"assistant","content":f"{_app_name} الأشهر والأوسع انتشاراً بالعراق"},
            {"role":"user","content":"أحسن من التاكسي العادي؟"},
            {"role":"assistant","content":f"{_app_name} أسعاره واضحة ومضمونة، التاكسي أسرع أحياناً"},
            {"role":"user","content":"أنا أفضل التاكسي"},
            {"role":"assistant","content":"كل واحد وذوقه، التاكسي له ميزة المساومة"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"أخوي، الساعة كم يقفل گراج {area1}؟"},
            {"role":"assistant","content":f"گراج {area1} يغلق الساعة {pick(['10 الليل','11 الليل','12 الليل','9 الليل'])}"},
            {"role":"user","content":"في گراج ثاني مفتوح طول الليل؟"},
            {"role":"assistant","content":f"إي، گراج {area2} مفتوح 24 ساعة"},
            {"role":"user","content":"الأجرة فيه؟"},
            {"role":"assistant","content":f"{vp(_park_fee)} دينار بالساعة، أو {vp(_park_fee * 8)} الليلة كاملة"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"بيش تاكسي مشترك لـ{area2}؟"},
            {"role":"assistant","content":f"مشترك لـ{area2} بـ{vp(_bus_price + 500)} دينار للشخص"},
            {"role":"user","content":"يطلع كل كم؟"},
            {"role":"assistant","content":f"كل {pick(['10','15','20'])} دقيقة لو في ركاب"},
            {"role":"user","content":"وقفة الركوب وين؟"},
            {"role":"assistant","content":f"قرب {pick(['إشارة المرور','البنك','الصيدلية','الحديقة'])} بـ{area1}"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"سيارتي توقفت بالشارع، أحتاج كاري"},
            {"role":"assistant","content":"وين توقفت بالضبط؟"},
            {"role":"user","content":f"بـ{area1} قرب {pick(['إشارة المرور','الجسر','البنك','المدرسة'])}"},
            {"role":"assistant","content":f"خلي البلاشر يشتغل. كاري يجيك خلال {_wait_time}"},
            {"role":"user","content":"وين يوديها؟"},
            {"role":"assistant","content":f"أي مكانيكي تختاره بـ{area2} أو أقرب ورشة"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"أريد سيارة تأجير بدون سائق ليومين"},
            {"role":"assistant","content":f"تأجير بدون سائق {pick(['سيدان','SUV','بيك أب'])} متاح"},
            {"role":"user","content":"بيش اليوم؟"},
            {"role":"assistant","content":f"{vp(pick([60000,75000,90000,120000]))} دينار اليوم مع تأمين"},
            {"role":"user","content":"شروط؟"},
            {"role":"assistant","content":f"رخصة قيادة، هوية، وعمر +21 سنة. الوقود على حسابك"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"في معبر بري لـ{_trip_city} من بغداد؟"},
            {"role":"assistant","content":f"إي، في باصات وسيارات مشتركة لـ{_trip_city}"},
            {"role":"user","content":"من وين تنطلق؟"},
            {"role":"assistant","content":f"من موقف {pick(['الأعظمية','باب المعظم','المشتل','الشرقية'])}"},
            {"role":"user","content":"بيش السفرة؟"},
            {"role":"assistant","content":f"باص {_trip_city} بـ{vp(_trip_price // 2)} دينار، سيارة خاصة {vp(_trip_price)} دينار"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":f"صاحبي، أجرتك {area1} كم؟"},
            {"role":"assistant","content":f"{area1}؟ {vp(_price1)} دينار"},
            {"role":"user","content":f"أنا فاضي معي {vp(_price1 - 1000)} بس"},
            {"role":"assistant","content":f"وال، ماشي اركب وأكمل الباقي باچر"},
            {"role":"user","content":"والله كفو عليك"},
            {"role":"assistant","content":"لا شكر على واجب يا عمي"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"اشتريت سيارة جديدة وما أعرف أوصلها البيت من {area1}"},
            {"role":"assistant","content":"في سائق نقل سيارات متخصص، بيوديها لباب بيتك"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"توصيل سيارة داخل بغداد {vp(_price3)} دينار"},
            {"role":"user","content":"رقمه؟"},
            {"role":"assistant","content":f"أبو {pick(['كريم','حسن','علي','طارق'])} لنقل السيارات، أرسل رقمه"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"الباص للمطار يمر من {area1}؟"},
            {"role":"assistant","content":f"إي، باص المطار عنده وقفة بـ{area1}"},
            {"role":"user","content":"الوقفة وين بالضبط؟"},
            {"role":"assistant","content":f"قدام {pick(['الفندق الكبير','المجمع','السوبرماركت','إشارة المرور'])} بـ{area1}"},
            {"role":"user","content":"والأجرة؟"},
            {"role":"assistant","content":f"باص المطار {vp(pick([5000,6000,7000,8000]))} دينار"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"الزحمة بـ{area1} من زمان هيج؟"},
            {"role":"assistant","content":f"لا، قبل كانت أهدأ. المشكلة ازداد عدد السيارات بـ{area1}"},
            {"role":"user","content":"شنو الحل؟"},
            {"role":"assistant","content":f"يقولون راح يسوون مترو لكن ما في موعد محدد"},
            {"role":"user","content":"إن شاء الله يسرعون"},
            {"role":"assistant","content":"إن شاء الله، الزحمة تعب كلنا"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"أريد تطبيق يحجز تاكسي من {area1} لـ{area2}"},
            {"role":"assistant","content":f"{_app_name} أحسن خيار، يحدد السعر قبل الركوب"},
            {"role":"user","content":"بيش تقريباً هالمسافة؟"},
            {"role":"assistant","content":f"تطبيق {_app_name} من {area1} لـ{area2} حوالي {vp(_price2)} دينار"},
            {"role":"user","content":"والانتظار؟"},
            {"role":"assistant","content":f"سائق {_app_name} يجيك خلال {_app_wait}"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"پاركنگ قريب من {area2} موجود؟"},
            {"role":"assistant","content":f"إي، في پاركنگ أمام {pick(['المجمع التجاري','المسجد','البنك','الحديقة'])} بـ{area2}"},
            {"role":"user","content":"الأجرة؟"},
            {"role":"assistant","content":f"{vp(_park_fee)} دينار بالساعة"},
            {"role":"user","content":"آمن؟"},
            {"role":"assistant","content":"إي، فيه حارس وكاميرات"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"أريد أشتري كرت پاص، وين؟"},
            {"role":"assistant","content":f"كروت الپاص تشتريها من نقاط البيع الرسمية بالمحطات"},
            {"role":"user","content":"بيش الكرت؟"},
            {"role":"assistant","content":f"كرت {pick(['أسبوعي','شهري','10 رحلات'])} بأسعار مختلفة"},
            {"role":"user","content":"الشهري بيش؟"},
            {"role":"assistant","content":f"الشهري {vp(pick([20000,25000,30000]))} دينار بخطوط غير محدودة"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":f"أخوي، طريق {area1} فيه إصلاحات هالأيام؟"},
            {"role":"assistant","content":f"إي، فيه إصلاحات بجزء من {area1} من أسبوع"},
            {"role":"user","content":"يطول كثير؟"},
            {"role":"assistant","content":f"قالوا {pick(['أسبوع','أسبوعين','شهر','ثلاثة أيام'])} لكن بالعراق ما تعرف"},
            {"role":"user","content":"ضروري أمر من هناك؟"},
            {"role":"assistant","content":f"لا، تكدر تمر من {_alt_route} وتوصل {area2}"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":f"هلو، أريد رقم تاكسي موثوق بـ{area1}"},
            {"role":"assistant","content":f"{taxi} يشتغل بـ{area1}، رقمه موجود معي"},
            {"role":"user","content":"أرسله لي"},
            {"role":"assistant","content":f"أرسلت رقم {taxi} واتساب. قوله أبو صالح أرسلك"},
            {"role":"user","content":"شكراً، موثوق؟"},
            {"role":"assistant","content":f"إي، {taxi} يشتغل معنا من سنين. معروف بالأمانة"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"في خدمة تاكسي للنساء فقط بالعراق؟"},
            {"role":"assistant","content":"إي، بعض التطبيقات فيها خاصية سائقة امرأة"},
            {"role":"user","content":"أي تطبيق؟"},
            {"role":"assistant","content":f"تطبيق {_app_name} فيه هذا الخيار، اختار 'سائقة' بالتطبيق"},
            {"role":"user","content":"متوفرة دايماً؟"},
            {"role":"assistant","content":"أحياناً في انتظار أطول للسائقات، بس موجودة"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":f"صاحبي، جيب لي عبوة {_fuel_type} من الستيشن"},
            {"role":"assistant","content":f"كم لتر تريد؟"},
            {"role":"user","content":f"5 لترات تكفي؟"},
            {"role":"assistant","content":f"لو سيارتك فاضية بالكامل، لا. 10 لترات أحسن"},
            {"role":"user","content":"ماشي 10 لترات، كم تكلف؟"},
            {"role":"assistant","content":f"10 لترات {_fuel_type} بـ{vp(_fuel_price * 10)} دينار"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"أريد أحجز مقعد بسرفيس {_trip_city}"},
            {"role":"assistant","content":f"سرفيس {_trip_city} موجود، تطلع الساعة {pick(['7 الصبح','8 الصبح','9 الصبح','6 الصبح'])}"},
            {"role":"user","content":"المقاعد كم باقية؟"},
            {"role":"assistant","content":f"عندي {pick(['3 مقاعد','مقعدين','مقعد واحد','4 مقاعد'])} بس"},
            {"role":"user","content":"آخذ واحد، بيش؟"},
            {"role":"assistant","content":f"مقعد {_trip_city} بـ{vp(_trip_price)} دينار. الدفع الحين"},
        ]
    elif tpl == 41:
        msgs = [
            {"role":"user","content":f"أخوي، هسه اتصل بيا {taxi} وقالي السيارة تأخرت"},
            {"role":"assistant","content":f"متى كلفته؟"},
            {"role":"user","content":f"كلفته قبل {pick(['ساعة','نص ساعة','ساعتين'])}"},
            {"role":"assistant","content":f"الزحمة بـ{area1} ممكن تسبب تأخير. صبر عليه شوي"},
            {"role":"user","content":"عندي طيارة مو وقتي هسه"},
            {"role":"assistant","content":f"اتصل بيه يعطيك وقت دقيق، وإلا طلب سيارة ثانية من {_app_name}"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"في خدمة أمين الحقائب بالمطار؟"},
            {"role":"assistant","content":"إي، أمين الحقائب موجود بمطار بغداد الدولي"},
            {"role":"user","content":"كم تكلف الساعة؟"},
            {"role":"assistant","content":f"{vp(pick([2000,3000,5000]))} دينار للحقيبة الواحدة"},
            {"role":"user","content":"يقبل حجز مسبق؟"},
            {"role":"assistant","content":"لا، فقط بالحضور. الإيصال مضمون"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"أريد أستأجر باص لرحلة عائلية لـ{_trip_city}"},
            {"role":"assistant","content":f"باص مريح لـ{_trip_city}؟ كم شخص؟"},
            {"role":"user","content":f"30 شخص تقريباً"},
            {"role":"assistant","content":f"باص 30 شخص لـ{_trip_city} {vp(pick([200000,250000,300000,350000]))} دينار الرحلة"},
            {"role":"user","content":"شامل السائق والبنزين؟"},
            {"role":"assistant","content":"إي، كل شي شامل. بس نحدد يوم الرحلة مسبقاً"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"ركبت {_app_name} والسائق مسار غلط وزاد المبلغ"},
            {"role":"assistant","content":f"هذا ما يصير. تكدر تشتكي بالتطبيق نفسه"},
            {"role":"user","content":"كيف؟"},
            {"role":"assistant","content":f"ادخل 'الدعم' بتطبيق {_app_name} واختار 'مشكلة بالرحلة'"},
            {"role":"user","content":"يرجعون الفرق؟"},
            {"role":"assistant","content":f"{_app_name} يرجع الفرق لو الشكوى مدعومة بالدليل"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"أريد أروح {area2} بس ما عندي فلوس كافية"},
            {"role":"assistant","content":f"كم معك؟"},
            {"role":"user","content":f"{vp(_bus_price * 2)} دينار بس"},
            {"role":"assistant","content":f"هذا يكفي للپاص {_bus_num} لـ{area2}. التاكسي أغلى"},
            {"role":"user","content":"وين وقفة الپاص؟"},
            {"role":"assistant","content":f"قرب {pick(['الإشارة الرئيسية','أمام البنك','عند المسجد'])} بـ{area1}"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"رحلة {area1} لـ{area2} بالكرام، نعم أو لا؟"},
            {"role":"assistant","content":f"ليش لا؟ الكرام وصل {area2}"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"من {area1} لـ{area2} بـ{vp(_price1)} دينار تقريباً"},
            {"role":"user","content":"والزحمة هالوقت؟"},
            {"role":"assistant","content":f"هالساعة {pick(['خفيفة','متوسطة','شوية ثقيلة'])} على {area1}"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"أخوي، تاكسي ورق يمر {area1}؟"},
            {"role":"assistant","content":f"إي، تاكسي الورق يمر من {area1} كل {pick(['10','15','20'])} دقيقة"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"{vp(_bus_price + 250)} دينار داخل المنطقة"},
            {"role":"user","content":"وين أنتظره؟"},
            {"role":"assistant","content":f"عند وقفة {pick(['البنك','المدرسة','السوق','الإشارة'])} بـ{area1}"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"أريد أسافر {_trip_city} وما أعرف كيف"},
            {"role":"assistant","content":f"لـ{_trip_city} عندك خيارات: سرفيس، باص، أو سيارة خاصة"},
            {"role":"user","content":"أيش الأرخص؟"},
            {"role":"assistant","content":f"الأرخص باص {_trip_city} بـ{vp(_trip_price // 2)} دينار"},
            {"role":"user","content":"يطلع من وين؟"},
            {"role":"assistant","content":f"موقف {pick(['المشتل','باب المعظم','الأعظمية','شارع الكفاح'])} بالصبح الباكر"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"سلام، {taxi} تعرفني؟ أنا {_nm}"},
            {"role":"assistant","content":f"إي {_nm}! وين تروح اليوم؟"},
            {"role":"user","content":f"نفس المشوار التعتاد، {area2}"},
            {"role":"assistant","content":f"ماشي يا {_nm}، ركب. اليوم زحمة شوية بـ{area1}"},
            {"role":"user","content":"مو مشكلة، أنا ما أستعجل اليوم"},
            {"role":"assistant","content":f"كفو، نروح من {_alt_route} أهدأ"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"أخوي، تاكسي من {area1} لـ{area2} كم يستغرق؟"},
            {"role":"assistant","content":f"بدون زحمة {pick(['10','15','20','25'])} دقيقة"},
            {"role":"user","content":"والأجرة؟"},
            {"role":"assistant","content":f"من {area1} لـ{area2} بـ{vp(_price2)} دينار"},
            {"role":"user","content":"أبحث لي واحد"},
            {"role":"assistant","content":f"{taxi} يشتغل هالمنطقة، أتصل بيه"},
        ]

    return {"id": f"trans_{i:04d}", "category": "transportation", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 16 - SPORTS & ENTERTAINMENT
# ============================================================
TEAMS   = ["الزوراء","الكهرباء","الطلبة","الشرطة","القوة الجوية","نادي أربيل"]
PLAYERS = ["علي عدنان","أيمن حسين","باسم قاسم","أحمد ياسر"]
GAMES   = ["فيفا","بلايستيشن","لعبة الپابجي","فورتنايت"]
CINEMAS = ["سينما السندباد","سينما بابل","سينما ريد"]

def gen_sports(i):
    team1  = pick(TEAMS)
    team2  = pick(TEAMS)
    while team2 == team1: team2 = pick(TEAMS)
    player = pick(PLAYERS)
    player2= pick(PLAYERS)
    game   = pick(GAMES)
    cinema = pick(CINEMAS)
    _gr    = pick(GREET)
    _ticket_normal = pick([5000,6000,7000,8000])
    _ticket_vip    = pick([15000,20000,25000,30000])
    _gym_monthly   = pick([40000,50000,60000,75000])
    _gym_annual    = pick([400000,500000,600000])
    _pool_add      = pick([15000,20000,25000])
    _cinema_normal = pick([7000,8000,10000])
    _cinema_vip    = pick([12000,15000,18000])
    _score1 = pick(["1-0","2-0","2-1","3-0","1-1","3-2","0-0","4-1"])
    _score2 = pick(["0-0","1-0","2-1","1-2","0-1","3-0"])
    _match_time = pick(["أمس","قبل يومين","مساء الجمعة","الأسبوع الماضي"])
    _match_day  = pick(["الجمعة","السبت","الخميس الليل","يوم الثلاثاء"])
    _sport_type = pick(["كورة","تنس","سباحة","كرة سلة","جودو","ملاكمة","كورة طائرة"])
    _child_age  = pick(["7","8","9","10","11","12"])
    _child_name = pick(["علي","محمد","حسين","أحمد","باسم","كريم"])
    _train_days = pick(["ثلاث مرات بالأسبوع","مرتين بالأسبوع","يومياً","أربع مرات"])
    _game_time  = pick(["الليلة بعد العشاء","الغد الصبح","الجمعة المسا","أي وقت تفضل"])
    _game_hour  = pick(["8 المسا","9 المسا","10 المسا","7 المسا"])
    _film_type  = pick(["أكشن أمريكي","رعب","خيال علمي","كوميدي عربي","دراما","كوميدي أجنبي"])
    _film_name  = pick(["Mission X","Top Action","Dark Rider","Star Fall","Night Chase","Desert Storm"])
    _hall_num   = pick(["1","2","3","الكبيرة","VIP"])
    _show_time  = pick(["6 المسا","8 المسا","10 المسا","4 العصر"])
    _goal_min   = pick(["الدقيقة 10","الدقيقة 35","الدقيقة 67","الدقيقة 88","الدقيقة 90+2"])
    _nm         = pick(ALL_NAMES)
    _trainer    = pick(["أبو طارق","المدرب علي","أستاذ حسن","كوتش صالح","المدرب محمد"])
    _stadium    = pick(["ملعب الشعب","ملعب الزوراء","ملعب الصداقة","ملعب بغداد الدولي"])
    _fitness_goal = pick(["أنزل وزن","أبني عضل","أتحسن بالياقة","أتعافى من إصابة"])
    _workout    = pick(["كارديو","وزن حديد","يوگا","كروس فت","برنامج دهون"])
    _console    = pick(["PS5","Xbox","PC","نينتندو"])
    _game_result = pick(["انتصرنا","انتهت بالتعادل","خسرنا","فزنا بالنقاط"])
    _entertain  = pick(["بولينگ","بلياردو","پلايستيشن كافيه","ملاهي","كافيه"])
    tpl = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"شوفت مباراة {team1} و{team2} {_match_time}؟"},
            {"role":"assistant","content":f"إي والله! {_score1} لـ{team1}، مباراة حماسية كلش!"},
            {"role":"user","content":f"الگول اللي سجله {player} بـ{_goal_min} يهبل"},
            {"role":"assistant","content":f"إي! هالگول ما يجي كثير. {player} اليوم كان بمستوى آخر"},
            {"role":"user","content":f"أنا من زمان أشجع {team1}"},
            {"role":"assistant","content":f"وأنا معك، {team1} هالموسم أحسن من السابق"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"تيكيت مباراة {team1} و{team2} بيش؟"},
            {"role":"assistant","content":f"التيكيت العادي {vp(_ticket_normal)} دينار، والـVIP {vp(_ticket_vip)} دينار"},
            {"role":"user","content":"وين أشتريه؟"},
            {"role":"assistant","content":f"بـ{_stadium} يوم المباراة أو أونلاين قبل يومين"},
            {"role":"user","content":"الكمية محدودة؟"},
            {"role":"assistant","content":f"إي، VIP لـ{_stadium} تبيع بسرعة. استعجل قبل {_match_day}"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"اشتراك النادي الرياضي بيش؟ أريد {_fitness_goal}"},
            {"role":"assistant","content":f"للـ{_fitness_goal}، شهري {vp(_gym_monthly)} دينار أو سنوي {vp(_gym_annual)} دينار"},
            {"role":"user","content":"يشمل جيم وسباحة؟"},
            {"role":"assistant","content":f"الجيم مشمول وبرنامج {_workout}. السباحة إضافة {vp(_pool_add)} شهري"},
            {"role":"user","content":"ساعات الدوام؟"},
            {"role":"assistant","content":f"من 6 الصبح لـ11 الليل. عندنا {_trainer} متخصص بالـ{_workout}"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"أنا و{_nm} نلعب {game} على {_console}، تعال معنا"},
            {"role":"assistant","content":f"إي أجي! {game} على {_console} يهبل!"},
            {"role":"user","content":f"{_game_time}، موافق؟"},
            {"role":"assistant","content":f"ماشي، أجيكم الساعة {_game_hour}"},
            {"role":"user","content":"عندك إنترنت زين؟ اللعبة أونلاين"},
            {"role":"assistant","content":f"إي، اشتريت باقة 100 جيگا جديدة، {game} ما تتقطع"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"تيكيت {cinema} اليوم بيش؟"},
            {"role":"assistant","content":f"تيكيت عادي {vp(_cinema_normal)} دينار، VIP {vp(_cinema_vip)} دينار"},
            {"role":"user","content":f"الفيلم شنو يعرضون؟"},
            {"role":"assistant","content":f"عندنا '{_film_name}'، {_film_type}، على الساعة {_show_time}"},
            {"role":"user","content":f"آخذ اثنين VIP لصالة {_hall_num}"},
            {"role":"assistant","content":f"حاضر، {vp(_cinema_vip * 2)} دينار المجموع. تفضل"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"شنو رأيك بأداء {team1} هالموسم؟"},
            {"role":"assistant","content":f"والله {team1} هالموسم متذبذب، فيه مباريات زينة وفيه خيبات"},
            {"role":"user","content":f"المشكلة بالمدرب ولا باللاعبين؟"},
            {"role":"assistant","content":f"عندي رأي اللاعبين ما يطبقون تعليمات المدرب بشكل صح"},
            {"role":"user","content":f"إن شاء الله {team1} يحسنون بالدوري"},
            {"role":"assistant","content":f"إن شاء الله، المشجعين يستاهلون أحسن من هيج"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"أريد أسجل ولدي {_child_name} بنادي {_sport_type} للأطفال"},
            {"role":"assistant","content":f"عمر {_child_name} كم سنة؟"},
            {"role":"user","content":f"{_child_age} سنين"},
            {"role":"assistant","content":f"كفو، عندنا فئة {_child_age} سنة. تدريب {_train_days}"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"شهري {vp(_gym_monthly - 10000)} دينار يشمل الزي الرياضي لـ{_child_name}"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"چاي ومباراة {team1} الليلة؟"},
            {"role":"assistant","content":f"إي والله! {team1} ضد {team2} اليوم بـ{_stadium}"},
            {"role":"user","content":"عندك شاشة كبيرة؟"},
            {"role":"assistant","content":"عندي تلفزيون 65 إنش، تعال عندي"},
            {"role":"user","content":"آجيبك چاي وكعك وأنا"},
            {"role":"assistant","content":f"كفو، نستناك. المباراة الساعة {pick(['7','8','9'])} المسا"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"من تشجع أكثر، {team1} ولا {team2}؟"},
            {"role":"assistant","content":f"أنا من عائلة مشجعة {team1} كلها، من جدي"},
            {"role":"user","content":"وأنا أشجع {team2} وأنت ضد"},
            {"role":"assistant","content":f"هذي سالفة! بس صداقة فوق كل شي"},
            {"role":"user","content":"طبعاً، المباراة مباراة والرفقة رفقة"},
            {"role":"assistant","content":f"كفو، هيج المفروض. لمن يخسر يدفع الچاي"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"المباراة النهائية بين {team1} و{team2} {_match_day}؟"},
            {"role":"assistant","content":f"إي، النهائي {_match_day} بـ{_stadium} الساعة {pick(['5','6','7'])} المسا"},
            {"role":"user","content":"أريد أروح بـ{_stadium}، تيكيت باقي؟"},
            {"role":"assistant","content":f"عادي باقي. VIP يمكن انتهى"},
            {"role":"user","content":"أروح من وين أشتري؟"},
            {"role":"assistant","content":f"شباك {_stadium} يفتح من الصبح {_match_day}. روح بكير"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"أريد أشترك بنادي {_sport_type}، شنو الشروط؟"},
            {"role":"assistant","content":f"نادي {_sport_type} يقبل من 15 سنة فأكثر"},
            {"role":"user","content":"عمري 17، كفو؟"},
            {"role":"assistant","content":f"كفو، لازم موافقة الوالد وإيصال دفع {vp(_gym_monthly)} دينار شهرياً"},
            {"role":"user","content":"فيه تجربة مجانية؟"},
            {"role":"assistant","content":f"إي، الأسبوع الأول مجاني. بعدين تقرر"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"شوفت {player} بالتدريب اليوم؟"},
            {"role":"assistant","content":f"إي، {player} كان بمستوى رائع بالتدريب"},
            {"role":"user","content":f"يستاهل يكون البداية ضد {team2}؟"},
            {"role":"assistant","content":f"برأيي إي. {player} أفضل من {player2} هالفترة"},
            {"role":"user","content":"إن شاء الله المدرب يختاره"},
            {"role":"assistant","content":f"إن شاء الله. {team1} يحتاجه بالمباراة الجاية"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد أسأل عن دورة {_sport_type} للمبتدئين"},
            {"role":"assistant","content":f"دورة {_sport_type} للمبتدئين عندنا تبدأ كل شهر"},
            {"role":"user","content":"كم جلسة؟"},
            {"role":"assistant","content":f"12 جلسة خلال شهر، {_train_days}"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"{vp(_gym_monthly)} دينار للدورة كاملة مع {_trainer}"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"فيلم '{_film_name}' بـ{cinema} يستاهل؟"},
            {"role":"assistant","content":f"'{_film_name}' {_film_type} ممتاز. قيّموه 8.5 على 10"},
            {"role":"user","content":"فيلم عنيف؟"},
            {"role":"assistant","content":f"فيه مشاهد أكشن بس ما شيء مبالغ. مناسب من 15 سنة"},
            {"role":"user","content":"كم ساعته؟"},
            {"role":"assistant","content":f"ساعتين وربع. العرض على {_show_time}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"أنا مبتدئ بالجيم، شنو أبدأ بيه لـ{_fitness_goal}؟"},
            {"role":"assistant","content":f"للـ{_fitness_goal} تبدأ بـ{_workout} أول أسبوعين"},
            {"role":"user","content":"كم مرة بالأسبوع؟"},
            {"role":"assistant","content":f"للمبتدئ، {pick(['3 مرات','4 مرات'])} بالأسبوع كافي. استراحة بين الجلسات مهمة"},
            {"role":"user","content":"أحتاج مدرب شخصي؟"},
            {"role":"assistant","content":f"{_trainer} متاح للتدريب الشخصي بـ{vp(_gym_monthly)} دينار شهري إضافة"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"قاعة {_entertain} زينة بالكرادة؟"},
            {"role":"assistant","content":f"إي، {_entertain} بالكرادة ممتاز وجو زين"},
            {"role":"user","content":"بيش ساعة؟"},
            {"role":"assistant","content":f"ساعة {_entertain} بـ{vp(pick([10000,15000,20000,25000]))} دينار"},
            {"role":"user","content":"نحتاج حجز مسبق؟"},
            {"role":"assistant","content":f"بعطل نهاية الأسبوع، الحجز ضروري. غيره مو لازم"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أخوي، نتيجة {team1} {_match_time} شنو؟"},
            {"role":"assistant","content":f"{team1} {_game_result} {_score1} ضد {team2}"},
            {"role":"user","content":f"ومين سجل؟"},
            {"role":"assistant","content":f"{player} سجل {pick(['گول','گولين','ثلاث گولات'])} وـ{player2} أسست"},
            {"role":"user","content":"الجمهور شلون كان؟"},
            {"role":"assistant","content":f"بـ{_stadium} كان ممتلئ وجو حماسي كلش"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"أريد أسجل بنادي ملاكمة"},
            {"role":"assistant","content":f"ملاكمة ممتاز. كم عمرك؟"},
            {"role":"user","content":f"أنا {pick(['18','20','22','25','30'])} سنة"},
            {"role":"assistant","content":f"كفو، نادي الملاكمة يقبل هالعمر. فحص طبي مطلوب أول"},
            {"role":"user","content":"الرسوم شهرية كم؟"},
            {"role":"assistant","content":f"شهري {vp(_gym_monthly)} دينار، {_train_days} مع {_trainer}"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"ساعات {cinema} الثلاثاء؟"},
            {"role":"assistant","content":f"{cinema} يفتح من {pick(['2','3','4'])} العصر للثلاثاء"},
            {"role":"user","content":f"أول عرض أي ساعة؟"},
            {"role":"assistant","content":f"أول عرض الساعة {_show_time}"},
            {"role":"user","content":"تحتاج تذاكر مسبقة؟"},
            {"role":"assistant","content":f"للأفلام الجديدة مثل '{_film_name}' الحجز مسبقاً أفضل"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"صاحبي، تلعب {game} بعد الظهر؟"},
            {"role":"assistant","content":f"إي زين! {game} على {_console}؟"},
            {"role":"user","content":"إي، عندك وقت؟"},
            {"role":"assistant","content":f"من الساعة {_game_hour}، تجي عندي؟"},
            {"role":"user","content":f"أجيبك أكل ونلعب"},
            {"role":"assistant","content":f"كفو، {game} وأكل، ليلة ما أحلى منها"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"أريد أشتري دراجة رياضية للتمرين"},
            {"role":"assistant","content":f"دراجة رياضية جيدة بكم ميزانيتك؟"},
            {"role":"user","content":f"بين {vp(100000)} وـ{vp(200000)} دينار"},
            {"role":"assistant","content":f"بهالميزانية تكدر تاخذ دراجة {pick(['شينماي','جيانت','ترك','قيانگ'])} جيدة"},
            {"role":"user","content":"وين أشتري؟"},
            {"role":"assistant","content":f"محلات الدراجات بـ{pick(['شارع الرشيد','الكرادة','المنصور','الكاظمية'])}"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"نادي السباحة عندكم مسبح 50 متر؟"},
            {"role":"assistant","content":f"إي، عندنا مسبح أولمبي 50 متر"},
            {"role":"user","content":"ساعات السباحة الحرة؟"},
            {"role":"assistant","content":f"السباحة الحرة من {pick(['6','7'])} الصبح لـ{pick(['10','11'])} وبعدين من {pick(['3','4'])} العصر"},
            {"role":"user","content":"اشتراك السباحة بمفردها؟"},
            {"role":"assistant","content":f"فقط السباحة شهري {vp(_pool_add)} دينار"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"أريد أرى مباراة {team1} بالتلفزيون، أي قناة؟"},
            {"role":"assistant","content":f"مباريات {team1} تنبث على {pick(['قناة الرياضية','الكأس','العراقية الرياضية','bein sports'])}"},
            {"role":"user","content":"عندي نايل سات بس"},
            {"role":"assistant","content":f"على نايل سات تقدر تشوف {pick(['العراقية الرياضية','الشرقية الرياضية','MBC Action'])}"},
            {"role":"user","content":"التردد؟"},
            {"role":"assistant","content":f"ابحث تردد {pick(['11938','12073','11054'])} على {pick(['Nilesat 101','Arabsat'])}"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"اشتريت {_console} جديد، أي لعبة تنصحني؟"},
            {"role":"assistant","content":f"على {_console}؟ {game} ممتاز هالفترة"},
            {"role":"user","content":f"لعبت {game} قبل؟"},
            {"role":"assistant","content":f"إي، {game} كلش ممتعة خصوصاً مع الأصحاب أونلاين"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"اللعبة الأصلية {vp(pick([30000,40000,50000,60000]))} دينار أو اشتري أونلاين أرخص"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"أريد أتمرن بالبيت بدون جيم، ممكن؟"},
            {"role":"assistant","content":f"إي ممكن كلش. {_workout} بالبيت فعال"},
            {"role":"user","content":"شأشتري من معدات؟"},
            {"role":"assistant","content":f"دمبل خفيف، حبل قفز، وحصيرة يكفون للـ{_workout}"},
            {"role":"user","content":"ميزانية؟"},
            {"role":"assistant","content":f"سيت معدات بيت بـ{vp(pick([50000,75000,100000]))} دينار تقريباً"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"أنا وأصحابي نبي نلعب كورة، وين نلاقي ملعب بالكرادة؟"},
            {"role":"assistant","content":f"في ملاعب خماسي بالكرادة للإيجار"},
            {"role":"user","content":"بيش الساعة؟"},
            {"role":"assistant","content":f"ساعة ملعب خماسي {vp(pick([30000,40000,50000,60000]))} دينار"},
            {"role":"user","content":"نحتاج حجز؟"},
            {"role":"assistant","content":f"لـ{_match_day} لازم تحجز من {pick(['يوم','يومين','3 أيام'])} قبل"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"شنو رأيك بـ{player} هالموسم؟"},
            {"role":"assistant","content":f"{player} هالموسم أفضل موسم له، سجل {pick(['5','7','10','12'])} أهداف"},
            {"role":"user","content":f"برأيك يستاهل يروح لدوري أجنبي؟"},
            {"role":"assistant","content":f"إي، مستواه يستاهل. بس أنا أفضل يكمل بـ{team1}"},
            {"role":"user","content":"إذا راح تخسر {team1}"},
            {"role":"assistant","content":f"صح، {player} صاحب {team1} هالفترة"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"أريد أشترك بفئة {_sport_type} للسيدات"},
            {"role":"assistant","content":f"فئة {_sport_type} للسيدات عندنا {_train_days}"},
            {"role":"user","content":"المدربة كفؤة؟"},
            {"role":"assistant","content":f"عندنا مدربة متخصصة و{_trainer} يشرف على البرنامج"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"شهري {vp(_gym_monthly)} دينار. أول أسبوع تجربة مجانية"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":f"أريد أنزل وزن، شنو أنسب رياضة؟"},
            {"role":"assistant","content":f"لإنزال الوزن، الكارديو + {_workout} أفضل مزيج"},
            {"role":"user","content":"كم مرة بالأسبوع؟"},
            {"role":"assistant","content":f"{pick(['4','5'])} مرات بالأسبوع للنتائج الأفضل"},
            {"role":"user","content":"أكيف أكلي؟"},
            {"role":"assistant","content":f"الأكل 70% من النتيجة. نقص السكريات والدهون وزد البروتين"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"شنو نتيجة دوري الكرة العراقي هالأسبوع؟"},
            {"role":"assistant","content":f"{team1} فاز {_score1} على {team2} بمباراة حماسية"},
            {"role":"user","content":f"و{team2} وين هالحين بالترتيب؟"},
            {"role":"assistant","content":f"{team2} بالمركز {pick(['الثالث','الرابع','الخامس','الثاني'])} بـ{pick(['25','28','30','32'])} نقطة"},
            {"role":"user","content":f"وـ{team1}؟"},
            {"role":"assistant","content":f"{team1} يتصدر بـ{pick(['35','38','40','42'])} نقطة"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"أريد أحجز صالة {cinema} لحفلة خاصة"},
            {"role":"assistant","content":f"صالة {cinema} للحفلات الخاصة؟ كم شخص؟"},
            {"role":"user","content":f"حوالي {pick(['30','50','80','100'])} شخص"},
            {"role":"assistant","content":f"صالة {_hall_num} تسع هذا العدد. الحجز {vp(pick([500000,750000,1000000]))} دينار"},
            {"role":"user","content":"يشمل العرض؟"},
            {"role":"assistant","content":"تختار الفيلم أو العرض اللي تريد. الأكل إضافي"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"أخوي، نلعب تنس الطاولة الليلة؟"},
            {"role":"assistant","content":"تنس الطاولة؟ أي مكان؟"},
            {"role":"user","content":f"نادي {pick(['الشباب','الرياضي','الأهلي','التضامن'])}"},
            {"role":"assistant","content":f"ماشي! الساعة {_game_hour}؟"},
            {"role":"user","content":"إي، أنا أحجز الطاولة"},
            {"role":"assistant","content":f"زين، وأنا آجيب ريشات جديدة. {_game_result} آخر مرة، أنتقم"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"أريد أتعلم {_sport_type} من الصفر"},
            {"role":"assistant","content":f"تعلم {_sport_type} من الصفر؟ عمرك كم؟"},
            {"role":"user","content":f"{pick(['16','18','20','25','30'])} سنة"},
            {"role":"assistant","content":f"ما في عمر لتعلم {_sport_type}. {_trainer} عنده برنامج للمبتدئين"},
            {"role":"user","content":"كم وقت أوصل مستوى جيد؟"},
            {"role":"assistant","content":f"بـ{pick(['3 أشهر','6 أشهر','سنة'])} تدريب منتظم تكدر تكون كفو"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"عندي إصابة بالركبة، أقدر أكمل رياضة؟"},
            {"role":"assistant","content":"إصابة الركبة تحتاج فحص أول قبل الرياضة"},
            {"role":"user","content":"الدكتور قال خفيفة"},
            {"role":"assistant","content":f"لو خفيفة، {_workout} الخفيف مثل السباحة أو الدراجة مناسب"},
            {"role":"user","content":f"الجيم أكدر؟"},
            {"role":"assistant","content":f"بتوجيه {_trainer} الرياضي، نعم. بس بعيد عن تمارين الركبة أول"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"فيلم هوليوود بـ{cinema} يستاهل ولا أشوفه بالبيت؟"},
            {"role":"assistant","content":f"تجربة {cinema} ما تشبه البيت، خصوصاً لـ{_film_type}"},
            {"role":"user","content":"شاشة كبيرة وصوت؟"},
            {"role":"assistant","content":f"إي، صالة {_hall_num} عندها {pick(['IMAX','Dolby','4DX','شاشة 4K'])} وصوت محيطي"},
            {"role":"user","content":"بيش التيكيت؟"},
            {"role":"assistant","content":f"عادي {vp(_cinema_normal)} دينار. {pick(['IMAX','4DX'])} أغلى بـ{vp(_cinema_vip)} دينار"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":f"ما تشجع {team1}؟ هالموسم خيّبوا"},
            {"role":"assistant","content":f"والله، {team1} هالموسم فيه تفاوت. بس ما أغير فريقي"},
            {"role":"user","content":f"المشكلة بالهجوم، ما في صانع ألعاب"},
            {"role":"assistant","content":f"صح، من رحل {player} ما لقوا بديل كفو"},
            {"role":"user","content":f"يجيب لاعب جديد الموسم الجاي؟"},
            {"role":"assistant","content":f"يقولون {team1} يفاوض لاعب {pick(['برازيلي','أرجنتيني','نيجيري','مغربي'])} الصيف"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":f"أريد أهدي صاحبي اشتراك نادي لعيد ميلاده"},
            {"role":"assistant","content":f"فكرة رائعة! أي رياضة يفضل؟"},
            {"role":"user","content":f"يحب {_sport_type}"},
            {"role":"assistant","content":f"عندنا كارت هدية اشتراك {_sport_type} شهري بـ{vp(_gym_monthly)} دينار"},
            {"role":"user","content":"يجي بكارت أنيق؟"},
            {"role":"assistant","content":"إي، نحضر كارت هدية مع مغلف مميز. هدية ممتازة"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"أريد أروح أشجع {team1} بـ{_stadium}، أي باب أدخل؟"},
            {"role":"assistant","content":f"مشجعو {team1} يدخلون من باب {pick(['الشرقي','الغربي','الشمالي','الجنوبي'])}"},
            {"role":"user","content":"پاركنگ قريب؟"},
            {"role":"assistant","content":f"في پاركنگ جنب {_stadium} بـ{vp(pick([3000,5000,7000]))} دينار"},
            {"role":"user","content":"أروح بكير؟"},
            {"role":"assistant","content":f"قبل المباراة بـ{pick(['ساعة','ساعة ونص','ساعتين'])} أحسن، الزحمة بـ{_stadium} كبيرة"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":f"أريد أسوي دوري كورة بين الأصحاب، شنو نحتاج؟"},
            {"role":"assistant","content":f"دوري الأصحاب؟ كم فريق؟"},
            {"role":"user","content":f"أربعة فرق، كل فريق {pick(['5','6','7'])} لاعبين"},
            {"role":"assistant","content":f"تحتاج ملعب خماسي مجدول بأيام، وتنظيم الجدول"},
            {"role":"user","content":"كم يكلف الملعب؟"},
            {"role":"assistant","content":f"ساعة ملعب خماسي {vp(pick([30000,40000,50000]))} دينار، بحساب {pick(['3','4','5'])} ساعات"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"أريد أنزل وزن 10 كيلو بشهرين، ممكن؟"},
            {"role":"assistant","content":"10 كيلو بشهرين كثير شوي. الصحي 1-2 كيلو بالأسبوع"},
            {"role":"user","content":"يعني شهرين ما يكفي؟"},
            {"role":"assistant","content":f"بحمية صارمة و{_workout} يومي ممكن 5-8 كيلو بشهرين"},
            {"role":"user","content":"أبدأ من وين؟"},
            {"role":"assistant","content":f"استشر {_trainer} وحدد برنامج {_workout} مناسب لجسمك"},
        ]
    elif tpl == 41:
        msgs = [
            {"role":"user","content":f"المباراة بين {team1} و{team2} {_match_day} بث مباشر؟"},
            {"role":"assistant","content":f"إي، بث مباشر على {pick(['قناة العراقية','bein','الكأس','كوورة'])}"},
            {"role":"user","content":"وقت المباراة؟"},
            {"role":"assistant","content":f"الساعة {pick(['5','6','7','8','9'])} مساءً بتوقيت بغداد"},
            {"role":"user","content":"أشوفها على النت؟"},
            {"role":"assistant","content":f"يوتيوب أو موقع الاتحاد العراقي فيه بث مجاني أحياناً"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"أريد أحضر تمارين اليوگا"},
            {"role":"assistant","content":f"اليوگا ممتاز! للرجال ولا للسيدات؟"},
            {"role":"user","content":"مختلط ولا فصل؟"},
            {"role":"assistant","content":f"عندنا كلاس {pick(['مختلط','للسيدات فقط'])} الصبح و{pick(['للرجال','مختلط'])} المسا"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"شهري {vp(_pool_add)} دينار لكلاسات اليوگا، {_train_days}"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"أريد أروح {cinema} الليلة بس ما أعرف الطريق"},
            {"role":"assistant","content":f"{cinema} بـ{pick(['الكرادة','المنصور','الكاظمية','الجادرية'])}"},
            {"role":"user","content":"وين بالضبط؟"},
            {"role":"assistant","content":f"قرب {pick(['البنك','المجمع التجاري','الحديقة','فندق قريب'])}، معروفة"},
            {"role":"user","content":"أحجز أونلاين؟"},
            {"role":"assistant","content":f"إي، {cinema} عنده موقع حجز أونلاين. أوفر وقت"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"أريد أشتري جهاز {_console} جديد، وين؟"},
            {"role":"assistant","content":f"{_console} تشتريه من محلات الإلكترونيات"},
            {"role":"user","content":"بيش السعر الحين؟"},
            {"role":"assistant","content":f"{_console} الجديد بـ{vp(pick([600000,700000,800000,1000000]))} دينار"},
            {"role":"user","content":"ضمان؟"},
            {"role":"assistant","content":f"الوكيل الرسمي يعطي ضمان سنة. المحلات الثانية أقل ضمان"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"أريد أعرف عن بطولة {_sport_type} العراقية هالموسم"},
            {"role":"assistant","content":f"بطولة {_sport_type} العراقية تبدأ {pick(['الشهر الجاي','بعد شهرين','الموسم الجاي'])}"},
            {"role":"user","content":"كم فريق مشارك؟"},
            {"role":"assistant","content":f"{pick(['12','14','16','18'])} فريق بالبطولة هالموسم"},
            {"role":"user","content":f"هل {team1} مشارك؟"},
            {"role":"assistant","content":f"إي، {team1} من المشاركين الأساسيين"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"أريد أعزم صاحبي على سينما، شنو تنصح؟"},
            {"role":"assistant","content":f"للعزومة، {cinema} فيه VIP مريح وأكل وشرب"},
            {"role":"user","content":f"شنو الفيلم الحين؟"},
            {"role":"assistant","content":f"'{_film_name}' {_film_type} جديد. التقييم عالي"},
            {"role":"user","content":"بيش مع الأكل؟"},
            {"role":"assistant","content":f"تيكيت VIP + پوبكورن وشراب {vp(_cinema_vip + pick([5000,7000,10000]))} دينار للشخص"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"هل في جيم للنساء فقط ببغداد؟"},
            {"role":"assistant","content":"إي، في جيمات مخصصة للنساء فقط ببغداد"},
            {"role":"user","content":"وين؟"},
            {"role":"assistant","content":f"في جيمات للسيدات بـ{pick(['الكرادة','المنصور','زيونة','حي بابل'])}"},
            {"role":"user","content":"الرسوم؟"},
            {"role":"assistant","content":f"شهري {vp(_gym_monthly)} دينار. عندهم مدربات متخصصات"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"أريد أروح كافيه پلايستيشن الليلة"},
            {"role":"assistant","content":f"كافيه پلايستيشن؟ زين! بيش الساعة؟"},
            {"role":"user","content":f"كم ساعة تقريباً؟"},
            {"role":"assistant","content":f"ساعة {vp(pick([10000,12000,15000]))} دينار، {_console} موجود"},
            {"role":"user","content":f"نلعب {game} وياك؟"},
            {"role":"assistant","content":f"إي زين! {game} على {_console} يهبل بالكافيه"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أريد أشتري ملابس رياضية، وين؟"},
            {"role":"assistant","content":f"محلات الملابس الرياضية بـ{pick(['الكرادة','المنصور','الجادرية'])} زينة"},
            {"role":"user","content":"أيش الماركات الموجودة؟"},
            {"role":"assistant","content":f"{pick(['نايك','أديداس'])} و{pick(['پوما','أوندر آرمر','ريبوك'])} متوفرة"},
            {"role":"user","content":"بيش عادةً؟"},
            {"role":"assistant","content":f"قطعة {pick(['أصلية','موجودة'])} من {vp(pick([40000,50000,75000,100000]))} دينار"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"عندي مباراة {_sport_type} باچر، تعطيني نصيحة؟"},
            {"role":"assistant","content":f"للـ{_sport_type} الغد، نم بكير الليلة وخذ راحة جيدة"},
            {"role":"user","content":"وقبل المباراة؟"},
            {"role":"assistant","content":f"أكل خفيف قبل {pick(['ساعة','ساعتين'])} واشرب ماي كلش زين"},
            {"role":"user","content":"وتحمية؟"},
            {"role":"assistant","content":f"تحمية 15 دقيقة لازمة قبل أي مباراة {_sport_type}"},
        ]

    return {"id": f"sport_{i:04d}", "category": "sports_entertainment", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 17 - FAMILY & HOME LIFE
# ============================================================
HOME_PARTS = ["الصالة","الديوان","المطبخ","غرفة النوم","الحوش","السطح"]
HOME_ITEMS = ["الثلاجة","الطباخ","المولد","الماطور","المكيف","الغسالة","التلفزيون"]
OCCASIONS  = ["عرس","ختانة","مولود جديد","نجاح","عيد ميلاد","تخرج"]

def gen_family(i):
    room    = pick(HOME_PARTS)
    room2   = pick(HOME_PARTS)
    item    = pick(HOME_ITEMS)
    item2   = pick(HOME_ITEMS)
    occ     = pick(OCCASIONS)
    nm1     = pick(MALE)
    nm2     = pick(FEMALE)
    hw_word = pick(HOME) if HOME else "بيت"
    _gr     = pick(GREET)
    _food   = fw()
    _food2  = fw()
    _repair_cost = pick([50000,100000,150000,200000,250000,300000])
    _paint_cost  = pick([150000,200000,250000,300000,400000])
    _item_cost   = pick([150000,200000,300000,400000,500000,600000])
    _rent_cost   = pick([300000,400000,500000,700000,1000000])
    _child_age   = pick(["سنة","سنتين","3 سنين","4 سنين","5 سنين"])
    _child_prob  = pick(["ما ينام بالليل","يبكي كثير","ما ياكل","حمى","سعال"])
    _nbr_name    = pick(["أبو حسن","جارنا الجديد","الجيران من فوق","العيلة الجديدة","أبو علي الجار"])
    _nbr_prob    = pick(["صوتهم عالي بالليل","يبنون بدون ترخيص","سياراتهم تسد المدخل","نفاياتهم أمام بيتنا","كلابهم تزعج"])
    _room_color  = pick(["بيج وبني","أخضر قديم","أزرق باهت","أصفر فاتح","رمادي قديم"])
    _new_color   = pick(["رمادي وأبيض","بيج فاتح","كريمي عصري","أزرق سماوي فاتح","أبيض ناصع"])
    _guests_num  = pick(["10","15","20","25","30","40"])
    _fix_type    = pick(["السباكة","الكهرباء","الأبواب والشبابيك","التبليط","الحمام"])
    _water_prob  = pick(["ما يطلع ماء","ضغطه واطي","لونه تغير","فيه رائحة","يقطع فجأة"])
    _elec_prob   = pick(["تقصير","المحول يحترق","الأسلاك قديمة","لا إنارة بالليل","المفاتيح خربانة"])
    _furniture   = pick(["كنبايات","طاولة سفرة","غرفة نوم","مطبخ","أثاث ديوان"])
    _furniture_cost = pick([300000,500000,750000,1000000,1500000])
    _cook_method = pick(["اطلب من المطعم","احجز طباخ خارجي","نطبخ مع بعض","كاتر موجود"])
    _plant_type  = pick(["ورود","نباتات خضراء","أشجار صغيرة","ياسمين","بونساي"])
    _ac_prob     = pick(["ما يبرد","يقطر ماي","صوته عالي","يشتغل وما يطفي","لا يشتغل أصلاً"])
    _technician  = pick(["أبو رياض","أبو طارق","المعلم حسن","أبو جاسم","ستاذ صالح"])
    tpl     = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{item} عطل من {pick(['الصبح','أمس','يومين'])}، شسوي؟"},
            {"role":"assistant","content":f"{item} عطل؟ شو العطل بالضبط؟"},
            {"role":"user","content":f"ما يشتغل خالص، يمكن {pick(['فيوز أحترق','موتور خربان','مشكلة بالكهرباء'])}"},
            {"role":"assistant","content":f"اتصل بـ{_technician}، يصلح {item} وكلشي"},
            {"role":"user","content":"رقمه عندك؟"},
            {"role":"assistant","content":f"إي، أرسل لك رقم {_technician} واتساب هسه"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"الكهرباء قطعت وـ{item} ما يشتغل بالمولد"},
            {"role":"assistant","content":f"المولد شايل حمل زيادة يمكن، {item} يأكل تيار كثير؟"},
            {"role":"user","content":f"إي، {item} شغال مع {item2} والمكيف"},
            {"role":"assistant","content":f"طفي {item2} وشغل {item} لوحده، المولد ما يشيل الاثنين"},
            {"role":"user","content":"جربت وما نفع"},
            {"role":"assistant","content":f"المولد يحتاج صيانة، اتصل بـ{_technician} الميكانيكي"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"عندنا {occ} {pick(['الأسبوع الجاي','الشهر الجاي','بعد أسبوعين'])}، شنو نجهز؟"},
            {"role":"assistant","content":f"أبشر على {occ}! كم شخص بالتقريب؟"},
            {"role":"user","content":f"{pick(['50','80','100','150'])} شخص تقريباً"},
            {"role":"assistant","content":f"للـ{pick(['50','80','100','150'])} شخص تحتاج صالة إجار أو مطعم"},
            {"role":"user","content":f"{hw_word} واسع، نسوي {occ} بالبيت"},
            {"role":"assistant","content":"أحسن، خصوصية أكثر وتوفر مصاري. احجز طباخ"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"أم {nm1}، شنو طابخة اليوم؟"},
            {"role":"assistant","content":f"طابخة {_food} وسلطة، وأريد أسوي {_food2} بعد"},
            {"role":"user","content":"وياني أجيب خبز وسمن؟"},
            {"role":"assistant","content":"إي أجيب صمون طازج من الفرن وسمن بلدي"},
            {"role":"user","content":"ماشي، بجي قبل الغداء"},
            {"role":"assistant","content":f"تفضل يا {nm2}، الأكل جاهز الساعة 1"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"{room} تحتاج تصليح، الجدران تشققت وفيه رطوبة"},
            {"role":"assistant","content":f"تشقق {room} من الرطوبة يمكن، أو العزل ضعيف"},
            {"role":"user","content":"كيف أعرف السبب؟"},
            {"role":"assistant","content":f"إذا التشقق قرب الحمام، يمكن تسرب مجاري"},
            {"role":"user","content":"كم يكلف التصليح؟"},
            {"role":"assistant","content":f"عزل وصباغة {room} من {vp(_paint_cost)} دينار حسب المساحة"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"ولدي {nm1} عنده {_child_prob}، كلش يعبني"},
            {"role":"assistant","content":f"عمر {nm1} كم؟"},
            {"role":"user","content":f"{_child_age}"},
            {"role":"assistant","content":f"بعمر {_child_age}، {_child_prob} ممكن طبيعي. جرب {pick(['تحميم قبل النوم','تغيير الروتين','تقليل الضوء','الهدوء بالبيت'])}"},
            {"role":"user","content":"ونجيبه دكتور؟"},
            {"role":"assistant","content":f"لو {_child_prob} مستمر أكثر من 3 أيام، روح الطبيب"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"{_nbr_name}، {_nbr_prob}"},
            {"role":"assistant","content":f"هذا ما يصير، كلمتهم؟"},
            {"role":"user","content":"خجلان أكلمهم"},
            {"role":"assistant","content":f"ما في بأس، قولهم بطريقة محترمة عن {_nbr_prob}"},
            {"role":"user","content":"وإذا ما غيروا؟"},
            {"role":"assistant","content":"تكدر تكلم المختار أو الشرطة المجتمعية"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"أريد أبدل ديكور {room}، شتنصحني؟"},
            {"role":"assistant","content":f"شنو اللون الحالي لـ{room}؟"},
            {"role":"user","content":f"{_room_color}"},
            {"role":"assistant","content":f"غير لـ{_new_color}، يطلع عصري وأرتاح للعين"},
            {"role":"user","content":"والستاير؟"},
            {"role":"assistant","content":f"بردات {pick(['بيضاء','رمادية فاتح','كريمية'])} تكمل ديكور {room}"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"أريد أعزم العيلة عندي، بس {hw_word} صغير"},
            {"role":"assistant","content":"كم شخص؟"},
            {"role":"user","content":f"{_guests_num} شخص"},
            {"role":"assistant","content":f"فرش الديوان والصالة مع بعض. {_guests_num} شخص يمشون"},
            {"role":"user","content":"والأكل؟"},
            {"role":"assistant","content":f"{_cook_method} أحسن لـ{_guests_num} شخص"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"الماي {_water_prob} من {pick(['يومين','أمس','أسبوع'])}"},
            {"role":"assistant","content":f"الماطور شغال؟"},
            {"role":"user","content":"إي شغال بس {_water_prob}"},
            {"role":"assistant","content":f"لو {_water_prob} يمكن انسداد بالمواسير أو الخزان"},
            {"role":"user","content":"شسوي؟"},
            {"role":"assistant","content":f"اتصل بسباك، {_water_prob} يحتاج واحد متخصص"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"المكيف {_ac_prob}، وأهل الحر جايين"},
            {"role":"assistant","content":f"مكيف {_ac_prob}؟ كم سنة عنده؟"},
            {"role":"user","content":f"{pick(['سنتين','3 سنين','5 سنين','أكثر من 5'])}"},
            {"role":"assistant","content":f"يمكن يحتاج غاز أو صيانة. {_technician} يجي يفحصه"},
            {"role":"user","content":"يكلف كثير؟"},
            {"role":"assistant","content":f"صيانة المكيف من {vp(pick([20000,30000,50000]))} دينار حسب العطل"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"أريد أغير {_furniture} للصالة، الحالي قديم"},
            {"role":"assistant","content":f"أيش تفضل بـ{_furniture}، عصري أو كلاسيكي؟"},
            {"role":"user","content":"عصري، بس ميزانيتي محدودة"},
            {"role":"assistant","content":f"{_furniture} عصري جيد من {vp(_furniture_cost)} دينار"},
            {"role":"user","content":"وين أشتري؟"},
            {"role":"assistant","content":f"شارع {pick(['المنصور','الكرادة','النهضة','مركز التسوق'])} فيه خيارات زينة لـ{_furniture}"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"{hw_word} محتاج صيانة {_fix_type}، من متى ما سوينا"},
            {"role":"assistant","content":f"صيانة {_fix_type}؟ من متى ما سويت؟"},
            {"role":"user","content":f"من {pick(['سنتين','3 سنين','سنة'])} تقريباً"},
            {"role":"assistant","content":f"هذا وقت معقول. {_fix_type} مهم يتصلح أول"},
            {"role":"user","content":"كم يكلف؟"},
            {"role":"assistant","content":f"صيانة {_fix_type} من {vp(_repair_cost)} حسب حجم المشكلة"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"الكهرباء الوطنية عندنا {_elec_prob} من يومين"},
            {"role":"assistant","content":f"{_elec_prob} مشكلة جدية. اتصلت بالشبكة؟"},
            {"role":"user","content":"اتصلت، قالوا عطل بالمحول"},
            {"role":"assistant","content":"يعني ساعات وترجع إن شاء الله"},
            {"role":"user","content":"والمولد تعبان بعد"},
            {"role":"assistant","content":f"اتصل بـ{_technician} للمولد هسه، ما تصبر بهالحر"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"أريد أسوي حوش البيت، في نباتات تنسحب؟"},
            {"role":"assistant","content":f"إي، {_plant_type} تنسحب بالحوش"},
            {"role":"user","content":f"أريد خضرة دايمة، {_plant_type} تصلح؟"},
            {"role":"assistant","content":f"إي، {_plant_type} تحتاج ري {pick(['يومي','يومين بيومين','أسبوعي'])} وتعيش بالجو العراقي"},
            {"role":"user","content":"وين أشتري؟"},
            {"role":"assistant","content":f"سوق {pick(['الشورجة','الجمعة','النباتات بالكرادة'])} فيه {_plant_type} بأسعار زينة"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أريد أبدل الباب الرئيسي لـ{hw_word}، شتنصح؟"},
            {"role":"assistant","content":f"باب {pick(['حديد','ألمنيوم','خشب مقوى','UPVC'])} أحسن هالأيام"},
            {"role":"user","content":"الحديد أمن؟"},
            {"role":"assistant","content":f"إي، الحديد أأمن وأطول عمر، بس ألمنيوم أخف"},
            {"role":"user","content":"بيش عادةً؟"},
            {"role":"assistant","content":f"باب حديد جيد من {vp(pick([200000,300000,400000,500000]))} دينار مع التركيب"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد أشتري {item} جديد، كم متوسط الأسعار؟"},
            {"role":"assistant","content":f"{item} جديد بميزانية كم؟"},
            {"role":"user","content":f"أفضل {pick(['الكوري','الياباني','الأمريكي','الصيني الجيد'])}"},
            {"role":"assistant","content":f"{item} {pick(['سامسونگ','LG','توشيبا','باناسونك'])} كفو من {vp(_item_cost)} دينار"},
            {"role":"user","content":"فيه ضمان؟"},
            {"role":"assistant","content":f"الوكيل الرسمي يعطي ضمان {pick(['سنة','سنتين','3 سنين'])}"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"بنت أختي تعبتنا اليوم بالبيت، صغيرة ومزعجة"},
            {"role":"assistant","content":"هههه، عمرها كم؟"},
            {"role":"user","content":f"{_child_age}"},
            {"role":"assistant","content":f"بعمر {_child_age} هيج يكون الأطفال، طبيعي"},
            {"role":"user","content":"صح، بس تعب"},
            {"role":"assistant","content":"الأطفال كنز، صبر عليها، تكبر وتحن عليها"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"الثلاجة ما تبرد، كل شي جوتها يخرب"},
            {"role":"assistant","content":"من متى الثلاجة هيج؟"},
            {"role":"user","content":f"من {pick(['أمس','يومين','أسبوع'])}"},
            {"role":"assistant","content":f"يمكن الغاز خلص أو الكمبريسر. {_technician} يشوفها"},
            {"role":"user","content":"أصلح ولا أشتري جديدة؟"},
            {"role":"assistant","content":f"لو الإصلاح فوق {vp(pick([100000,150000]))}, أحسن تشتري جديدة"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"والله {hw_word} يحتاج طلاء جديد، اللون تغير"},
            {"role":"assistant","content":"من متى ما دهنت؟"},
            {"role":"user","content":f"من {pick(['3 سنين','5 سنين','7 سنين'])} تقريباً"},
            {"role":"assistant","content":f"وقت كافي للطلاء الجديد. {_new_color} شيك هالأيام"},
            {"role":"user","content":"كم يكلف؟"},
            {"role":"assistant","content":f"صباغة {hw_word} كامل من {vp(_paint_cost)} حسب المساحة"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"أريد أستأجر بيت جديد، الإيجار هالأيام غالي؟"},
            {"role":"assistant","content":"إي والله، الإيجارات ارتفعت كلش"},
            {"role":"user","content":f"إيجار {pick(['بيت صغير','شقة غرفتين','شقة ثلاث غرف'])} بكم؟"},
            {"role":"assistant","content":f"بالمنطقة الكويسة من {vp(_rent_cost)} دينار شهرياً"},
            {"role":"user","content":"وين أدور؟"},
            {"role":"assistant","content":"دلالين العقارات أو مجموعات واتساب العقارات"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"ولدي {nm1} ما يحب ياكل خضار، كيف أخليه يياكل؟"},
            {"role":"assistant","content":f"هذي مشكلة شايعة. كم عمر {nm1}؟"},
            {"role":"user","content":f"{_child_age}"},
            {"role":"assistant","content":f"جرب تخبي الخضار بالأكل اللي يحبه، مثلاً بالمكرونة أو الطعام"},
            {"role":"user","content":"ما جربت هيج"},
            {"role":"assistant","content":f"جرب، الأطفال بعمر {_child_age} ما يلاحظون لو الخضار مخبية"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"أريد أحوّل {room} لمكتب عمل بالبيت"},
            {"role":"assistant","content":f"فكرة زينة! {room} واسعة؟"},
            {"role":"user","content":f"معقولة، {pick(['3×4','4×5','3×3'])} متر"},
            {"role":"assistant","content":f"تكفي. تحتاج مكتب، كرسي مريح، وإضاءة جيدة لـ{room}"},
            {"role":"user","content":"كم يكلف التجهيز؟"},
            {"role":"assistant","content":f"مكتب وكرسي جيد من {vp(pick([200000,300000,400000]))} دينار"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"الغسالة ما تدور، الملابس بالداخل"},
            {"role":"assistant","content":"منذ متى وقفت؟"},
            {"role":"user","content":"هسه وقفت"},
            {"role":"assistant","content":f"جرب أطفيها وشغلها ثاني. لو ما اشتغلت، {_technician} يجي يفحص"},
            {"role":"user","content":"لو تحتاج قطعة غيار؟"},
            {"role":"assistant","content":f"قطع الغسالة متوفرة، غالباً {vp(pick([30000,50000,80000]))} دينار"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"عندنا فئران بـ{hw_word}، كيف أخلص منها؟"},
            {"role":"assistant","content":"فئران مشكلة! وين تشوفهم؟"},
            {"role":"user","content":f"بـ{room} وبالمطبخ"},
            {"role":"assistant","content":f"سدد كل الثقوب والشقوق أول، وحط أفخاخ أو سم"},
            {"role":"user","content":"في شركة إبادة؟"},
            {"role":"assistant","content":f"إي، شركات إبادة حشرات بـ{vp(pick([50000,75000,100000]))} دينار للجلسة"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"أريد أسوي حفلة عيد ميلاد لـ{nm2} بالبيت"},
            {"role":"assistant","content":f"أبشر! كم عمر {nm2} هالسنة؟"},
            {"role":"user","content":f"{pick(['3','5','7','10','12'])} سنين"},
            {"role":"assistant","content":f"حلو! تحتاج كيك وزينة وعزيمة للأطفال"},
            {"role":"user","content":"الكيك من وين؟"},
            {"role":"assistant","content":f"حلويات {pick(['أبو ستيفن','الزهاوي','مودة','بيت الحلويات'])} زينة للأطفال"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"الدرج بـ{hw_word} خطر، الأولاد ممكن يوقعون"},
            {"role":"assistant","content":"لازم تسوي درابزون أو حاجز أمان"},
            {"role":"user","content":"كيف؟"},
            {"role":"assistant","content":f"حدادة تسوي درابزون حديد أو خشب من {vp(pick([50000,80000,100000]))} دينار"},
            {"role":"user","content":"يستغرق كم يوم؟"},
            {"role":"assistant","content":f"يومين لـ3 أيام ينجز"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"ولدي {nm1} يريد يسوي مكتبة بغرفته"},
            {"role":"assistant","content":f"فكرة رائعة لـ{nm1}! خشب ولا حديد؟"},
            {"role":"user","content":"خشب أحسن"},
            {"role":"assistant","content":f"نجار يسوي مكتبة خشب حسب المقاس من {vp(pick([100000,150000,200000]))} دينار"},
            {"role":"user","content":"وين أدور نجار؟"},
            {"role":"assistant","content":f"نجارين شارع {pick(['الكفاح','النهضة','المعلمين'])} زينين"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":f"أريد أسوي مجلس بالحوش للصيف"},
            {"role":"assistant","content":"فكرة رائعة! حوشك كبير؟"},
            {"role":"user","content":f"{pick(['واسع','معقول','صغير شوية'])}"},
            {"role":"assistant","content":f"تحتاج مظلة وكراسي مريحة وإضاءة للليل"},
            {"role":"user","content":"الكلفة؟"},
            {"role":"assistant","content":f"مجلس حوش كامل من {vp(pick([200000,300000,500000]))} حسب المساحة"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"اشترينا بيت جديد ونريد نبدل كل {_furniture}"},
            {"role":"assistant","content":f"تهانينا على البيت الجديد! {_furniture} ذوق خاص"},
            {"role":"user","content":"ميزانيتي محدودة"},
            {"role":"assistant","content":f"{_furniture} جيد من {vp(_furniture_cost)} دينار. فيه أسعار مختلفة"},
            {"role":"user","content":"كيف أختار الجيد؟"},
            {"role":"assistant","content":f"اشتر {_furniture} من محل موثوق مع ضمان، متجنب الرخيص جداً"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"الطباخ الغاز ينطفي من نفسه"},
            {"role":"assistant","content":"هذا خطر! متى بدأ؟"},
            {"role":"user","content":f"من {pick(['أمس','يومين','أسبوع'])}"},
            {"role":"assistant","content":"يمكن الشعلة محتاجة تنظيف أو الصمام خربان"},
            {"role":"user","content":"خطير أستمر بيه؟"},
            {"role":"assistant","content":f"لا، اتصل بـ{_technician} هسه قبل ما يصير حادث"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"أريد أزرع خضار بـ{pick(['الحوش','السطح','الشرفة'])} بالبيت"},
            {"role":"assistant","content":"فكرة ممتازة! خضار البيت طازج وأوفر"},
            {"role":"user","content":"شنو أزرع هالوقت؟"},
            {"role":"assistant","content":f"{pick(['طماطة وفلفل','خيار وبامية','باذنجان وكوسة'])} مناسبة لهالفصل"},
            {"role":"user","content":"احتاج تربة خاصة؟"},
            {"role":"assistant","content":f"تربة زراعية + سماد عضوي من {vp(pick([10000,15000,20000]))} دينار"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"صنبور المطبخ يقطر ماي، يغلي علينا فاتورة الماء"},
            {"role":"assistant","content":"يمكن الباكيه خربان، سهل يتغير"},
            {"role":"user","content":"أقدر أغيره لحالي؟"},
            {"role":"assistant","content":"إي، لو تعرف. غير الباكيه بالجزء الداخلي للصنبور"},
            {"role":"user","content":"لو ما أعرف؟"},
            {"role":"assistant","content":f"سباك يسويها بـ{vp(pick([10000,15000,20000]))} دينار، سريع"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"عندنا طفرة بالنمل بـ{hw_word}، شسوي؟"},
            {"role":"assistant","content":"النمل من رطوبة أو ماكو نظافة. وين يظهر؟"},
            {"role":"user","content":f"بـ{room} وبالمطبخ"},
            {"role":"assistant","content":f"خلي الأكل بعلب مغلقة وسدد الشقوق. استخدم مبيد خاص للنمل"},
            {"role":"user","content":"المبيد آمن للأطفال؟"},
            {"role":"assistant","content":"اشتر مبيد آمن من الصيدلية، والأهم تهوية البيت بعد الرش"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"أريد أعمّر غرفة إضافية على السطح"},
            {"role":"assistant","content":"بناء على السطح يحتاج ترخيص من البلدية"},
            {"role":"user","content":"ضروري؟"},
            {"role":"assistant","content":"إي، بدون ترخيص ممكن يجون ويهدمون"},
            {"role":"user","content":"كم يكلف الترخيص؟"},
            {"role":"assistant","content":f"ترخيص البناء من {vp(pick([100000,200000,300000]))} حسب المساحة"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":f"الجيران بنوا حائط عالي يقطع الهواء عن {hw_word}"},
            {"role":"assistant","content":"هذا مشكلة، كلمتهم؟"},
            {"role":"user","content":"كلمتهم وقالوا حقهم"},
            {"role":"assistant","content":"قد يكونون صح لو البناء داخل أرضهم"},
            {"role":"user","content":"شسوي؟"},
            {"role":"assistant","content":"مهندس يقيس الحدود، وإذا تجاوز البلدية تتدخل"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":f"أريد أسوي {pick(['برنامج تلفزيون ذكي','إنترنت سريع','نظام صوت'])} بـ{hw_word}"},
            {"role":"assistant","content":"فكرة ممتازة! شنو الميزانية؟"},
            {"role":"user","content":f"بين {vp(pick([200000,300000]))} وـ{vp(pick([500000,700000]))} دينار"},
            {"role":"assistant","content":f"بهالميزانية تقدر تسوي {pick(['تلفزيون ذكي','راوتر فايبر','نظام صوت محيطي'])} ممتاز"},
            {"role":"user","content":"من ينصبه؟"},
            {"role":"assistant","content":f"{_technician} يجي ينصب ويوضح الاستخدام"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"أريد أسوي إفطار عائلي يوم الجمعة، شنو أطبخ؟"},
            {"role":"assistant","content":"إفطار الجمعة يحتاج يكون خاص. كم شخص؟"},
            {"role":"user","content":f"{pick(['10','15','20'])} شخص"},
            {"role":"assistant","content":f"{_food} مع {_food2} وسلطة، أكل عراقي أصيل"},
            {"role":"user","content":"كل شي من البيت؟"},
            {"role":"assistant","content":f"إي، الأحسن أكل البيت. تحتاج {pick(['ساعتين','3 ساعات'])} تحضير"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":f"أريد أشتري بيت، شنو الخطوات؟"},
            {"role":"assistant","content":"أول تحدد الميزانية والمنطقة اللي تريد"},
            {"role":"user","content":f"ميزانيتي {vp(pick([100000000,150000000,200000000]))} دينار"},
            {"role":"assistant","content":"بهالميزانية تلقى بيت جيد. تدور عبر دلالين أو أونلاين"},
            {"role":"user","content":"في فحص قانوني؟"},
            {"role":"assistant","content":"لازم تفحص الصك وتتأكد من السجل العقاري قبل الشراء"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"الحمام يحتاج تجديد كامل، من متى ما جددناه"},
            {"role":"assistant","content":"تجديد الحمام مكلف شوي، شنو يحتاج؟"},
            {"role":"user","content":f"{pick(['تبليط جديد','تغيير المغسلة','تغيير كل شي'])}"},
            {"role":"assistant","content":f"تجديد الحمام {pick(['كامل','جزئي'])} من {vp(pick([300000,500000,750000]))} دينار"},
            {"role":"user","content":"يستغرق كم يوم؟"},
            {"role":"assistant","content":f"بين {pick(['3','5','7'])} أيام حسب حجم التجديد"},
        ]
    elif tpl == 41:
        msgs = [
            {"role":"user","content":f"أريد أزين {room} لعيد الميلاد بكره"},
            {"role":"assistant","content":f"زينة عيد ميلاد بـ{room}! شو ألوان تفضل؟"},
            {"role":"user","content":f"{pick(['ذهبي وبيج','أحمر وأبيض','بنفسجي وذهبي','أزرق وفضي'])}"},
            {"role":"assistant","content":f"بالوان {pick(['ذهبي وبيج','أحمر وأبيض','بنفسجي وذهبي'])} تطلع رائعة"},
            {"role":"user","content":"وين أشتري الزينة؟"},
            {"role":"assistant","content":f"محلات الزينة بـ{pick(['الشورجة','سوق السراي','المجمع'])} زينة وبأسعار مناسبة"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"عندنا صراصير بالمطبخ، كيف نخلص منها؟"},
            {"role":"assistant","content":"الصراصير مزعجة! الأكل مكشوف؟"},
            {"role":"user","content":"إي، صعب نغلق كلشي"},
            {"role":"assistant","content":f"علب مغلقة للأكل، وضع مصايد أو مبيد حشري"},
            {"role":"user","content":"في شركة إبادة ترخص؟"},
            {"role":"assistant","content":f"إي، شركة إبادة حشرات تجي وتطهر المطبخ بـ{vp(pick([50000,75000,100000]))} دينار"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"أريد أسوي حجرة إضافية لـ{nm1} لما يكبر"},
            {"role":"assistant","content":f"مبادرة زينة، عمر {nm1} كم؟"},
            {"role":"user","content":f"{_child_age}"},
            {"role":"assistant","content":f"وقت مناسب تجهز لـ{nm1}. تحتاج مقاولين وتصريح"},
            {"role":"user","content":"كم يكلف تقريباً؟"},
            {"role":"assistant","content":f"غرفة جديدة بناء ودهن من {vp(pick([500000,750000,1000000]))} دينار"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"التلفزيون كبر بالشاشة بس ما يوضح صورة"},
            {"role":"assistant","content":"التلفزيون عمره كم؟"},
            {"role":"user","content":f"{pick(['سنتين','3 سنين','5 سنين','7 سنين'])}"},
            {"role":"assistant","content":f"يمكن بورد الصورة أو اللوحة الداخلية. {_technician} يفحصه"},
            {"role":"user","content":"أصلح ولا أشتري جديد؟"},
            {"role":"assistant","content":f"لو الإصلاح فوق {vp(pick([100000,150000]))}, أشتري جديد أفضل"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"أريد أنظف {hw_word} نظافة عميقة للعيد"},
            {"role":"assistant","content":"نظافة عيد! كم غرفة عندك؟"},
            {"role":"user","content":f"{pick(['3 غرف','4 غرف','5 غرف'])}"},
            {"role":"assistant","content":f"تحتاج يوم كامل للنظافة العميقة، أو شركة نظافة متخصصة"},
            {"role":"user","content":"شركة النظافة كم تكلف؟"},
            {"role":"assistant","content":f"نظافة عميقة لـ{pick(['3','4','5'])} غرف من {vp(pick([50000,75000,100000]))} دينار"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"المطبخ ضيق كلش، أريد أوسعه"},
            {"role":"assistant","content":"توسيع المطبخ يعني هدم حائط؟"},
            {"role":"user","content":"إي، في حائط يمكن يتزال"},
            {"role":"assistant","content":"لازم مهندس يشوف إذا الحائط حامل لا"},
            {"role":"user","content":"كم يكلف المهندس؟"},
            {"role":"assistant","content":f"مهندس إنشائي للكشف من {vp(pick([30000,50000,75000]))} دينار"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"الماطور شغال بس الماي ما يطلع بـ{room2}"},
            {"role":"assistant","content":f"الماي يطلع بغرف ثانية؟"},
            {"role":"user","content":"إي، بس مو بـ{room2}"},
            {"role":"assistant","content":f"يمكن انسداد بمواسير {room2} تحديداً. سباك يفحص"},
            {"role":"user","content":"يستغرق إصلاحه وقت؟"},
            {"role":"assistant","content":f"إذا انسداد بسيط، {pick(['ساعة','ساعتين','يوم'])} يكفي"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"أريد أسوي وليمة للعيلة، كم شخص تقدر تسع {room}؟"},
            {"role":"assistant","content":f"{room} كبيرة ولا صغيرة؟"},
            {"role":"user","content":f"{pick(['4×6','5×7','3×5'])} متر"},
            {"role":"assistant","content":f"بهالمساحة تسع {pick(['15','20','25'])} شخص مريحين"},
            {"role":"user","content":"وين نحط الأكل؟"},
            {"role":"assistant","content":"طاولة طويلة بالوسط أو تفرش بالأرض على الطريقة العراقية الأصيلة"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"المصعد ببنايتنا خربان من أسبوع"},
            {"role":"assistant","content":"في كم طابق؟"},
            {"role":"user","content":f"الطابق {pick(['الثالث','الرابع','الخامس','السادس'])}"},
            {"role":"assistant","content":"يعني تصعد درج كل مرة! هذا تعب"},
            {"role":"user","content":"من المسؤول؟"},
            {"role":"assistant","content":"ارفع شكوى لإدارة البناية، هم مسؤولين عن صيانة المصعد"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"والله {hw_word} محتاج صيانة شاملة"},
            {"role":"assistant","content":"من متى ما سويت صيانة؟"},
            {"role":"user","content":f"من {pick(['سنتين','3 سنين','4 سنين'])} تقريباً"},
            {"role":"assistant","content":f"وقت معقول. ابدأ بـ{_fix_type} أول لأنه الأهم"},
            {"role":"user","content":"وبعدين؟"},
            {"role":"assistant","content":f"الصباغة والتبليط، وبعدين تفصيل حسب الميزانية"},
        ]

    return {"id": f"fam_{i:04d}", "category": "family_home", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 18 - RELIGIOUS & OCCASIONS
# ============================================================
MONTHS_OCC = ["رمضان","العيد الكبير","العيد الصغير","الأربعين","محرم","ذكرى الوفاة"]
WEDDING_Q  = ["الصالة","الطعام","الزفة","الميكاپ","الدزدار","التصوير"]

def gen_occasions(i):
    occ  = pick(MONTHS_OCC)
    occ2 = pick(MONTHS_OCC)
    wq   = pick(WEDDING_Q)
    nm   = pick(ALL_NAMES)
    nm2  = pick(ALL_NAMES)
    rw_w = pick(RELIGION) if RELIGION else "إن شاء الله"
    _gr  = pick(GREET)
    _hall_price  = pick([2000000,2500000,3000000,3500000,4000000,5000000])
    _catering    = pick([12000,15000,18000,20000,25000])
    _dj_price    = pick([400000,500000,600000,750000,1000000])
    _photo_price = pick([500000,600000,750000,1000000])
    _makeup_price= pick([150000,200000,250000,300000])
    _gift_price  = pick([30000,50000,75000,100000,150000])
    _child_name  = pick(MALE)
    _child_age   = pick(["3 سنين","5 سنين","7 سنين","10 سنين"])
    _eid_money   = pick([5000,10000,15000,20000,25000,50000])
    _mourner_nm  = pick(ALL_NAMES)
    _sermon_topic= pick(["الصبر","الشكر","الأخلاق","الصدق","بر الوالدين","حسن الجوار"])
    _iftar_food  = pick(["مرق وأرز","تشريب وچورخ","پاچة","قيمة وقيمر","مسقوف","كباب ومتبگ"])
    _suhoor_food = pick(["بيض وجبن","فول وسمن","خبز ولبن","عجة","باقلاء"])
    _dua_topic   = pick(["الرزق","الصحة","الزواج","النجاح","الأبناء","الستر"])
    _ziyara_city = pick(["كربلاء","النجف","سامراء","الكاظمية"])
    _walk_days   = pick(["3 أيام","يومين","4 أيام"])
    _start_place = pick(["باب المعظم","الكاظمية","النهضة","الشعلة"])
    _wedding_day = pick(["الخميس","الجمعة","السبت","الأحد"])
    _wedding_nm  = pick(MALE)
    _wedding_girl= pick(FEMALE)
    _quran_part  = pick(["جزء","ربع القرآن","نصف القرآن","جزءين"])
    _charity_amt = pick([10000,20000,50000,100000,200000])
    _occasion_prep = pick(["شراء الهدايا","تجهيز الملابس","طبخ الحلويات","ترتيب البيت","دعوة الأهل"])
    tpl  = random.randint(1, 50)

    if tpl == 1:
        _ramadan_prep2 = pick(["ملء المؤن","شراء التمر والسمن","تهيئة غرفة الإفطار","تجهيز مائدة الإفطار","دعوة الجيران"])
        _iftar_time    = pick(["الساعة 7","الساعة 6:30","بعد الأذان مباشرة","الساعة 7:15"])
        msgs = [
            {"role":"user","content":f"رمضان كريم {nm}، كيف الاستعداد عندكم؟"},
            {"role":"assistant","content":f"رمضان كريم {nm2}! جاهزين، {_ramadan_prep2} و{_occasion_prep} من أمس"},
            {"role":"user","content":f"شنو تفطرون عادةً وأي ساعة؟"},
            {"role":"assistant","content":f"{_iftar_time} نفطر. الأول تمر وشاي، وبعدين {_iftar_food}"},
            {"role":"user","content":f"مثلنا تماماً! التمر {_iftar_time} أول شي"},
            {"role":"assistant","content":f"سنة النبي صلى الله عليه وسلم. {_iftar_food} أكل رمضان الأصيل"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"عيد مبارك {nm}، كل عام وأنتم بخير"},
            {"role":"assistant","content":f"وأنتم بألف خير {nm2}، الله يديم عليكم النعمة والصحة"},
            {"role":"user","content":"وين تروحون العيد هالسنة؟"},
            {"role":"assistant","content":f"نزور الأهل أول، بعدين نطلع نزهة لـ{pick(['الحديقة','الكورنيش','المول','أهل الريف'])}"},
            {"role":"user","content":"عيدية الأولاد جاهزة؟"},
            {"role":"assistant","content":f"إي والله، {vp(_eid_money)} لكل واحد. الأولاد فرحانين من أمس"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"عندنا زيارة الأربعين، تجي معنا لـ{_ziyara_city}؟"},
            {"role":"assistant","content":f"إن شاء الله، متى تنطلقون؟"},
            {"role":"user","content":f"الأسبوع الجاي، ماشياً من {_start_place}"},
            {"role":"assistant","content":f"ماشياً؟ كم يوم الطريق لـ{_ziyara_city}؟"},
            {"role":"user","content":f"تقريباً {_walk_days} مشي"},
            {"role":"assistant","content":f"إن شاء الله أجي معكم، الزيارة ماشياً لـ{_ziyara_city} ثواب عظيم"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"أريد أحجز صالة عرس لـ{pick(['200','250','300','400'])} شخص"},
            {"role":"assistant","content":f"صالة {pick(['200','250','300'])} شخص متاحة. الليلة {vp(_hall_price)} دينار"},
            {"role":"user","content":"يشمل الأكل؟"},
            {"role":"assistant","content":f"لا، الأكل منفصل. كيترنگ بوفيه بـ{vp(_catering)} للشخص"},
            {"role":"user","content":"والدزدار والمصور؟"},
            {"role":"assistant","content":f"دزدار بـ{vp(_dj_price)} دينار، تصوير بـ{vp(_photo_price)} دينار"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"توفي والد {_mourner_nm}، عزاء عندهم باچر"},
            {"role":"assistant","content":f"إنا لله وإنا إليه راجعون، الله يرحمه. متى التوفي؟"},
            {"role":"user","content":"البارحة، العزاء بيتهم"},
            {"role":"assistant","content":f"البقية بحياتكم يا {nm}. وين بيتهم؟"},
            {"role":"user","content":f"بـ{pick(['الكاظمية','الكرادة','المنصور','الأعظمية'])}"},
            {"role":"assistant","content":f"إن شاء الله أجي العزاء، الله يصبر {_mourner_nm} وأهله"},
        ]
    elif tpl == 6:
        _lailat_night = pick(["ليلة القدر","الليلة السابعة والعشرين","الليلة التاسعة والعشرين","ليلة نزول القرآن"])
        _quran_finish = pick(["جزء","جزءين","3 أجزاء","ربع القرآن","نصف القرآن"])
        _special_dua  = pick(["الرزق والرزق الحلال","شفاء أمي","زواج أخوي","نجاح ولدي","السلامة والستر"])
        msgs = [
            {"role":"user","content":f"اليوم {_lailat_night}، شنو تسوي؟"},
            {"role":"assistant","content":f"أحيي {_lailat_night} بالصلاة والدعاء وأطلب {_dua_topic} إن شاء الله"},
            {"role":"user","content":f"وأنا أريد أختم {_quran_finish} الليلة وأدعو بـ{_special_dua}"},
            {"role":"assistant","content":f"الله يتقبل. ختم {_quran_finish} بـ{_lailat_night} شي عظيم الأجر"},
            {"role":"user","content":f"إن شاء الله يستجاب دعاء {_special_dua}"},
            {"role":"assistant","content":f"آمين يا رب. {_lailat_night} دعواتها مستجابة بإذن الله"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"ابني {_wedding_nm} يتزوج {_wedding_day} الجاي، شنو نجهز بعد؟"},
            {"role":"assistant","content":f"ألف مبارك على {_wedding_nm}! الصالة والدزدار جهزتوا؟"},
            {"role":"user","content":"الصالة حجزناها والدزدار، باقي الميكاپ والمصور"},
            {"role":"assistant","content":f"ميكاپ العروس من {vp(_makeup_price)} دينار. المصور الجيد بـ{vp(_photo_price)}"},
            {"role":"user","content":"الدزدار غالي هالأيام"},
            {"role":"assistant","content":f"إي، الدزدار الجيد من {vp(_dj_price)} دينار. كفو على {_wedding_nm}"},
        ]
    elif tpl == 8:
        _mosque_nm   = pick(["جامع المحلة","جامع الإمام علي","جامع الصديق","جامع الكبير","مسجد الحارة"])
        msgs = [
            {"role":"user","content":f"جمعة مباركة {nm}، الله يقبل منا ومنكم"},
            {"role":"assistant","content":f"جمعة مباركة {nm2}، الله يبارك فيك ويقبل طاعتك"},
            {"role":"user","content":f"روحت {_mosque_nm}؟"},
            {"role":"assistant","content":f"إي، صليت الجمعة بـ{_mosque_nm} وسمعت خطبة ممتازة عن {_sermon_topic}"},
            {"role":"user","content":f"موضوع {_sermon_topic} مهم كلش هالأيام"},
            {"role":"assistant","content":f"إي والله، خطيب {_mosque_nm} يختار مواضيع تلمس القلب. الله يجازيه"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"عندنا ختانة {_child_name} الغداة، تعال تفرح معنا"},
            {"role":"assistant","content":f"ألف مبارك! {_child_name} يعيش ويكبر بصحة وعافية"},
            {"role":"user","content":f"الغداة الساعة {pick(['2','3','4'])} العصر"},
            {"role":"assistant","content":"إن شاء الله أجي وأجيب هدية للعريس الصغير"},
            {"role":"user","content":"ما تحتاج، وجودك يكفي"},
            {"role":"assistant","content":f"لا، لازم أجيب شي لـ{_child_name}، العيال تفرح بالهدايا"},
        ]
    elif tpl == 10:
        _community_iftar_place = pick(["بالجامع","بالحسينية","بساحة الحارة","بمجلس المختار"])
        _community_num  = pick(["50","80","100","150","200"])
        _volunteer_role = pick(["الطبخ والتوزيع","التنظيم والاستقبال","تجهيز المائدة","شراء المواد"])
        msgs = [
            {"role":"user","content":f"رمضان جاي، شنو تسوون للإفطار الجماعي {_community_iftar_place}؟"},
            {"role":"assistant","content":f"نسوي إفطار جماعي {_community_iftar_place}، {_iftar_food} وحلويات"},
            {"role":"user","content":"كم شخص تقريباً؟"},
            {"role":"assistant","content":f"متوقعين {_community_num} شخص من الحارة والأصحاب {_community_iftar_place}"},
            {"role":"user","content":"أساعد بالتنظيم؟"},
            {"role":"assistant","content":f"أبشر! نحتاج متطوعين لـ{_volunteer_role}. الله يبارك فيك"},
        ]
    elif tpl == 11:
        _baby_name   = pick(["محمد","علي","حسين","أحمد","عمر","إبراهيم","يوسف","زيد"])
        _baby_weight = pick(["3 كيلو","3.2 كيلو","3.5 كيلو","4 كيلو","2.8 كيلو"])
        _aqeeqa_type = pick(["ذبيحتين لأن ولد","خروف كامل","ذبيحة وتوزيع"])
        msgs = [
            {"role":"user","content":f"عندنا مولود جديد، {nm} ولدها ولد اليوم وزنه {_baby_weight}"},
            {"role":"assistant","content":f"ألف ألف مبارك! {_baby_weight} وزن ممتاز. الله يخلي المولود ويبارك فيه"},
            {"role":"user","content":f"سميناه {_baby_name}"},
            {"role":"assistant","content":f"اسم {_baby_name} طيب ومبارك! متى العقيقة؟"},
            {"role":"user","content":f"بعد أسبوع، {_aqeeqa_type}"},
            {"role":"assistant","content":f"إن شاء الله، {_aqeeqa_type} مبارك. الله يبارك في {_baby_name}"},
        ]
    elif tpl == 12:
        _eid_sweet   = pick(["كليجة","بقلاوة","معمول","كنافة","عيش الحلوم","قطايف"])
        _kids_count  = pick(["3","4","5","6"])
        _cloth_store = pick(["سوق البزازين","مول الكرادة","محلات المنصور","السوق المركزي"])
        msgs = [
            {"role":"user","content":f"شنو تجهزون للعيد هالسنة؟"},
            {"role":"assistant","content":f"من أمس نسوي {_occasion_prep} ونطبخ {_eid_sweet}"},
            {"role":"user","content":"الملابس اشتريتم؟"},
            {"role":"assistant","content":f"إي، من {_cloth_store}. الـ{_kids_count} أولاد كلهم بملابس جديدة"},
            {"role":"user","content":"إن شاء الله عيد مبارك وبركة"},
            {"role":"assistant","content":f"وعليكم إن شاء الله. {_eid_sweet} بالبيت تنادي وكل شي جاهز"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"أريد أعزم الأهل على إفطار رمضان، الأحسن بالبيت ولا بمطعم؟"},
            {"role":"assistant","content":"البيت أحسن للخصوصية، المطعم أريح لو كثار"},
            {"role":"user","content":f"نحن {pick(['10','15','20'])} شخص"},
            {"role":"assistant","content":f"لـ{pick(['10','15','20'])} شخص، البيت ممكن. طبخ {_iftar_food} يكفي؟"},
            {"role":"user","content":"وسوي حلويات بعد؟"},
            {"role":"assistant","content":f"قيمر وعسل وبقلاوة، إفطار كامل للضيوف"},
        ]
    elif tpl == 14:
        _special_night = pick(["ليلة النصف من شعبان","ليلة القدر","ليلة الجمعة الأخيرة من رمضان","أول ليلة من رجب"])
        _ibada = pick(["الصلاة والذكر","التلاوة والدعاء","الاستغفار والتوبة","قيام الليل وصلاة التهجد"])
        _dua2 = pick(["الرزق الحلال","شفاء المرضى","هداية الأولاد","الزواج الميسر","قضاء الديون"])
        msgs = [
            {"role":"user","content":f"{_special_night} اليوم، شنو خاص فيها؟"},
            {"role":"assistant","content":f"{_special_night} فيها فضل كبير، يقولون ترفع فيها الأعمال وتُقبل التوبة"},
            {"role":"user","content":f"شنو أفضل {_ibada} فيها؟"},
            {"role":"assistant","content":f"{_ibada} من أفضل الأعمال في {_special_night}"},
            {"role":"user","content":f"إن شاء الله يستجاب دعاء {_dua2}"},
            {"role":"assistant","content":f"آمين يا رب، الله يقبل دعواتنا ويرزقنا {_dua2}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"ابنتي {nm2} خطبت اليوم، الله يبارك"},
            {"role":"assistant","content":f"ألف مبارك على {nm2}! الله يكملها بالخير"},
            {"role":"user","content":f"الشاب من عيلة {pick(['محترمة','طيبة','أصيلة','معروفة'])}"},
            {"role":"assistant","content":f"الله يوفقهم ويجمعهم على الخير. متى العرس؟"},
            {"role":"user","content":"بعد ستة أشهر إن شاء الله"},
            {"role":"assistant","content":"إن شاء الله يكمل بالخير ويكون عرس مبارك"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أريد أسوي صدقة بمناسبة {occ}، أيش تنصح؟"},
            {"role":"assistant","content":f"صدقة بمناسبة {occ} زينة! تقدر توزع أكل على المحتاجين"},
            {"role":"user","content":f"الميزانية {vp(_charity_amt)} دينار"},
            {"role":"assistant","content":f"بـ{vp(_charity_amt)} تقدر توزع وجبات إفطار أو حقائب مواد"},
            {"role":"user","content":"وين أوزع؟"},
            {"role":"assistant","content":f"دور الأيتام أو الجمعيات الخيرية في {pick(['الكاظمية','الكرادة','الأعظمية'])}"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"عندنا نجاح {nm} بالبكلوريوس، نسوي احتفال؟"},
            {"role":"assistant","content":f"أبشر على {nm}! نجاح الجامعة يستاهل احتفال"},
            {"role":"user","content":"مطعم ولا بالبيت؟"},
            {"role":"assistant","content":f"مطعم للعيلة والأصحاب أريح. أو بالبيت لو تريد خصوصية"},
            {"role":"user","content":"الهدية شنو تنصح؟"},
            {"role":"assistant","content":f"ساعة أو لابتوب أو {vp(_gift_price)} دينار نقد لـ{nm}"},
        ]
    elif tpl == 18:
        _muharram_place = pick(["الحسينية","الجامع","بيتنا","الديوان","ساحة الحارة"])
        _muharram_food  = pick(["هريسة","عصيدة","تمن أحمر","شاي وقهوة للزائرين","وجبات للفقراء"])
        _muharram_night = pick(["ليلة عاشوراء","ليلة التاسع","ليلة السابع","كل ليالي العشر"])
        msgs = [
            {"role":"user","content":f"محرم يجي، شنو استعداداتكم بـ{_muharram_place}؟"},
            {"role":"assistant","content":f"نستعد بـ{_muharram_place} للمجالس والزيارات. نسوي {_muharram_food} للناس"},
            {"role":"user","content":f"مجالس عزاء عندكم أي ليلة؟"},
            {"role":"assistant","content":f"إي، خصوصاً {_muharram_night} فيه مجلس كبير بـ{_muharram_place}"},
            {"role":"user","content":"إن شاء الله يكون شهر بركة وذكرى"},
            {"role":"assistant","content":f"إن شاء الله، ذكرى الحسين تجمع الناس على الخير بـ{_muharram_place}"},
        ]
    elif tpl == 19:
        _sahoor_wake   = pick(["قبل الأذان بساعة","قبل الفجر بساعتين","على الساعة 3 الفجر","على الساعة 3:30"])
        _sahoor_extra  = pick(["وتمر وماي","ونبق","وفاكهة","وقيمر"])
        _sahoor_person = pick(["أمي","زوجتي","أم علي","أم أحمد","أم حسين"])
        msgs = [
            {"role":"user","content":f"السحور شنو تاكلون هالرمضان؟"},
            {"role":"assistant","content":f"السحور عندنا {_suhoor_food} {_sahoor_extra} وچاي بزيادة"},
            {"role":"user","content":"وين تصحون للسحور؟"},
            {"role":"assistant","content":f"{_sahoor_person} تصحينا {_sahoor_wake}"},
            {"role":"user","content":"عندنا كمان، النساء اللي تصحي الكل"},
            {"role":"assistant","content":f"هههه، الأمهات قوة! {_sahoor_person} تعبانة علينا. الله يحفظها"},
        ]
    elif tpl == 20:
        _grave_area  = pick(["الكاظمية","النجف","الغزالية","الأعظمية","الشعب"])
        _grave_offer = pick(["فاتحة وزهور","قراءة سورة يس","ختمة قرآن","زهور وماء للزرع"])
        _grave_freq  = pick(["كل جمعة","بكل مناسبة","مرة بالشهر","بالمواسم الدينية"])
        msgs = [
            {"role":"user","content":f"أريد أزور قبر أبوي بمناسبة {occ}، وين المقبرة؟"},
            {"role":"assistant","content":f"مقبرة وين؟ أي منطقة؟"},
            {"role":"user","content":f"مقبرة {_grave_area}"},
            {"role":"assistant","content":f"مقبرة {_grave_area} معروفة. تاخذ {_grave_offer} لروحه"},
            {"role":"user","content":f"نزورهم {_grave_freq}. الله يرحمه ويوسع مضجعه"},
            {"role":"assistant","content":f"آمين يا رب، الله يرحم {_mourner_nm} وكل أمواتنا. زيارة {_grave_freq} طيبة"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"أريد أشتري هدية للعرس، شتنصح لـ{nm}؟"},
            {"role":"assistant","content":f"للعروس؟ شنو ميزانيتك؟"},
            {"role":"user","content":f"بين {vp(_gift_price)} وـ{vp(_gift_price * 2)} دينار"},
            {"role":"assistant","content":f"بهالميزانية تشتري {pick(['طقم مطبخ','عطر فاخر','إكسسوار','قطعة ذهب صغيرة'])} للعروس"},
            {"role":"user","content":"وين أشتري؟"},
            {"role":"assistant","content":f"محلات {pick(['الكرادة','المنصور','زيتون'])} فيه خيارات زينة للهدايا"},
        ]
    elif tpl == 22:
        _ram_season  = pick(["صيفي كلش","ربيعي","شتوي نوعاً","خريفي"])
        _ram_hours   = pick(["16 ساعة","14 ساعة","12 ساعة","15 ساعة","13 ساعة"])
        _ram_challenge = pick(["العطش بالحر","طول ساعات الصيام","العمل بالصيام","حر الصيف وقت الأذان"])
        msgs = [
            {"role":"user","content":"رمضان هالسنة صيفي ولا شتوي؟"},
            {"role":"assistant","content":f"هالسنة رمضان {_ram_season}، يعني الصيام حوالي {_ram_hours} يومياً"},
            {"role":"user","content":f"الصيام {_ram_hours} صعب، خصوصاً {_ram_challenge}"},
            {"role":"assistant","content":f"صح، {_ram_challenge} تعب. بس ثواب رمضان {_ram_season} أكثر"},
            {"role":"user","content":"إن شاء الله يمر بسلامة"},
            {"role":"assistant","content":f"آمين، رمضان {_ram_season} كريم على الجميع"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"أريد أسوي عقيقة على المولود، شنو المطلوب؟"},
            {"role":"assistant","content":"العقيقة سنة مستحبة. ذبيحتين للولد وواحدة للبنت"},
            {"role":"user","content":"الذبيحة بيش هالأيام؟"},
            {"role":"assistant","content":f"خروف العقيقة من {vp(pick([300000,400000,500000]))} دينار"},
            {"role":"user","content":"نوزع على الجيران والفقراء؟"},
            {"role":"assistant","content":"إي، التوزيع على المحتاجين أفضل وأكثر بركة"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"صاحبي {nm} اليوم عيد ميلاده، أجيبله هدية شنو؟"},
            {"role":"assistant","content":f"عيد ميلاد {nm}! كم عمره هالسنة؟"},
            {"role":"user","content":f"{pick(['25','30','35','40'])} سنة"},
            {"role":"assistant","content":f"بعمر {pick(['25','30','35','40'])} تنصحه بـ{pick(['ساعة','كتاب خاص','رحلة','تجربة جديدة'])}"},
            {"role":"user","content":"الميزانية محدودة"},
            {"role":"assistant","content":f"عشاء مع الأصحاب وهدية بسيطة من {vp(_gift_price)} دينار كافي"},
        ]
    elif tpl == 25:
        _iftar_place2  = pick(["الجامع","الحسينية","ساحة الحارة","بيت المختار","نادي المنطقة"])
        _iftar_guests  = pick(["100","150","200","250","300"])
        _iftar_day     = pick(["الجمعة","السبت","الأحد","ليلة القدر","العشرة الأواخر"])
        msgs = [
            {"role":"user","content":f"عندنا إفطار جماعي بـ{_iftar_place2} يوم {_iftar_day}، تجي؟"},
            {"role":"assistant","content":f"إي والله أجي! إفطار {_iftar_place2} يوم {_iftar_day} روح ومحبة"},
            {"role":"user","content":f"الساعة {pick(['6','7'])} المغرب. متوقعين {_iftar_guests} شخص"},
            {"role":"assistant","content":f"إن شاء الله أكون هناك. {_iftar_guests} شخص؟ منظمين كلش"},
            {"role":"user","content":"إي، الجامع جاهز. بس الحضور يكفي"},
            {"role":"assistant","content":f"ماشي، إن شاء الله أجي مع العيلة لـ{_iftar_place2}"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"عندنا تخرج {nm} من الجامعة، نسوي احتفال؟"},
            {"role":"assistant","content":f"ألف مبارك على تخرج {nm}! لازم تحتفلون"},
            {"role":"user","content":"مطعم ولا بالبيت؟"},
            {"role":"assistant","content":f"تخرج {nm} يستاهل مطعم جيد. الكل يرتاح وما أكو ضغط طبخ"},
            {"role":"user","content":"ميزانيتي محدودة"},
            {"role":"assistant","content":f"مطعم عادي بـ{vp(pick([100000,150000,200000]))} للعيلة. أو بالبيت أوفر"},
        ]
    elif tpl == 27:
        _ashura_food   = pick(["هريسة","عصيدة","تمن أحمر","حساء العدس","كبة"])
        _ashura_place2 = pick(["الحسينية","الجامع","بيت العيلة","ساحة الحارة","بيت كبير العيلة"])
        _ashura_dist   = pick(["الجيران","الفقراء","المحتاجين","العابرين","أيتام الحارة"])
        msgs = [
            {"role":"user","content":f"يوم عاشوراء كيف تقضونه؟"},
            {"role":"assistant","content":f"عاشوراء نروح {_ashura_place2} ونقرأ الفاتحة على أرواح الشهداء"},
            {"role":"user","content":"أكلات خاصة فيه؟"},
            {"role":"assistant","content":f"عندنا تقليد نسوي {_ashura_food} كصدقة عن روح الحسين"},
            {"role":"user","content":f"نوزع على {_ashura_dist}؟"},
            {"role":"assistant","content":f"إي، توزيع {_ashura_food} على {_ashura_dist} من العادات العريقة عندنا"},
        ]
    elif tpl == 28:
        _father_nm  = pick(["أبو علي","الحاج محمد","أبو حسين","الحاج إبراهيم","أبو صالح"])
        _forty_loc  = pick(["بيتنا","بيت العيلة","الحسينية","الجامع المحلي"])
        _forty_night= pick(["ليلة الأربعين","ليلة العشرة","ليلة التاسع والعشرين"])
        msgs = [
            {"role":"user","content":f"عندنا ذكرى أربعين {_father_nm} {pick(['هالأسبوع','باچر','الجمعة'])}"},
            {"role":"assistant","content":f"الله يرحم {_father_nm} ويوسع مضجعه. مجلس عزاء بـ{_forty_loc}؟"},
            {"role":"user","content":f"إي، {_forty_night} بـ{_forty_loc}، تعال"},
            {"role":"assistant","content":f"إن شاء الله أجي وأكون معكم بـ{_forty_loc}. ذكرى {_father_nm} مهمة"},
            {"role":"user","content":"الله يجازيك يا أخوي"},
            {"role":"assistant","content":f"الله يرحم {_father_nm} ويجعل قبره روضة من رياض الجنة"},
        ]
    elif tpl == 29:
        _khatma_num  = pick(["5","7","10","15","20"])
        _khatma_food = pick(["چاي وكعك","قهوة وحلويات","عشاء خفيف","إفطار رمضان","أكل عراقي"])
        _khatma_dua  = pick(["على روح المتوفي","للمناسبة","لأهل البيت","لخير المسلمين"])
        msgs = [
            {"role":"user","content":f"أريد أسوي ختمة قرآن بمناسبة {occ}، شنو تنصح؟"},
            {"role":"assistant","content":f"ختمة قرآن بـ{occ} مبارك! بالبيت ولا بالجامع؟"},
            {"role":"user","content":f"بالبيت، مع الأهل والجيران، نكون {_khatma_num} أشخاص"},
            {"role":"assistant","content":f"نقسم القرآن بين {_khatma_num} أشخاص، كل واحد {_quran_part}. بعدها {_khatma_food}"},
            {"role":"user","content":f"والدعاء {_khatma_dua}"},
            {"role":"assistant","content":f"الله يتقبل ختمتنا والدعاء {_khatma_dua}. الختمة الجماعية بركة"},
        ]
    elif tpl == 30:
        _ziyara_hour   = pick(["4 الفجر","5 الصبح","6 الصبح","7 الصبح"])
        _ziyara_stay   = pick(["يوم وليلة","يومين","3 أيام","يوم واحد"])
        _ziyara_ritual = pick(["الزيارة والصلاة","الطواف حول الضريح","قراءة زيارة عاشوراء","الدعاء عند الضريح"])
        msgs = [
            {"role":"user","content":f"عندي زيارة {_ziyara_city} الأسبوع الجاي بمناسبة المحرم، هل الطريق آمن؟"},
            {"role":"assistant","content":f"الطريق لـ{_ziyara_city} هالأيام آمن إن شاء الله، روح بقلب مطمئن"},
            {"role":"user","content":f"بالسيارة كم ساعة لـ{_ziyara_city}؟"},
            {"role":"assistant","content":f"لـ{_ziyara_city} من بغداد {pick(['ساعتين','3 ساعات','ساعة ونص'])} بالسيارة بدون زحمة"},
            {"role":"user","content":f"نروح الساعة {_ziyara_hour}؟"},
            {"role":"assistant","content":f"الساعة {_ziyara_hour} ممتاز، الزحمة تصير بعد الضحى. تمكثون {_ziyara_stay}؟"},
        ]
    elif tpl == 31:
        _comp_type  = pick(["مسابقة قرآن","مسابقة حفظ القرآن","مسابقة تجويد","مسابقة تفسير"])
        _comp_prize = pick(["50000","75000","100000","150000","200000"])
        _kid_name   = pick(MALE)
        _age_range  = pick(["7 لـ12 سنة","10 لـ15 سنة","7 لـ15 سنة","8 لـ14 سنة"])
        msgs = [
            {"role":"user","content":f"اليوم {_comp_type} بالجامع، سمعت؟"},
            {"role":"assistant","content":f"إي سمعت! {_comp_type} للأطفال ولا للكبار؟"},
            {"role":"user","content":f"للأطفال من {_age_range}. الجائزة {vp(int(_comp_prize))} دينار"},
            {"role":"assistant","content":f"ماشاءالله! {_comp_type} بجائزة {vp(int(_comp_prize))} يحفز الأولاد"},
            {"role":"user","content":f"ابني {_kid_name} يشارك"},
            {"role":"assistant","content":f"الله يوفق {_kid_name} ويبارك فيه. تشجيعك له أهم شي من الجائزة"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"عندنا إعلان خطوبة {nm} الليلة، تعال فرحنا"},
            {"role":"assistant","content":f"ألف مبارك مسبقاً! من هو الشاب؟"},
            {"role":"user","content":f"شاب {pick(['محترم','كفو','طيب','عراقي'])} من عيلة زينة"},
            {"role":"assistant","content":f"الله يكمل على خير لـ{nm}. إن شاء الله أجي الليلة"},
            {"role":"user","content":"العزومة بالبيت الساعة 7"},
            {"role":"assistant","content":"إن شاء الله أكون هناك. مبروك مسبقاً"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"أريد أحجز طباخ للعرس، كم أكو؟"},
            {"role":"assistant","content":"طباخ العرس يعتمد على عدد الضيوف. كم شخص؟"},
            {"role":"user","content":f"{pick(['200','300','400','500'])} شخص"},
            {"role":"assistant","content":f"طباخ متخصص بأعراس بـ{vp(pick([300000,400000,500000]))} دينار + البضاعة"},
            {"role":"user","content":"يطبخ أيش؟"},
            {"role":"assistant","content":f"عادةً {pick(['تمن وقيمة ودجاج','تمن ولحم ومرق','بوفيه عراقي كامل'])} للأعراس"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"عندنا لمة رجال ليلة الجمعة بمناسبة {occ}"},
            {"role":"assistant","content":f"لمة رجال؟ زين! كم شخص تقريباً؟"},
            {"role":"user","content":f"{pick(['10','15','20'])} شخص من الأهل والأصحاب"},
            {"role":"assistant","content":"شنو تجهزون؟"},
            {"role":"user","content":f"چاي وقهوة وأكل. أريد أطبخ {_iftar_food}"},
            {"role":"assistant","content":f"{_iftar_food} للرجال ممتاز! لمة زينة"},
        ]
    elif tpl == 35:
        _bday_age    = pick(["20","25","30","35","40","50"])
        _surprise_venue = pick(["بيتنا","مطعم","كافيه","الحديقة","نادي"])
        _bday_theme  = pick(["ألوان ذهبية","أزرق وأبيض","أحمر وأسود","كرتوني","هادي وبسيط"])
        msgs = [
            {"role":"user","content":f"أريد أهنئ {nm} بعيد ميلاده الـ{_bday_age} بطريقة مميزة"},
            {"role":"assistant","content":f"طريقة مميزة لعيد ميلاد {_bday_age}؟ مفاجأة؟"},
            {"role":"user","content":f"إي، مفاجأة بـ{_surprise_venue}"},
            {"role":"assistant","content":f"فكرة رائعة! نظم حفلة بـ{_surprise_venue} بثيم {_bday_theme}"},
            {"role":"user","content":"كيف أنظم؟"},
            {"role":"assistant","content":f"اتصل بأصحاب {nm} سراً، حدد {_surprise_venue}، واجيبوا كيك وزينة {_bday_theme}"},
        ]
    elif tpl == 36:
        _eid_tradition = pick(["نلبس ملابس جديدة","نزور الأهل أول شي","نطبخ الهريسة","نتجمع بيت كبير العيلة","نوزع العيديات"])
        _adha_animal   = pick(["خروف","عجل","ناقة مشتركة","ذبيحتين"])
        _ftr_special   = pick(["الكليجة","القيمر والعسل","الكنافة","العيش الحلوم","بقلاوة العيد"])
        msgs = [
            {"role":"user","content":"شنو فرق عيد الفطر والأضحى عند العراقيين بالاحتفال؟"},
            {"role":"assistant","content":f"عيد الفطر نحتفل بـ{_eid_tradition} وأكل {_ftr_special}"},
            {"role":"user","content":"والأضحى؟"},
            {"role":"assistant","content":f"الأضحى نذبح {_adha_animal} ونوزع على الفقراء والجيران"},
            {"role":"user","content":"أيهما أكثر فرح عندكم؟"},
            {"role":"assistant","content":f"عيد الفطر أكثر فرح بسبب {_ftr_special} والملابس الجديدة. بس الأضحى أكثر بركة"},
        ]
    elif tpl == 37:
        _abroad_country = pick(["السويد","ألمانيا","كندا","الإمارات","تركيا","مصر","هولندا"])
        _abroad_who     = pick(["أخوي","أختي","ابن عمي","ولدي","بنتي","أبوي"])
        _abroad_yrs     = pick(["سنتين","3 سنين","5 سنين","7 سنين","10 سنين"])
        msgs = [
            {"role":"user","content":f"أريد أرسل تهنئة {occ} لـ{_abroad_who} بـ{_abroad_country}"},
            {"role":"assistant","content":f"واتساب ولا مكالمة فيديو أحسن لـ{_abroad_who} بـ{_abroad_country}؟"},
            {"role":"user","content":"مكالمة فيديو أحسن، نشوف بعض"},
            {"role":"assistant","content":f"صح، الوجه بالوجه يحس بـ{occ} أكثر. {_abroad_who} من كم سنة برة؟"},
            {"role":"user","content":f"من {_abroad_yrs} بـ{_abroad_country}"},
            {"role":"assistant","content":f"إن شاء الله يرجع {_abroad_who} قريب من {_abroad_country}. الغربة تعب"},
        ]
    elif tpl == 38:
        _lost_when  = pick(["برمضان الماضي","قبل العيد بشهر","الصيف الماضي","السنة الماضية"])
        _lost_who   = pick(["أبوي","أمي","أخوي الكبير","جدتي","عمي العزيز"])
        _grieve_act = pick(["نقرأ الفاتحة على روحه","نزور قبره","نسوي صدقة باسمه","نعزم الأهل لختمة"])
        msgs = [
            {"role":"user","content":f"{_lost_who} توفي {_lost_when}، هالعيد الأول بدونه صعب"},
            {"role":"assistant","content":f"الله يرحم {_lost_who}. أول عيد بعد فقد {_lost_who} صعب كلش"},
            {"role":"user","content":"الحزن كبير، بس الحياة تكمل"},
            {"role":"assistant","content":f"طبيعي. {_lost_who} يحب يشوفكم بخير وفرح حتى في حزنكم"},
            {"role":"user","content":f"صح، نحاول نفرح ونـ{_grieve_act}"},
            {"role":"assistant","content":f"الله يرحم {_lost_who} ويبارك في أيامكم. {_grieve_act} طيب"},
        ]
    elif tpl == 39:
        _mahr_amount = pick([500000,750000,1000000,1500000,2000000,3000000])
        _contract_loc= pick(["بيت العروس","المأذونية","الجامع","المحكمة"])
        _attendees   = pick(["أهل العروس والعريس","العيلة فقط","الأهل والأصحاب المقربين"])
        msgs = [
            {"role":"user","content":f"عندنا عقد قران {nm} بـ{_contract_loc} باچر، شنو لازم يكون جاهز؟"},
            {"role":"assistant","content":f"عقد قران {nm} بـ{_contract_loc}! المأذون محدد؟"},
            {"role":"user","content":"إي، المأذون جاي. الصداق حددنا"},
            {"role":"assistant","content":f"تحتاج شاهدين مسلمين، والصداق {vp(_mahr_amount)} دينار صح؟"},
            {"role":"user","content":f"إي. الحضور {_attendees}"},
            {"role":"assistant","content":f"كامل. الله يبارك لـ{nm} ويكمل بالخير. {_contract_loc} جاهز؟"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"أريد أسوي ختانة ابني {_child_name} بمستشفى ولا بالبيت؟"},
            {"role":"assistant","content":"مستشفى أأمن وأسهل من البيت للختانة"},
            {"role":"user","content":"كم تكلف بالمستشفى؟"},
            {"role":"assistant","content":f"ختانة بالمستشفى من {vp(pick([50000,75000,100000]))} دينار"},
            {"role":"user","content":"وما في مشاكل؟"},
            {"role":"assistant","content":"بالمستشفى تحت إشراف طبي، أأمن بكثير من البيت"},
        ]
    elif tpl == 41:
        _dates_type  = pick(["تمر المضافة","تمر الزاهدي","تمر برحي","تمر دقلة نور","تمر البصراوي"])
        _dates_price = pick([10000,15000,20000,25000,30000])
        _provisions  = pick(["سمن وأرز","زيت وطحين","مواد التمن","توابل وسكر","بضاعة رمضان كاملة"])
        msgs = [
            {"role":"user","content":"رمضان جاي بعد أسبوعين، شنو استعداداتكم؟"},
            {"role":"assistant","content":f"من الأسبوع هذا نشتري {_dates_type} و{_provisions}"},
            {"role":"user","content":f"الأسعار غالية هالسنة؟ {_dates_type} بكم؟"},
            {"role":"assistant","content":f"{_dates_type} {vp(_dates_price)} للكيلو هالسنة، {pick(['غلا','ثبت','ارتفع شوي'])}"},
            {"role":"user","content":"إن شاء الله يكون رمضان بركة وخير"},
            {"role":"assistant","content":f"آمين، رمضان كريم على الجميع. {_dates_type} تمر البيوت العراقية"},
        ]
    elif tpl == 42:
        _charity_org = pick(["الهلال الأحمر","جمعية إحسان","أيادي الخير","جمعية الأمل","مبادرة خير"])
        _charity_type= pick(["ملابس أطفال","ملابس رجالية ونسائية","أدوات مدرسية","طعام ومواد","حقائب العيد"])
        _charity_area= pick(["الكاظمية","الصدر","الشعب","دار الأيتام","المخيمات"])
        msgs = [
            {"role":"user","content":f"أريد أتبرع بـ{_charity_type} للمحتاجين قبل {occ}، وين؟"},
            {"role":"assistant","content":f"تبرع بـ{_charity_type} بمناسبة {occ}؟ ماشاءالله! فيه جمعيات موثوقة"},
            {"role":"user","content":"أي جمعية تنصح؟"},
            {"role":"assistant","content":f"{_charity_org} موثوقة وتوزع {_charity_type} بـ{_charity_area}"},
            {"role":"user","content":"كيف أوصل التبرع؟"},
            {"role":"assistant","content":f"اتصل بـ{_charity_org} يجون يستلمون {_charity_type} من بيتك"},
        ]
    elif tpl == 43:
        _mawlid_act  = pick(["نقيم مجلس صلاة على النبي","نوزع الحلوى والتمر","نسوي قصيدة مدح","نقيم سهرة دينية"])
        _mawlid_loc  = pick(["بالجامع","بالحسينية","بالديوان","ببيتنا","بالساحة"])
        _mawlid_time = pick(["الليلة","باچر","يوم الجمعة","هذا المساء"])
        msgs = [
            {"role":"user","content":f"اليوم مناسبة المولد النبوي الشريف، شنو تسوون؟"},
            {"role":"assistant","content":f"نحتفل بـ{_mawlid_act} {_mawlid_loc}"},
            {"role":"user","content":f"عندكم تجمع {_mawlid_time}؟"},
            {"role":"assistant","content":f"إي، {_mawlid_time} بـ{_mawlid_loc} {_mawlid_act}. أهلاً بيكم"},
            {"role":"user","content":"إن شاء الله نروح"},
            {"role":"assistant","content":f"اللهم صلّ على محمد. {_mawlid_loc} يفتح الساعة {pick(['7','8','9'])} المسا"},
        ]
    elif tpl == 44:
        _sweet1 = pick(["كليجة","عيش الحلوم","بقلاوة","معمول","كنافة"])
        _sweet2 = pick(["قطايف","حلاوة الجبن","لقيمات","زنگولة","أم علي"])
        _sweet_ingr = pick(["دقيق وسمن وهيل وسكر","دقيق وتمر وسمن","جبن وقشطة","سميد وسكر وسمن"])
        _sweet_helper = pick(["أمي","زوجتي","أختي","جارتنا أم حسين"])
        msgs = [
            {"role":"user","content":f"شنو تجهزون من حلويات للعيد؟"},
            {"role":"assistant","content":f"كل سنة نسوي {_sweet1} و{_sweet2} بالبيت. {_sweet_helper} تساعدنا"},
            {"role":"user","content":f"وصفة {_sweet1} عندك؟"},
            {"role":"assistant","content":f"وصفة {_sweet_helper}: {_sweet_ingr}. أرسلها واتساب إن شاء الله"},
            {"role":"user","content":f"شكراً، نسوي {_sweet1} مثلكم"},
            {"role":"assistant","content":f"عيد حلو! {_sweet1} و{_sweet2} بحلويات البيت تكمل الفرحة"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"أريد أحجز فوتوغرافر للعرس، كم أسعارهم؟"},
            {"role":"assistant","content":f"تصوير العرس من {vp(_photo_price)} دينار حسب الخبرة"},
            {"role":"user","content":"يشمل الفيديو؟"},
            {"role":"assistant","content":f"الفوتوغرافر الجيد يشمل صور وفيديو بـ{vp(_photo_price + 200000)} دينار"},
            {"role":"user","content":"كيف أختار الجيد؟"},
            {"role":"assistant","content":"شوف أعماله السابقة على إنستغرام وخذ توصيات من الأصحاب"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"عندنا سبوع المولود باچر، شنو يجيبون الضيوف عادةً؟"},
            {"role":"assistant","content":"السبوع تقليد عراقي جميل! الضيوف يجيبون هدايا للمولود"},
            {"role":"user","content":"ملابس ولا فلوس؟"},
            {"role":"assistant","content":"الاثنين مقبول. ملابس للمولود أو هدية الفلوس للأم"},
            {"role":"user","content":"شنو أجيب للأم بعد؟"},
            {"role":"assistant","content":f"عطر أو حلوى أو هدية بـ{vp(_gift_price)} دينار للأم يكفي"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"عشاء {occ} عندنا كبير، نطبخ كام نوع أكل؟"},
            {"role":"assistant","content":f"عشاء {occ}؟ كم ضيف عندك؟"},
            {"role":"user","content":f"{pick(['30','50','70'])} شخص"},
            {"role":"assistant","content":f"نوعين رئيسيين يكفون: {_iftar_food} والمقبلات"},
            {"role":"user","content":"الحلويات بعد؟"},
            {"role":"assistant","content":f"حلويات {pick(['بيت الحلوى','مطعم حلويات','من البيت'])} تكمل العشاء"},
        ]
    elif tpl == 48:
        _visit_city  = pick(["الناصرية","الديوانية","بابل","كربلاء","البصرة","الموصل","كركوك"])
        _visit_stay  = pick(["يومين","3 أيام","أسبوع","يوم وليلة"])
        _visit_gift  = pick(["هدايا للأولاد","حلويات وتمر","أكل وحلو عراقي","ملابس للكبار والصغار"])
        msgs = [
            {"role":"user","content":f"أريد أزور أهلي بـ{_visit_city} بمناسبة {occ2}، بس السفر بعيد"},
            {"role":"assistant","content":f"زيارة الأهل بـ{occ2} واجب. {_visit_city} بعيدة، تروح بالسيارة؟"},
            {"role":"user","content":f"إي، بالسيارة. نمكث {_visit_stay} هناك"},
            {"role":"assistant","content":f"{_visit_stay} بـ{_visit_city} وقت زين مع الأهل. شتاخذون معكم؟"},
            {"role":"user","content":f"نأخذ {_visit_gift} وهدايا للأطفال"},
            {"role":"assistant","content":f"ماشاءالله، {_visit_gift} أحسن هدية. الله يجمعكم {_visit_stay} بخير"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أبشر، {nm} ولدته أمه اليوم"},
            {"role":"assistant","content":f"ألف ألف مبارك! بنت ولا ولد؟"},
            {"role":"user","content":f"{pick(['ولد','بنت'])}، أول واحد لهم"},
            {"role":"assistant","content":"ماشاءالله! الله يبارك في المولود ويجعله قرة عين"},
            {"role":"user","content":"اسمه شنو؟"},
            {"role":"assistant","content":"إن ما سموه بعد، الاسم أهم قرار. الله يلهمهم الأحسن"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"اليوم ذكرى {occ}، الجو مختلف"},
            {"role":"assistant","content":f"إي والله، {occ} دايماً يجيب روح خاصة"},
            {"role":"user","content":"شنو تحس بهالمناسبة؟"},
            {"role":"assistant","content":f"أحس بفرح وتواصل مع الأهل والأصحاب. {rw_w}"},
            {"role":"user","content":"إن شاء الله كلها خير وبركة"},
            {"role":"assistant","content":"آمين يا رب، الله يديم الخير والمحبة علينا"},
        ]

    return {"id": f"occ_{i:04d}", "category": "religious_occasions", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 19 - NEIGHBORHOOD & COMMUNITY
# ============================================================
NEIGHBOR_ISSUES = ["زحمة السيارات","الكهرباء","الماء","النظافة","الكلاب الضالة",
                   "بناء جديد بالشارع","تسليك المجاري","الإنارة بالليل"]
LOCAL_PLACES    = ["الجامع","البقالة","الحلاق","الصيدلية","المدرسة","الپاركنگ"]

def gen_neighborhood(i):
    issue  = pick(NEIGHBOR_ISSUES)
    issue2 = pick(NEIGHBOR_ISSUES)
    place  = pick(LOCAL_PLACES)
    area   = pick(AREAS)
    nm     = pick(MALE)
    nm2    = pick(FEMALE)
    _gr    = pick(GREET)
    _nbr_origin = pick(["الكاظمية","الأعظمية","الكرادة","المنصور","الشعلة","الصدر"])
    _elec_hours  = pick(["4 ساعات","6 ساعات","8 ساعات","ساعتين","3 ساعات"])
    _elec_sched  = pick(["ساعة وساعة","ساعتين وساعتين","3 و3","4 و2"])
    _gen_fuel    = pick(["بنزين","ديزل","غاز"])
    _gen_price   = pick([50000,60000,75000,80000,100000])
    _water_days  = pick(["يوم بيوم","كل يومين","مرتين بالأسبوع","كل ثلاثة أيام"])
    _water_tank  = pick([5000,6000,7000,8000,10000])
    _road_prob   = pick(["حفر كبيرة","مطبات بدون لون","أسفلت مكسور","تصريف مياه مسدود","طريق ضيق"])
    _road_since  = pick(["من شهر","من 3 أشهر","من نص سنة","من سنة","من سنتين"])
    _build_floor = pick(["طابق ثاني","طابق ثالث","إضافة غرف","توسعة المطبخ"])
    _build_noise = pick(["الغبار","الصوت","الاهتزاز","الأوساخ","الضوضاء"])
    _dog_time    = pick(["الليل","الفجر","بعد منتصف الليل","آخر الليل"])
    _dog_count   = pick(["3","4","5","6","7"])
    _shop_type   = pick(["بقالة","صيدلية","حلاق","مكوجي","ورشة تصليح موبايلات","مخبز"])
    _shop_owner  = pick(["أبو حسن","الحاج صالح","أبو طارق","أبو رياض","الحاج محمد"])
    _light_since = pick(["من أسبوع","من أسبوعين","من 10 أيام","من 3 أيام"])
    _light_risk  = pick(["حوادث سيارات","سرقة","خوف الأولاد","لا يكدرون ينزلون"])
    _mukhtar_nm  = pick(["أبو جاسم","أبو علي","الحاج عبدالله","أبو كريم","الشيخ حمزة"])
    _petition_num= pick(["10","15","20","25","30"])
    _park_prob   = pick(["السيارات تسد المدخل","ما أكو پاركنگ كافي","يپاركون على الرصيف","يحجزون الشارع"])
    _park_owner  = pick(["الجار الجديد","سيارات الزوار","موظفي المحل القريب","أصحاب الشركة التحت"])
    _garbage_day = pick(["يوم وبكره","ثلاث مرات بالأسبوع","كل يوم بالصبح","مرتين بالأسبوع"])
    _garbage_comp= pick(["البلدية","شركة النظافة الأهلية","متطوعي الحارة","خدمة الحي"])
    _sewer_since = pick(["من أمس","من يومين","من أسبوع","من 3 أيام"])
    _sewer_smell = pick(["الرائحة وصلت للبيوت","الأطفال ما يقدرون ينزلون","الشارع فيضان","الحشرات كثرت"])
    _new_fam_from= pick(["بغداد","ديالى","بابل","كربلاء","الناصرية","البصرة"])
    _new_fam_size= pick(["3 أشخاص","4 أشخاص","عيلة كبيرة","زوجين وأطفال"])
    _mosque_time = pick(["الفجر","الظهر","العصر","المغرب","العشاء"])
    _mosque_issue= pick(["الصوت عالي كلش","مكبر الصوت خربان","الباب مغلق أحياناً","ما أكو وضوء"])
    _park_garden = pick(["حديقة الشارع","الساحة القديمة","الفضاء الفارغ","أرض الحارة الفاضية"])
    _park_cost   = pick([500000,750000,1000000,1500000])
    _internet_co = pick(["نت كاك","شركة فايبر","نت المنطقة","شبكة الحي"])
    _internet_spd= pick(["10 ميگا","20 ميگا","50 ميگا","100 ميگا"])
    _internet_pr = pick([25000,30000,35000,40000,50000])
    _stray_action= pick(["البلدية تجمعهم","جمعية حماية الحيوان","نروح المجلس البلدي","نرفع شكوى رسمية"])
    _council_loc = pick(["قرب الجامع الكبير","شارع المدرسة","ساحة الحارة","مبنى البلدية الفرعي"])
    _wall_state  = pick(["مائل ويخوف","متصدع من الزلزال","قديم من 20 سنة","خطر على المارة"])
    _wall_owner  = pick(["الجار أبو سعد","الدار المهجورة","البيت الفارغ من سنين","ورثة البيت القديم"])
    _security_pr = pick(["سرقة بالمنطقة","سيارات مجهولة تتوقف","شباب مجهولون بالليل","حوادث متكررة"])
    _security_sol= pick(["كاميرات مراقبة","بوابة على الحارة","نقطة شرطة","حارس ليلي للحارة"])
    _festival_occ= pick(["عيد الأضحى","عيد الفطر","ذكرى عاشوراء","رمضان","مناسبة وطنية"])
    _festival_act= pick(["لمة جيران وعشاء","توزيع حلويات للأطفال","إضاءة وزينة","مباراة كرة بالشارع"])
    _rent_old    = pick([200000,250000,300000,350000,400000])
    _rent_new    = pick([450000,500000,600000,700000,800000])
    _rent_reason = pick(["ارتفاع الأسعار العام","تحسين المنطقة","مالك جديد","ضغط السوق"])
    tpl = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{_gr} أبو {nm}، الكهرباء من الصبح مقطوعة"},
            {"role":"assistant","content":f"إي والله، حتى عندنا. الجدول {_elec_sched} هالأيام"},
            {"role":"user","content":"اتصلت بالشبكة، قالوا عطل بالمحول"},
            {"role":"assistant","content":f"عطل المحول يستغرق {pick(['ساعات','يوم كامل','ساعتين'])}. المولد شغال عندك؟"},
            {"role":"user","content":f"المولد يشتغل {_elec_hours} بس، وقوده {_gen_fuel} غالي"},
            {"role":"assistant","content":f"إي، {_gen_fuel} وصل {vp(_gen_price)} للكنة. الله يصبرنا"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"من اشتروا البيت الجديد بالحارة يا {nm}؟"},
            {"role":"assistant","content":f"عائلة من {_nbr_origin}، ناس زينين ما شاء الله"},
            {"role":"user","content":f"شوفتهم؟ كم نفر؟"},
            {"role":"assistant","content":f"إي رحبت فيهم. {_new_fam_size}، أهل طيبين كلش"},
            {"role":"user","content":"لازم نزورهم ونرحب بيهم بالحارة"},
            {"role":"assistant","content":f"باچر نروح معاً، نجيب حلو ونرحب. الجار من {_nbr_origin} عادةً أهل"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"الشارع فيه {_road_prob} من {_road_since}، كلش ما يصير"},
            {"role":"assistant","content":f"إي والله، {_road_prob} من {_road_since} وما أحد طالع"},
            {"role":"user","content":"المختار اتصل بالبلدية؟"},
            {"role":"assistant","content":f"{_mukhtar_nm} اتصل مرتين، قالوا خلال أسبوع يجون"},
            {"role":"user","content":"إن شاء الله يجون ويصلحون"},
            {"role":"assistant","content":f"من {_road_since} وهم يوعدون. لازم نرفع شكوى رسمية"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"أريد أفتح {_shop_type} ببداية الشارع، ينفع يا {nm}؟"},
            {"role":"assistant","content":f"{_shop_type} بالحارة؟ فكرة ممتازة، المنطقة تحتاج"},
            {"role":"user","content":"ما أكو منافسة قريبة؟"},
            {"role":"assistant","content":f"أقرب {_shop_type} بـ{pick(['10 دقايق','ربع ساعة','5 دقايق'])} مشي. السوق حر"},
            {"role":"user","content":f"صاحب {_shop_type} بالشارع الثاني كيف عنده؟"},
            {"role":"assistant","content":f"{_shop_owner} شغله زين لأنه نظيف ومحترم. أنت كمان تكدر"},
        ]
    elif tpl == 5:
        _build_since  = pick(["من أسبوع","من شهر","من أسبوعين","من 3 أيام"])
        _build_time   = pick(["الصبح الباكر","الليل","كل الوقت","أوقات الراحة"])
        msgs = [
            {"role":"user","content":f"جارنا يبني {_build_floor} من {_build_since} و{_build_noise} يدخل بيتنا {_build_time}"},
            {"role":"assistant","content":f"{_build_noise} بـ{_build_time} من {_build_since}؟ مؤذي. كلمته بأدب؟"},
            {"role":"user","content":f"كلمته مرتين وما اهتم، {_build_floor} كبيرة"},
            {"role":"assistant","content":f"روح البلدية، {_build_floor} بدون ترخيص ممكن يوقفونه فوراً"},
            {"role":"user","content":"يقول عنده ترخيص بالبناء"},
            {"role":"assistant","content":f"حتى مع الترخيص، {_build_noise} بـ{_build_time} يخالف. راجع البلدية"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"الكلاب بالشارع بـ{_dog_time} تخوف الأولاد، صار {_dog_count} كلاب"},
            {"role":"assistant","content":f"إي، من أسبوعين صارت أكثر. {_dog_count} كلاب كثير بالحارة"},
            {"role":"user","content":"من يتصل بالبلدية؟"},
            {"role":"assistant","content":f"أنا أتصل باچر الصبح، {_stray_action} الحل الأفضل"},
            {"role":"user","content":"شكراً يا حجي، الأولاد خايفين بـ{_dog_time}"},
            {"role":"assistant","content":f"ولا يهمك. {_dog_count} كلاب بالحارة خطر. نتصل بـ{_stray_action} سوية"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"{_shop_type} الجديد بالحارة، جربته يا {nm}؟"},
            {"role":"assistant","content":f"إي، {_shop_owner} صاحبه محترم وأسعاره معقولة"},
            {"role":"user","content":"شنو يبيع تحديداً؟"},
            {"role":"assistant","content":f"متخصص بـ{_shop_type}، نظيف ومرتب. أحسن من اللي قبله"},
            {"role":"user","content":"أروح أشوف أسعاره"},
            {"role":"assistant","content":f"اروح بكير قبل ما يزدحم. {_shop_owner} يفتح الساعة {pick(['8','9','7'])} الصبح"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"الإنارة بالشارع مطفية من {_light_since}"},
            {"role":"assistant","content":f"إي، من {_light_since} خطر بالليل. {_light_risk}"},
            {"role":"user","content":"الأولاد ما يكدرون ينزلون بالمسا"},
            {"role":"assistant","content":f"روح مجلس الحي، {_council_loc}، هم المسؤولين"},
            {"role":"user","content":"أروح وحدي؟"},
            {"role":"assistant","content":f"نروح {_petition_num} جار سوية، أقوى تأثير. أنا معك"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"الماي بالحارة يجي {_water_days}، ما يكفي للبيت"},
            {"role":"assistant","content":f"إي، {_water_days} ضعيف. التنك بيش عندك؟"},
            {"role":"user","content":f"التنك {vp(_water_tank)} دينار وما يكفي أسبوع"},
            {"role":"assistant","content":f"غالي وقليل. الفلتر الكبير يوفر. رفعتم طلب للبلدية؟"},
            {"role":"user","content":"رفعنا من شهر ومجاوبين"},
            {"role":"assistant","content":f"اجمع {_petition_num} توقيع من الجيران وارفع شكوى رسمية للبلدية"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"{_park_prob}، ما أكدر أوصل لبيتي بالسيارة"},
            {"role":"assistant","content":f"مشكلة {_park_prob} زادت هالأيام. من سببها؟"},
            {"role":"user","content":f"{_park_owner}"},
            {"role":"assistant","content":f"كلم {_mukhtar_nm} المختار، هو يتكلم مع {_park_owner}"},
            {"role":"user","content":"وإذا ما اهتم؟"},
            {"role":"assistant","content":f"صور الوضع وارسل للبلدية مع شكوى رسمية. حقك مكفول"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"النفايات بالحارة تتراكم، ما يجون {_garbage_comp}"},
            {"role":"assistant","content":f"{_garbage_comp} المفروض يجون {_garbage_day}. متأخرين؟"},
            {"role":"user","content":f"من {pick(['أسبوع','10 أيام','أسبوعين'])} وما جاء أحد"},
            {"role":"assistant","content":f"اتصل بـ{_garbage_comp} مباشرة وبلغ مع {_mukhtar_nm}"},
            {"role":"user","content":"رقم البلدية عندك؟"},
            {"role":"assistant","content":f"مكتوب على لوحة المجلس بـ{_council_loc}. أو أعطيك إياه"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"المجاري بالشارع طافحة من {_sewer_since}، {_sewer_smell}"},
            {"role":"assistant","content":f"مجاري طافحة من {_sewer_since}؟ هذا خطر صحي"},
            {"role":"user","content":"البلدية ما ترد على اتصالاتنا"},
            {"role":"assistant","content":f"روح {_council_loc} شخصياً، وصور الوضع كدليل"},
            {"role":"user","content":"ونروح متى؟"},
            {"role":"assistant","content":f"باچر الصبح بكير. {_petition_num} جار يرفعون شكوى واحدة أقوى"},
        ]
    elif tpl == 13:
        _welcome_gift = pick(["حلو وبقلاوة","تمر وقهوة","أكل بيتي","كيكة بيت","فاكهة وعصير"])
        _new_fam_house= pick(["بيت أبو سامر القديم","الدار الفاضية","البيت اللي تباع من سنة","دار أبو طلال"])
        msgs = [
            {"role":"user","content":f"عيلة جديدة سكنت {_new_fam_house} من {_new_fam_from}، {_new_fam_size}"},
            {"role":"assistant","content":f"من {_new_fam_from} سكنوا {_new_fam_house}؟ شوفتهم؟"},
            {"role":"user","content":f"إي، {_new_fam_size}، ناس هادين ومحترمين"},
            {"role":"assistant","content":f"ماشاءالله! أهل {_new_fam_from} طيبين. ننزل نرحب فيهم؟"},
            {"role":"user","content":f"بكره نروح ونأخذ لهم {_welcome_gift}"},
            {"role":"assistant","content":f"فكرة زينة! {_welcome_gift} ترحيب أصيل للجيران الجدد من {_new_fam_from}"},
        ]
    elif tpl == 14:
        _mosque_nm2   = pick(["جامع الحارة","جامع المحلة","الجامع الكبير","مسجد الحي","جامع الأئمة"])
        _mosque_since = pick(["من أسبوع","من أسبوعين","من شهر","من فترة"])
        msgs = [
            {"role":"user","content":f"{_mosque_nm2} عنده مشكلة بـ{_mosque_issue} من {_mosque_since}"},
            {"role":"assistant","content":f"{_mosque_issue} بـ{_mosque_nm2} من {_mosque_since}؟ يأثر على الصلاة؟"},
            {"role":"user","content":f"إي، صلاة {_mosque_time} تأثرت بسبب {_mosque_issue}"},
            {"role":"assistant","content":f"كلم لجنة {_mosque_nm2}، هم المسؤولين عن {_mosque_issue}"},
            {"role":"user","content":"وين أجيهم؟"},
            {"role":"assistant","content":f"بعد صلاة {_mosque_time} بـ{_mosque_nm2}، أو كلم الإمام مباشرة"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"نريد نسوي {_park_garden} لأطفال الحارة، الفكرة تنجح؟"},
            {"role":"assistant","content":f"فكرة ممتازة! {_park_garden} يفيد عيال الحارة كلها"},
            {"role":"user","content":f"التكلفة تقريباً {vp(_park_cost)} دينار"},
            {"role":"assistant","content":f"بـ{vp(_park_cost)} تجيب ألعاب ونباتات. لو تجمعتم الجيران يصير"},
            {"role":"user","content":"كيف نجمع التبرعات؟"},
            {"role":"assistant","content":f"كل بيت {vp(_park_cost // 20)} دينار، {_petition_num} بيت تكفي. نكلم {_mukhtar_nm}"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"إنترنت الحارة {_internet_co} ضعيف كلش"},
            {"role":"assistant","content":f"إنترنت {_internet_co} بطيء؟ كم ميگا عندك؟"},
            {"role":"user","content":f"ادفع على {_internet_spd} بس ما يوصل"},
            {"role":"assistant","content":f"مشكلة عامة أو عندك بس؟ كلم {_internet_co} مباشرة"},
            {"role":"user","content":"كل الحارة تشكي"},
            {"role":"assistant","content":f"فيه شركة ثانية بالمنطقة بـ{vp(_internet_pr)} للشهر. جرب تحول"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"الجار من فوق صوته {_build_noise} كلش بالليل"},
            {"role":"assistant","content":f"صوت {_build_noise} بالليل مزعج. كلمته؟"},
            {"role":"user","content":"خجلت أكلمه"},
            {"role":"assistant","content":f"الكلام بأدب حق. قل له بـ{_dog_time} صوت {_build_noise} يوصل"},
            {"role":"user","content":"وإذا ما اهتم؟"},
            {"role":"assistant","content":f"بلغ {_mukhtar_nm} المختار، هو يتوسط. حقك بالراحة"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"الجدار بين بيتنا وبيت {_wall_owner} {_wall_state}"},
            {"role":"assistant","content":f"جدار {_wall_state} خطير. {_wall_owner} موجود؟"},
            {"role":"user","content":"البيت فارغ من فترة"},
            {"role":"assistant","content":f"البلدية تقدر تلزم {_wall_owner} بإصلاحه لو خطر على الجيران"},
            {"role":"user","content":"كيف نبلغ؟"},
            {"role":"assistant","content":f"صور الجدار وروح {_council_loc} مع الصور. يجون يكشفون"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"بالحارة {_security_pr}، خايفين على بيوتنا"},
            {"role":"assistant","content":f"{_security_pr} تعب. من متى صار هذا؟"},
            {"role":"user","content":f"من {pick(['أسبوع','أسبوعين','شهر'])}، أهل الحارة مضطربين"},
            {"role":"assistant","content":f"أحسن حل {_security_sol} للحارة. كلمتوا {_mukhtar_nm}؟"},
            {"role":"user","content":"بكره نجتمع عنده"},
            {"role":"assistant","content":f"زين، اقترح {_security_sol} بالاجتماع. الأمان أولوية"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"نريد نسوي {_festival_act} بمناسبة {_festival_occ}، الحارة تتفق؟"},
            {"role":"assistant","content":f"فكرة رائعة! {_festival_act} بـ{_festival_occ} يجمع الجيران"},
            {"role":"user","content":"كيف ننظم؟"},
            {"role":"assistant","content":f"نكلم {_mukhtar_nm} ونحدد مكان. الجيران يتبرعون بـ{_festival_act}"},
            {"role":"user","content":"الأطفال رح يفرحون"},
            {"role":"assistant","content":f"إي والله، {_festival_act} بـ{_festival_occ} ذكرى ما تنسى للعيال"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"صاحب البيت رفع الإيجار من {vp(_rent_old)} لـ{vp(_rent_new)}"},
            {"role":"assistant","content":f"ارتفاع من {vp(_rent_old)} لـ{vp(_rent_new)} كبير. سبب المالك؟"},
            {"role":"user","content":f"قال {_rent_reason}"},
            {"role":"assistant","content":f"{_rent_reason} حجة، بس الزيادة هذي كبيرة. كلمه يتحمل"},
            {"role":"user","content":"ما نفع، يقول هذا السوق"},
            {"role":"assistant","content":f"روح مكتب عقارات ثاني وشوف. {vp(_rent_new)} ممكن تلاقي أحسن"},
        ]
    elif tpl == 22:
        _privacy_act = pick(["يطلون من فوق","يسمعون كلامنا","يصورون بالتراس","يتفحصون من الشباك"])
        _privacy_sol = pick(["شبك أو ستائر فوق الجدار","حاجز خشبي","شجر كثيف يحجب","لوح ألمنيوم"])
        msgs = [
            {"role":"user","content":f"أبو {nm}، الجيران الجدد من {_nbr_origin} ما يحترمون الخصوصية"},
            {"role":"assistant","content":"شنو يسوون تحديداً؟"},
            {"role":"user","content":f"{_privacy_act} بشكل متكرر"},
            {"role":"assistant","content":f"كلمهم بأدب أولاً. ربما ما يدرون بـ{_privacy_act}"},
            {"role":"user","content":"جربت مرتين وما نفع"},
            {"role":"assistant","content":f"اعمل {_privacy_sol}. حقك بالخصوصية مكفول"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"الشارع بعد المطر فيه مياه راكدة من {pick(['أمس','يومين','3 أيام'])}"},
            {"role":"assistant","content":"تصريف الماي مشكلة قديمة بالحارة"},
            {"role":"user","content":"الأطفال ما يكدرون يروحون المدرسة"},
            {"role":"assistant","content":f"صور الوضع وارسل لـ{_mukhtar_nm} والبلدية فوراً"},
            {"role":"user","content":"البلدية تستجيب؟"},
            {"role":"assistant","content":f"لو أرسلت صور بالواتساب لـ{_council_loc} عادةً يجون خلال يوم"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"نريد ننظف {_park_garden} سوية يوم الجمعة، تشارك؟"},
            {"role":"assistant","content":f"تنظيف {_park_garden} سوية فكرة رائعة، أكيد أشارك"},
            {"role":"user","content":"نجمع كم شخص؟"},
            {"role":"assistant","content":f"لو جمعنا {_petition_num} شخص من الجيران يكفي ويزيد"},
            {"role":"user","content":"أنا أكلم جيران الشمال وأنت الجنوب؟"},
            {"role":"assistant","content":f"تمام، نتقابل {_park_garden} الجمعة الساعة {pick(['8','9','7'])} الصبح"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"الطريق الضيق بالحارة، كيف تحل هالمشكلة؟"},
            {"role":"assistant","content":f"الطريق الضيق مشكلة مزمنة. سببه {_park_prob}؟"},
            {"role":"user","content":f"إي، {_park_prob} يضيق أكثر"},
            {"role":"assistant","content":f"لازم نرسم أماكن وقوف ونضع لوحات. نكلم {_mukhtar_nm}"},
            {"role":"user","content":"البلدية تدعم؟"},
            {"role":"assistant","content":f"إذا رفعنا طلب رسمي من {_petition_num} جار، البلدية تتصرف"},
        ]
    elif tpl == 26:
        _new_mukhtar  = pick(["أبو سعد","ابن الحاج حمزة","أبو زيد","الشاب كريم","أبو لؤي"])
        _mukhtar_age  = pick(["30","32","35","28","40"])
        _mukhtar_job  = pick(["مهندس","معلم","صاحب محل","موظف"])
        msgs = [
            {"role":"user","content":f"{_mukhtar_nm} مختار الحارة من سنين، صار كبير بالسن"},
            {"role":"assistant","content":f"{_mukhtar_nm} خدم الحارة كثير. أكو بديل جاهز؟"},
            {"role":"user","content":f"فكرين بـ{_new_mukhtar}، عمره {_mukhtar_age}، {_mukhtar_job}"},
            {"role":"assistant","content":f"{_new_mukhtar} شاب {_mukhtar_job}؟ يستاهل. أكثر طاقة لمشاكل الحارة"},
            {"role":"user","content":f"بس بعض الكبار ما يقبلون بـ{_new_mukhtar}"},
            {"role":"assistant","content":f"الانتخابات تحسم. {_new_mukhtar} لو معروف ومحترم بالحارة ينجح"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"أريد أشتري بيت بالحارة، المنطقة زينة؟"},
            {"role":"assistant","content":f"الحارة هادية وأهلها طيبين. القرب من {place} ميزة"},
            {"role":"user","content":"الأسعار معقولة؟"},
            {"role":"assistant","content":f"أسعار الحارة ارتفعت. البيت المتوسط من {vp(pick([150000000,200000000,250000000]))} مليون"},
            {"role":"user","content":"غالي شوي"},
            {"role":"assistant","content":f"المنطقة آمنة وقريبة من {place}. القيمة تستاهل"},
        ]
    elif tpl == 28:
        _sick_illness = pick(["ظهرها تعبان","ضغط الدم عالي","سكري ما تتحكم","بعد عملية","كسر بالرجل"])
        _sick_need    = pick(["نوصلها للدكتور","نشتري أدويتها","نطبخ لها","نتبادل زيارتها"])
        msgs = [
            {"role":"user","content":f"جارتنا {nm2} مريضة، {_sick_illness} وتحتاج مساعدة"},
            {"role":"assistant","content":f"{nm2} مريضة بـ{_sick_illness}؟ وحدها بالبيت؟"},
            {"role":"user","content":f"إي، وحدها. نقدر {_sick_need}"},
            {"role":"assistant","content":f"نتناوب الجيران. أنا أبدأ اليوم بـ{_sick_need}، أنت باچر"},
            {"role":"user","content":f"فكرة زينة، {nm2} كل عمرها تساعد الجيران"},
            {"role":"assistant","content":f"دورنا الآن نسدد جميلها. {_sick_illness} يحتاج رعاية"},
        ]
    elif tpl == 29:
        _heat_temp    = pick(["46 درجة","48 درجة","50 درجة","45 درجة"])
        _gen_ampere   = pick(["15 أمبير","20 أمبير","25 أمبير","30 أمبير"])
        _gen_houses   = pick(["5 بيوت","8 بيوت","10 بيوت","6 بيوت"])
        msgs = [
            {"role":"user","content":f"الحرارة {_heat_temp} هالأيام، المكيفات تشغل المولد ويقطع"},
            {"role":"assistant","content":f"مولد {_gen_ampere} ما يتحمل مكيفات {_gen_houses} سوية"},
            {"role":"user","content":f"ينقطع الكهرباء دايماً بسبب {_gen_houses} تشغّل سوية"},
            {"role":"assistant","content":f"نحدد ساعات {_elec_sched}، كل {_gen_houses} تشغّل بالتناوب"},
            {"role":"user","content":"من ينظم هذا؟"},
            {"role":"assistant","content":f"{_mukhtar_nm} ينظم جدول. {_gen_ampere} يكفي لو نتناوب"},
        ]
    elif tpl == 30:
        _accident_type = pick(["دهس دراجة","حادثة سيارة","سقوط طفل","تصادم يومي"])
        _street_name   = pick(["شارع المدرسة","الشارع الرئيسي","شارع السوق","الطريق الفرعي"])
        _traffic_sol   = pick(["إشارة ضوئية","مطب اصطناعي","لوحة توقف","إشارة مرور يدوية"])
        msgs = [
            {"role":"user","content":f"{_street_name} ما أكو {_traffic_sol}، صارت {_accident_type} فيه"},
            {"role":"assistant","content":f"{_accident_type} بـ{_street_name}؟ خطر كبير على الأطفال"},
            {"role":"user","content":f"كيف نطلب {_traffic_sol} لـ{_street_name}؟"},
            {"role":"assistant","content":f"ارفع طلب لمديرية المرور مع توقيع {_petition_num} ساكن وصور الحوادث"},
            {"role":"user","content":"كم يستغرق حتى يركبون؟"},
            {"role":"assistant","content":f"من شهر لـ3 أشهر. {_petition_num} توقيع مع دليل {_accident_type} تسرع"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"فيه بناء غير مرخص بالحارة يضر الجيران"},
            {"role":"assistant","content":"بناء غير مرخص مخالفة صريحة"},
            {"role":"user","content":"صاحبه ما يسمع الكلام"},
            {"role":"assistant","content":f"صور البناء وروح البلدية بـ{_council_loc}. يوقفون البناء فوراً"},
            {"role":"user","content":"من يروح معي؟"},
            {"role":"assistant","content":f"أنا وأبو {nm} نروح معك. {_petition_num} شخص أفضل"},
        ]
    elif tpl == 32:
        _school_dist  = pick(["20 دقيقة","ربع ساعة","30 دقيقة","25 دقيقة"])
        _school_danger= pick(["يعبرون الشارع الرئيسي","يمرون بمناطق خطرة","الشارع بدون إنارة","البعد يتعبهم"])
        _school_grade = pick(["ابتدائية","متوسطة","ثانوية","ابتدائية وروضة"])
        msgs = [
            {"role":"user","content":f"الحارة ما فيها {_school_grade}، الأطفال يمشون {_school_dist}"},
            {"role":"assistant","content":f"{_school_dist} مشي للـ{_school_grade}؟ كثير على الصغار"},
            {"role":"user","content":f"المشكلة {_school_danger} بالطريق"},
            {"role":"assistant","content":f"خطر! ارفعوا طلب لوزارة التربية لـ{_school_grade} قريبة مع توقيع {_petition_num} أهل"},
            {"role":"user","content":"فيه أمل يستجيبون؟"},
            {"role":"assistant","content":f"لو {_petition_num} عيلة وقّعت مع توثيق {_school_danger} يصير ضغط حقيقي"},
        ]
    elif tpl == 33:
        _shop_waste   = pick(["كراتين وأكياس","نفايات مطعم","زيوت وقطع محرك","بقايا بناء","نفايات كيماوية"])
        _waste_since  = pick(["من أسبوع","من أسبوعين","من شهر","من يومين"])
        msgs = [
            {"role":"user","content":f"صاحب {_shop_type} يرمي {_shop_waste} قدام بيوتنا من {_waste_since}"},
            {"role":"assistant","content":f"{_shop_waste} من {_shop_type}؟ مو صح. كلمته؟"},
            {"role":"user","content":f"كلمته مرتين وقال ما أكو مكان ثاني لـ{_shop_waste}"},
            {"role":"assistant","content":f"هذا مو عذر. بلغ {_garbage_comp} وبلغ البلدية بـ{_council_loc} فوراً"},
            {"role":"user","content":"يستحق غرامة؟"},
            {"role":"assistant","content":f"إي، رمي {_shop_waste} العشوائي من {_waste_since} فيه غرامة قانونية"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"في ورشة بالحارة تشتغل لـ{_dog_time} والأصوات تزعج"},
            {"role":"assistant","content":f"ورشة بـ{_dog_time}؟ مخالفة أوقات العمل"},
            {"role":"user","content":"شكونا وما اهتم"},
            {"role":"assistant","content":f"ارفع شكوى لبلدية {area} مع توثيق الأوقات بالصوت أو الفيديو"},
            {"role":"user","content":"يوقفون الورشة؟"},
            {"role":"assistant","content":"بالليل ممنوع قانونياً. البلدية تلزمه بالإيقاف أو الغرامة"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"أبو {nm}، الحارة تحتاج صندوق إسعاف للطوارئ"},
            {"role":"assistant","content":"فكرة ممتازة! من يتبرع؟"},
            {"role":"user","content":f"لو كل بيت يعطي {vp(pick([5000,10000,15000]))} دينار يكفي"},
            {"role":"assistant","content":f"ونشتري صندوق إسعاف كامل بـ{vp(pick([50000,75000,100000]))} دينار"},
            {"role":"user","content":"وين نضعه؟"},
            {"role":"assistant","content":f"عند {_mukhtar_nm} أو بـ{place} الحارة، معروف للكل"},
        ]
    elif tpl == 36:
        _group_admin  = pick(["أبو سعد الشاب","كريم المهندس","أبو علي ابن المختار","ابنة الحاج صالح"])
        _group_rules  = pick(["لا سياسة ولا خلافات","أخبار الحارة بس","بالاحترام والأدب","لا إعلانات تجارية"])
        msgs = [
            {"role":"user","content":f"نريد نسوي واتساب جروب لجيران الحارة ونحل مشكلة {issue}"},
            {"role":"assistant","content":f"جروب الجيران ممتاز لتنسيق حل {issue}! من يدير؟"},
            {"role":"user","content":f"فكرين بـ{_group_admin}، محترم وموثوق"},
            {"role":"assistant","content":f"{_group_admin} خيار ممتاز. والقواعد؟"},
            {"role":"user","content":f"{_group_rules} نحكم عليه"},
            {"role":"assistant","content":f"ممتاز. جروب بـ{_group_rules} يخدم {issue} والتواصل بالحارة"},
        ]
    elif tpl == 37:
        _car_color    = pick(["سوداء","بيضاء","رمادية","حمراء","زرقاء"])
        _car_type     = pick(["كيا","تويوتا","هيونداي","كورولا","سيارة بكب"])
        _park_duration= pick(["من الصبح للمسا","طول الليل","أيام متتالية","كل يوم"])
        msgs = [
            {"role":"user","content":f"{_car_type} {_car_color} دايماً يپارك قدام بيتنا {_park_duration}"},
            {"role":"assistant","content":f"{_car_type} {_car_color} {_park_duration}؟ صاحبها من الحارة؟"},
            {"role":"user","content":f"لا، زوار الجيران من فوق. {_park_duration} يزعجنا"},
            {"role":"assistant","content":f"كلم الجيران يحلون مع زوارهم. حق مدخلك أمام بيتك"},
            {"role":"user","content":"ما يهتمون رغم الكلام"},
            {"role":"assistant","content":f"صوّر {_car_type} {_car_color} واتصل بالمرور 104. حقك مكفول"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"فيه بالوعة مكسورة بمنتصف الشارع، خطر"},
            {"role":"assistant","content":"من متى وهي هيج؟"},
            {"role":"user","content":f"من {pick(['أمس','يومين','3 أيام'])}، حصلت عليها حوادث"},
            {"role":"assistant","content":f"طوارئ! اتصل ببلدية {area} فوراً وحط إشارة تحذيرية هسه"},
            {"role":"user","content":"رقم البلدية؟"},
            {"role":"assistant","content":f"142 طوارئ البلدية، أو روح شخصياً بـ{_council_loc}"},
        ]
    elif tpl == 39:
        _pharm_dist   = pick(["15 دقيقة","20 دقيقة","ربع ساعة","25 دقيقة"])
        _pharm_need   = pick(["المرضى والكبار","أمهات الأطفال","المرضى المزمنين","كل الحارة"])
        _pharm_loc    = pick(["ببداية الشارع","جنب الجامع","قرب البقالة","أول الحارة"])
        msgs = [
            {"role":"user","content":f"الحارة ما فيها صيدلية، أقرب واحدة {_pharm_dist} مشي"},
            {"role":"assistant","content":f"{_pharm_dist} بعيد خصوصاً على {_pharm_need}. من يتضرر أكثر؟"},
            {"role":"user","content":f"أكثر شي {_pharm_need} يعانون من البعد"},
            {"role":"assistant","content":f"فيه محل فاضي {_pharm_loc} بالحارة؟"},
            {"role":"user","content":f"إي، محل فاضي {_pharm_loc}"},
            {"role":"assistant","content":f"كلم صيدلاني يفتح فرع {_pharm_loc}. الحارة {_petition_num} بيت سوق كافي"},
        ]
    elif tpl == 40:
        _food_at_risk = pick(["لحم وأسماك","دجاج مذبوح","حليب وأجبان","طبيخ من الصبح","خضار وفاكهة"])
        _nbr_gen_nm   = pick(["أبو حسن","الجار أبو طارق","جارنا أبو سعد","أبو رياض"])
        msgs = [
            {"role":"user","content":f"الكهرباء قطعت {_elec_hours}، الـ{_food_at_risk} بالثلاجة راح يتعفن"},
            {"role":"assistant","content":f"{_elec_hours} انقطاع كثير والـ{_food_at_risk} تعفن بسرعة. المولد؟"},
            {"role":"user","content":f"المولد خربان من أمس، خايف على الـ{_food_at_risk}"},
            {"role":"assistant","content":f"اطلع الـ{_food_at_risk} وشيله لجارك اللي عنده مولد"},
            {"role":"user","content":f"فكرة زينة، {_nbr_gen_nm} عنده مولد شغال"},
            {"role":"assistant","content":f"اتصل بـ{_nbr_gen_nm} هسه. الجيران يساعدون بعض بالأزمات"},
        ]
    elif tpl == 41:
        _lost_child_age  = pick(["4","5","6","7","3"])
        _lost_child_desc = pick(["لابس قميص أزرق","لابس ثوب أخضر","بنية شعرها مجدولة","ولد شعره قصير"])
        _lost_child_nm   = pick(["ما يعرف اسمه يكمل","اسمه حسين","اسمه علي","اسمها فاطمة"])
        msgs = [
            {"role":"user","content":f"فيه طفل ضايع بالحارة، {_lost_child_desc}، {_lost_child_nm}"},
            {"role":"assistant","content":f"طفل ضايع؟ كم عمره تقريباً وهوين شوفته؟"},
            {"role":"user","content":f"حوالي {_lost_child_age} سنين، {_lost_child_desc}، يبكي عند {place}"},
            {"role":"assistant","content":f"خذه لعندك هسه وابدأ نادي بالحارة. أنا أساعد بالبحث"},
            {"role":"user","content":"وإذا ما لاقينا أهله؟"},
            {"role":"assistant","content":f"اتصل بالشرطة 104 فوراً. أرسل صورة {_lost_child_desc} للجروب"},
        ]
    elif tpl == 42:
        _travel_duration = pick(["شهر","أسبوعين","3 أسابيع","شهرين"])
        _travel_dest     = pick(["زيارة الأهل بالجنوب","علاج بالخارج","عمل بالخليج","حج أو عمرة"])
        _watch_schedule  = pick(["كل يوم","يوم بيوم","كل يومين","الصبح والمسا"])
        msgs = [
            {"role":"user","content":f"جارنا {nm} مسافر {_travel_duration} لـ{_travel_dest}، بيته فاضي"},
            {"role":"assistant","content":f"واجب نحافظ على بيت {nm} {_travel_duration}. نراقب {_watch_schedule}؟"},
            {"role":"user","content":f"إي، {_watch_schedule} نمر عليه"},
            {"role":"assistant","content":f"نتناوب الجيران، كل واحد يمر بيت {nm} {_watch_schedule}"},
            {"role":"user","content":"وإذا لاحظنا شي مشبوه؟"},
            {"role":"assistant","content":f"اتصل بـ{nm} أولاً. لو ما رد اتصل بالشرطة فوراً 104"},
        ]
    elif tpl == 43:
        _stranger_desc = pick(["يتفحص البيوت","يقيس الأبواب والشبابيك","يصور بموبايله","يتكلم بالهاتف ويشير"])
        _stranger_nights = pick(["من أسبوع","3 ليالي متتالية","كل ليلة","من يومين"])
        msgs = [
            {"role":"user","content":f"فيه شخص غريب يتجول بالحارة بـ{_dog_time}، {_stranger_desc}"},
            {"role":"assistant","content":f"شخص غريب بـ{_dog_time} {_stranger_desc}؟ خطر. من {_stranger_nights}؟"},
            {"role":"user","content":f"إي، من {_stranger_nights}، {_stranger_desc} بشكل متعمد"},
            {"role":"assistant","content":f"اتصل بالشرطة 104 فوراً. {_stranger_desc} سلوك مشبوه"},
            {"role":"user","content":"وإذا ما جاءت الشرطة بالوقت؟"},
            {"role":"assistant","content":f"صوّره من بعيد كدليل وبلغ {_mukhtar_nm}. نجتمع الجيران بـ{_dog_time}"},
        ]
    elif tpl == 44:
        _garden_size  = pick(["2 متر على 3 متر","3 متر على 4 متر","متر ونص عرض","جنب المدخل"])
        _garden_plant = pick(["أشجر ظل وزهور","ياسمين وورد","نباتات خضراء وأزهار","أشجار ليمون وسدر"])
        _garden_cost  = pick([50000,75000,100000,150000])
        msgs = [
            {"role":"user","content":f"أريد أعمل حديقة {_garden_size} أمام بيتي بـ{_garden_plant}"},
            {"role":"assistant","content":f"حديقة {_garden_size} بـ{_garden_plant} جميلة! بس الرصيف ملكية عامة"},
            {"role":"user","content":"ما تسد الطريق، {_garden_plant} بس"},
            {"role":"assistant","content":f"{_garden_plant} مقبولة لو ما تسد المشي. راجع البلدية بـ{_council_loc}"},
            {"role":"user","content":f"التكلفة تقريباً {vp(_garden_cost)}؟"},
            {"role":"assistant","content":f"{vp(_garden_cost)} للـ{_garden_size} بـ{_garden_plant} معقول. الجيران يفرحون بيها"},
        ]
    elif tpl == 45:
        _dinner_day   = pick(["الجمعة","السبت","الخميس","الأحد"])
        _dinner_loc   = pick(["ساحة الحارة","قدام بيت المختار","الشارع العريض","الفضاء المشترك"])
        _dinner_food  = pick(["مسقوف وتمن","كباب وتشريب","دجاج مشوي وسلطات","قيمة وعيش"])
        msgs = [
            {"role":"user","content":f"نريد ندعو كل جيران الحارة لعشاء جماعي يوم {_dinner_day}"},
            {"role":"assistant","content":f"فكرة رائعة! عشاء يوم {_dinner_day}؟ وين نجمع؟"},
            {"role":"user","content":f"بـ{_dinner_loc}، ونطبخ {_dinner_food}"},
            {"role":"assistant","content":f"ممتاز! {_dinner_food} بـ{_dinner_loc} يوم {_dinner_day}. نوزع المهام"},
            {"role":"user","content":f"أكم عيلة بالحارة تقريباً؟"},
            {"role":"assistant","content":f"حوالي {_petition_num} عيلة. {_dinner_food} يوم {_dinner_day} يجمع الكل"},
        ]
    elif tpl == 46:
        _susp_shop_type = pick(["محل مغلق بالنهار","بيت قديم فاضي","مستودع","غرفة بآخر الشارع"])
        _susp_activity  = pick(["ناس يدخلون ويطلعون بسرعة","أصوات غريبة","سيارات مختلفة كل ليلة","أضواء خافتة"])
        _susp_since     = pick(["من أسبوع","من أسبوعين","من شهر","من 10 أيام"])
        msgs = [
            {"role":"user","content":f"فيه {_susp_shop_type} بالحارة، {_susp_activity} بـ{_dog_time}"},
            {"role":"assistant","content":f"{_susp_activity} بـ{_dog_time} بـ{_susp_shop_type}؟ من {_susp_since}؟"},
            {"role":"user","content":f"إي، من {_susp_since}. {_susp_activity} بشكل متكرر"},
            {"role":"assistant","content":f"مريب. لا تتدخل وحدك، اتصل بالشرطة 104 فوراً"},
            {"role":"user","content":"بدون ما أعرف نفسي؟"},
            {"role":"assistant","content":f"إي، بلّغ عن {_susp_activity} بـ{_susp_shop_type} بس. سلامتك أهم"},
        ]
    elif tpl == 47:
        _fire_source  = pick(["مولد الكهرباء","دار مهجورة","محل أسطوانات غاز","مستودع","سيارة بالشارع"])
        _fire_spread  = pick(["والدخان يطلع","وصار كبير","ويخاف ينتشر","والريح تزيده"])
        msgs = [
            {"role":"user","content":f"فيه حريق بـ{_fire_source} بالحارة {_fire_spread}، شسوي؟"},
            {"role":"assistant","content":f"حريق بـ{_fire_source} {_fire_spread}؟ اتصل بالإطفاء 115 فوراً!"},
            {"role":"user","content":f"صغير لحد الآن، أكدر أطفيه قبل ما يكبر؟"},
            {"role":"assistant","content":f"لا! {_fire_source} {_fire_spread} يتطور بثواني. 115 أولاً وابعد الناس"},
            {"role":"user","content":"ماشي، أتصل هسه"},
            {"role":"assistant","content":f"وأخبر الجيران يبتعدون عن {_fire_source}. سرعة التصرف تنقذ الحارة"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"الغبار والدخان من {_shop_type} القريب يؤذي أطفالنا"},
            {"role":"assistant","content":f"غبار {_shop_type} صحياً ضار خصوصاً للأطفال"},
            {"role":"user","content":"كلمنا صاحبه وما اكتفى بحاجز"},
            {"role":"assistant","content":f"هذا مخالفة بيئية. ارفع شكوى لبلدية {area} ووزارة البيئة"},
            {"role":"user","content":"يغلقون المحل؟"},
            {"role":"assistant","content":"يلزمونه بالحاجز أو الانتقال. حق أطفالك بالهواء النظيف"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أبو {nm}، نريد نجمع تبرعات لعيلة فقيرة بالحارة"},
            {"role":"assistant","content":"ماشاءالله، أهل الحارة طيبين. كم تحتاج العيلة؟"},
            {"role":"user","content":f"تقريباً {vp(pick([100000,150000,200000]))} دينار للشهر"},
            {"role":"assistant","content":f"لو كل بيت يعطي {vp(pick([5000,10000,15000]))} دينار نكمل"},
            {"role":"user","content":"أنا أبدأ بالتبرع"},
            {"role":"assistant","content":f"جزاك الله خير. أنا كمان معك. نكلم {_mukhtar_nm} ينظم"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"أبو {nm}، {issue} بالحارة من {pick(['أمس','يومين','أسبوع'])}"},
            {"role":"assistant","content":f"والله من {pick(['أمس','يومين'])} وأنا أشوف {issue}"},
            {"role":"user","content":"شنو نسوي؟"},
            {"role":"assistant","content":f"نجمع {_petition_num} جار ونحكي مع {_mukhtar_nm}"},
            {"role":"user","content":"فكرة زينة، الوحدة قوة"},
            {"role":"assistant","content":f"إي، لو كلنا نطلب بصوت واحد يستجيبون لـ{issue}"},
        ]

    return {"id": f"neigh_{i:04d}", "category": "neighborhood_community", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# FILE 20 - WORK & JOBS
# ============================================================
JOBS      = ["مهندس","محاسب","مدرس","طبيب","محامي","مصمم غرافيك","مبرمج",
             "سائق","موظف حكومي","صاحب محل"]
COMPANIES = ["شركة الرافدين","شركة بغداد للتجارة","مجموعة النهرين",
             "مصنع البصرة","شركة المنصور للتطوير"]
SALARIES  = [300000, 400000, 500000, 700000, 1000000, 1500000]

def gen_work(i):
    job    = pick(JOBS)
    job2   = pick(JOBS)
    comp   = pick(COMPANIES)
    sal    = pick(SALARIES)
    sal2   = pick(SALARIES)
    nm     = pick(ALL_NAMES)
    nm2    = pick(ALL_NAMES)
    ww     = pick(WORK_W) if WORK_W else "شغل"
    _gr    = pick(GREET)
    _exp_yrs    = pick(["سنة","سنتين","3 سنين","5 سنين","7 سنين","10 سنين"])
    _search_time= pick(["شهرين","3 أشهر","6 أشهر","8 أشهر","سنة"])
    _overtime_h = pick(["ساعتين","3 ساعات","4 ساعات","ساعة إضافية"])
    _work_prob  = pick(["ضغط وتوتر","ما أكو تقدير","راتب ما يكفي","الزملاء صعبين","المدير ظالم"])
    _manager_nm = pick(["أبو سامر","المدير حسن","المدير العام","مسؤول الأقسام","الرئيس المباشر"])
    _freelance_skill = pick(["تصميم","برمجة","محاسبة","كتابة محتوى","ترجمة","تسويق رقمي"])
    _freelance_site  = pick(["مستقل","خمسات","فريلانسر","أبورك","لينكدإن"])
    _project_type = pick(["كيترنگ","محل ملابس","ورشة","مشروع زراعي","محل إلكترونيات","مطعم صغير"])
    _project_capital = pick([2000000,3000000,5000000,7000000,10000000])
    _project_loc  = pick(["بالبيت","بالمنطقة","بمول","بشارع تجاري","أونلاين"])
    _partner_nm   = pick(["أبو طارق","صاحبي كريم","ابن عمي","صاحبي القديم","شريك من الشغل"])
    _cv_skill     = pick(["أوفيس","تصميم","تحليل بيانات","إدارة مشاريع","مبيعات","تسويق"])
    _interview_q  = pick(["نقاط ضعفك شنو؟","ليش تركت شغلك السابق؟","وين تشوف نفسك بعد 5 سنين؟","شنو تعرف عن شركتنا؟"])
    _interview_sal= pick([600000,700000,800000,1000000,1200000,1500000])
    _leave_reason = pick(["ظروف عائلة","تعب","حضور حفل زواج","وفاة قريب","كشف طبي"])
    _raise_pct    = pick(["10%","15%","20%","25%"])
    _raise_reason = pick(["زيادة الأسعار","إنجازاتي بالسنة","خبرة إضافية اكتسبتها","مسؤوليات زادت"])
    _conflict_person = pick(["زميل في نفس الدرجة","المشرف المباشر","شخص من قسم ثاني","موظف أقدم مني"])
    _conflict_cause  = pick(["يأخذ الفضل على شغلي","يتغيب ويحسب علي","يسرّب معلومات سرية","يتنمر بالاجتماعات"])
    _remote_days  = pick(["يومين بالأسبوع","يوم بالأسبوع","3 أيام من البيت","كل الأسبوع"])
    _remote_tool  = pick(["زوم","تيمز","سلاك","گوگل ميت"])
    _train_topic  = pick(["مبيعات","قيادة","أوفيس متقدم","خدمة عملاء","تحليل بيانات"])
    _train_cost   = pick([100000,150000,200000,250000,300000])
    _resign_notice= pick(["أسبوعين","شهر","3 أشهر","أسبوع"])
    _resign_reason= pick(["عرض أحسن","بفتح مشروعي","راتب أفضل بشركة ثانية","بيتنا انتقل لمنطقة ثانية"])
    _retire_yrs   = pick(["25 سنة","28 سنة","30 سنة","33 سنة"])
    _retire_pension = pick([600000,700000,800000,1000000])
    _bonus_amt    = pick([100000,150000,200000,300000,500000])
    _promotion_pos= pick(["مدير قسم","نائب مدير","مشرف أول","رئيس فريق","مستشار"])
    _contract_type= pick(["دوام كامل","دوام جزئي","عقد مؤقت 6 أشهر","عقد سنوي قابل للتجديد"])
    _layoff_reason= pick(["إعادة هيكلة","خسارة الشركة","دمج أقسام","أتمتة العمل"])
    _side_job     = pick(["تدريس خصوصي","فريلانس أونلاين","خياطة بالبيت","بيع أونلاين","إيجار سيارة"])
    _gov_grade    = pick(["الدرجة الخامسة","الدرجة السادسة","الدرجة السابعة","الدرجة الثامنة"])
    _gov_ministry = pick(["وزارة الصحة","وزارة التربية","وزارة المالية","وزارة الداخلية","وزارة النفط"])
    _abroad_comp  = pick(["شركة خليجية","شركة سعودية","شركة إماراتية","شركة كويتية","شركة قطرية"])
    _abroad_sal   = pick([3000000,4000000,5000000,7000000,10000000])
    _ref_person   = pick(["مديري السابق","أستاذ الجامعة","صاحب عمل سابق","مشرف التدريب"])
    _work_award   = pick(["موظف الشهر","أفضل أداء ربعي","جائزة الإبداع","شهادة تقدير سنوية"])
    tpl = random.randint(1, 50)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"أريد أتقدم لوظيفة {job}، كيف أبدأ؟"},
            {"role":"assistant","content":f"تحتاج سي في محدث يبرز خبرتك بـ{_cv_skill}"},
            {"role":"user","content":f"خبرتي {_exp_yrs} بـ{job}، كافية؟"},
            {"role":"assistant","content":f"{_exp_yrs} خبرة ممتازة. {comp} تدور {job} هالأيام"},
            {"role":"user","content":"الراتب تقريباً كم؟"},
            {"role":"assistant","content":f"بين {vp(sal)} و{vp(int(sal*1.3))} دينار حسب الخبرة بـ{job}"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"أنا {job} حكومي والراتب {vp(sal)} ما يكفي، شسوي؟"},
            {"role":"assistant","content":f"راتب {vp(sal)} صعب هالأيام. عندك خيارات"},
            {"role":"user","content":"الفريلانس بالإنترنت ينفع؟"},
            {"role":"assistant","content":f"إي، بـ{_freelance_skill} تقدر تشتغل على {_freelance_site}"},
            {"role":"user","content":f"أنا أعرف {_cv_skill}، ينفع؟"},
            {"role":"assistant","content":f"{_cv_skill} مطلوب على {_freelance_site}. جرب وبتفاجأ"},
        ]
    elif tpl == 3:
        _bias_type = pick(["يعطي فرص الترقية لناس معينة","يوزع الشغل بشكل غير عادل","يأخذ إجازة لناس ويرفضها لثانيين","يتجاهل شكاويي دايماً"])
        _bias_proof= pick(["رسائل ايميل","جداول الشغل القديمة","شهادات زملاء","سجل الحضور"])
        msgs = [
            {"role":"user","content":f"{_manager_nm} مو عادل، {_bias_type} بشكل واضح"},
            {"role":"assistant","content":f"{_bias_type} من {_manager_nm} ظلم. عندك دليل؟"},
            {"role":"user","content":f"عندي {_bias_proof} تثبت {_bias_type}"},
            {"role":"assistant","content":f"{_bias_proof} دليل قوي. ارفع شكوى رسمية لـHR بـ{comp} بالدليل"},
            {"role":"user","content":"HR مو فاعلة بشركتنا"},
            {"role":"assistant","content":f"إذاً راجع محامي عمالي. {_bias_proof} يثبت {_bias_type} قانونياً"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"خلصت {job} من الجامعة وما لاقيت شغل من {_search_time}"},
            {"role":"assistant","content":f"من {_search_time} تدور؟ صعبة. جربت نتورك مع معارفك؟"},
            {"role":"user","content":"أكثر الوظائف بواسطة للأسف"},
            {"role":"assistant","content":f"صح. بس لينكدإن و{_freelance_site} فيه فرص بدون واسطة"},
            {"role":"user","content":"ما أعرف أسوي سي في زين"},
            {"role":"assistant","content":f"سي في يبرز {_cv_skill} وخبراتك. أساعدك تعدّله إذا تريد"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"عندي مقابلة {job} بـ{comp} باچر، شتنصحني؟"},
            {"role":"assistant","content":f"استعد جواب على: {_interview_q}"},
            {"role":"user","content":"وإذا سألوا عن الراتب المطلوب؟"},
            {"role":"assistant","content":f"قول {vp(_interview_sal)} ولا تنقص نفسك. {job} يستاهل"},
            {"role":"user","content":"خايف من المقابلة"},
            {"role":"assistant","content":f"طبيعي. ثق بنفسك وخبرتك بـ{_cv_skill}. إن شاء الله تنجح"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"الدوام بـ{comp} 8 ساعات و{_overtime_h} إضافية بدون مكافأة"},
            {"role":"assistant","content":f"{_overtime_h} إضافية بدون راتب؟ مخالفة قانون العمل"},
            {"role":"user","content":"بس ما أكدر أشكو، خايف أخسر الشغل"},
            {"role":"assistant","content":f"وثّق الساعات الإضافية برسائل أو ايميل"},
            {"role":"user","content":"ومن بعدين؟"},
            {"role":"assistant","content":"راجع محامي عمالي. {comp} ملزمة بدفع {_overtime_h} إضافية"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"أريد أفتح {_project_type} {_project_loc}، رأيك؟"},
            {"role":"assistant","content":f"{_project_type} {_project_loc}؟ السوق يحتاج. ما خبرتك فيه؟"},
            {"role":"user","content":f"عندي خبرة {_exp_yrs} بالمجال"},
            {"role":"assistant","content":f"{_exp_yrs} خبرة ممتازة. رأس المال كم عندك؟"},
            {"role":"user","content":f"حوالي {vp(_project_capital)} دينار"},
            {"role":"assistant","content":f"{vp(_project_capital)} يكفي لـ{_project_type} {_project_loc}. ابدأ بخطة عمل"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"{_partner_nm} يعرض علي شراكة بـ{_project_type}، أوافق؟"},
            {"role":"assistant","content":f"شراكة بـ{_project_type} مع {_partner_nm}؟ شنو نسبتك؟"},
            {"role":"user","content":f"{pick(['50%','40%','30%'])} وأنا أشارك بـ{vp(_project_capital)}"},
            {"role":"assistant","content":f"لازم عقد شراكة موثق قبل أي شي. حتى مع {_partner_nm}"},
            {"role":"user","content":"يقول الثقة كافية"},
            {"role":"assistant","content":f"العقد يحمي الاثنين لو صارت خلافات. لا تتنازل عن العقد"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"الحكومي ثابت بس راتبه {vp(sal)} قليل. الخاص أحسن؟"},
            {"role":"assistant","content":f"الخاص بـ{comp} قد يوصل {vp(sal2)} بس بدون ضمان"},
            {"role":"user","content":"عندي عائلة ومسؤوليات"},
            {"role":"assistant","content":"الثبات أهم لو عندك مسؤوليات. الحكومي أمان"},
            {"role":"user","content":f"بس {vp(sal)} ما يكفي هالأيام"},
            {"role":"assistant","content":f"اشتغل {_side_job} جانب الحكومي. تكمّل الدخل"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"طلبت إجازة {pick(['أسبوع','يومين','3 أيام'])} لـ{_leave_reason} وما وافقوا"},
            {"role":"assistant","content":f"{_leave_reason} سبب مشروع. من رفض؟"},
            {"role":"user","content":f"{_manager_nm} يقول ما أكو بديل"},
            {"role":"assistant","content":"إجازة الظروف الطارئة حق مكفول قانونياً"},
            {"role":"user","content":"كيف أتصرف؟"},
            {"role":"assistant","content":f"روح شؤون الموظفين بـ{comp} رسمياً. لا تخاف"},
        ]
    elif tpl == 11:
        _raise_project = pick(["مشروع التوسعة","إطلاق المنتج الجديد","تحسين المبيعات بـ30%","توفير تكاليف الشركة","تقليل أوقات التسليم"])
        _raise_timing  = pick(["بعد اجتماع التقييم السنوي","بعد نجاح مشروعي الأخير","قبل موسم الميزانية","بعد التقييم الربعي"])
        msgs = [
            {"role":"user","content":f"أريد أطلب زيادة راتب {_raise_pct} من {_manager_nm}، كيف أقنعه؟"},
            {"role":"assistant","content":f"زيادة {_raise_pct} معقولة. احضّر إنجازاتك بالأرقام"},
            {"role":"user","content":f"إنجازي الكبير كان {_raise_project}، وسبب طلبي {_raise_reason}"},
            {"role":"assistant","content":f"{_raise_project} و{_raise_reason} حجج قوية جداً. قدّمها بالأرقام"},
            {"role":"user","content":f"متى أكلم {_manager_nm}؟"},
            {"role":"assistant","content":f"أفضل وقت {_raise_timing}. التوقيت يفرق كثير بطلب زيادة {_raise_pct}"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"في خلاف بيني وبين {_conflict_person}، {_conflict_cause}"},
            {"role":"assistant","content":f"{_conflict_cause} تعب. تكلمت معه مباشرة؟"},
            {"role":"user","content":"كلمته وزاد الأمر"},
            {"role":"assistant","content":f"وثّق {_conflict_cause} بالتواريخ وأرسل لـHR بـ{comp}"},
            {"role":"user","content":"الHR يتصرفون بجدية؟"},
            {"role":"assistant","content":f"لو عندك دليل على {_conflict_cause} لازم يتصرفون"},
        ]
    elif tpl == 13:
        _commute_time = pick(["ساعة","ساعة ونص","ساعتين","45 دقيقة"])
        _remote_benefit = pick(["توفير وقت المواصلات","راحة البيت","توفير مصاريف السيارة","التركيز أكثر"])
        msgs = [
            {"role":"user","content":f"شركتي تعرض دوام عن بعد {_remote_days}، أقبل؟"},
            {"role":"assistant","content":f"دوام {_remote_days} من البيت فرصة! موصلاتك الحالية كم؟"},
            {"role":"user","content":f"{_commute_time} يومياً رايح وجاي بـ{comp}"},
            {"role":"assistant","content":f"{_commute_time} مواصلات! {_remote_days} يوفر {_remote_benefit} كبير"},
            {"role":"user","content":f"برنامج التواصل {_remote_tool}، الشغل يتأثر؟"},
            {"role":"assistant","content":f"{_remote_tool} سهل التعوّد. دوام {_remote_days} بنفس الراتب وتوفير {_commute_time}"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"الشركة تعرض تدريب {_train_topic} بتكلفة {vp(_train_cost)}، أشارك؟"},
            {"role":"assistant","content":f"تدريب {_train_topic} يزيد قيمتك بالسوق. يستاهل"},
            {"role":"user","content":f"بس {vp(_train_cost)} كثير علي"},
            {"role":"assistant","content":"اسأل إذا الشركة تتحمل جزء. بعضها تدفع التدريب كاملاً"},
            {"role":"user","content":"وإذا ما وافقوا؟"},
            {"role":"assistant","content":f"تدريب {_train_topic} استثمار بنفسك. {vp(_train_cost)} يرجع بزيادة راتب"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"أريد أستقيل من {comp}، كيف أتصرف؟"},
            {"role":"assistant","content":f"استقالة من {comp}؟ لازم تعطي إشعار {_resign_notice} قبل"},
            {"role":"user","content":f"سبب الاستقالة {_resign_reason}"},
            {"role":"assistant","content":f"{_resign_reason} سبب مفهوم. هل عندك بديل جاهز؟"},
            {"role":"user","content":"إي، عندي عرض ثاني"},
            {"role":"assistant","content":f"ممتاز. قدّم الاستقالة بخطاب رسمي لـ{_manager_nm}"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"قاربت على التقاعد بعد {_retire_yrs} بـ{_gov_ministry}"},
            {"role":"assistant","content":f"{_retire_yrs} خدمة؟ ماشاءالله! التقاعد متى بالضبط؟"},
            {"role":"user","content":f"بعد سنة تقريباً"},
            {"role":"assistant","content":f"راجع ديوان التقاعد الآن. الراتب التقاعدي حوالي {vp(_retire_pension)}"},
            {"role":"user","content":"كيف أجهز أوراقي؟"},
            {"role":"assistant","content":f"كشف خدمة من {_gov_ministry} وهوية ووثائق التعيين الأساسية"},
        ]
    elif tpl == 17:
        _side_income = pick([200000,300000,400000,500000])
        _side_hours  = pick(["ساعتين يومياً","3 ساعات بالمسا","عطلة نهاية الأسبوع","بعد الدوام مباشرة"])
        msgs = [
            {"role":"user","content":f"أشتغل {_side_job} جانب شغلي بـ{comp}، قانوني؟"},
            {"role":"assistant","content":f"{_side_job} جانب {comp}؟ يعتمد على بنود عقدك"},
            {"role":"user","content":f"العقد ما يمنع. أشتغل {_side_hours} على {_side_job}"},
            {"role":"assistant","content":f"لو ما يمنع، {_side_job} حلال. {_side_hours} جانب {comp} ممكن"},
            {"role":"user","content":f"الدخل من {_side_job} يوصل {vp(_side_income)} شهرياً"},
            {"role":"assistant","content":f"{vp(_side_income)} من {_side_job} بـ{_side_hours}؟ ممتاز. بس ما تأثر على {comp}"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"الشركة فصلت موظفين بسبب {_layoff_reason}، خايف على شغلي"},
            {"role":"assistant","content":f"{_layoff_reason} يهدد الكل. شلون أداؤك بالفترة الأخيرة؟"},
            {"role":"user","content":"تقييمي ممتاز دايماً"},
            {"role":"assistant","content":f"الأداء الجيد يحميك. وثّق إنجازاتك بـ{comp}"},
            {"role":"user","content":"وإذا حصلني؟"},
            {"role":"assistant","content":f"حقك تعويض {_layoff_reason}. راجع محامي عمالي قبل توقيع أي شي"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"{_abroad_comp} تعرض علي {vp(_abroad_sal)} دينار، أروح؟"},
            {"role":"assistant","content":f"{vp(_abroad_sal)} دينار؟ عرض ممتاز. أين تحديداً؟"},
            {"role":"user","content":f"بـ{pick(['الخليج','السعودية','الإمارات','قطر'])}، {_contract_type}"},
            {"role":"assistant","content":f"{_contract_type} بـ{vp(_abroad_sal)} جيد. بس العيلة والبعد؟"},
            {"role":"user","content":"العيلة أكبر هاجس عندي"},
            {"role":"assistant","content":f"فكّر بالمدى البعيد. {_abroad_sal} يبني مستقبل ويستاهل التضحية"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"طُرحت ترقية لـ{_promotion_pos} وأنا وزميل نتنافس"},
            {"role":"assistant","content":f"منافسة صحية! شنو مؤهلاتك لـ{_promotion_pos}؟"},
            {"role":"user","content":f"خبرة {_exp_yrs} وإنجازات وثّقتها"},
            {"role":"assistant","content":f"ممتاز. ابرز {_cv_skill} وقيادتك لمشاريع بـ{comp}"},
            {"role":"user","content":"وإذا ما أخذتها؟"},
            {"role":"assistant","content":f"اسأل {_manager_nm} شنو تحتاج لتأهل للترقية القادمة"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"شغل الحكومة بـ{_gov_ministry} أفضل ولا {comp} الخاصة؟"},
            {"role":"assistant","content":f"الحكومة أمان وتقاعد. {comp} راتب أعلى وفرص نمو"},
            {"role":"user","content":f"الحكومة {_gov_grade} الراتب {vp(sal)}"},
            {"role":"assistant","content":f"{comp} تعطي {vp(sal2)} ابتداءً. الفرق كبير بس بدون ضمان"},
            {"role":"user","content":"أنا شاب عندي مخاطرة"},
            {"role":"assistant","content":f"الشباب يتحمل مخاطرة {comp}. الخبرة والدخل أعلى بكثير"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"صاحبي {nm} تعثّر مشروعه وما كدر يرجع ديوني {vp(_project_capital)}"},
            {"role":"assistant","content":f"{vp(_project_capital)} رقم كبير. في عقد بينكم؟"},
            {"role":"user","content":"اتفقنا شفهياً بدون عقد"},
            {"role":"assistant","content":"صعب بدون عقد. بس شهود أو رسائل واتساب تثبت الدين"},
            {"role":"user","content":"شوية رسائل عندي"},
            {"role":"assistant","content":"راجع محامي بالرسائل. تقدر تطالب بـ{vp(_project_capital)} قانونياً"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"فزت بـ{_work_award} من {comp}، شلون أستفيد منها؟"},
            {"role":"assistant","content":f"{_work_award} شهادة على كفاءتك. مبروك!"},
            {"role":"user","content":"أكتبها بالسي في؟"},
            {"role":"assistant","content":f"أكيد! {_work_award} من {comp} تقوّي ملفك كثير"},
            {"role":"user","content":"هل تساعد بطلب زيادة راتب؟"},
            {"role":"assistant","content":f"إي، {_work_award} حجة ممتازة لطلب زيادة {_raise_pct}"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"كيف أكتب سي في زين لوظيفة {job}؟"},
            {"role":"assistant","content":f"سي في {job} يبدأ بملخص مهني، بعدين الخبرات والمهارات"},
            {"role":"user","content":f"مهاراتي {_cv_skill} وخبرتي {_exp_yrs}"},
            {"role":"assistant","content":f"{_cv_skill} مهارة مطلوبة و{_exp_yrs} خبرة جيدة. أبرزهم"},
            {"role":"user","content":"كم صفحة المناسب؟"},
            {"role":"assistant","content":f"صفحة واحدة أو صفحتين أقصى. مختصر ومركّز أفضل لـ{job}"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"أريد أغير مسيرتي المهنية من {job} لـ{job2}، ممكن؟"},
            {"role":"assistant","content":f"التحول من {job} لـ{job2} ممكن بس يحتاج تأهيل"},
            {"role":"user","content":f"عندي {_exp_yrs} بـ{job}"},
            {"role":"assistant","content":f"خبرة {job} تنفع جزئياً. تحتاج تدريب {_train_topic} لـ{job2}"},
            {"role":"user","content":"كم وقت يستغرق التحول؟"},
            {"role":"assistant","content":f"من 6 أشهر لسنة تقدر تتحول. {_freelance_site} يساعدك تبدأ"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"عرضوا علي {_contract_type} بـ{comp}، ينفع؟"},
            {"role":"assistant","content":f"{_contract_type}؟ أقرأ البنود كلها قبل توقيع"},
            {"role":"user","content":f"الراتب {vp(sal)} ومزايا جيدة"},
            {"role":"assistant","content":f"{vp(sal)} مع مزايا ممتاز. اشوف بند إنهاء العقد"},
            {"role":"user","content":"بند التجديد مضمون؟"},
            {"role":"assistant","content":"ما أكو ضمان بالخاص. اشتغل بأداء عالٍ يضمن التجديد"},
        ]
    elif tpl == 27:
        _skill_platform = pick(["Coursera","Udemy","LinkedIn Learning","edX","يوديمي العربي"])
        _skill_time     = pick(["ساعة يومياً","ساعتين بالمسا","3 ساعات بالعطلة","30 دقيقة صبح ومسا"])
        _skill_cert     = pick(["شهادة Coursera","شهادة Google","شهادة AWS","شهادة Microsoft","شهادة Adobe"])
        msgs = [
            {"role":"user","content":f"أريد أطور مهاراتي بـ{_freelance_skill}، من وين أبدأ عملياً؟"},
            {"role":"assistant","content":f"{_freelance_skill} طلبها عالي. ابدأ بـ{_skill_platform}"},
            {"role":"user","content":f"كم وقت أخصص؟ أنا مشغول بـ{comp}"},
            {"role":"assistant","content":f"{_skill_time} كافية. {_skill_platform} عنده كورسات مرنة"},
            {"role":"user","content":f"بعدين آخذ {_skill_cert}؟"},
            {"role":"assistant","content":f"{_skill_cert} قيمة بالسوق مع {_freelance_skill}. من 3-6 أشهر تصير محترف"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"طلبت مرجع من {_ref_person}، كيف أطلب بأدب؟"},
            {"role":"assistant","content":f"{_ref_person} مناسب كمرجع. ابعث رسالة مؤدبة"},
            {"role":"user","content":"شنو أكتب بالرسالة؟"},
            {"role":"assistant","content":f"اذكر الوظيفة اللي تتقدم لها و{job}، وشكره مسبقاً"},
            {"role":"user","content":"يرفض؟"},
            {"role":"assistant","content":f"{_ref_person} يعرفك جيد. الأغلب يوافق لو طلبت باحترام"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":f"أريد أشتغل فريلانس على {_freelance_site}، كيف أبدأ؟"},
            {"role":"assistant","content":f"ابدأ بملف قوي على {_freelance_site} يبرز {_freelance_skill}"},
            {"role":"user","content":"ما عندي بورتفوليو"},
            {"role":"assistant","content":f"اسوي 3-5 أعمال نموذجية تبرز {_freelance_skill}. حتى لو مجانية"},
            {"role":"user","content":"كم الدخل في البداية؟"},
            {"role":"assistant","content":f"البداية {vp(pick([100000,150000,200000]))} شهرياً. يزيد مع السمعة بـ{_freelance_site}"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"شركتي أعلنت مكافأة {_bonus_amt} دينار لأفضل أداء"},
            {"role":"assistant","content":f"مكافأة {vp(_bonus_amt)}؟ فرصة ممتازة. شنو معيار التقييم؟"},
            {"role":"user","content":f"المشاريع المنجزة والنقاط من العملاء"},
            {"role":"assistant","content":f"وثّق مشاريعك وجمع تقييمات العملاء. {vp(_bonus_amt)} يستاهل الجهد"},
            {"role":"user","content":"المنافسة شديدة"},
            {"role":"assistant","content":f"ركّز على جودة الشغل لا الكمية. {_work_award} يعزز فرصتك"},
        ]
    elif tpl == 31:
        _absent_person_role = pick(["المحاسب","مدير المبيعات","مسؤول المستودع","موظف الاستقبال","المبرمج"])
        _absent_duration    = pick(["من شهر","من شهرين","من 6 أسابيع","من 3 أشهر"])
        _absent_reason      = pick(["إجازة مرضية","إجازة بدون راتب","استقال ولم يعوض","مسافر طويل"])
        msgs = [
            {"role":"user","content":f"{_manager_nm} يريدني أسوي شغل {_absent_person_role} الغايب {_absent_duration}"},
            {"role":"assistant","content":f"شغل {_absent_person_role} الغايب {_absent_duration} بدون تعويض؟"},
            {"role":"user","content":f"إي، {_absent_person_role} {_absent_reason} ويروح علي شغله"},
            {"role":"assistant","content":f"من حقك تعويض على مهام {_absent_person_role} من {_absent_duration}"},
            {"role":"user","content":"كيف أطلب التعويض؟"},
            {"role":"assistant","content":f"راسل {_manager_nm} رسمياً تطلب تعويض على مهام {_absent_person_role} الإضافية"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"زميلي {nm} رُقّي وأنا أعمل أكثر منه، ليش؟"},
            {"role":"assistant","content":"مؤسف. الترقية عادةً بالأداء والعلاقات معاً"},
            {"role":"user","content":"علاقتي مع الإدارة جيدة وأدائي ممتاز"},
            {"role":"assistant","content":f"اطلب اجتماع مع {_manager_nm} واسأل صراحة عن معايير الترقية"},
            {"role":"user","content":"صراحة تنفع؟"},
            {"role":"assistant","content":"إي، الوضوح يفتح الأبواب ويحدد طريقك للأمام"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"أنا {job} بـ{comp} وأريد أفتح مشروعي جانب الشغل"},
            {"role":"assistant","content":f"{_project_type} جانب {job}؟ اقرأ بند التعارض بعقدك أول"},
            {"role":"user","content":"العقد ما يذكر المنافسة"},
            {"role":"assistant","content":f"إذاً {_project_type} {_project_loc} حلال. نظّم وقتك"},
            {"role":"user","content":"الشغل يتأثر؟"},
            {"role":"assistant","content":f"لو {_project_type} بـ{_project_loc} مساءً ما يتأثر شغلك بـ{comp}"},
        ]
    elif tpl == 34:
        _late_months  = pick(["شهر","شهرين","3 أشهر","6 أسابيع"])
        _late_amount  = pick([400000,500000,700000,1000000,1500000])
        _late_excuse  = pick(["ضائقة مالية","مشاكل بالحسابات البنكية","انتظار تحويل حكومي","أزمة سيولة مؤقتة"])
        msgs = [
            {"role":"user","content":f"{comp} ما بعثت لي راتب {_late_months}، المبلغ {vp(_late_amount)} دينار"},
            {"role":"assistant","content":f"تأخير {_late_months} وـ{vp(_late_amount)}؟ مخالفة صريحة لقانون العمل"},
            {"role":"user","content":f"يقولون {_late_excuse}"},
            {"role":"assistant","content":f"{_late_excuse} مو عذر. راتبك {vp(_late_amount)} حق قانوني. راجع {_manager_nm} رسمياً"},
            {"role":"user","content":"وإذا ما أعطوا؟"},
            {"role":"assistant","content":f"وزارة العمل أو محكمة العمل. وثّق كل التواصل عن {_late_months} التأخير"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"عندي اجتماع مهم بـ{comp} باچر وما عارف كيف أعرض مشروعي"},
            {"role":"assistant","content":"شنو موضوع المشروع؟"},
            {"role":"user","content":f"مشروع {_train_topic} لتطوير الفريق بتكلفة {vp(_train_cost)}"},
            {"role":"assistant","content":f"ابدأ بالمشكلة، بعدين حلك، وبعدين {vp(_train_cost)} كاستثمار"},
            {"role":"user","content":"كم دقيقة المثالي للعرض؟"},
            {"role":"assistant","content":f"10-15 دقيقة مع سلايدات واضحة. خذ أسئلة بعدين"},
        ]
    elif tpl == 36:
        _network_goal = pick(["أدور شغل","أتوسع بمشروعي","أطور مسيرتي","أجد شركاء","أتعلم من الخبراء"])
        _network_event= pick(["مؤتمر البيزنس","فعاليات لينكدإن العراق","ملتقى رجال الأعمال","ورشة عمل مهنية"])
        _network_msg  = pick(["رسالة تعريفية قصيرة","سؤال عن تجربتهم","طلب نصيحة مهنية","تعليق على منشوراتهم"])
        msgs = [
            {"role":"user","content":f"أريد أبني شبكة علاقات مهنية لـ{_network_goal}. كيف أبدأ؟"},
            {"role":"assistant","content":f"لـ{_network_goal} تحتاج نتورك حقيقي. لينكدإن أولاً"},
            {"role":"user","content":f"وبعد لينكدإن؟"},
            {"role":"assistant","content":f"احضر {_network_event} بمجالك. التواصل الشخصي يبني الثقة"},
            {"role":"user","content":f"كيف أبدأ الحديث مع ناس ما أعرفهم؟"},
            {"role":"assistant","content":f"ابدأ بـ{_network_msg}. الفضول الحقيقي يفتح أبواب لـ{_network_goal}"},
        ]
    elif tpl == 37:
        _change_age   = pick(["40","42","45","48","50"])
        _current_job  = pick(["موظف حكومي من سنين","مدرس من 15 سنة","محاسب روتيني","موظف مبيعات"])
        _change_fear  = pick(["يقولون الريسك كبير","خايف ما أعرف أتكيف","عيلتي قلقانة","ما عندي خبرة بالمجال الجديد"])
        msgs = [
            {"role":"user","content":f"عمري {_change_age} وأنا {_current_job}، أريد أغير لـ{_freelance_skill}، متأخر؟"},
            {"role":"assistant","content":f"{_current_job} لسنين طويلة؟ ما أكو متأخر للتغيير بعمر {_change_age}"},
            {"role":"user","content":f"بس {_change_fear}"},
            {"role":"assistant","content":f"{_change_fear} طبيعي. بس خبرة {_current_job} ميزة لتعلم {_freelance_skill}"},
            {"role":"user","content":f"السوق يقبل {_change_age} سنة بـ{_freelance_skill}؟"},
            {"role":"assistant","content":f"السوق يريد نتائج لا عمر. {_current_job} يعطيك نضج يفرق بـ{_freelance_skill}"},
        ]
    elif tpl == 38:
        _illegal_act  = pick(["تزوير فواتير","إخفاء خسائر الشركة","تحويل أموال بدون إذن","ختم وثائق مزورة","تغيير بيانات رسمية"])
        _illegal_who  = pick(["{_manager_nm}","المدير العام","مسؤول المالية","مدير القسم"])
        msgs = [
            {"role":"user","content":f"{_manager_nm} طلب مني {_illegal_act}، شسوي؟"},
            {"role":"assistant","content":f"{_illegal_act}؟ هذا عمل غير قانوني. رفضه واجب ومحمي قانونياً"},
            {"role":"user","content":f"خايف يطردني لو رفضت {_illegal_act}"},
            {"role":"assistant","content":f"تهديد الفصل بسبب رفض {_illegal_act} هو بحد ذاته جريمة"},
            {"role":"user","content":"كيف أتصرف؟"},
            {"role":"assistant","content":f"وثّق طلب {_manager_nm} بالرسائل واستشر محامي قبل أي خطوة"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":f"أريد أبدأ مشروع {_project_type} بـ{vp(_project_capital)}، من وين أحصل تمويل؟"},
            {"role":"assistant","content":f"{vp(_project_capital)} لـ{_project_type}؟ عندك خيارات"},
            {"role":"user","content":"القرض البنكي؟"},
            {"role":"assistant","content":f"بنك {pick(['الرافدين','الرشيد','الإسلامي للاستثمار'])} عنده قروض مشاريع"},
            {"role":"user","content":"الفائدة كم؟"},
            {"role":"assistant","content":f"الفائدة {pick(['5%','7%','4%'])} سنوياً. قدّم خطة عمل واضحة للبنك"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"صاحبي يعرض علي شغل بـ{comp} براتب {vp(sal)} ولكن بدون عقد"},
            {"role":"assistant","content":"بدون عقد؟ خطر كبير حتى مع الصديق"},
            {"role":"user","content":"يقول ما أكو قانون يلزمه"},
            {"role":"assistant","content":"قانون العمل يلزم العقد لو طالبت. بدون عقد حقوقك مو مضمونة"},
            {"role":"user","content":"أشتغل ولا لا؟"},
            {"role":"assistant","content":f"لا توافق بدون عقد. حتى {comp} الصغيرة لازم توقّع"},
        ]
    elif tpl == 41:
        _client_prob  = pick(["يغير رأيه كل مرة","يرفض الشغل بدون سبب واضح","يطلب تعديلات بلا نهاية","يقارن بنماذج ما تشبه طلبه"])
        _client_field = pick(["تصميم الشعار","كتابة المحتوى","البرمجة","التسويق الرقمي","الترجمة"])
        _client_solution = pick(["عقد مكتوب بعدد التعديلات","نموذج موافقة قبل كل مرحلة","جلسة بريف مفصلة","عرض 3 اتجاهات قبل البدء"])
        msgs = [
            {"role":"user","content":f"عميل بـ{_client_field} {_client_prob}، كيف أتعامل معه؟"},
            {"role":"assistant","content":f"عميل {_client_prob} بـ{_client_field}؟ شنو بالضبط يشكي؟"},
            {"role":"user","content":f"يقول {_client_prob} ويطلب تعديلات مجانية"},
            {"role":"assistant","content":f"الحل {_client_solution} قبل البدء بأي {_client_field}"},
            {"role":"user","content":f"وإذا أكمل {_client_prob} بعد التوقيع؟"},
            {"role":"assistant","content":f"العقد يحمي بـ{_client_solution}. بعدها التعديل بسعر إضافي"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"أريد أشتغل بـ{_gov_ministry}، كيف أتقدم؟"},
            {"role":"assistant","content":f"وظائف {_gov_ministry} تُعلن بالجريدة الرسمية وموقع الوزارة"},
            {"role":"user","content":"الشروط شنو عادةً؟"},
            {"role":"assistant","content":f"شهادة {job}، هوية مدنية، وبطاقة سكن. بعض الوظائف يحتاج {_cv_skill}"},
            {"role":"user","content":"الراتب بالحكومة؟"},
            {"role":"assistant","content":f"{_gov_grade} تبدأ من {vp(sal)} وتزيد مع الأقدمية"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"عرضوا علي منصب {_promotion_pos} بـ{comp} بس الضغط أكثر"},
            {"role":"assistant","content":f"منصب {_promotion_pos} ضغط أكثر لكن مسؤولية وراتب أعلى"},
            {"role":"user","content":f"الزيادة {vp(int(sal * 0.3))} دينار"},
            {"role":"assistant","content":f"زيادة {vp(int(sal * 0.3))} مقابل {_promotion_pos} يستاهل لو تتحمل الضغط"},
            {"role":"user","content":"كيف أقرر؟"},
            {"role":"assistant","content":f"اسأل نفسك: هل تريد قيادة فريق؟ {_promotion_pos} مسار مهني مختلف"},
        ]
    elif tpl == 44:
        _course_goal   = pick(["أرفع راتبي","أغير مسيرتي","أتأهل للترقية","أشتغل فريلانس","أطور كفاءتي"])
        _course_budget = pick([50000,75000,100000,150000,200000])
        _course_lang   = pick(["بالعربي","بالإنجليزي مع ترجمة","باللهجة العراقية","بالعربي الفصيح"])
        msgs = [
            {"role":"user","content":f"أريد أسوي كورس {_train_topic} أونلاين لـ{_course_goal}، أيش تنصح؟"},
            {"role":"assistant","content":f"كورس {_train_topic} لـ{_course_goal}؟ الميزانية كم؟"},
            {"role":"user","content":f"حوالي {vp(_course_budget)} دينار، أريده {_course_lang}"},
            {"role":"assistant","content":f"بـ{vp(_course_budget)} تلاقي كورس {_train_topic} {_course_lang} ممتاز"},
            {"role":"user","content":"شهادة معتمدة توصل لـ{_course_goal}؟"},
            {"role":"assistant","content":f"شهادة {_train_topic} مع مشاريع عملية تفرق لـ{_course_goal} كثير"},
        ]
    elif tpl == 45:
        _time_mgmt_tool = pick(["جوجل كالندر","تطبيق Notion","قائمة ورقية","Trello","تطبيق توقيت"])
        _side_hours2    = pick(["ساعتين بالمسا","3 ساعات بعد الدوام","الصبح الباكر","نهاية الأسبوع"])
        _rest_day       = pick(["الجمعة","السبت","الخميس","أحد أيام الأسبوع"])
        msgs = [
            {"role":"user","content":f"أريد أنظم وقتي بين {comp} و{_side_job} الجانبي، الاثنين مرهقين"},
            {"role":"assistant","content":f"شغلين معاً؟ تنظيم الوقت أهم شي. تستخدم {_time_mgmt_tool}؟"},
            {"role":"user","content":f"لا، مجرب بس ما انتظم"},
            {"role":"assistant","content":f"خصص {_side_hours2} ثابتة لـ{_side_job}. {_time_mgmt_tool} يساعد بالتنظيم"},
            {"role":"user","content":"التعب يأثر على جودة شغلي بـ{comp}"},
            {"role":"assistant","content":f"يوم {_rest_day} كامل راحة. الإنتاجية تحتاج شحن لا تراكم تعب"},
        ]
    elif tpl == 46:
        _hours_old    = pick(["6 ساعات","7 ساعات","8 ساعات"])
        _hours_new    = pick(["9 ساعات","10 ساعات","11 ساعات","12 ساعة"])
        _change_since = pick(["من الشهر الماضي","من أول الفصل","من بداية السنة","من قبل أسبوعين"])
        msgs = [
            {"role":"user","content":f"{comp} غيّرت ساعاتنا من {_hours_old} لـ{_hours_new} بدون زيادة، من {_change_since}"},
            {"role":"assistant","content":f"من {_hours_old} لـ{_hours_new} بدون زيادة؟ تغيير أحادي مخالف للعقد"},
            {"role":"user","content":f"قالوا قرار إداري من {_change_since}"},
            {"role":"assistant","content":f"القرار الإداري ما يلغي عقدك الأصلي اللي يحدد {_hours_old}"},
            {"role":"user","content":"كيف أحتج على {_hours_new} بدون زيادة؟"},
            {"role":"assistant","content":f"راسل {_manager_nm} رسمياً ترفض تعديل الساعات. وثّق كل شي من {_change_since}"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"صاحبي {nm} يشتغل فريلانس وربح {vp(pick([500000,700000,1000000]))} الشهر الماضي"},
            {"role":"assistant","content":"ماشاءالله! بأي مجال يشتغل؟"},
            {"role":"user","content":f"{_freelance_skill} على {_freelance_site}"},
            {"role":"assistant","content":f"{_freelance_skill} على {_freelance_site} سوق ممتاز. ليش ما تجرب؟"},
            {"role":"user","content":"ما أعرف أبدأ من وين"},
            {"role":"assistant","content":f"ابدأ بملف على {_freelance_site} مع 3 نماذج شغل. الأول صعب، بعدين تنطلق"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"أريد أتقدم لوظيفة بـ{_abroad_comp}، شلون مؤهلاتي؟"},
            {"role":"assistant","content":f"{_abroad_comp} تدور مؤهلات عالية. شنو خبرتك؟"},
            {"role":"user","content":f"{job} بخبرة {_exp_yrs} وأعرف {_cv_skill}"},
            {"role":"assistant","content":f"ممتاز! {_abroad_comp} تريد {job} بـ{_cv_skill} بالضبط"},
            {"role":"user","content":"الراتب هناك كم؟"},
            {"role":"assistant","content":f"بدايةً من {vp(_abroad_sal)} دينار مع مزايا إضافية"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أريد أستثمر مدخراتي {vp(_project_capital)} بمشروع، أيش تنصح؟"},
            {"role":"assistant","content":f"{vp(_project_capital)} مبلغ جيد. شنو مجالك؟"},
            {"role":"user","content":f"أجيد {_freelance_skill} وعندي خبرة {_exp_yrs}"},
            {"role":"assistant","content":f"افتح {_project_type} يعتمد على {_freelance_skill} بـ{_project_loc}"},
            {"role":"user","content":"المخاطرة كبيرة؟"},
            {"role":"assistant","content":f"ابدأ صغير من {_project_loc}. {vp(_project_capital)} يكفي للبداية الآمنة"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"شغلي كـ{job} بـ{comp} تعبان هالأيام بسبب {_work_prob}"},
            {"role":"assistant","content":f"{_work_prob} مشكلة. من كم وقت هيج؟"},
            {"role":"user","content":f"من {pick(['شهر','شهرين','3 أشهر'])} والأمور تزداد"},
            {"role":"assistant","content":f"الله يوفقك. تكدر تتكلم مع {_manager_nm} بصراحة؟"},
            {"role":"user","content":"مجرب وما نفع"},
            {"role":"assistant","content":f"إذاً فكر بخطوتك الثانية. {job} بـ{comp} ثانية تعطيك أفق أوسع"},
        ]

    return {"id": f"work_{i:04d}", "category": "work_jobs", "dialect": "iraqi_arabic", "messages": msgs}


# ============================================================
# MAIN
# ============================================================
FILES = [
    ("iraqi_train_11_health.json",       gen_health,       "health"),
    ("iraqi_train_12_education.json",    gen_education,    "education"),
    ("iraqi_train_13_government.json",   gen_government,   "government"),
    ("iraqi_train_14_restaurant.json",   gen_restaurant,   "restaurant"),
    ("iraqi_train_15_transport.json",    gen_transport,    "transport"),
    ("iraqi_train_16_sports.json",       gen_sports,       "sports"),
    ("iraqi_train_17_family.json",       gen_family,       "family"),
    ("iraqi_train_18_occasions.json",    gen_occasions,    "occasions"),
    ("iraqi_train_19_neighborhood.json", gen_neighborhood, "neighborhood"),
    ("iraqi_train_20_work.json",         gen_work,         "work"),
]

OUT_DIR = os.path.join(os.path.dirname(__file__), "iraqi_training_data")
os.makedirs(OUT_DIR, exist_ok=True)

for fname, gen_fn, _ in FILES:
    print(f"Generating {fname} ...")
    data = [gen_fn(i+1) for i in range(10000)]
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved 10000 conversations to {path}")

print("\nDone! Files 11-20 generated.")

