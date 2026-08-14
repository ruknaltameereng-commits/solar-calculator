import streamlit as st
import math

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="شركة ركن التعمير - حاسبة المنظومات الشمسية",
    page_icon="☀️",
    layout="wide"
)

# ==========================================
# 2. البيانات الفنية الرسمية والأسعار
# ==========================================

PANEL_OPTIONS = [
    {"brand": "Jinko Solar 725W (Voc 49.12V)", "power_w": 725, "price": 175, "max_string_size": 9},
    {"brand": "Longi Solar 640W (Voc 53.70V)", "power_w": 640, "price": 165, "max_string_size": 8},
    {"brand": "لوح قياسي 640W", "power_w": 640, "price": 160, "max_string_size": 9}
]

DC_ACCESSORIES_PRICE_PER_STRING = 30
EARTHING_SYSTEM_PRICE = 160

# قاعدة بيانات الإنفرترات المدعومة ببيانات Datasheets الرسمية
# (I_dc_max من الكتالوج الرسمي، V_dc = 51.5V ، V_grid = 210V ، نسبة الأمان = 80%)
INVERTER_BRANDS = [
    # Deye
    {
        "brand": "Deye Off-Grid (6K)", 
        "model": "SUN-6K-OG", 
        "power_kw": 6.0, 
        "price": 700, 
        "phase": "single",
        "max_charge_idc": 120,
        "cable_spec": "4 x 4 mm²"
    },
    {
        "brand": "Deye Hybrid (5K)", 
        "model": "SUN-5K-SG04LP1-EU-SM2", 
        "power_kw": 5.0, 
        "price": 750, 
        "phase": "single",
        "max_charge_idc": 120,
        "cable_spec": "4 x 4 mm²"
    },
    {
        "brand": "Deye Hybrid (6K)", 
        "model": "SUN-6K-SG04LP1-EU-SM2", 
        "power_kw": 6.0, 
        "price": 875, 
        "phase": "single",
        "max_charge_idc": 135,
        "cable_spec": "4 x 6 mm²"
    },
    {
        "brand": "Deye Hybrid (8K)", 
        "model": "SUN-8K-SG05LP1-EU-SM2", 
        "power_kw": 8.0, 
        "price": 1225, 
        "phase": "single",
        "max_charge_idc": 190,
        "cable_spec": "4 x 10 mm²"
    },
    {
        "brand": "Deye Hybrid (12K)", 
        "model": "SUN-12K-SG02LP1-EU-AM3", 
        "power_kw": 12.0, 
        "price": 1800, 
        "phase": "single",
        "max_charge_idc": 250,
        "cable_spec": "4 x 16 mm²"
    },
    {
        "brand": "Deye Hybrid (16K)", 
        "model": "SUN-16K-SG01LP1-EU", 
        "power_kw": 16.0, 
        "price": 2000, 
        "phase": "single",
        "max_charge_idc": 290,
        "cable_spec": "4 x 16 mm²"
    },

    # Solis
    {
        "brand": "Solis Hybrid (5K)", 
        "model": "S6-EH1P5K-L-PLUS", 
        "power_kw": 5.0, 
        "price": 750, 
        "phase": "single",
        "max_charge_idc": 112,
        "cable_spec": "4 x 4 mm²"
    },
    {
        "brand": "Solis Hybrid (6K)", 
        "model": "S6-EH1P6K-L-PLUS", 
        "power_kw": 6.0, 
        "price": 800, 
        "phase": "single",
        "max_charge_idc": 135,
        "cable_spec": "4 x 6 mm²"
    },
    {
        "brand": "Solis Hybrid (8K)", 
        "model": "S6-EH1P8K-L-PLUS", 
        "power_kw": 8.0, 
        "price": 1300, 
        "phase": "single",
        "max_charge_idc": 190,
        "cable_spec": "4 x 10 mm²"
    },
    {
        "brand": "Solis Hybrid (10K)", 
        "model": "S6-EH1P10K-L-PLUS", 
        "power_kw": 10.0, 
        "price": 1650, 
        "phase": "single",
        "max_charge_idc": 210,
        "cable_spec": "4 x 10 mm²"
    },
    {
        "brand": "Solis Hybrid (12K)", 
        "model": "S6-EH1P12K03-NV-YD-L", 
        "power_kw": 12.0, 
        "price": 1900, 
        "phase": "single",
        "max_charge_idc": 250,
        "cable_spec": "4 x 16 mm²"
    },
    {
        "brand": "Solis Hybrid (16K)", 
        "model": "S6-EH1P16K03-NV-YD-L", 
        "power_kw": 16.0, 
        "price": 2100, 
        "phase": "single",
        "max_charge_idc": 290,
        "cable_spec": "4 x 16 mm²"
    },

    # SRNE
    {
        "brand": "SRNE Off-Grid (16K)", 
        "model": "SRNE-16K-IP20", 
        "power_kw": 16.0, 
        "price": 1600, 
        "phase": "single",
        "max_charge_idc": 200,
        "cable_spec": "4 x 10 mm²"
    },

    # 3-Phase HV
    {
        "brand": "Deye HV 3-Phase (30K)", 
        "model": "SUN-30K-SG01HP3", 
        "power_kw": 30.0, 
        "price": 3800, 
        "phase": "three",
        "max_charge_idc": 100,
        "cable_spec": "4 x 16 mm²"
    },
    {
        "brand": "Deye HV 3-Phase (50K)", 
        "model": "SUN-50K-SG01HP3", 
        "power_kw": 50.0, 
        "price": 5200, 
        "phase": "three",
        "max_charge_idc": 150,
        "cable_spec": "4 x 25 mm²"
    }
]

