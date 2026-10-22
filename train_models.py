import pandas as pd
import numpy as np

from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor, VotingRegressor

import joblib


print("백엔드: 다중 모델 및 앙상블 학습을 시작합니다...")


# =========================================================
# 1. 가상 학습 데이터 생성
# =========================================================

np.random.seed(42)

n = 5000

df = pd.DataFrame({

    "vessels_in_port":
        np.random.randint(
            5,
            70,
            n
        ),

    "waiting_vessels":
        np.random.randint(
            0,
            25,
            n
        ),

    "berth_occupancy":
        np.random.uniform(
            20,
            100,
            n
        ),

    "arrivals_next_1h":
        np.random.randint(
            0,
            15,
            n
        ),

    "departures_next_1h":
        np.random.randint(
            0,
            12,
            n
        ),

    "crane_utilization":
        np.random.uniform(
            20,
            100,
            n
        ),

    "yard_queue":
        np.random.randint(
            0,
            40,
            n
        ),

    "wind_speed":
        np.random.uniform(
            0,
            18,
            n
        ),

    "wave_height":
        np.random.uniform(
            0.1,
            3.5,
            n
        )
})


# =========================================================
# 2. 가상의 혼잡도 정답 생성
# =========================================================

congestion = (

    0.5 * df["vessels_in_port"]

    + 1.2 * df["waiting_vessels"]

    + 0.30 * df["berth_occupancy"]

    + 1.1 * df["arrivals_next_1h"]

    - 0.8 * df["departures_next_1h"]

    + 0.12 * df["crane_utilization"]

    + 0.4 * df["yard_queue"]

    + 0.3 * df["wind_speed"]

    + 1.0 * df["wave_height"]
)


# 실제 데이터처럼 약간의 오차 추가
congestion += np.random.normal(
    0,
    5,
    n
)


# 0 ~ 100 범위 제한
df["congestion"] = np.clip(
    congestion,
    0,
    100
)


# =========================================================
# 3. 입력 데이터와 정답 분리
# =========================================================

X = df.drop(
    columns=["congestion"]
)

y = df["congestion"]


# =========================================================
# 4. XGBoost 학습
# =========================================================

print("XGBoost 학습 중...")


xgb_model = XGBRegressor(

    n_estimators=300,

    max_depth=5,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42
)


xgb_model.fit(
    X,
    y
)


# =========================================================
# 5. Random Forest 학습
# =========================================================

print("Random Forest 학습 중...")


rf_model = RandomForestRegressor(

    n_estimators=200,

    max_depth=8,

    random_state=42,

    n_jobs=-1
)


rf_model.fit(
    X,
    y
)


# =========================================================
# 6. Ensemble 모델 학습
# =========================================================

print("앙상블 모델 학습 중...")


ensemble_model = VotingRegressor(

    estimators=[

        (
            "xgb",
            XGBRegressor(
                n_estimators=300,
                max_depth=5,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
        ),

        (
            "rf",
            RandomForestRegressor(
                n_estimators=200,
                max_depth=8,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


ensemble_model.fit(
    X,
    y
)


# =========================================================
# 7. 모델 저장
# =========================================================

joblib.dump(
    xgb_model,
    "xgb_model.pkl"
)


joblib.dump(
    rf_model,
    "rf_model.pkl"
)


joblib.dump(
    ensemble_model,
    "ensemble_model.pkl"
)


print("✅ 모든 모델 학습 및 저장 완료!")