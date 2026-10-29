import streamlit as st
import pandas as pd
import numpy as np
import joblib
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

def ecoro_page():

    st.title(
        "🌱 E-co로 (최적 감속 운항 경로)"
    )

    st.markdown(
        "AI 예측 기반으로 타임슬롯에 맞춘 "
        "권고 속도(Eco-speed)를 안내합니다."
    )


    col1, col2 = st.columns(2)


    col1.metric(
        label="현재 속도",
        value="15 Knots",
        delta="-3 Knots (권고)"
    )


    col2.metric(
        label="예상 유류비 절감액",
        value="$ 4,500",
        delta="탄소 12% 저감"
    )


    st.info(
        "💡 12 Knots로 감속 유지 시, "
        "외항 대기 없이 예약된 선석에 "
        "즉시 접안이 가능합니다."
    )


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