"""
KBO 경기 예측 AI 모델 구조 예시
ML 모델 설계 명세서 참고용

주요 모델 타입:
1. LSTM (Long Short-Term Memory)
2. GRU (Gated Recurrent Unit)  
3. Ensemble (앙상블)
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout, Bidirectional
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
import joblib


# ==============================================
# 1. 데이터 전처리 및 특성 추출
# ==============================================

def extract_team_features(matches, team_id, n_games=10):
    """
    팀별 최근 N경기 특성 추출
    
    Args:
        matches: 경기 데이터 DataFrame
        team_id: 팀 ID
        n_games: 최근 N경기
    
    Returns:
        dict: 팀 특성 딕셔너리
    """
    # 홈/원정 경기 필터링
    team_matches = matches[
        (matches['home_team_id'] == team_id) | 
        (matches['away_team_id'] == team_id)
    ].tail(n_games)
    
    features = {
        'recent_wins': 0,
        'recent_losses': 0,
        'avg_score': 0.0,
        'avg_allowed': 0.0,
        'win_rate': 0.0,
    }
    
    scores = []
    allowed = []
    
    for _, match in team_matches.iterrows():
        is_home = match['home_team_id'] == team_id
        score = match['home_score'] if is_home else match['away_score']
        opponent_score = match['away_score'] if is_home else match['home_score']
        
        scores.append(score)
        allowed.append(opponent_score)
        
        if match['winner'] == ('home' if is_home else 'away'):
            features['recent_wins'] += 1
        else:
            features['recent_losses'] += 1
    
    features['avg_score'] = np.mean(scores) if scores else 0.0
    features['avg_allowed'] = np.mean(allowed) if allowed else 0.0
    features['win_rate'] = features['recent_wins'] / n_games if n_games > 0 else 0.0
    
    return features


def prepare_sequence_data(matches, window_size=10):
    """
    시계열 시퀀스 데이터 준비
    
    Args:
        matches: 경기 데이터
        window_size: 시퀀스 윈도우 크기
    
    Returns:
        X, y: 입력 시퀀스와 타겟
    """
    sequences = []
    targets = []
    
    for i in range(len(matches) - window_size):
        # 최근 N경기 특성 추출
        window = matches.iloc[i:i+window_size]
        features = []
        
        for _, match in window.iterrows():
            home_features = extract_team_features(matches, match['home_team_id'])
            away_features = extract_team_features(matches, match['away_team_id'])
            
            feature_vector = [
                home_features['win_rate'],
                home_features['avg_score'],
                away_features['win_rate'],
                away_features['avg_score'],
                1 if match['home_team_id'] == match['home_team_id'] else 0,  # 홈/원정
            ]
            features.append(feature_vector)
        
        sequences.append(features)
        targets.append(1 if matches.iloc[i+window_size]['winner'] == 'home' else 0)
    
    return np.array(sequences), np.array(targets)


# ==============================================
# 2. LSTM 모델 정의
# ==============================================

def build_lstm_model(sequence_length=10, feature_dim=20):
    """
    LSTM 모델 구성
    
    Args:
        sequence_length: 시퀀스 길이
        feature_dim: 특성 차원
    
    Returns:
        model: Keras 모델
    """
    model = Sequential([
        # Bidirectional LSTM
        Bidirectional(LSTM(64, return_sequences=True), 
                     input_shape=(sequence_length, feature_dim)),
        Dropout(0.2),
        
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        
        Dense(16, activation='relu'),
        Dropout(0.2),
        
        Dense(1, activation='sigmoid')  # 홈팀 승률 예측
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model


# ==============================================
# 3. GRU 모델 정의
# ==============================================

def build_gru_model(sequence_length=10, feature_dim=20):
    """
    GRU 모델 구성
    
    Args:
        sequence_length: 시퀀스 길이
        feature_dim: 특성 차원
    
    Returns:
        model: Keras 모델
    """
    model = Sequential([
        GRU(64, return_sequences=True, 
            input_shape=(sequence_length, feature_dim)),
        Dropout(0.2),
        
        GRU(32, return_sequences=False),
        Dropout(0.2),
        
        Dense(16, activation='relu'),
        Dropout(0.2),
        
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model


# ==============================================
# 4. 확률 보정 (Calibration)
# ==============================================

def calibrate_predictions(model, X_val, y_val, predictions):
    """
    예측 확률 보정
    
    Args:
        model: 학습된 모델
        X_val: 검증 데이터
        y_val: 검증 타겟
        predictions: 원본 예측
    
    Returns:
        calibrated_predictions: 보정된 예측
    """
    # Temperature Scaling
    calibrated_model = tf.keras.Model(
        inputs=model.input,
        outputs=model.output
    )
    
    # Platt Scaling 또는 Isotonic Regression
    # (간단한 예시, 실제로는 sklearn 사용 권장)
    
    return calibrated_predictions


# ==============================================
# 5. 앙상블 모델
# ==============================================

class EnsembleModel:
    """
    여러 모델의 앙상블
    """
    
    def __init__(self, models, weights=None):
        self.models = models
        self.weights = weights if weights else [1.0 / len(models)] * len(models)
    
    def predict(self, X):
        """
        앙상블 예측
        
        Args:
            X: 입력 데이터
        
        Returns:
            predictions: 가중 평균된 예측
        """
        predictions = []
        for model in self.models:
            pred = model.predict(X)
            predictions.append(pred)
        
        # 가중 평균
        ensemble_pred = np.average(predictions, axis=0, weights=self.weights)
        return ensemble_pred


# ==============================================
# 6. 베팅 전략 (Kelly Criterion)
# ==============================================

def calculate_kelly_percentage(win_probability, odds):
    """
    켈리 포뮬러로 베팅 비율 계산
    
    Args:
        win_probability: 승률 (0~1)
        odds: 배당률
    
    Returns:
        kelly_percentage: 베팅 비율
    """
    kelly = (win_probability * odds - 1) / (odds - 1)
    # 음수이면 베팅하지 않음
    return max(0, kelly)


def calculate_expected_value(win_probability, odds, bet_amount):
    """
    기대값 계산
    
    Args:
        win_probability: 승률
        odds: 배당률
        bet_amount: 베팅 금액
    
    Returns:
        ev: 기대값
    """
    expected_profit = win_probability * (odds - 1) * bet_amount
    expected_loss = (1 - win_probability) * bet_amount
    ev = expected_profit - expected_loss
    return ev


# ==============================================
# 7. 베팅 모델 결정
# ==============================================

def decide_betting_strategy(prediction, odds, model_type='스탠다드'):
    """
    베팅 모델에 따른 베팅 결정
    
    Args:
        prediction: AI 예측 확률
        odds: 배당률
        model_type: 베팅 모델 (하이리턴/스탠다드/로우리스크)
    
    Returns:
        decision: 베팅 결정 (bet/pass)
        kelly_pct: 켈리 비율
    """
    # 베팅 모델별 임계값
    thresholds = {
        '하이리턴': {'min_confidence': 0.55, 'min_ev': 1000, 'max_kelly': 0.25},
        '스탠다드': {'min_confidence': 0.60, 'min_ev': 500, 'max_kelly': 0.15},
        '로우리스크': {'min_confidence': 0.70, 'min_ev': 300, 'max_kelly': 0.10},
    }
    
    threshold = thresholds.get(model_type, thresholds['스탠다드'])
    
    # 켈리 비율 계산
    kelly_pct = calculate_kelly_percentage(prediction['home_win_probability'], odds)
    
    # 기대값 계산
    ev = calculate_expected_value(
        prediction['home_win_probability'], 
        odds, 
        10000  # 기본 베팅 금액
    )
    
    # 베팅 결정
    if (prediction['confidence_score'] >= threshold['min_confidence'] and
        ev >= threshold['min_ev'] and
        kelly_pct <= threshold['max_kelly']):
        return 'bet', kelly_pct
    else:
        return 'pass', kelly_pct


# ==============================================
# 8. 모델 학습 예시
# ==============================================

def train_model_example():
    """
    모델 학습 예시
    """
    # 데이터 로드
    matches = load_matches_from_db()
    
    # 시퀀스 데이터 준비
    X, y = prepare_sequence_data(matches, window_size=10)
    
    # Train/Validation/Test Split
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    # 정규화
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
    X_val = scaler.transform(X_val.reshape(-1, X_val.shape[-1])).reshape(X_val.shape)
    
    # LSTM 모델 학습
    lstm_model = build_lstm_model(sequence_length=10, feature_dim=X.shape[-1])
    
    history = lstm_model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=5),
            tf.keras.callbacks.ModelCheckpoint('models/lstm_best.h5', save_best_only=True)
        ]
    )
    
    # 모델 저장
    lstm_model.save('models/lstm_model.h5')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    return lstm_model


# ==============================================
# 9. 모델 평가 예시
# ==============================================

def evaluate_model(model, X_test, y_test):
    """
    모델 성능 평가
    
    Returns:
        metrics: 성능 지표
    """
    predictions = model.predict(X_test)
    
    from sklearn.metrics import log_loss, brier_score_loss
    
    metrics = {
        'accuracy': np.mean((predictions > 0.5) == y_test),
        'log_loss': log_loss(y_test, predictions),
        'brier_score': brier_score_loss(y_test, predictions),
    }
    
    return metrics


# ==============================================
# 10. 사용 예시
# ==============================================

if __name__ == '__main__':
    # 모델 학습
    # model = train_model_example()
    
    # 예측 생성
    # predictions = model.predict(X_new)
    
    # 베팅 결정
    # prediction = {
    #     'home_win_probability': 0.65,
    #     'confidence_score': 0.75
    # }
    # odds = 2.5
    # decision, kelly_pct = decide_betting_strategy(prediction, odds, '스탠다드')
    # print(f"베팅 결정: {decision}, 켈리 비율: {kelly_pct:.2%}")
    
    pass


