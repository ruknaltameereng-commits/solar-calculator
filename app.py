import streamlit as st
import math

# ==========================================
# 1. إعدادات الصفحة والقائمة الجانبية للتحكم
# ==========================================
st.set_page_config(
    page_title="شركة ركن التعمير - حاسبة المنظومات الشمسية",
    page_icon="☀️",
    layout="wide"
)

# مفتاح تحكم لإظهار أو إخفاء المعادلات الحسابية
with st.sidebar:
    st.header("⚙️ إعدادات العرض")
    show_formulas = st.toggle("إظهار المعادلات والآلية الحسابية", value=False)
    st.caption("تفعيل هذا الخيار سيظهر الشرح الرياضي والمعادلات المستخدمة في الحسابات.")

# ==========================================
# 2. البيانات الفنية الرسمية والأسعار
# ==========================================

PANEL_OPTIONS = [
    {"brand": "Jinko Solar 725W (Voc 49.12V)", "power_w": 725, "price": 175, "max_string_size": 9},
    {"brand": "Longi Solar 640W (Voc 53.70V)", "power_w": 640, "price": 165, "max_string_size": 8}
]

DC_ACCESSORIES_PRICE_PER_STRING = 30
EARTHING_SYSTEM_PRICE = 160

INVERTER_BRANDS = [
    # Hybrid Inverters
    {"brand": "Deye Hybrid", "model": "SUN-5K-SG04LP1-EU-SM2", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-6K-SG04LP1-EU-SM2", "power_kw": 6.0, "price": 875, "phase": "single", "type": "Hybrid", "max_charge_idc": 135, "cable_spec": "4 x 6 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-8K-SG05LP1-EU-SM2", "power_kw": 8.0, "price": 1225, "phase": "single", "type": "Hybrid", "max_charge_idc": 190, "cable_spec": "4 x 10 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-12K-SG02LP1-EU-AM3", "power_kw": 12.0, "price": 1800, "phase": "single", "type": "Hybrid", "max_charge_idc": 250, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye Hybrid", "model": "SUN-16K-SG01LP1-EU", "power_kw": 16.0, "price": 2000, "phase": "single", "type": "Hybrid", "max_charge_idc": 290, "cable_spec": "4 x 16 mm²"},

    {"brand": "Solis Hybrid", "model": "S6-EH1P5K-L-PLUS", "power_kw": 5.0, "price": 750, "phase": "single", "type": "Hybrid", "max_charge_idc": 112, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis Hybrid", "model": "S6-EH1P6K-L-PLUS", "power_kw": 6.0, "price": 800, "phase": "single", "type": "Hybrid", "max_charge_idc": 135, "cable_spec": "4 x 6 mm²"},
    {"brand": "Solis Hybrid", "model": "S6-EH1P8K-L-PLUS", "power_kw": 8.0, "price": 1300, "phase": "single", "type": "Hybrid", "max_charge_idc": 190, "cable_spec": "4 x 10 mm²"},
    {"brand": "Solis Hybrid", "model": "S6-EH1P10K-L-PLUS", "power_kw": 10.0, "price": 1650, "phase": "single", "type": "Hybrid", "max_charge_idc": 210, "cable_spec": "4 x 10 mm²"},
    {"brand": "Solis Hybrid", "model": "S6-EH1P12K03-NV-YD-L", "power_kw": 12.0, "price": 1900, "phase": "single", "type": "Hybrid", "max_charge_idc": 250, "cable_spec": "4 x 16 mm²"},
    {"brand": "Solis Hybrid", "model": "S6-EH1P16K03-NV-YD-L", "power_kw": 16.0, "price": 2100, "phase": "single", "type": "Hybrid", "max_charge_idc": 290, "cable_spec": "4 x 16 mm²"},

    # Off-Grid Inverters
    {"brand": "Deye Off-Grid", "model": "SUN-6K-OG", "power_kw": 6.0, "price": 700, "phase": "single", "type": "Off-Grid", "max_charge_idc": 120, "cable_spec": "4 x 4 mm²"},
    {"brand": "SRNE Off-Grid", "model": "SRNE-16K-IP20", "power_kw": 16.0, "price": 1600, "phase": "single", "type": "Off-Grid", "max_charge_idc": 200, "cable_spec": "4 x 10 mm²"},
    {"brand": "Growatt Off-Grid", "model": "SPF 5000 ES", "power_kw": 5.0, "price": 650, "phase": "single", "type": "Off-Grid", "max_charge_idc": 100, "cable_spec": "4 x 4 mm²"},

    # On-Grid Inverters
    {"brand": "Solis On-Grid", "model": "S6-GR1P5K", "power_kw": 5.0, "price": 500, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 4 mm²"},
    {"brand": "Solis On-Grid", "model": "S6-GR1P10K", "power_kw": 10.0, "price": 950, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 10 mm²"},
    {"brand": "Deye On-Grid", "model": "SUN-16K-G04", "power_kw": 16.0, "price": 1300, "phase": "single", "type": "On-Grid", "max_charge_idc": 0, "cable_spec": "4 x 16 mm²"},

    # High Voltage / 3-Phase Systems
    {"brand": "Deye HV 3-Phase", "model": "SUN-30K-SG01HP3", "power_kw": 30.0, "price": 3800, "phase": "three", "type": "Hybrid", "max_charge_idc": 100, "cable_spec": "4 x 16 mm²"},
    {"brand": "Deye HV 3-Phase", "model": "SUN-50K-SG01HP3", "power_kw": 50.0, "price": 5200, "phase": "three", "type": "Hybrid", "max_charge_idc": 150, "cable_spec": "4 x 25 mm²"}
]

# تم الإبقاء فقط على بطاريات أُوكلي (AOKLY) وبيكودي (BICODI)
BATTERIES = [
    {"name": "AOKLY جدارية / أرضية", "capacity_kwh": 10.24, "price": 1350},
    {"name": "BICODI Lithuim", "capacity_kwh": 10.24, "price": 1300},
    {"name": "BICODI Lithuim", "capacity_kwh": 12.0, "price": 1450},
    {"name": "AOKLY بعجلات", "capacity_kwh": 15.0, "price": 1700},
    {"name": "BICODI Lithuim", "capacity_kwh": 15.0, "price": 1650},
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
        return 550

def calculate_panels_auto(day_current, required_battery_kwh, selected_panel):
    panel_watt = selected_panel["power_w"]
    max_string = selected_panel["max_string_size"]
    
    day_power_w = day_current * 230 * 1.3
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    
    total_panels_raw = (day_power_w + charging_power_w) / panel_watt
    target_panels = math.ceil(total_panels_raw)
    
    for num_strings in range(1, 15):
        panels_per_string = math.ceil(target_panels / num_strings)
        if panels_per_string <= max_string:
            return panels_per_string * num_strings, num_strings, panels_per_string
    return target_panels, 1, target_panels

def determine_inverter_size_and_qty(req_kw, target_phase, sys_type="Hybrid"):
    filtered_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == target_phase and inv["type"] == sys_type]
    
    if not filtered_inverters:
        filtered_inverters = [inv for inv in INVERTER_BRANDS if inv["phase"] == target_phase]

    best_option = None
    min_qty = 999
    min_price = 999999
    
    for inv in filtered_inverters:
        for qty in range(1, 5):
            total_power = inv["power_kw"] * qty
            if total_power >= req_kw:
                if qty < min_qty or (qty == min_qty and inv["price"] * qty < min_price):
                    min_qty = qty
                    min_price = inv["price"] * qty
                    best_option = {"target_power_kw": inv["power_kw"], "qty": qty}
                    
    return best_option

def determine_battery_size_and_qty(req_kwh):
    all_combos = []
    for bat in BATTERIES:
        for qty in range(1, 6):
            total_cap = bat["capacity_kwh"] * qty
            diff = total_cap - req_kwh
            if diff >= -0.2:  # السماح بنسبة بسيطة جداً
                all_combos.append({
                    "unit_cap": bat["capacity_kwh"],
                    "qty": qty,
                    "total_cap": round(total_cap, 2),
                    "diff": diff
                })
    
    if all_combos:
        # ترتيب حسب الأقرب للحاجة أولاً، ثم حسب التكلفة والعدد الأقل
        all_combos.sort(key=lambda x: (x["diff"], x["qty"]))
        return all_combos[0]
    return {"unit_cap": 10.24, "qty": 1, "total_cap": 10.24}

# ==========================================
# 4. واجهة المستخدم (User Interface)
# ==========================================
st.title("☀️ حاسبة وتصميم المنظومات الشمسية - شركة ركن التعمير")
st.caption(" اعداد المهندس محمد النوري والمهندسة زينة الحمداني برمجة وتصميم هندسي مخصص للحسابات الدقيقة واختيار الأجهزة والتعديل التفاعلي")

st.markdown("---")

# 1. إدخال أحمال المنظومة
st.subheader("📥 1. إدخال أحمال المنظومة")
col1, col2, col3 = st.columns(3)

with col1:
    day_amp = st.number_input("أمبير النهار (ن)", min_value=1, max_value=300, value=100, step=1)

with col2:
    night_amp = st.number_input("أمبير الليل (ل)", min_value=1, max_value=300, value=60, step=1)

with col3:
    night_hours = st.number_input("ساعات التشغيل الليلي (س)", min_value=1, max_value=24, value=4, step=1)

is_hv_3ph = st.checkbox("تطبيق نظام HV-3PH (ثلاثي الأطوار / High Voltage)", value=False)

st.markdown("---")

# 2. الحسابات التلقائية الأولية
load_kw = (day_amp * 230) / 1000.0
recommended_kw = load_kw * 1.2
req_kwh = night_amp * 0.285 * night_hours
target_phase = "three" if is_hv_3ph else "single"

# 3. قسم خيارات التعديل اليدوي المباشر
st.subheader("⚙️ 2. تحديد نوع المنظومة والماركات والمواصفات")

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
        final_panels = st.number_input("حدد عدد الألواح المطلوب:", min_value=1, max_value=200, value=auto_panels, step=1)
    else:
        final_panels = auto_panels

# --- اختيار نوع المنظومة وماركة الإنفرتر ---
with col_i:
    st.markdown("##### 🔌 الإنفرتر الهجين / العاكس")
    
    selected_system_type = st.selectbox(
        "نوع نظام الإنفرتر:",
        options=["Hybrid", "Off-Grid", "On-Grid"],
        index=0
    )
    
    inv_spec = determine_inverter_size_and_qty(recommended_kw, target_phase, sys_type=selected_system_type)
    
    if inv_spec:
        target_size = inv_spec["target_power_kw"]
        inv_qty = inv_spec["qty"]
        total_power = target_size * inv_qty
        
        st.info(f"📌 **قدرة الجهاز المناسب:** `{target_size} kW` | **العدد:** `{inv_qty}` (إجمالي `{total_power} kW`)")
        
        matching_brands = [
            inv for inv in INVERTER_BRANDS 
            if inv["phase"] == target_phase and inv["power_kw"] == target_size and inv["type"] == selected_system_type
        ]
        
        if not matching_brands:
            matching_brands = [
                inv for inv in INVERTER_BRANDS 
                if inv["phase"] == target_phase and inv["power_kw"] == target_size
            ]
        
        if matching_brands:
            brand_options = [f"{inv['brand']} [{inv['model']}] - (${inv['price'] * inv_qty} إجمالي)" for inv in matching_brands]
            selected_brand_str = st.selectbox(
                f"اختر الماركة المتوفرة بحجم ({target_size} kW):",
                options=brand_options
            )
            chosen_single_inv = matching_brands[brand_options.index(selected_brand_str)]
            
            chosen_inv_combo = {
                "inverter": chosen_single_inv,
                "qty": inv_qty,
                "total_power": total_power,
                "total_price": chosen_single_inv["price"] * inv_qty
            }
        else:
            st.warning(f"لا تتوفر ماركات حالياً بحجم {target_size} kW.")
            chosen_inv_combo = None
    else:
        st.error("الحمل كبير جداً، يرجى مراجعة المهندس المختص.")
        chosen_inv_combo = None

# --- اختيار البطارية المناسبة بناءً على الحمل وتحديد الماركة ---
with col_b:
    st.markdown("##### 🔋 بنك البطاريات")
    
    if selected_system_type == "On-Grid":
        st.caption("ℹ️ نظام On-Grid لا يحتاج إلى بطاريات لتخزين الطاقة.")
        chosen_bat = {"brand": "بدون بطاريات (نظام On-Grid)", "unit_cap": 0, "total_cap": 0, "qty": 0, "unit_price": 0, "total_price": 0}
    else:
        bat_spec = determine_battery_size_and_qty(req_kwh)
        target_bat_cap = bat_spec["unit_cap"]
        bat_qty = bat_spec["qty"]
        total_bat_cap = bat_spec["total_cap"]
        
        st.info(f"📌 **حجم البطارية المناسب:** `{target_bat_cap} kWh` | **العدد:** `{bat_qty}` (إجمالي `{total_bat_cap} kWh`)")
        
        matching_batteries = [b for b in BATTERIES if b["capacity_kwh"] == target_bat_cap]
        
        if not matching_batteries:
            matching_batteries = BATTERIES
            
        bat_brand_options = [f"{b['name']} ({b['capacity_kwh']} kWh) - (${b['price'] * bat_qty} إجمالي)" for b in matching_batteries]
        selected_bat_brand_str = st.selectbox(
            f"اختر الماركة المتوفرة بحجم ({target_bat_cap} kWh):",
            options=bat_brand_options
        )
        chosen_single_bat = matching_batteries[bat_brand_options.index(selected_bat_brand_str)]
        
        chosen_bat = {
            "brand": chosen_single_bat["name"],
            "unit_cap": chosen_single_bat["capacity_kwh"],
            "total_cap": total_bat_cap,
            "qty": bat_qty,
            "unit_price": chosen_single_bat["price"],
            "total_price": chosen_single_bat["price"] * bat_qty
        }

st.markdown("---")

# 4. زر الحساب وإظهار النتائج
if st.button("🚀 عرض نتائج المنظومة والتكلفة الإجمالية", type="primary", use_container_width=True):
    if chosen_inv_combo is None:
        st.error("يرجى اختيار ماركة إنفرتر متوفرة أولاً.")
    else:
        # حسابات السلاسل والتكاليف
        max_string = chosen_panel["max_string_size"]
        num_strings = math.ceil(final_panels / max_string)
        
        ac_board_cost = get_ac_board_price(day_amp)
        panels_cost = final_panels * chosen_panel["price"]
        dc_acc_cost = num_strings * DC_ACCESSORIES_PRICE_PER_STRING
        inv_cost = chosen_inv_combo["total_price"]
        bat_cost = chosen_bat["total_price"]
        
        total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE
        
        single_inv = chosen_inv_combo["inverter"]
        inv_qty = chosen_inv_combo["qty"]
        total_inv_kw = chosen_inv_combo["total_power"]
        
        actual_charge_idc = single_inv["max_charge_idc"] * 0.80 * inv_qty
        charge_power_w = actual_charge_idc * 51.5
        charge_iac_210v = charge_power_w / (210.0 * 0.95) if charge_power_w > 0 else 0

        # ====================================================
        # 📐 عرض المعادلات الرياضية (إذا تم تفعيل الخيار من قبلك)
        # ====================================================
        if show_formulas:
            st.subheader("📐 المعادلات الرياضية والآلية الحسابية للمنظومة")
            day_p_val = day_amp * 230 * 1.3
            chg_p_val = (req_kwh * 1000) / 9.0
            
            st.write(f"1. قدرة أحمال النهار المطلوبة: **{load_kw:.2f} kW**")
            st.latex(r"\text{Load Power (kW)} = \frac{\text{Day Amp} \times 230}{1000}")
            
            st.write(f"2. السعة المطلوبة للبطاريات ليلاً: **{req_kwh:.2f} kWh**")
            st.latex(r"\text{Battery kWh} = \text{Night Amp} \times 0.285 \times \text{Night Hours}")
            
            st.write(f"3. إجمالي الألواح الشمسية المطلوبة: **{final_panels} لوحاً**")
            st.latex(rf"\text{{Day Power}} = {day_amp} \times 230 \times 1.3 = {day_p_val:.0f}\text{{ W}}")
            st.latex(rf"\text{{Charging Power}} = \frac{{{req_kwh:.2f} \times 1000}}{{9.0}} = {chg_p_val:.0f}\text{{ W}}")
            
            st.write(f"4. حساب تيار الشحن المسحوب من الوطنية (AC): **{charge_iac_210v:.1f} A**")
            st.latex(rf"\text{{DC Charge Current (80\%)}} = {actual_charge_idc:.1f}\text{{ A (DC)}}")
            st.latex(rf"\text{{AC Current at 210V}} = \frac{{{actual_charge_idc:.1f} \times 51.5}}{{210 \times 0.95}} = {charge_iac_210v:.1f}\text{{ A (AC)}}")
            st.markdown("---")

        # ----------------------------------------------------
        # التنبيهات والاقتراحات الفنية
        # ----------------------------------------------------
        st.subheader("💡 التنبيهات والاقتراحات الفنية")
        
        st.success(f"✅ **الإنفرتر المختار:** تم اختيار **({inv_qty})** جهاز من نوع **[{single_inv['type']}]** ماركة **{single_inv['brand']}** موديل **[{single_inv['model']}]** بحجم **{single_inv['power_kw']} kW** لكل جهاز (إجمالي قدرة **{total_inv_kw} kW**).")
            
        if selected_system_type != "On-Grid":
            actual_hours = chosen_bat["total_cap"] / (0.285 * night_amp) if night_amp > 0 else 0
            actual_amp_available = chosen_bat["total_cap"] / (0.285 * night_hours) if night_hours > 0 else 0
            
            if chosen_bat["total_cap"] < req_kwh * 0.95:
                st.warning(f"⚠️ **تنبيه سعة البطارية:** سعة البطارية المختارة ({chosen_bat['total_cap']} kWh) أقل من المطلوب ليلاً ({req_kwh:.2f} kWh). ستكفي لتشغيل {night_amp} أمبير لمدة **{actual_hours:.2f} ساعة فقط** بدلاً من {night_hours} ساعات.")
            else:
                st.success(f"✅ **البطارية المختارة:** تم اختيار **({chosen_bat['qty']})** بطارية ماركة **{chosen_bat['brand']}** بسعة **{chosen_bat['unit_cap']} kWh** لكل وحدة (إجمالي سعة **{chosen_bat['total_cap']} kWh**).")

            st.markdown("---")

            st.info(f"ℹ️ **ملاحظة حسابية (1):** كمية الأمبيرات التي يمكن أخذها من بنك البطاريات المختار خلال ({night_hours}) ساعات هي: **{actual_amp_available:.2f} أمبير**.")
            st.info(f"ℹ️ **ملاحظة حسابية (2):** عدد الساعات التي يمكن خلالها استخدام بنك البطاريات المختار عند سحب ({night_amp}) أمبير هي: **{int(actual_hours)} ساعات و {int((actual_hours % 1) * 60)} دقيقة**.")
            
            if charge_iac_210v > 0:
                st.warning(
                    f"🔌 **ملاحظة توصيل كابل الشحن من الشبكة الوطنية (210V):**\n\n"
                    f"عند ضبط تيار الشحن على النسبة الآمنة **80%** للأجهزة ({actual_charge_idc:.1f}A DC إجمالي)، "
                    f"يكون تيار الـ AC الإجمالي المسحوب من الوطنية حوالي **{charge_iac_210v:.1f} أمبير**.\n\n"
                    f"📌 **المقطع الأدنى المعتمد لكابل الـ AC الرباعي (4-Core):** **({single_inv['cable_spec']}) لكل إنفرتر**."
                )

        st.markdown("---")

        # جدول المواد والتفاصيل
        st.subheader("📋 جدول المواد والتفاصيل - شركة ركن التعمير")
        
        table_data = [
            {"المكون / الملحق": "الألواح الشمسية", "المواصفات والوصف": f"لوح {chosen_panel['brand']} (شامل الهيكل والتركيب)", "الكمية": f"{final_panels} لوحاً", "سعر الوحدة ($)": f"${chosen_panel['price']}", "الإجمالي ($)": f"${panels_cost}"},
            {"المكون / الملحق": "ملحقات الـ DC", "المواصفات والوصف": "أسلاك + قواطع + فيوزات + MC4 + أنابيب", "الكمية": f"{num_strings} سلاسل", "سعر الوحدة ($)": f"${DC_ACCESSORIES_PRICE_PER_STRING}", "الإجمالي ($)": f"${dc_acc_cost}"},
            {"المكون / الملحق": "العاكس / الإنفرتر", "المواصفات والوصف": f"{inv_qty}x {single_inv['brand']} ({single_inv['model']}) - [{single_inv['type']}]", "الكمية": f"{inv_qty}", "سعر الوحدة ($)": f"${single_inv['price']}", "الإجمالي ($)": f"${inv_cost}"},
            {"المكون / الملحق": "بنك البطاريات", "المواصفات والوصف": f"{chosen_bat['brand']} ({chosen_bat['unit_cap']} kWh)" if chosen_bat['qty'] > 0 else "بدون بطاريات", "الكمية": f"{chosen_bat['qty']}", "سعر الوحدة ($)": f"${chosen_bat['unit_price']}", "الإجمالي ($)": f"${bat_cost}"},
            {"المكون / الملحق": "بورد الـ AC", "المواصفات والوصف": f"بورد حماية وتوازي AC لغاية ({day_amp}A)", "الكمية": "1", "سعر الوحدة ($)": f"${ac_board_cost}", "الإجمالي ($)": f"${ac_board_cost}"},
            {"المكون / الملحق": "منظومة التأريض", "المواصفات والوصف": "وتد نحاسي + أسلاك 30m + مادة تأريض + الحفر والربط", "الكمية": "1", "سعر الوحدة ($)": f"${EARTHING_SYSTEM_PRICE}", "الإجمالي ($)": f"${EARTHING_SYSTEM_PRICE}"},
        ]
        
        st.table(table_data)

        st.subheader("💰 الكلفة الإجمالية النهائية")
        st.success(f"**الكلفة الإجمالية المباشرة للمشروع بناءً على اختيار الماركات: ${total_cost:,}**")