BATTERIES = [
    {"name": "AOKLY جدارية / أرضية", "capacity_kwh": 10.24, "price": 1350},
    {"name": "BICODI Lithuim", "capacity_kwh": 12.0, "price": 1450},
    {"name": "AOKLY بعجلات", "capacity_kwh": 15.0, "price": 1700},
    {"name": "BICODI Lithuim", "capacity_kwh": 16.1, "price": 1850},
    {"name": "BICODI Lithuim", "capacity_kwh": 17.66, "price": 2100},
]

# ==========================================
# 3. الدوال الحسابية
# ==========================================
def get_ac_board_price(current_amp):
    if 8 <= current_amp <= 15:
        return 125
    elif 15 < current_amp <= 25:
        return 160
    elif 25 < current_amp <= 40:
        return 180
    elif 40 < current_amp <= 60:
        return 250
    elif 80 <= current_amp <= 120:
        return 350
    elif 120 < current_amp <= 150:
        return 450
    else:
        return 180

def calculate_panels_auto(day_current, required_battery_kwh, selected_panel):
    panel_watt = selected_panel["power_w"]
    max_string = selected_panel["max_string_size"]
    
    day_power_w = day_current * 230 * 1.3
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    
    total_panels_raw = (day_power_w + charging_power_w) / panel_watt
    target_panels = math.ceil(total_panels_raw)
    
    for num_strings in range(1, 10):
        panels_per_string = math.ceil(target_panels / num_strings)
        if panels_per_string <= max_string:
            return panels_per_string * num_strings, num_strings, panels_per_string
    return target_panels, 1, target_panels

# ==========================================
# 4. واجهة المستخدم (User Interface)
# ==========================================
st.title("☀️ RUKEN AL TAMWWE CALCULATER - شركة ركن التعمير")
st.caption(" اعداد المهندس محمد النوري والمهندسة زينة ثامر برمجة وتصميم هندسي مخصص للحسابات الدقيقة واختيار الأجهزة والتعديل التفاعلي")

st.markdown("---")

# 1. إدخال أحمال المنظومة
st.subheader("📥 1. إدخال أحمال المنظومة")
col1, col2, col3 = st.columns(3)

