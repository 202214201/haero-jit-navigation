import streamlit as st
import pandas as pd
import numpy as np
import joblib
import math

from datetime import datetime, timedelta
from lighthouse_hero import draw_lighthouse



# =========================================================
# 1. 웹 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="해로(海路) - 해상 내비게이션",
    layout="wide"
)


# =========================================================
# 2. 화면 전환 설정
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "main"


def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()


# =========================================================
# 3. 저장된 머신러닝 모델 불러오기
# =========================================================

@st.cache_resource
def load_models():

    xgb_model = joblib.load(
        "xgb_model.pkl"
    )

    rf_model = joblib.load(
        "rf_model.pkl"
    )

    ensemble_model = joblib.load(
        "ensemble_model.pkl"
    )

    return (
        xgb_model,
        rf_model,
        ensemble_model
    )


xgb_model, rf_model, ensemble_model = load_models()


# =========================================================
# 4. 사이드바
# =========================================================

with st.sidebar:

    st.markdown(
        "### 2026 해양산업 AX 아이디어 공모전"
    )

    st.markdown(
        "**팀명:** 넥서스 (NEXUS)"
    )

    st.markdown("---")

    if st.button(
        "🏠 메인 화면으로",
        use_container_width=True,
        key="sidebar_main"
    ):

        navigate_to(
            "main"
        )


# =========================================================
# 5. 메인 화면
# =========================================================

def main_page():

    # =====================================================
    # 1. 메인 배너
    # =====================================================

    st.image(
        "banner.png",
        use_container_width=True
    )


    # =====================================================
    # 2. 등대 표지 + 라이트/야간모드
    # =====================================================

    dark_mode = st.toggle(
        "🌙 야간모드",
        key="lighthouse_dark"
    )

    draw_lighthouse(
        "dark" if dark_mode else "light"
    )


    # =====================================================
    # 3. 소개 문구
    # =====================================================

    st.markdown(
        "### 바다 위의 하이패스, 대기 없는 항해를 시작하세요."
    )

    st.write("---")


    # =====================================================
    # 4. 메인 기능 메뉴
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.info(
            "📊 실시간 항만 상황"
        )

        if st.button(
            "실시간 항구 혼잡도",
            use_container_width=True,
            key="btn_congestion"
        ):

            navigate_to(
                "congestion"
            )


    with col2:

        st.success(
            "🌱 친환경 에코 운항"
        )

        if st.button(
            "E-co로 (에코로)",
            use_container_width=True,
            key="btn_ecoro"
        ):

            navigate_to(
                "ecoro"
            )


    with col3:

        st.warning(
            "🎫 스마트 타임슬롯"
        )

        if st.button(
            "입항 예약 (예약 보증금)",
            use_container_width=True,
            key="btn_reservation"
        ):

            navigate_to(
                "reservation"
            )


    with col4:

        st.error(
            "🧭 안전 접안 지원"
        )

        if st.button(
            "입항 가이드",
            use_container_width=True,
            key="btn_guide"
        ):

            navigate_to(
                "guide"
            )


# =========================================================
# 6. 실시간 항구 혼잡도
# =========================================================

