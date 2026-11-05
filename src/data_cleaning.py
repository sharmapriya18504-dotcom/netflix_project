# =====================================
# NETFLIX DATA ANALYSIS
# TASK 1: DATA CLEANING
# =====================================

import pandas as pd
import numpy as np

# Step 1: Load Dataset

df = pd.read_csv("data/Dataset.csv")

print("\n========== DATASET LOADED ==========")

# Step 2: Display First 5 Rows

print(df.head())

# Step 3: Dataset Information

print("\n========== DATASET INFORMATION ==========")

print(df.info())

# Step 4: Dataset Shape

print("\n========== DATASET SHAPE ==========")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Step 5: Check Missing Values

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())

# Step 6: Check Duplicate Records

print("\n========== DUPLICATE RECORDS ==========")

print("Duplicates:", df.duplicated().sum())

# Step 7: Statistical Summary

print("\n========== STATISTICAL SUMMARY ==========")

print(df.describe(include="all"))
