import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from io import StringIO
import os

# Page configuration
st.set_page_config(page_title="🏭 Production Line Bottleneck Detection", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("🏭 Production Line Bottleneck Detection")
st.markdown("**Intelligent Manufacturing Analytics System**")
st.markdown("---")

# Load and process data with notebook's feature engineering
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv("../data/dataset.csv")
    except:
        st.warning("Dataset not found, generating sample data...")
        np.random.seed(42)
        stages = ['Assembly', 'Welding', 'Painting', 'Quality Check', 'Packaging']
        n_samples = 200
        
        df = pd.DataFrame({
            'Stage': np.random.choice(stages, n_samples),
            'Cycle_Time': np.random.uniform(10, 120, n_samples),
            'Waiting_Time': np.random.uniform(0, 60, n_samples),
            'Downtime': np.random.uniform(0, 30, n_samples),
            'Defect_Rate': np.random.uniform(0, 0.1, n_samples),
            'Units_Produced': np.random.randint(50, 500, n_samples)
        })
    
    # Feature Engineering from notebook
    df_numeric = df.select_dtypes(include=[np.number])
    df_numeric_normalized = (df_numeric - df_numeric.mean()) / df_numeric.std()
    
    df["Bottleneck_Score"] = np.abs(df_numeric_normalized).mean(axis=1)
    df["Missing_Features_Ratio"] = df_numeric.isna().sum(axis=1) / len(df_numeric.columns)
    df["Efficiency_Score"] = 0.6 * df["Bottleneck_Score"] + 0.4 * df["Missing_Features_Ratio"]
    
    # Production Issue classification
    df["Production_Issue"] = ((df["Defect_Rate"] > 0.06) | (df["Downtime"] > 12)).astype(int)
    
    # Severity classification
    df["Severity"] = pd.cut(df["Efficiency_Score"], 
                             bins=[0, 0.25, 0.5, 0.75, 2.0],
                             labels=["Excellent", "Good", "Poor", "Critical"])
    
    return df


df = load_and_process_data()

# Sidebar Controls
st.sidebar.header("📊 Filter & Analysis Options")
analysis_type = st.sidebar.radio("Select View", ["📈 Dashboard", "🤖 ML Clustering", "🔮 Predictions", "📥 Export Data"])

selected_stage = st.sidebar.selectbox("Filter by Production Stage", ["All Stages"] + list(df["Stage"].unique()))
severity_filter = st.sidebar.multiselect("Filter by Severity", ["Excellent", "Good", "Poor", "Critical"], default=["Excellent", "Good", "Poor", "Critical"])

# Apply filters
if selected_stage == "All Stages":
    filtered_df = df
else:
    filtered_df = df[df["Stage"] == selected_stage]

filtered_df = filtered_df[filtered_df["Severity"].isin(severity_filter)]

# KPIs
st.header("Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    issue_count = filtered_df["Production_Issue"].sum()
    st.metric("🚨 Issues Found", f"{issue_count}/{len(filtered_df)}", delta=f"{100*issue_count/len(filtered_df):.1f}%")

with col2:
    avg_efficiency = filtered_df["Efficiency_Score"].mean()
    st.metric("⚡ Avg Efficiency", f"{avg_efficiency:.3f}", delta=f"{avg_efficiency-0.5:.3f} target")

with col3:
    avg_cycle = filtered_df["Cycle_Time"].mean()
    st.metric("⏱️ Avg Cycle Time", f"{avg_cycle:.1f} min", delta=f"{avg_cycle-50:.1f}")

with col4:
    avg_downtime = filtered_df["Downtime"].mean()
    st.metric("⬇️ Avg Downtime", f"{avg_downtime:.1f} min", delta=f"{avg_downtime-15:.1f}")

with col5:
    avg_units = filtered_df["Units_Produced"].mean()
    st.metric("📦 Avg Units", f"{avg_units:.0f}", delta=f"{avg_units-300:.0f}")

st.markdown("---")

# Dashboard View
if analysis_type == "📈 Dashboard":
    st.header("📈 Production Analysis Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Efficiency Distribution
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(filtered_df["Efficiency_Score"], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
        ax.axvline(filtered_df["Efficiency_Score"].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {filtered_df["Efficiency_Score"].mean():.3f}')
        ax.set_xlabel("Efficiency Score")
        ax.set_ylabel("Count")
        ax.set_title("Efficiency Score Distribution", fontweight='bold')
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        # Severity Pie Chart
        severity_counts = filtered_df["Severity"].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#2ecc71', '#f1c40f', '#e74c3c', '#c0392b']
        ax.pie(severity_counts, labels=severity_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title("Production Status Breakdown", fontweight='bold')
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Issues by Stage
        fig, ax = plt.subplots(figsize=(8, 5))
        stage_issues = filtered_df.groupby("Stage")["Production_Issue"].agg(['sum', 'count'])
        stage_issues['percentage'] = (stage_issues['sum'] / stage_issues['count'] * 100)
        stage_issues['percentage'].plot(kind='bar', ax=ax, color='coral')
        ax.set_title("Production Issue Rate by Stage", fontweight='bold')
        ax.set_ylabel("Issue Percentage (%)")
        ax.set_xlabel("Stage")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        # Cycle Time vs Efficiency
        fig, ax = plt.subplots(figsize=(8, 5))
        scatter = ax.scatter(filtered_df["Cycle_Time"], filtered_df["Efficiency_Score"],
                            c=filtered_df["Production_Issue"], cmap="RdYlGn_r", s=100, alpha=0.6)
        ax.set_xlabel("Cycle Time (min)")
        ax.set_ylabel("Efficiency Score")
        ax.set_title("Cycle Time vs Efficiency", fontweight='bold')
        plt.colorbar(scatter, ax=ax, label="Issue (0=No, 1=Yes)")
        st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("📋 Detailed Records")
    st.dataframe(filtered_df[["Stage", "Cycle_Time", "Downtime", "Defect_Rate", "Efficiency_Score", "Severity", "Production_Issue"]].head(10), use_container_width=True)

# ML Clustering View
elif analysis_type == "🤖 ML Clustering":
    st.header("🤖 Machine Learning Clustering Analysis")
    
    # Perform KMeans clustering
    features_for_clustering = ["Cycle_Time", "Waiting_Time", "Downtime", "Defect_Rate", "Units_Produced"]
    X = df[features_for_clustering].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)
    filtered_df["Cluster"] = df["Cluster"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cluster Distribution Pie Chart
        cluster_counts = filtered_df["Cluster"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_clusters = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        ax.pie(cluster_counts, labels=[f"Cluster {i}" for i in cluster_counts.index], autopct='%1.1f%%', colors=colors_clusters)
        ax.set_title("Production Clusters Distribution", fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        # Cluster Efficiency Box Plot
        fig, ax = plt.subplots(figsize=(8, 5))
        cluster_data = [filtered_df[filtered_df["Cluster"] == i]["Efficiency_Score"].values for i in range(4)]
        ax.boxplot(cluster_data, labels=[f"Cluster {i}" for i in range(4)])
        ax.set_ylabel("Efficiency Score")
        ax.set_title("Efficiency Score by Cluster", fontweight='bold')
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Cluster Statistics Table
    st.subheader("📊 Cluster Statistics")
    cluster_stats = filtered_df.groupby("Cluster").agg({
        "Efficiency_Score": ["mean", "std"],
        "Production_Issue": "sum",
        "Cycle_Time": "mean"
    }).round(3)
    st.dataframe(cluster_stats, use_container_width=True)

# Predictions View
elif analysis_type == "🔮 Predictions":
    st.header("🔮 Production Issue Predictions")
    
    # Train ML Model
    features = ["Cycle_Time", "Waiting_Time", "Downtime", "Defect_Rate", "Units_Produced"]
    X = df[features]
    y = df["Production_Issue"]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X, y)
    
    # Predictions
    df["Predicted_Issue"] = model.predict(X)
    df["Issue_Probability"] = model.predict_proba(X)[:, 1]
    filtered_df = df.copy()
    
    # Feature Importance
    col1, col2 = st.columns(2)
    
    with col1:
        feature_importance = pd.DataFrame({
            'Feature': features,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(feature_importance['Feature'], feature_importance['Importance'], color='skyblue')
        ax.set_xlabel("Importance")
        ax.set_title("ML Model - Feature Importance", fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        # Prediction Accuracy
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model_test = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        model_test.fit(X_train, y_train)
        accuracy = model_test.score(X_test, y_test)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        y_pred = model_test.predict(X_test)
        scatter = ax.scatter(y_test, y_pred, c=model_test.predict_proba(X_test)[:, 1], 
                            cmap='RdYlGn_r', s=100, alpha=0.6)
        ax.plot([0, 1], [0, 1], 'r--', lw=2)
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title(f"Predictions vs Actual (Accuracy: {accuracy:.1%})", fontweight='bold')
        plt.colorbar(scatter, ax=ax, label="Probability")
        st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("🎯 High-Risk Production Records")
    high_risk = filtered_df[filtered_df["Issue_Probability"] > 0.5].sort_values("Issue_Probability", ascending=False)
    if len(high_risk) > 0:
        st.dataframe(high_risk[["Stage", "Cycle_Time", "Downtime", "Efficiency_Score", "Issue_Probability"]].head(10), use_container_width=True)
    else:
        st.success("✅ No high-risk records detected!")

# Export View
elif analysis_type == "📥 Export Data":
    st.header("📥 Export Analysis Results")
    
    export_format = st.radio("Select Export Format", ["CSV", "Excel"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Filtered Data", use_container_width=True):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="production_analysis.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Export Summary Report", use_container_width=True):
            summary_text = f"""
PRODUCTION LINE BOTTLENECK DETECTION - ANALYSIS REPORT
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

=== KEY METRICS ===
Total Records: {len(filtered_df)}
Production Issues: {filtered_df['Production_Issue'].sum()} ({100*filtered_df['Production_Issue'].sum()/len(filtered_df):.1f}%)
Average Efficiency Score: {filtered_df['Efficiency_Score'].mean():.3f}
Average Cycle Time: {filtered_df['Cycle_Time'].mean():.1f} min
Average Downtime: {filtered_df['Downtime'].mean():.1f} min

=== SEVERITY DISTRIBUTION ===
{filtered_df['Severity'].value_counts().to_string()}

=== STAGE PERFORMANCE ===
{filtered_df.groupby('Stage')['Production_Issue'].agg(['sum', 'count']).to_string()}
            """
            st.download_button(
                label="Download Report",
                data=summary_text,
                file_name="production_report.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    st.info("💡 **Tip**: Download analysis results for further review or stakeholder presentations.")

st.markdown("---")
st.info("💡 **Navigation**: Use the sidebar radio buttons to switch between Dashboard, ML Clustering, Predictions, and Export views.")