def congestion_page():

    st.title(
        "📊 실시간 항구 혼잡도 맵"
    )

    st.markdown(
        "현재 항만 인근 해역의 구역별 선박 밀집도를 "
        "실시간으로 모니터링합니다."
    )


    # =====================================================
    # 항구 / 부두 / 묘박지 중심으로 선박 위치 생성
    # =====================================================

    np.random.seed(42)

    port_points = [
        {
            "name": "부산항 북항",
            "lat": 35.103,
            "lon": 129.040,
            "status": "제1부두 (혼잡)"
        },
        {
            "name": "감천항",
            "lat": 35.055,
            "lon": 129.006,
            "status": "제1부두 (혼잡)"
        },
        {
            "name": "부산항 신항",
            "lat": 35.075,
            "lon": 128.825,
            "status": "신항 (원활)"
        },
        {
            "name": "북항 외항 묘박지",
            "lat": 35.075,
            "lon": 129.075,
            "status": "외항 묘박지 (매우 혼잡)"
        },
        {
            "name": "감천항 외항 묘박지",
            "lat": 35.015,
            "lon": 129.020,
            "status": "외항 묘박지 (매우 혼잡)"
        },
        {
            "name": "신항 외항 묘박지",
            "lat": 35.040,
            "lon": 128.790,
            "status": "외항 묘박지 (매우 혼잡)"
        }
    ]

    ship_data = []

    for point in port_points:

        if point["status"] == "외항 묘박지 (매우 혼잡)":
            n_ships = 18

        elif point["status"] == "제1부두 (혼잡)":
            n_ships = 12

        else:
            n_ships = 7

        for _ in range(n_ships):

            ship_data.append({
                "lat":
                    point["lat"]
                    + np.random.normal(0, 0.0025),

                "lon":
                    point["lon"]
                    + np.random.normal(0, 0.0025),

                "상태":
                    point["status"]
            })

    map_df = pd.DataFrame(
        ship_data
    )

    color_map = {
        "외항 묘박지 (매우 혼잡)": "#FF0000",
        "제1부두 (혼잡)": "#FFA500",
        "신항 (원활)": "#00FF00"
    }

    map_df["color"] = (
        map_df["상태"]
        .map(color_map)
    )

    st.map(
        map_df,
        latitude="lat",
        longitude="lon",
        color="color",
        zoom=11
    )

    st.info(
        "💡 항구·부두·묘박지 주변의 선박 위치를 기반으로 "
        "항만 혼잡 상황을 시각화합니다."
    )


    # =====================================================
    # 머신러닝 혼잡도 예측
    # =====================================================

    st.write("---")

    st.subheader(
        "🤖 머신러닝 기반 항구 혼잡도 예측"
    )


    col1, col2, col3 = st.columns(3)


    # -----------------------------------------------------
    # 첫 번째 입력 그룹
    # -----------------------------------------------------

    with col1:

        vessels_in_port = st.number_input(
            "현재 항내 선박 수",
            min_value=0,
            max_value=100,
            value=38
        )

        waiting_vessels = st.number_input(
            "외항 대기 선박 수",
            min_value=0,
            max_value=50,
            value=9
        )

        berth_occupancy = st.slider(
            "선석 점유율 (%)",
            0,
            100,
            78
        )


    # -----------------------------------------------------
    # 두 번째 입력 그룹
    # -----------------------------------------------------

    with col2:

        arrivals_next_1h = st.number_input(
            "향후 1시간 입항 예정 선박 수",
            min_value=0,
            max_value=30,
            value=8
        )

        departures_next_1h = st.number_input(
            "향후 1시간 출항 예정 선박 수",
            min_value=0,
            max_value=30,
            value=5
        )

        crane_utilization = st.slider(
            "크레인 가동률 (%)",
            0,
            100,
            72
        )


    # -----------------------------------------------------
    # 세 번째 입력 그룹
    # -----------------------------------------------------

    with col3:

        yard_queue = st.number_input(
            "야드 트럭 대기 수",
            min_value=0,
            max_value=100,
            value=16
        )

        wind_speed = st.number_input(
            "풍속 (m/s)",
            min_value=0.0,
            max_value=30.0,
            value=5.0
        )

        wave_height = st.number_input(
            "파고 (m)",
            min_value=0.0,
            max_value=10.0,
            value=1.2
        )


    # =====================================================
    # 머신러닝 입력 데이터
    # =====================================================

    input_data = pd.DataFrame({

        "vessels_in_port":
            [vessels_in_port],

        "waiting_vessels":
            [waiting_vessels],

        "berth_occupancy":
            [berth_occupancy],

        "arrivals_next_1h":
            [arrivals_next_1h],

        "departures_next_1h":
            [departures_next_1h],

        "crane_utilization":
            [crane_utilization],

        "yard_queue":
            [yard_queue],

        "wind_speed":
            [wind_speed],

        "wave_height":
            [wave_height]
    })


    # =====================================================
    # 3개 모델 예측
    # =====================================================

    xgb_prediction = (
        xgb_model
        .predict(
            input_data
        )[0]
    )


    rf_prediction = (
        rf_model
        .predict(
            input_data
        )[0]
    )


    ensemble_prediction = (
        ensemble_model
        .predict(
            input_data
        )[0]
    )


    # 0 ~ 100 범위 제한
    xgb_prediction = np.clip(
        xgb_prediction,
        0,
        100
    )

    rf_prediction = np.clip(
        rf_prediction,
        0,
        100
    )

    ensemble_prediction = np.clip(
        ensemble_prediction,
        0,
        100
    )


    # =====================================================
    # 모델별 결과
    # =====================================================

    st.write("---")

    st.subheader(
        "📊 모델별 혼잡도 예측"
    )


    result1, result2, result3 = st.columns(3)


    result1.metric(
        "XGBoost",
        f"{xgb_prediction:.1f} / 100"
    )


    result2.metric(
        "Random Forest",
        f"{rf_prediction:.1f} / 100"
    )


    result3.metric(
        "앙상블 모델",
        f"{ensemble_prediction:.1f} / 100"
    )


    # =====================================================
    # 최종 혼잡도 = Ensemble
    # =====================================================

    prediction = ensemble_prediction


    if prediction < 40:

        congestion_status = (
            "🟢 원활"
        )


    elif prediction < 70:

        congestion_status = (
            "🟡 보통"
        )


    elif prediction < 85:

        congestion_status = (
            "🟠 혼잡"
        )


    else:

        congestion_status = (
            "🔴 매우 혼잡"
        )


    st.write("---")

    st.subheader(
        "🤖 최종 AI 판단"
    )


    result1, result2 = st.columns(2)


    result1.metric(
        "최종 혼잡도",
        f"{prediction:.1f} / 100"
    )


    result2.metric(
        "현재 항만 상태",
        congestion_status
    )


    st.progress(
        int(prediction)
    )


    # -----------------------------------------------------
    # 혼잡도에 따른 안내
    # -----------------------------------------------------

    if prediction >= 85:

        st.error(
            "현재 항만이 매우 혼잡합니다. "
            "입항 시간 조정을 권장합니다."
        )


    elif prediction >= 70:

        st.warning(
            "항만 혼잡도가 높습니다. "
            "E-co로 감속 운항을 고려하세요."
        )


    elif prediction >= 40:

        st.info(
            "현재 항만 상황은 보통 수준입니다."
        )


    else:

        st.success(
            "현재 항만 상황이 원활합니다."
        )


    # =====================================================
    # XGBoost 변수 중요도
    # =====================================================

    st.write("---")

    st.subheader(
        "📈 XGBoost 변수 중요도"
    )


    korean_names = {

        "vessels_in_port":
            "현재 항내 선박 수",

        "waiting_vessels":
            "외항 대기 선박 수",

        "berth_occupancy":
            "선석 점유율",

        "arrivals_next_1h":
            "향후 1시간 입항 예정 선박 수",

        "departures_next_1h":
            "향후 1시간 출항 예정 선박 수",

        "crane_utilization":
            "크레인 가동률",

        "yard_queue":
            "야드 트럭 대기 수",

        "wind_speed":
            "풍속",

        "wave_height":
            "파고"
    }


    importance_df = pd.DataFrame({

        "변수": [
            korean_names[col]
            for col in input_data.columns
        ],

        "중요도":
            xgb_model.feature_importances_
    })


    importance_df = (
        importance_df
        .sort_values(
            "중요도",
            ascending=False
        )
    )


    st.bar_chart(
        importance_df,
        x="변수",
        y="중요도"
    )


    # =====================================================
    # 뒤로가기
    # =====================================================

    st.write("---")

    if st.button(
        "⬅️ 뒤로가기",
        key="back_congestion"
    ):

        navigate_to(
            "main"
        )


