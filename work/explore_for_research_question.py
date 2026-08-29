"""
Quick data exploration to support the research question (ML-02)
"""
import pandas as pd
import numpy as np
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load the data
df = pd.read_csv('../data/raw/content_refresh_anonymized.csv')

print("=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)
print(f"Total rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Unique clients: {df['client_id'].nunique()}")
print(f"Unique content items: {df['content_id'].nunique()}")
print()

print("=" * 70)
print("LANE 2: REFRESH OPPORTUNITY SCORING - KEY NUMBERS")
print("=" * 70)

# 1. Declining content with demand
declining = df[df['trend_direction'].str.lower() == 'down']
print(f"\n1. DECLINING PAGES:")
print(f"   - Total declining pages: {len(declining):,} ({len(declining)/len(df)*100:.1f}%)")
print(f"   - Declining WITH demand (>=100 impressions): {len(declining[declining['impressions_90d'] >= 100]):,}")
print(f"   - Total impressions at risk: {declining['impressions_90d'].sum():,.0f}")
print(f"   - Median impressions (declining pages): {declining['impressions_90d'].median():.0f}")

# 2. Stale visible pages
stale_visible = df[(df['days_since_last_update'] >= 180) & (df['impressions_90d'] >= 500)]
print(f"\n2. STALE VISIBLE PAGES:")
print(f"   - Stale (180+ days) + visible (500+ impressions): {len(stale_visible):,}")
print(f"   - Total impressions on stale pages: {stale_visible['impressions_90d'].sum():,.0f}")
print(f"   - Average age of stale pages: {stale_visible['days_since_last_update'].mean():.0f} days")

# 3. Thin content with visibility
thin_visible = df[(df['word_count'] > 0) & (df['word_count'] < 1200) & (df['impressions_90d'] >= 250)]
print(f"\n3. THIN VISIBLE PAGES:")
print(f"   - Thin (<1200 words) + visible (250+ impressions): {len(thin_visible):,}")
print(f"   - Average word count: {thin_visible['word_count'].mean():.0f} words")
print(f"   - Total impressions on thin pages: {thin_visible['impressions_90d'].sum():,.0f}")

# 4. Page 1 with age risk
page_one_aging = df[(df['avg_position'] > 0) & (df['avg_position'] <= 10) & (df['content_age_days'] >= 180)]
print(f"\n4. PAGE 1 AGING RISK:")
print(f"   - Page 1 (pos ≤10) + aging (180+ days): {len(page_one_aging):,}")
print(f"   - Average position: {page_one_aging['avg_position'].mean():.2f}")
print(f"   - Total impressions: {page_one_aging['impressions_90d'].sum():,.0f}")

# 5. Low CTR visible pages
low_ctr = df[(df['impressions_90d'] >= 500) & (df['avg_position'] > 0) &
             (df['avg_position'] <= 20) & (df['ctr'] < 0.5)]
print(f"\n5. LOW CTR OPPORTUNITY:")
print(f"   - High visibility + low CTR (<0.5%): {len(low_ctr):,}")
print(f"   - Average CTR: {low_ctr['ctr'].mean():.3f}%")
print(f"   - Average position: {low_ctr['avg_position'].mean():.2f}")
print(f"   - Potential clicks if CTR improved: ~{(low_ctr['impressions_90d'].sum() * 0.01):,.0f}")

# 6. Overall refresh opportunity scope
refresh_candidates = df[
    ((df['trend_direction'].str.lower() == 'down') & (df['impressions_90d'] >= 100)) |
    ((df['days_since_last_update'] >= 180) & (df['impressions_90d'] >= 500)) |
    ((df['word_count'] > 0) & (df['word_count'] < 1200) & (df['impressions_90d'] >= 250))
]

print(f"\n6. OVERALL REFRESH OPPORTUNITY:")
print(f"   - Pages meeting ANY refresh criteria: {len(refresh_candidates):,} ({len(refresh_candidates)/len(df)*100:.1f}%)")
print(f"   - Total impressions covered: {refresh_candidates['impressions_90d'].sum():,.0f}")
print(f"   - % of all impressions: {refresh_candidates['impressions_90d'].sum()/df['impressions_90d'].sum()*100:.1f}%")

print("\n" + "=" * 70)
print("DECISION FRAMING CONTEXT")
print("=" * 70)

# Content editor capacity context
print(f"\nIf an editor can review 50 pages/month:")
print(f"  - That's {len(refresh_candidates)/50:.1f} months to review all candidates")
print(f"  - A ranking model helps prioritize: WHICH 50 first?")

# Cost of wrong call
print(f"\nCost of wrong prioritization:")
print(f"  - Editor time wasted on low-impact pages: opportunity cost")
print(f"  - High-value declining pages missed: continued traffic loss")
print(f"  - Pages in top 10 declining: {len(page_one_aging[page_one_aging['trend_direction'].str.lower() == 'down']):,} need protection")

print("\n" + "=" * 70)
print("DATASET QUALITY FOR ML")
print("=" * 70)

# Check if we have enough signal
print(f"\nFeature availability:")
print(f"  - Pages with position data: {(df['avg_position'] > 0).sum():,} ({(df['avg_position'] > 0).sum()/len(df)*100:.1f}%)")
print(f"  - Pages with session data: {(df['sessions_90d'] > 0).sum():,} ({(df['sessions_90d'] > 0).sum()/len(df)*100:.1f}%)")
print(f"  - Pages with engagement data: {(df['engagement_rate'] > 0).sum():,} ({(df['engagement_rate'] > 0).sum()/len(df)*100:.1f}%)")
print(f"  - Pages with word count: {(df['word_count'] > 0).sum():,} ({(df['word_count'] > 0).sum()/len(df)*100:.1f}%)")

# Label distribution for modeling
print(f"\nTarget label distribution (trend_direction):")
for direction in df['trend_direction'].value_counts().head():
    print(f"  - {direction}: {(df['trend_direction'] == direction).sum():,} ({(df['trend_direction'] == direction).sum()/len(df)*100:.1f}%)")

print("\n" + "=" * 70)
print("READY FOR RESEARCH QUESTION NOTEBOOK")
print("=" * 70)
print("Copy the compelling numbers above into your notebook sections!")
