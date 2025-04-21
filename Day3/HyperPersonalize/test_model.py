import pandas as pd
import numpy as np
import random

from openai import OpenAI

import streamlit as st
import joblib
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from pydantic import BaseModel

model = joblib.load("recommendation_model.pkl")

llm = OpenAI(model="gpt-4", temperature=0.7)

def generate_explanation(customer_name, product):
    prompt = f"""
    A bank is recommending a financial product to {customer_name} based on their spending history.

    Recommended Product: {product}

    Generate a personalized AI explanation that makes the customer feel valued and highlights why this product suits them.
    """
    return llm.predict(prompt)