# -*- coding: utf-8 -*-

import sys
import io

# 標準出力のエンコーディングを設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

def kl_bernoulli(p, q):
    """KL divergence between Bern(p) and Bern(q)"""
    eps = 1e-12  # avoid log(0)
    p = np.clip(p, eps, 1 - eps)
    q = np.clip(q, eps, 1 - eps)
    return p * np.log(p / q) + (1 - p) * np.log((1 - p) / (1 - q))

# パラメータの設定
p = 0.2
q = 0.5
r = 0.8

# KLダイバージェンスの計算
D_pq = kl_bernoulli(p, q)
D_qr = kl_bernoulli(q, r)
D_pr = kl_bernoulli(p, r)

# 結果表示
print(f"D(P‖Q) = {D_pq:.6f}")
print(f"D(Q‖R) = {D_qr:.6f}")
print(f"D(P‖R) = {D_pr:.6f}")

# 三角不等式のような関係の確認
lhs = D_pq + D_qr
rhs = D_pr

print(f"\nD(P‖Q) + D(Q‖R) = {lhs:.6f}")
print(f"D(P‖R) = {rhs:.6f}")

if lhs >= rhs:
    print("\n✅ D(P‖Q) + D(Q‖R) ≥ D(P‖R) が成り立っています")
else:
    print("\n❌ D(P‖Q) + D(Q‖R) < D(P‖R) です（三角不等式のようには成り立ちません）")