# =========================================================
# 7. E-co로
# =========================================================

# =========================================================
# 7. E-co로
# =========================================================

def ecoro_page():

    st.title("🌱 E-co로 : JIT 최적 감속 운항")

    st.markdown(
        "선박의 현재 운항상태, 성능, 연료, 배출량, "
        "목적지 및 JIT 입항시간을 종합하여 "
        "최적 속도와 권고 방향을 계산합니다."
    )

    st.write("---")


    # =====================================================
    # 1. 선박 기본정보
    # =====================================================

    st.subheader("🚢 1. 선박 기본정보")

    col1, col2, col3 = st.columns(3)

    with col1:

        vessel_name = st.text_input(
            "선박명",
            value="NEXUS STAR"
        )

        vessel_type = st.selectbox(
            "선박 종류",
            [
                "컨테이너선",
                "벌크선",
                "유조선",
                "LNG선",
                "자동차운반선",
                "기타"
            ]
        )

    with col2:

        vessel_length = st.number_input(
            "선박 길이 (m)",
            min_value=50.0,
            max_value=500.0,
            value=300.0
        )

        draft = st.number_input(
            "흘수 (m)",
            min_value=1.0,
            max_value=30.0,
            value=12.0
        )

    with col3:

        displacement = st.number_input(
            "배수량 (ton)",
            min_value=1000.0,
            max_value=500000.0,
            value=80000.0
        )

        cargo_load = st.slider(
            "적재율 (%)",
            0,
            100,
            75
        )


    # =====================================================
    # 2. 현재 운항상태
    # =====================================================

    st.write("---")

    st.subheader("🧭 2. 현재 운항상태")

    col1, col2, col3 = st.columns(3)

    with col1:

        current_speed = st.number_input(
            "현재 속도 (knots)",
            min_value=0.0,
            max_value=35.0,
            value=15.0
        )

        current_heading = st.number_input(
            "현재 방향 (°)",
            min_value=0.0,
            max_value=359.0,
            value=75.0
        )

    with col2:

        engine_rpm = st.number_input(
            "현재 엔진 RPM",
            min_value=0.0,
            max_value=200.0,
            value=85.0
        )

        engine_load = st.slider(
            "엔진 부하 (%)",
            0,
            100,
            70
        )

    with col3:

        remaining_distance = st.number_input(
            "목적지까지 남은 거리 (NM)",
            min_value=1.0,
            max_value=5000.0,
            value=120.0
        )

        current_fuel = st.number_input(
            "현재 연료 보유량 (ton)",
            min_value=0.0,
            max_value=10000.0,
            value=500.0
        )


    # =====================================================
    # 3. 선박 성능모델
    # =====================================================

    st.write("---")

    st.subheader("⚙️ 3. 선박 성능모델")

    col1, col2, col3 = st.columns(3)

    with col1:

        design_speed = st.number_input(
            "설계 속도 (knots)",
            min_value=5.0,
            max_value=35.0,
            value=20.0
        )

    with col2:

        design_fuel = st.number_input(
            "설계 속도 기준 연료소모량 (ton/day)",
            min_value=1.0,
            max_value=500.0,
            value=80.0
        )

    with col3:

        max_speed = st.number_input(
            "최대 운항 속도 (knots)",
            min_value=5.0,
            max_value=40.0,
            value=22.0
        )


    # =====================================================
    # 4. 목적지 정보
    # =====================================================

    st.write("---")

    st.subheader("⚓ 4. 목적지 및 JIT 타임슬롯")

    col1, col2, col3 = st.columns(3)

    with col1:

        destination = st.selectbox(
            "목적지 항만",
            [
                "부산항 신항",
                "부산항 북항",
                "감천항",
                "인천항",
                "울산항",
                "광양항"
            ]
        )

    with col2:

        target_berth = st.selectbox(
            "목표 선석",
            [
                "1번 선석",
                "2번 선석",
                "3번 선석",
                "4번 선석"
            ]
        )

    with col3:

        target_arrival_time = st.time_input(
            "JIT 목표 도착시간"
        )


    # =====================================================
    # 5. 환경 / 항로 조건
    # =====================================================

    st.write("---")

    st.subheader("🌊 5. 환경 및 항로 조건")

    col1, col2, col3 = st.columns(3)

    with col1:

        wind_speed = st.number_input(
            "풍속 (m/s)",
            min_value=0.0,
            max_value=50.0,
            value=6.0
        )

        wind_direction = st.number_input(
            "풍향 (°)",
            min_value=0.0,
            max_value=359.0,
            value=120.0
        )

    with col2:

        wave_height = st.number_input(
            "파고 (m)",
            min_value=0.0,
            max_value=15.0,
            value=1.5
        )

        current_speed_sea = st.number_input(
            "해류 속도 (knots)",
            min_value=0.0,
            max_value=10.0,
            value=1.0
        )

    with col3:

        current_direction = st.number_input(
            "해류 방향 (°)",
            min_value=0.0,
            max_value=359.0,
            value=80.0
        )

        direct_bearing = st.number_input(
            "목적지 직선 방위 (°)",
            min_value=0.0,
            max_value=359.0,
            value=78.0
        )


    # =====================================================
    # 6. 연료 및 배출량 설정
    # =====================================================

    st.write("---")

    st.subheader("⛽ 6. 연료 및 배출량")

    col1, col2 = st.columns(2)

    with col1:

        fuel_price = st.number_input(
            "연료 가격 ($/ton)",
            min_value=0.0,
            max_value=5000.0,
            value=650.0
        )

    with col2:

        co2_factor = st.number_input(
            "CO₂ 배출계수 (tCO₂ / ton fuel)",
            min_value=0.0,
            max_value=10.0,
            value=3.114
        )


    # =====================================================
    # 7. 계산
    # =====================================================

    now = datetime.now()

    target_datetime = datetime.combine(
        now.date(),
        target_arrival_time
    )

    if target_datetime <= now:
        target_datetime += timedelta(days=1)

    available_hours = (
        target_datetime - now
    ).total_seconds() / 3600


    # -----------------------------------------------------
    # ETA 예측
    # -----------------------------------------------------

    if current_speed > 0:

        current_eta_hours = (
            remaining_distance /
            current_speed
        )

    else:

        current_eta_hours = 999


    current_eta = (
        now +
        timedelta(
            hours=current_eta_hours
        )
    )


    # =====================================================
    # 8. 기본 권고 속도 계산
    # =====================================================

    if available_hours > 0:

        base_recommended_speed = (
            remaining_distance /
            available_hours
        )

    else:

        base_recommended_speed = max_speed


    # =====================================================
    # 9. 환경 영향 보정
    # =====================================================

    environmental_penalty = 0


    # 파고 보정
    if wave_height > 3:
        environmental_penalty += 1.0

    elif wave_height > 2:
        environmental_penalty += 0.5


    # 강풍 보정
    if wind_speed > 15:
        environmental_penalty += 0.7

    elif wind_speed > 10:
        environmental_penalty += 0.3


    # 적재율 보정
    load_penalty = (
        cargo_load /
        100
    ) * 0.3


    recommended_speed = (
        base_recommended_speed
        + environmental_penalty
        + load_penalty
    )


    recommended_speed = np.clip(
        recommended_speed,
        6.0,
        max_speed
    )


    # =====================================================
    # 10. 방향 최적화
    # =====================================================

    angle_diff = (
        current_direction -
        direct_bearing
    )

    current_effect = (
        current_speed_sea *
        math.sin(
            math.radians(
                angle_diff
            )
        )
    )


    recommended_heading = (
        direct_bearing -
        current_effect * 3
    ) % 360


    # =====================================================
    # 11. 연료 소비 모델
    #
    # 속도 증가 시 연료소모가 대략 세제곱에 비례한다는
    # 단순 프로토타입 모델
    # =====================================================

    current_daily_fuel = (
        design_fuel *
        (
            current_speed /
            design_speed
        ) ** 3
    )


    recommended_daily_fuel = (
        design_fuel *
        (
            recommended_speed /
            design_speed
        ) ** 3
    )


    current_trip_fuel = (
        current_daily_fuel *
        current_eta_hours /
        24
    )


    recommended_eta_hours = (
        remaining_distance /
        recommended_speed
    )


    recommended_trip_fuel = (
        recommended_daily_fuel *
        recommended_eta_hours /
        24
    )


    fuel_saving = (
        current_trip_fuel -
        recommended_trip_fuel
    )


    fuel_saving = max(
        fuel_saving,
        0
    )


    # =====================================================
    # 12. CO2
    # =====================================================

    current_co2 = (
        current_trip_fuel *
        co2_factor
    )


    recommended_co2 = (
        recommended_trip_fuel *
        co2_factor
    )


    co2_saving = max(
        current_co2 -
        recommended_co2,
        0
    )


    # =====================================================
    # 13. 비용
    # =====================================================

    fuel_cost_saving = (
        fuel_saving *
        fuel_price
    )


    # =====================================================
    # 14. 추천 ETA
    # =====================================================

    recommended_eta = (
        now +
        timedelta(
            hours=recommended_eta_hours
        )
    )


    # =====================================================
    # 결과 표시
    # =====================================================

    st.write("---")

    st.subheader(
        "🤖 E-co로 AI 분석 결과"
    )


    result1, result2, result3, result4 = st.columns(4)


    result1.metric(
        "현재 속도",
        f"{current_speed:.1f} kn"
    )


    result2.metric(
        "권고 속도",
        f"{recommended_speed:.1f} kn",
        delta=f"{recommended_speed - current_speed:+.1f} kn"
    )


    result3.metric(
        "현재 방향",
        f"{current_heading:.0f}°"
    )


    result4.metric(
        "권고 방향",
        f"{recommended_heading:.0f}°",
        delta=f"{recommended_heading - current_heading:+.1f}°"
    )


    # =====================================================
    # ETA
    # =====================================================

    st.write("---")

    st.subheader(
        "🕒 ETA 예측"
    )


    eta1, eta2, eta3 = st.columns(3)


    eta1.metric(
        "현재 속도 유지 ETA",
        current_eta.strftime(
            "%m/%d %H:%M"
        )
    )


    eta2.metric(
        "E-co로 권고 ETA",
        recommended_eta.strftime(
            "%m/%d %H:%M"
        )
    )


    eta3.metric(
        "JIT 목표시간",
        target_datetime.strftime(
            "%m/%d %H:%M"
        )
    )


    # =====================================================
    # 연료
    # =====================================================

    st.write("---")

    st.subheader(
        "⛽ 예상 연료소모량"
    )


    fuel1, fuel2, fuel3 = st.columns(3)


    fuel1.metric(
        "현재 속도 유지",
        f"{current_trip_fuel:.2f} ton"
    )


    fuel2.metric(
        "E-co로 운항",
        f"{recommended_trip_fuel:.2f} ton"
    )


    fuel3.metric(
        "예상 연료 절감",
        f"{fuel_saving:.2f} ton"
    )


    # =====================================================
    # 배출량
    # =====================================================

    st.write("---")

    st.subheader(
        "🌍 CO₂ 배출량"
    )


    co1, co2, co3 = st.columns(3)


    co1.metric(
        "현재 운항 예상 CO₂",
        f"{current_co2:.2f} tCO₂"
    )


    co2.metric(
        "E-co로 예상 CO₂",
        f"{recommended_co2:.2f} tCO₂"
    )


    co3.metric(
        "CO₂ 절감",
        f"{co2_saving:.2f} tCO₂"
    )


    # =====================================================
    # 경제성
    # =====================================================

    st.write("---")

    st.subheader(
        "💰 운항 경제성"
    )


    eco1, eco2 = st.columns(2)


    eco1.metric(
        "예상 연료비 절감",
        f"${fuel_cost_saving:,.0f}"
    )


    if current_trip_fuel > 0:

        saving_rate = (
            fuel_saving /
            current_trip_fuel *
            100
        )

    else:

        saving_rate = 0


    eco2.metric(
        "연료 절감률",
        f"{saving_rate:.1f}%"
    )


    # =====================================================
    # 최종 AI 운항 권고
    # =====================================================

    st.write("---")

    st.subheader(
        "🧭 최종 운항 권고"
    )


    if recommended_speed < current_speed:

        st.success(
            f"현재 {current_speed:.1f} kn에서 "
            f"{recommended_speed:.1f} kn으로 감속을 권장합니다. "
            f"권고 방향은 {recommended_heading:.0f}°이며, "
            f"JIT 타임슬롯에 맞춰 운항할 수 있습니다."
        )

    elif recommended_speed > current_speed:

        st.warning(
            f"현재 속도보다 약간 빠른 "
            f"{recommended_speed:.1f} kn 운항이 필요합니다. "
            f"권고 방향은 {recommended_heading:.0f}°입니다."
        )

    else:

        st.info(
            "현재 속도를 유지하는 것이 적절합니다."
        )


    # =====================================================
    # 운항 정보 요약
    # =====================================================

    summary_df = pd.DataFrame({

        "항목": [
            "선박명",
            "선종",
            "목적항",
            "목표 선석",
            "남은 거리",
            "현재 속도",
            "권고 속도",
            "현재 방향",
            "권고 방향",
            "예상 연료 절감",
            "예상 CO₂ 절감"
        ],

        "결과": [
            vessel_name,
            vessel_type,
            destination,
            target_berth,
            f"{remaining_distance:.1f} NM",
            f"{current_speed:.1f} kn",
            f"{recommended_speed:.1f} kn",
            f"{current_heading:.0f}°",
            f"{recommended_heading:.0f}°",
            f"{fuel_saving:.2f} ton",
            f"{co2_saving:.2f} tCO₂"
        ]
    })


    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # 뒤로가기
    # =====================================================

    st.write("---")


    if st.button(
        "⬅️ 뒤로가기",
        key="back_ecoro"
    ):

        navigate_to(
            "main"
        )

