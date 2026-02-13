import argparse
import joblib
import pandas as pd
import numpy as np
from pathlib import Path


MODEL_FEATURE_COLUMNS = [
    'dst_port', 'protocol', 'flow_duration', 'tot_fwd_pkts', 'tot_bwd_pkts',
    'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max',
    'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std',
    'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean',
    'bwd_pkt_len_std', 'flow_byts_s', 'flow_pkts_s', 'flow_iat_mean',
    'flow_iat_std', 'flow_iat_max', 'flow_iat_min', 'fwd_iat_tot',
    'fwd_iat_mean', 'fwd_iat_std', 'fwd_iat_max', 'fwd_iat_min',
    'bwd_iat_tot', 'bwd_iat_mean', 'bwd_iat_std', 'bwd_iat_max',
    'bwd_iat_min', 'fwd_psh_flags', 'bwd_psh_flags', 'fwd_urg_flags',
    'bwd_urg_flags', 'fwd_header_len', 'bwd_header_len', 'fwd_pkts_s',
    'bwd_pkts_s', 'pkt_len_min', 'pkt_len_max', 'pkt_len_mean',
    'pkt_len_std', 'pkt_len_var', 'fin_flag_cnt', 'syn_flag_cnt',
    'rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt', 'urg_flag_cnt',
    'cwe_flag_count', 'ece_flag_cnt', 'down_up_ratio', 'pkt_size_avg',
    'fwd_seg_size_avg', 'bwd_seg_size_avg', 'fwd_byts_b_avg',
    'fwd_pkts_b_avg', 'fwd_blk_rate_avg', 'bwd_byts_b_avg',
    'bwd_pkts_b_avg', 'bwd_blk_rate_avg', 'subflow_fwd_pkts',
    'subflow_fwd_byts', 'subflow_bwd_pkts', 'subflow_bwd_byts',
    'init_fwd_win_byts', 'init_bwd_win_byts', 'fwd_act_data_pkts',
    'fwd_seg_size_min', 'active_mean', 'active_std', 'active_max',
    'active_min', 'idle_mean', 'idle_std', 'idle_max', 'idle_min'
]


def load_artifacts(model_path: Path, scaler_path: Path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def preprocess_data(csv_path: Path, scaler):
    df = pd.read_csv(csv_path)

    # Validate features
    missing_cols = set(MODEL_FEATURE_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = df[MODEL_FEATURE_COLUMNS]
    scaled_data = scaler.transform(df)

    return scaled_data


def run_inference(model, data):
    predictions = model.predict(data)
    labels = np.argmax(predictions, axis=1)
    return labels


def main():
    parser = argparse.ArgumentParser(description="Run model inference on network traffic data.")
    parser.add_argument("--input", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--model", type=str, default="./models/cnn-model.pkl")
    parser.add_argument("--scaler", type=str, default="./scaler.pkl")

    args = parser.parse_args()

    model, scaler = load_artifacts(Path(args.model), Path(args.scaler))
    data = preprocess_data(Path(args.input), scaler)
    labels = run_inference(model, data)

    print("Predictions:")
    print(labels)


if __name__ == "__main__":
    main()
