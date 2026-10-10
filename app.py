import streamlit as st

# solar_system_calculator.py
# ==============================================================================
# برنامج حساب وتصحيح المنظومات الشمسية - إعداد المهندس مراد
# ==============================================================================

import math

# ------------------------------------------------------------------------------
# 1. سُلم الأسعار والمعايير الفنية المعتمدة (System Rules & Pricing Matrix)
# ------------------------------------------------------------------------------

PANEL_SPECS = {
    "power_w": 640,
    "price_per_unit": 175,  # شامل الهيكل والتركيب
    "max_string_size": 9,   # الحد الأقصى للألواح بالسلسلة الواحدة
}

DC_ACCESSORIES_PRICE_PER_STRING = 30  # أسلاك 40m + قاطع DC + فيوزات + MC4 + أنابيب

INVERTERS = [
    {"name": "Growatt 6 kW (IP21)", "power_kw": 6.0, "price": 400, "phase": "single"},
    {"name": "Deye / Solis 6 kW (IP65)", "power_kw": 6.0, "price": 1350, "phase": "single"},
    {"name": "Deye / Solis 8 kW (IP65)", "power_kw": 8.0, "price": 1550, "phase": "single"},
    {"name": "Deye 10 kW (IP65)", "power_kw": 10.0, "price": 1750, "phase": "single"},
    {"name": "Deye 12 kW Single Phase", "power_kw": 12.0, "price": 1900, "phase": "single"},
    {"name": "Deye High Voltage 30 kW 3-Phase", "power_kw": 30.0, "price": 3800, "phase": "three"},
    {"name": "Deye High Voltage 50 kW 3-Phase", "power_kw": 50.0, "price": 5200, "phase": "three"}
]

BATTERIES = [
    {"name": "AOKLY جدارية / أرضية", "capacity_kwh": 10.24, "price": 1350},
    {"name": "BICODI", "capacity_kwh": 12.0, "price": 1450},
    {"name": "AOKLY بعجلات", "capacity_kwh": 15.0, "price": 1700},
    {"name": "BICODI", "capacity_kwh": 16.1, "price": 1850},
    {"name": "BICODI", "capacity_kwh": 17.66, "price": 2100},
]

EARTHING_SYSTEM_PRICE = 160  # وتد نحاسي + أسلاك 30m + مادة تأريض + الحفر والربط


# ------------------------------------------------------------------------------
# 2. القواعد والدوال الحسابية (Engine Calculations)
# ------------------------------------------------------------------------------

def get_ac_board_price(current_amp):
    """تحديد سعر بورد الـ AC بناءً على الأمبيرية النهارية"""
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
        return 0  # تخضع لتقدير المهندس للكشف النهائي


def calculate_battery_bank(night_current, night_hours):
    """معادلة طاقة البطاريات: Energy (kWh) = Current (A) * 0.285 * Hours (h)"""
    required_kwh = night_current * 0.285 * night_hours
    
    best_option = None
    min_diff = float('inf')
    
    for bat in BATTERIES:
        # فحص وحدة واحدة
        if bat["capacity_kwh"] >= required_kwh:
            diff = bat["capacity_kwh"] - required_kwh
            if diff < min_diff:
                min_diff = diff
                best_option = {"model": bat["name"], "capacity": bat["capacity_kwh"], "qty": 1, "price": bat["price"]}
        # فحص وحدتين بالتوازي
        elif (bat["capacity_kwh"] * 2) >= required_kwh:
            diff = (bat["capacity_kwh"] * 2) - required_kwh
            if diff < min_diff:
                min_diff = diff
                best_option = {"model": bat["name"], "capacity": bat["capacity_kwh"], "qty": 2, "price": bat["price"]}
                
    return required_kwh, best_option