# =========================================================
# 8. 입항 예약
# =========================================================

def reservation_page():

    st.title(
        "🎫 입항 예약 및 보증금 결제"
    )

    st.markdown(
        "항만 주차권 개념의 "
        "'가상 입항(Virtual Arrival)' "
        "티켓을 발급합니다."
    )


    with st.form(
        "reservation_form"
    ):


        st.selectbox(
            "목적지 선석 추천 리스트",
            [
                "부산항 신항 2부두 (추천)",
                "부산항 제3부두"
            ]
        )


        st.date_input(
            "입항 예정일"
        )


        st.time_input(
            "AI 추천 타임슬롯"
        )


        st.markdown(
            "**예약 보증금:** "
            "500,000 KRW "
            "(정시 도착 시 전액 환급 및 "
            "사용료 할인 인센티브)"
        )


        submitted = (
            st.form_submit_button(
                "스마트 컨트랙트 예약 진행"
            )
        )


        if submitted:

            st.success(
                "✅ 성공적으로 입항 예약권이 "
                "발급되었습니다! "
                "E-co로 경로가 동기화됩니다."
            )


    if st.button(
        "⬅️ 뒤로가기",
        key="back_reservation"
    ):

        navigate_to(
            "main"
        )


# =========================================================
# 9. 입항 가이드
# =========================================================

def guide_page():

    st.title(
        "🧭 안전 입항 가이드"
    )

    st.markdown(
        "선석 접안까지 남은 절차와 "
        "실시간 관제 현황을 안내합니다."
    )


    st.checkbox(
        "1단계: 항만 진입 수로 통과 (완료)",
        value=True,
        disabled=True
    )


    st.checkbox(
        "2단계: 도선사 및 예인선 합류 (진행 중)",
        value=False
    )


    st.checkbox(
        "3단계: 예약된 15:30 정각 선석 접안",
        value=False
    )


    st.write("---")


    if st.button(
        "⬅️ 뒤로가기",
        key="back_guide"
    ):

        navigate_to(
            "main"
        )


# =========================================================
# 10. 앱 라우팅
# =========================================================

if st.session_state.page == "main":

    main_page()


elif st.session_state.page == "congestion":

    congestion_page()


elif st.session_state.page == "ecoro":

    ecoro_page()


elif st.session_state.page == "reservation":

    reservation_page()


elif st.session_state.page == "guide":

    guide_page()