with col1:
    day_amp = st.number_input("أمبير النهار (ن)", min_value=1, max_value=200, value=30, step=1)

with col2:
    night_amp = st.number_input("أمبير الليل (ل)", min_value=1, max_value=200, value=12, step=1)

with col3:
    night_hours = st.number_input("ساعات التشغيل الليلي (س)", min_value=1, max_value=24, value=4, step=1)

is_hv_3ph = st.checkbox("تطبيق نظام HV-3PH (ثلاثي الأطوار / High Voltage)", value=False)

st.markdown("---")

# 2. الحسابات التلقائية الأولية
load_kw = (day_amp * 230) / 1000.0
recommended_kw = load_kw * 1.2
req_kwh = night_amp * 0.285 * night_hours
target_phase = "three" if is_hv_3ph else "single"

# أ. تحديد الإنفرتر التلقائي
phase_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == target_phase]
available_powers = sorted(list(set([inv["power_kw"] for inv in phase_inverters])))

auto_power_kw = available_powers[-1]
for pkw in available_powers:
    if pkw >= recommended_kw:
        auto_power_kw = pkw
        break

# ب. تحديد البطارية التلقائية الأقرب (أقل هامش زيادة لمراعاة التكلفة)
all_bat_combos = []
for bat in BATTERIES:
    for qty in [1, 2, 3]:
        total_cap = bat["capacity_kwh"] * qty
        if total_cap >= req_kwh:
            all_bat_combos.append({
                "brand": bat["name"],
                "unit_cap": bat["capacity_kwh"],
                "total_cap": round(total_cap, 2),
                "qty": qty,
                "unit_price": bat["price"],
                "total_price": bat["price"] * qty,
                "diff": total_cap - req_kwh
            })

all_bat_combos.sort(key=lambda x: x["diff"])
auto_bat_combo = all_bat_combos[0] if all_bat_combos else None

# 3. قسم خيارات التعديل اليدوي المباشر
st.subheader("⚙️ 2. تحديد الماركات وتخصيص الخيارات (يدوياً حسب الرغبة)")

col_p, col_i, col_b = st.columns(3)

# --- اختيار اللوح والتعديل اليدوي ---
with col_p:
    st.markdown("##### ☀️ الألواح الشمسية")
    panel_names = [f"{p['brand']} - (${p['price']})" for p in PANEL_OPTIONS]
    selected_p_str = st.selectbox("نوع اللوح:", options=panel_names)
    chosen_panel = PANEL_OPTIONS[panel_names.index(selected_p_str)]
    
    auto_panels, auto_strings, auto_per_string = calculate_panels_auto(day_amp, req_kwh, chosen_panel)
    
    override_panels = st.checkbox("تعديل يدوي على عدد الألواح")
    if override_panels:
        final_panels = st.number_input("حدد عدد الألواح المطلوب:", min_value=1, max_value=100, value=auto_panels, step=1)
    else:
        final_panels = auto_panels

# --- اختيار الإنفرتر والتعديل اليدوي ---
with col_i:
    st.markdown("##### 🔌 الإنفرتر الهجين")
    override_inv = st.checkbox("تعديل يدوي / اختيار قدرة أعلى")
    
    if override_inv:
        selected_power_kw = st.selectbox("اختر قدرة الإنفرتر (kW):", options=available_powers, index=available_powers.index(auto_power_kw))
    else:
        selected_power_kw = auto_power_kw
        
    brands_for_power = [inv for inv in phase_inverters if inv["power_kw"] == selected_power_kw]
    brand_options = [f"{inv['brand']} [{inv['model']}] - (${inv['price']})" for inv in brands_for_power]
    selected_brand_str = st.selectbox(f"الماركة والموديل لـ ({selected_power_kw} kW):", options=brand_options)
    chosen_inverter = brands_for_power[brand_options.index(selected_brand_str)]

