# Investigating Feature Leakage in Flow-Based Intrusion Detection  
**A Case Study Using CSE-CIC-IDS2018 and Real SSH Brute-Force Traffic**

## Overview
This project investigates the generalization behavior of flow-based machine learning models for intrusion detection. A Random Forest classifier was trained on the CSE-CIC-IDS2018 dataset to detect SSH and FTP brute-force attacks. While the model achieved near-perfect accuracy on benchmark test data, it failed to detect real SSH brute-force traffic generated in a controlled virtual lab.

Through systematic analysis, this project demonstrates that the observed performance was driven by dataset-specific feature leakage rather than generalizable attack behavior.

---

## Key Contributions
- Trained a flow-based Random Forest IDS using CICFlowMeter features
- Achieved near-perfect benchmark accuracy on IDS2018
- Performed **external validation** using Hydra-generated SSH brute-force traffic
- Diagnosed model failure using **feature importance, robustness checks, and ablation**
- Identified TCP stack and flow-timing artifacts as dominant non-generalizable features
- Demonstrated that hyperparameter tuning had minimal impact compared to feature selection

---

## Dataset
- **CSE-CIC-IDS2018**
- Classes used:
  - Benign
  - SSH Brute Force
  - FTP Brute Force
- Features:
  - Flow-level features extracted using CICFlowMeter

> ⚠️ Note: IDS2018 flows originate from fixed capture environments, operating systems, and attack scripts, which introduces potential feature leakage.

---

## Experimental Setup

### Model
- Random Forest Classifier (scikit-learn)

### Hyperparameter Search
```python
{
  'n_estimators': [10, 20, 40],
  'max_depth': [None, 10, 20],
  'min_samples_split': [2, 5],
  'min_samples_leaf': [1, 2],
  'bootstrap': [True, False]
}
```
Hyperparameter tuning was performed using cross-validation on benchmark data.

Initial Results (Benchmark Evaluation)
Near-perfect accuracy on held-out IDS2018 test data

Clean confusion matrix across all three classes

⚠️ While impressive, this result raised concerns about possible data leakage or shortcut learning.

External Validation (Real Attack Traffic)
To evaluate real-world applicability, SSH brute-force traffic was generated using Hydra in a virtual lab environment:

Attacker: Hydra

Target: SSH service in VM

Traffic capture: tcpdump

Flow extraction: CICFlowMeter

Evaluation: model inference on generated flows

Result
All Hydra-generated SSH brute-force traffic was classified as benign.

This demonstrated a critical generalization failure.

Feature Importance Analysis
Feature importance analysis revealed that the model relied primarily on TCP- and flow-level artifacts rather than behavioral indicators of brute-force attacks.

Top Features (Example)

### Feature	Importance

```
dst_port	        0.17
flow_pkts_s	        0.15
fwd_seg_size_min	0.14
bwd_pkts_s	        0.10
init_fwd_win_byts	0.04
```

### Observations

```
TCP segment size features (fwd_seg_size_min, fwd_seg_size_avg)

TCP window size features (init_fwd_win_byts, init_bwd_win_byts)

Destination port

Flow timing and rate statistics
```

These features are:

1. Dependent on TCP stack implementation

2. Sensitive to OS, kernel version, NIC, and capture tool

3. Unrelated to authentication semantics

### Robustness Check
The model was retrained with modified hyperparameters and constraints. While feature importance magnitudes shifted, the same feature categories consistently dominated across configurations.

This demonstrates that the behavior was not caused by overfitting alone, but by dataset-intrinsic feature leakage.

### Ablation Insight
Removing the highest-importance features (TCP window sizes, segment sizes, ports, and timing features) caused a significant drop in benchmark accuracy, confirming that the original performance depended on non-generalizable shortcuts.

### Key Findings
Perfect benchmark accuracy does not imply real-world detection capability

Flow-based ML models can learn environment fingerprints instead of attack behavior

Hyperparameter tuning had minimal impact compared to feature selection

External validation is essential for security ML evaluation

Flow-only features are insufficient for detecting authentication-based attacks such as SSH brute force

### Limitations
Analysis focused on flow-level features only

No host-based or authentication log data was used

Results are specific to flow-based ML approaches

### Implications
This study highlights the risks of relying solely on benchmark IDS datasets and accuracy metrics. Without external validation, models may appear highly effective while failing in real operational environments.

### Future Work
1. Incorporate sliding-window and per-source aggregation features
2. Try other ML and Deep learning Models
3. Combine flow-based ML with rule-based or log-based detection
4. Evaluate cross-dataset generalization using additional IDS benchmarks
5. Explore hybrid detection architectures for authentication attacks

### Technologies Used
1. Python
2. scikit-learn
3. CICFlowMeter
4. tcpdump
5. Hydra
6. Linux / Virtualized lab environment