def calculate_panels(day_current, required_battery_kwh):
    """
    معادلة الألواح المعتمدة:
    1. ألواح النهار = (التيار * 230 * 1.3) / 640
    2. ألواح الشحن = ((طاقة البطارية * 1000) / 9) / 640
    3. تحقيق شرط التساوي بالسلاسل والحد الأقصى 9 ألواح/سلسلة
    """
    day_power_w = day_current * 230 * 1.3
    day_panels_exact = day_power_w / PANEL_SPECS["power_w"]
    
    charging_power_w = (required_battery_kwh * 1000) / 9.0
    charging_panels_exact = charging_power_w / PANEL_SPECS["power_w"]
    
    total_panels_raw = day_panels_exact + charging_panels_exact
    target_panels = math.ceil(total_panels_raw)
    
    for num_strings in range(1, 10):
        panels_per_string = math.ceil(target_panels / num_strings)
        if panels_per_string <= PANEL_SPECS["max_string_size"]:
            final_panel_count = panels_per_string * num_strings
            return {
                "total_panels": final_panel_count,
                "strings_count": num_strings,
                "panels_per_string": panels_per_string
            }


def select_inverter(day_current):
    """اختيار العاكس بحساب هامش أمان +20% على الأحمال النهارية"""
    load_kw = (day_current * 230) / 1000.0
    required_kw_with_safety = load_kw * 1.2
    
    for inv in INVERTERS:
        if inv["power_kw"] >= required_kw_with_safety and inv["phase"] == "single":
            return inv
    return INVERTERS[-1]


# ------------------------------------------------------------------------------
# 3. دالة المعالجة والتسعير (Core System Engine)
# ------------------------------------------------------------------------------

def process_solar_request(day_amp, night_amp, night_hours):
    req_kwh, bat_selected = calculate_battery_bank(night_amp, night_hours)
    panels_info = calculate_panels(day_amp, req_kwh)
    inverter = select_inverter(day_amp)
    ac_board_cost = get_ac_board_price(day_amp)
    
    # التكاليف
    panels_cost = panels_info["total_panels"] * PANEL_SPECS["price_per_unit"]
    dc_acc_cost = panels_info["strings_count"] * DC_ACCESSORIES_PRICE_PER_STRING
    inv_cost = inverter["price"]
    bat_cost = bat_selected["price"] * bat_selected["qty"]
    
    total_cost = panels_cost + dc_acc_cost + inv_cost + bat_cost + ac_board_cost + EARTHING_SYSTEM_PRICE
    
    # طباعة التقرير الفني والتسعيري
    print("\n" + "="*60)
    print(f"📊 التقرير الفني وعرض السعر للمنظومة: ({day_amp}ن {night_amp}ل {night_hours}س)")
    print("="*60)
    print(f"1. بنك البطاريات : {bat_selected['qty']}x {bat_selected['model']} ({bat_selected['capacity']} kWh) -> ${bat_cost}")
    print(f"2. الألواح الشمسية: {panels_info['total_panels']} لوح ({panels_info['strings_count']} سلاسل × {panels_info['panels_per_string']} ألواح) -> ${panels_cost}")
    print(f"3. ملحقات الـ DC   : {panels_info['strings_count']} سلاسل -> ${dc_acc_cost}")
    print(f"4. العاكس الهجين  : {inverter['name']} -> ${inv_cost}")
    print(f"5. بورد الـ AC     : أمبيرية ({day_amp}A) -> ${ac_board_cost if ac_board_cost > 0 else 'تقدير مهندس'}")
    print(f"6. منظومة التأريض  : ثابتة وشاملة -> ${EARTHING_SYSTEM_PRICE}")
    print("-" * 60)
    print(f"💰 الإجمالي النهائي المباشر للمشروع: ${total_cost}")
    print("="*60 + "\n")


# ------------------------------------------------------------------------------
# 4. تشغيل تجريبي (مثال: 40ن 30ل 4س)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # يمكن إدخال أي قيمة بالترتيب: (أمبير النهار، أمبير الليل، ساعات الليل)
    process_solar_request(day_amp=40, night_amp=30, night_hours=4)