# --- اختيار البطارية والتعديل اليدوي ---
with col_b:
    st.markdown("##### 🔋 بنك البطاريات")
    override_bat = st.checkbox("تعديل يدوي / تغيير حجم البطارية")
    
    all_possible_bats = []
    for bat in BATTERIES:
        for qty in [1, 2, 3]:
            all_possible_bats.append({
                "brand": bat["name"],
                "unit_cap": bat["capacity_kwh"],
                "total_cap": round(bat["capacity_kwh"] * qty, 2),
                "qty": qty,
                "unit_price": bat["price"],
                "total_price": bat["price"] * qty
            })
            
    if override_bat:
        bat_display_list = [f"{b['qty']}x {b['brand']} ({b['total_cap']} kWh) - (${b['total_price']})" for b in all_possible_bats]
        selected_bat_str = st.selectbox("اختر البطارية يدوياً:", options=bat_display_list)
        chosen_bat = all_possible_bats[bat_display_list.index(selected_bat_str)]
    else:
        chosen_bat = auto_bat_combo

st.markdown("---")

# 4. زر الحساب وإظهار النتائج
if st.button("🚀 عرض نتائج المنظومة والتكلفة الإجمالية", type="primary", use_container_width=True):
    
    # حسابات السلاسل والتكاليف
    max_string = chosen_panel["max_string_size"]
    num_strings = math.ceil(final_panels / max_string)
    
    ac_board_cost = get_ac_board_price(day_amp)
    panels_cost = final_panels * chosen_panel["price"]
    dc_acc_cost = num_strings * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = chosen_inverter["price"]
    bat_cost = chosen_bat["total_price"]
    
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE
    
    # حسابات شحن الـ AC المعتمدة على داتا شيت الجهاز (80% من تيار الشحن، 210V، جهد بطارية 51.5V)
    actual_charge_idc = chosen_inverter["max_charge_idc"] * 0.80
    charge_power_w = actual_charge_idc * 51.5
    charge_iac_210v = charge_power_w / (210.0 * 0.95)
    
    # ----------------------------------------------------
    # التنبيهات والاقتراحات الفنية
    # ----------------------------------------------------
    st.subheader("💡 التنبيهات والاقتراحات الفنية")
    
    if chosen_inverter["power_kw"] < recommended_kw:
        st.error(f"⚠️ **تنبيه خطأ/نقص قدرة:** قدرة الإنفرتر المختار ({chosen_inverter['power_kw']} kW) أقل من أحمال النهار المطلوبة مع هامش الأمان ({recommended_kw:.2f} kW). قد يتوقف الجهاز عند تشغيل كامل الأحمال.")
    elif chosen_inverter["power_kw"] > recommended_kw * 1.3:
        st.info(f"💡 **اقتراح توسعة:** الإنفرتر المختار ({chosen_inverter['power_kw']} kW) أكبر من احتياجك الحالي، وهو خيار ممتاز يتيح لك إضافة أحمال أو ألواح شمسية مستقبلاً.")
    else:
        st.success(f"✅ **الإنفرتر:** قدرة الإنفرتر متوافقة تماماً مع الأحمال المطلوبة.")
        
    actual_hours = chosen_bat["total_cap"] / (0.285 * night_amp)
    actual_amp_available = chosen_bat["total_cap"] / (0.285 * night_hours)
    
    if chosen_bat["total_cap"] < req_kwh * 0.95:
        st.warning(f"⚠️ **تنبيه سعة البطارية:** سعة البطارية المختارة ({chosen_bat['total_cap']} kWh) أقل من المطلوب ليلاً ({req_kwh:.2f} kWh). ستكفي لتشغيل {night_amp} أمبير لمدة **{actual_hours:.2f} ساعة فقط** بدلاً من {night_hours} ساعات.")
    else:
        st.success(f"✅ **البطارية:** سعة البطارية تغطي ساعات التشغيل الليلي المطلوب وزيادة.")

    st.markdown("---")

    # الملاحظات الحسابية المحددة والخاصة بك
    st.info(f"ℹ️ **ملاحظة حسابية (1):** كمية الأمبيرات التي يمكن أخذها من بنك البطاريات المختار خلال ({night_hours}) ساعات هي: **{actual_amp_available:.2f} أمبير**.")
    st.info(f"ℹ️ **ملاحظة حسابية (2):** عدد الساعات التي يمكن خلالها استخدام بنك البطاريات المختار عند سحب ({night_amp}) أمبير هي: **{int(actual_hours)} ساعات و {int((actual_hours % 1) * 60)} دقيقة**.")
    
    # ملاحظة كابل الـ AC من الشبكة الوطنية بناءً على الداتا شيت والمعايير المعتمدة
    st.warning(
        f"🔌 **ملاحظة توصيل كابل الشحن من الشبكة الوطنية (210V):**\n\n"
        f"عند ضبط تيار الشحن على النسبة الآمنة **80%** ({actual_charge_idc:.1f}A DC) لحماية الجهاز، "
        f"يكون تيار الـ AC المسحوب من الوطنية حوالي **{charge_iac_210v:.1f} أمبير**.\n\n"
        f"📌 **المقطع الأدنى المعتمد لكابل الـ AC الرباعي (4-Core):** **({chosen_inverter['cable_spec']})**."
    )

    st.markdown("---")

    # جدول المواد والتفاصيل
    st.subheader("📋 جدول المواد والتفاصيل - شركة ركن التعمير")
    
    table_data = [
        {"المكون / الملحق": "الألواح الشمسية", "المواصفات والوصف": f"لوح {chosen_panel['brand']} (شامل الهيكل والتركيب)", "الكمية": f"{final_panels} لوحاً", "سعر الوحدة ($)": f"${chosen_panel['price']}", "الإجمالي ($)": f"${panels_cost}"},
        {"المكون / الملحق": "ملحقات الـ DC", "المواصفات والوصف": "أسلاك + قواطع + فيوزات + MC4 + أنابيب", "الكمية": f"{num_strings} سلاسل", "سعر الوحدة ($)": f"${DC_ACCESSORIES_PRICE_PER_STRING}", "الإجمالي ($)": f"${dc_acc_cost}"},
        {"المكون / الملحق": "العاكس الهجين المختار", "المواصفات والوصف": f"{chosen_inverter['power_kw']} kW - {chosen_inverter['brand']} ({chosen_inverter['model']})", "الكمية": "1", "سعر الوحدة ($)": f"${inv_cost}", "الإجمالي ($)": f"${inv_cost}"},
        {"المكون / الملحق": "بنك البطاريات", "المواصفات والوصف": f"{chosen_bat['brand']} ({chosen_bat['unit_cap']} kWh)", "الكمية": f"{chosen_bat['qty']}", "سعر الوحدة ($)": f"${chosen_bat['unit_price']}", "الإجمالي ($)": f"${bat_cost}"},
        {"المكون / الملحق": "بورد الـ AC", "المواصفات والوصف": f"بورد حماية AC لغاية ({day_amp}A)", "الكمية": "1", "سعر الوحدة ($)": f"${ac_board_cost}", "الإجمالي ($)": f"${ac_board_cost}"},
        {"المكون / الملحق": "منظومة التأريض", "المواصفات والوصف": "وتد نحاسي + أسلاك 30m + مادة تأريض + الحفر والربط", "الكمية": "1", "سعر الوحدة ($)": f"${EARTHING_SYSTEM_PRICE}", "الإجمالي ($)": f"${EARTHING_SYSTEM_PRICE}"},
    ]
    
    st.table(table_data)

    # الكلفة الإجمالية
    st.subheader("💰 الكلفة الإجمالية النهائية")
    st.success(f"**الكلفة الإجمالية المباشرة للمشروع بناءً على اختيار الماركات: ${total_cost:,}**")
