import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Customer Segmentation System",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #6A0DAD;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cluster-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #6A0DAD;
        margin: 10px 0px;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0px;
    }
</style>
""", unsafe_allow_html=True)

class CustomerSegmenter:
    def __init__(self):
        self.data = None
        self.customer_data = None
        self.scaler = StandardScaler()
        self.kmeans_model = None
        self.cluster_labels = None
        self.optimal_clusters = 0
        
    def load_data(self):
        """Load the online retail dataset"""
        try:
            self.data = pd.read_csv('online_retail.csv', encoding='ISO-8859-1')
            st.success(f"✅ Dataset loaded successfully with {len(self.data)} records")
            return True
        except FileNotFoundError:
            st.error("❌ 'online_retail.csv' not found. Please make sure the file exists.")
            return False
        except Exception as e:
            st.error(f"❌ Error loading dataset: {e}")
            return False
    
    def preprocess_data(self):
        """Preprocess the retail data and create customer features"""
        st.subheader("🛠️ Data Preprocessing")
        
        # Create a copy of the data
        df = self.data.copy()
        
        # Display basic info about the dataset
        st.write("**Dataset Overview:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Total Customers", df['CustomerID'].nunique())
        with col3:
            st.metric("Total Products", df['StockCode'].nunique())
        with col4:
            st.metric("Total Countries", df['Country'].nunique())
        
        # Show original data sample
        st.write("**Original Data Sample:**")
        st.dataframe(df.head())
        
        # Data cleaning steps
        st.write("**Data Cleaning Steps:**")
        
        # Remove missing values
        initial_count = len(df)
        df = df.dropna(subset=['CustomerID'])
        st.write(f"✅ Removed {initial_count - len(df)} records with missing CustomerID")
        
        # Remove negative quantities and prices
        df = df[df['Quantity'] > 0]
        df = df[df['UnitPrice'] > 0]
        st.write(f"✅ Removed records with negative quantities/prices")
        
        # Create TotalAmount column
        df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
        
        # Remove outliers (very high amounts that might be errors)
        Q1 = df['TotalAmount'].quantile(0.05)
        Q3 = df['TotalAmount'].quantile(0.95)
        df = df[(df['TotalAmount'] >= Q1) & (df['TotalAmount'] <= Q3)]
        st.write(f"✅ Removed outlier transactions")
        
        # Create customer-level features
        st.write("**Creating Customer Features:**")
        
        customer_features = df.groupby('CustomerID').agg({
            'TotalAmount': ['sum', 'mean', 'count'],
            'Quantity': ['sum', 'mean'],
            'InvoiceNo': 'nunique',
            'InvoiceDate': lambda x: (pd.to_datetime(x).max() - pd.to_datetime(x).min()).days
        }).reset_index()
        
        # Flatten column names
        customer_features.columns = [
            'CustomerID', 'TotalSpent', 'AvgTransactionValue', 'TotalItems',
            'TotalQuantity', 'AvgQuantity', 'Frequency', 'Recency'
        ]
        
        # Handle infinite recency values (customers with only one purchase)
        customer_features['Recency'] = customer_features['Recency'].replace(0, 1)
        
        # Calculate additional metrics
        customer_features['AvgOrderValue'] = customer_features['TotalSpent'] / customer_features['Frequency']
        
        self.customer_data = customer_features
        
        st.write("**Customer Features Created:**")
        st.dataframe(self.customer_data.head())
        
        st.success(f"✅ Preprocessing completed! Final dataset: {len(self.customer_data)} customers")
        
        return True
    
    def prepare_features(self):
        """Prepare features for clustering"""
        st.subheader("📊 Feature Preparation for Clustering")
        
        # Select features for clustering
        features_for_clustering = ['TotalSpent', 'Frequency', 'AvgTransactionValue', 'Recency']
        
        # Show feature distributions
        st.write("**Feature Distributions:**")
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.ravel()
        
        for i, feature in enumerate(features_for_clustering):
            axes[i].hist(self.customer_data[feature], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            axes[i].set_title(f'Distribution of {feature}')
            axes[i].set_xlabel(feature)
            axes[i].set_ylabel('Frequency')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Prepare the feature matrix
        X = self.customer_data[features_for_clustering]
        
        # Log transform skewed features to make them more normal
        for feature in ['TotalSpent', 'Frequency', 'AvgTransactionValue']:
            X[feature] = np.log1p(X[feature])
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        st.write("**Features selected for clustering:**", features_for_clustering)
        st.write("**Feature matrix shape:**", X_scaled.shape)
        
        return X_scaled, features_for_clustering
    
    def find_optimal_clusters(self, X_scaled):
        """Find optimal number of clusters using Elbow Method and Silhouette Score"""
        st.subheader("🔍 Determining Optimal Number of Clusters")
        
        # Calculate WCSS for different numbers of clusters
        wcss = []
        silhouette_scores = []
        cluster_range = range(2, 11)
        
        with st.spinner("Calculating optimal clusters..."):
            for i in cluster_range:
                kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
                kmeans.fit(X_scaled)
                wcss.append(kmeans.inertia_)
                
                # Calculate silhouette score
                if len(np.unique(kmeans.labels_)) > 1:  # Need at least 2 clusters for silhouette score
                    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
                else:
                    silhouette_scores.append(0)
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Elbow Method plot
        ax1.plot(cluster_range, wcss, marker='o', linestyle='-', color='b')
        ax1.set_xlabel('Number of Clusters')
        ax1.set_ylabel('Within-Cluster Sum of Squares (WCSS)')
        ax1.set_title('Elbow Method for Optimal Clusters')
        ax1.grid(True)
        
        # Silhouette Score plot
        ax2.plot(cluster_range, silhouette_scores, marker='o', linestyle='-', color='r')
        ax2.set_xlabel('Number of Clusters')
        ax2.set_ylabel('Silhouette Score')
        ax2.set_title('Silhouette Score for Optimal Clusters')
        ax2.grid(True)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Find optimal clusters (using both methods)
        optimal_by_elbow = self._find_elbow_point(wcss) + 2  # +2 because range starts from 2
        optimal_by_silhouette = cluster_range[np.argmax(silhouette_scores)]
        
        st.write(f"**Optimal clusters by Elbow Method:** {optimal_by_elbow}")
        st.write(f"**Optimal clusters by Silhouette Score:** {optimal_by_silhouette}")
        
        # Let user choose or use the optimal
        col1, col2 = st.columns(2)
        with col1:
            st.info("💡 **Recommendation:** Choose the number where the elbow curve bends significantly")
        with col2:
            self.optimal_clusters = st.selectbox(
                "Select number of clusters:",
                options=cluster_range,
                index=optimal_by_elbow-2  # -2 because range starts from 2
            )
        
        return self.optimal_clusters
    
    def _find_elbow_point(self, wcss):
        """Helper function to find the elbow point in WCSS curve"""
        # Calculate the second derivative to find the elbow
        first_deriv = np.diff(wcss)
        second_deriv = np.diff(first_deriv)
        elbow_point = np.argmin(second_deriv) + 1  # +1 because we took two diffs
        return min(elbow_point, len(wcss) - 1)
    
    def apply_kmeans(self, X_scaled, n_clusters):
        """Apply K-Means clustering"""
        st.subheader("🎯 Applying K-Means Clustering")
        
        with st.spinner(f"Training K-Means with {n_clusters} clusters..."):
            self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            self.cluster_labels = self.kmeans_model.fit_predict(X_scaled)
        
        # Add cluster labels to customer data
        self.customer_data['Cluster'] = self.cluster_labels
        
        # Calculate cluster statistics
        cluster_stats = self.customer_data.groupby('Cluster').agg({
            'TotalSpent': ['count', 'mean', 'std'],
            'Frequency': ['mean', 'std'],
            'AvgTransactionValue': ['mean', 'std'],
            'Recency': ['mean', 'std']
        }).round(2)
        
        st.write("**Cluster Statistics:**")
        st.dataframe(cluster_stats)
        
        # Calculate silhouette score
        silhouette_avg = silhouette_score(X_scaled, self.cluster_labels)
        st.metric("Silhouette Score", f"{silhouette_avg:.3f}")
        
        st.success(f"✅ K-Means clustering completed with {n_clusters} clusters")
        
        return self.cluster_labels
    
    def visualize_clusters(self, X_scaled, features):
        """Visualize clusters using PCA and t-SNE"""
        st.subheader("📊 Cluster Visualization")
        
        # Create subplots
        fig = plt.figure(figsize=(20, 6))
        
        # PCA Visualization
        plt.subplot(1, 3, 1)
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_scaled)
        
        scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=self.cluster_labels, cmap='viridis', alpha=0.7)
        plt.colorbar(scatter)
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
        plt.title('PCA - Customer Clusters')
        
        # t-SNE Visualization
        plt.subplot(1, 3, 2)
        tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(X_scaled)-1))
        X_tsne = tsne.fit_transform(X_scaled)
        
        scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=self.cluster_labels, cmap='viridis', alpha=0.7)
        plt.colorbar(scatter)
        plt.xlabel('t-SNE Component 1')
        plt.ylabel('t-SNE Component 2')
        plt.title('t-SNE - Customer Clusters')
        
        # Cluster Size Distribution
        plt.subplot(1, 3, 3)
        cluster_counts = self.customer_data['Cluster'].value_counts().sort_index()
        colors = plt.cm.viridis(np.linspace(0, 1, len(cluster_counts)))
        bars = plt.bar(cluster_counts.index, cluster_counts.values, color=colors, alpha=0.7)
        plt.xlabel('Cluster')
        plt.ylabel('Number of Customers')
        plt.title('Cluster Size Distribution')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Show feature importance in PCA
        st.write("**PCA Feature Importance:**")
        pca_features = pd.DataFrame({
            'Feature': features,
            'PC1_Importance': np.abs(pca.components_[0]),
            'PC2_Importance': np.abs(pca.components_[1])
        })
        st.dataframe(pca_features)
    
    def analyze_clusters(self):
        """Analyze and interpret each cluster"""
        st.subheader("🔍 Cluster Analysis & Interpretation")
        
        # Calculate mean values for each cluster
        cluster_analysis = self.customer_data.groupby('Cluster').agg({
            'TotalSpent': 'mean',
            'Frequency': 'mean',
            'AvgTransactionValue': 'mean',
            'Recency': 'mean',
            'CustomerID': 'count'
        }).round(2)
        
        cluster_analysis = cluster_analysis.rename(columns={'CustomerID': 'CustomerCount'})
        
        # Normalize the metrics for radar chart
        normalized_data = cluster_analysis.copy()
        for column in ['TotalSpent', 'Frequency', 'AvgTransactionValue', 'Recency']:
            normalized_data[column] = (cluster_analysis[column] - cluster_analysis[column].min()) / (cluster_analysis[column].max() - cluster_analysis[column].min())
        
        # Create radar chart
        self._create_radar_chart(normalized_data, cluster_analysis.columns[:-1])
        
        # Display cluster profiles
        st.write("**Cluster Profiles:**")
        
        for cluster_id in sorted(self.customer_data['Cluster'].unique()):
            cluster_data = self.customer_data[self.customer_data['Cluster'] == cluster_id]
            
            with st.expander(f"📋 Cluster {cluster_id} - {len(cluster_data)} customers"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Average Total Spent", f"${cluster_data['TotalSpent'].mean():.2f}")
                    st.metric("Average Frequency", f"{cluster_data['Frequency'].mean():.1f}")
                
                with col2:
                    st.metric("Average Transaction Value", f"${cluster_data['AvgTransactionValue'].mean():.2f}")
                    st.metric("Average Recency (days)", f"{cluster_data['Recency'].mean():.1f}")
                
                # Provide business interpretation
                self._interpret_cluster(cluster_id, cluster_data)
    
    def _create_radar_chart(self, data, features):
        """Create radar chart for cluster comparison"""
        fig = plt.figure(figsize=(12, 8))
        
        # Set angles for radar chart
        angles = np.linspace(0, 2*np.pi, len(features), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        # Create subplot
        ax = fig.add_subplot(111, polar=True)
        
        # Plot each cluster
        colors = plt.cm.viridis(np.linspace(0, 1, len(data)))
        for i, (cluster, row) in enumerate(data.iterrows()):
            values = row[features].tolist()
            values += values[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, label=f'Cluster {cluster}', color=colors[i])
            ax.fill(angles, values, alpha=0.1, color=colors[i])
        
        # Add feature labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(features)
        ax.set_ylim(0, 1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        plt.title('Cluster Comparison Radar Chart', size=14, fontweight='bold')
        
        st.pyplot(fig)
    
    def _interpret_cluster(self, cluster_id, cluster_data):
        """Provide business interpretation for each cluster"""
        avg_spent = cluster_data['TotalSpent'].mean()
        avg_frequency = cluster_data['Frequency'].mean()
        avg_value = cluster_data['AvgTransactionValue'].mean()
        avg_recency = cluster_data['Recency'].mean()
        
        # Determine cluster characteristics
        if avg_spent > self.customer_data['TotalSpent'].mean():
            spending = "High Spender"
        else:
            spending = "Low Spender"
        
        if avg_frequency > self.customer_data['Frequency'].mean():
            frequency = "Frequent Buyer"
        else:
            frequency = "Occasional Buyer"
        
        if avg_value > self.customer_data['AvgTransactionValue'].mean():
            value = "High Value Transactions"
        else:
            value = "Low Value Transactions"
        
        if avg_recency < self.customer_data['Recency'].mean():
            recency = "Recent Customer"
        else:
            recency = "Less Recent Customer"
        
        # Provide recommendations
        st.write("**Characteristics:**")
        st.write(f"- {spending}")
        st.write(f"- {frequency}")
        st.write(f"- {value}")
        st.write(f"- {recency}")
        
        st.write("**Business Recommendations:**")
        if spending == "High Spender" and frequency == "Frequent Buyer":
            st.write("💎 **VIP Customers**: Offer exclusive rewards and premium support")
        elif spending == "High Spender" and frequency == "Occasional Buyer":
            st.write("🎯 **High Potential**: Encourage more frequent purchases with targeted campaigns")
        elif spending == "Low Spender" and frequency == "Frequent Buyer":
            st.write("📈 **Loyal but Low Value**: Upsell higher-value products")
        else:
            st.write("📱 **At-Risk Customers**: Re-engagement campaigns needed")
    
    def deployment_recommendations(self):
        """Provide deployment recommendations"""
        st.subheader("🚀 Deployment Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📋 Marketing Strategies by Cluster:
            
            **VIP Customers (High Spend, High Frequency):**
            - Exclusive loyalty programs
            - Early access to new products
            - Personalized service
            
            **High Potential (High Spend, Low Frequency):**
            - Targeted email campaigns
            - Bundle offers
            - Cross-selling opportunities
            
            **Loyal but Low Value (Low Spend, High Frequency):**
            - Volume discounts
            - Product recommendations
            - Upselling strategies
            
            **At-Risk Customers (Low Spend, Low Frequency):**
            - Win-back campaigns
            - Special discounts
            - Feedback collection
            """)
        
        with col2:
            st.markdown("""
            ### 🛠️ Implementation Steps:
            
            1. **Integrate with CRM System**
               - Tag customers with cluster labels
               - Update customer profiles
               
            2. **Automate Campaigns**
               - Set up automated email sequences
               - Create segment-specific promotions
               
            3. **Monitor Performance**
               - Track cluster migration over time
               - Measure campaign effectiveness
               
            4. **Continuous Improvement**
               - Retrain model quarterly
               - Update features based on business needs
               
            ### 📊 Key Metrics to Track:
            - Customer Lifetime Value by cluster
            - Retention rates
            - Campaign conversion rates
            - Cluster stability over time
            """)

def main():
    st.markdown('<h1 class="main-header">👥 Retail Customer Segmentation</h1>', unsafe_allow_html=True)
    
    # Initialize segmenter
    segmenter = CustomerSegmenter()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio(
        "Choose Section",
        ["🏠 Home", "📊 Data Preprocessing", "🔍 Cluster Analysis", "🎯 Clustering", "📈 Visualization", "🚀 Deployment"]
    )
    
    # Load data
    if not segmenter.load_data():
        st.stop()
    
    if app_mode == "🏠 Home":
        st.markdown("""
        ## Welcome to Customer Segmentation System
        
        This application uses K-Means clustering to segment retail customers based on their 
        purchasing behavior and spending patterns.
        
        ### 📋 What you can do:
        - **Data Preprocessing**: Clean and prepare retail transaction data
        - **Feature Engineering**: Create customer-level features for clustering
        - **Optimal Clusters**: Use Elbow Method to find the best number of clusters
        - **K-Means Clustering**: Group customers into meaningful segments
        - **Cluster Visualization**: Explore clusters using PCA and t-SNE
        - **Business Insights**: Get actionable recommendations for each segment
        
        ### 🎯 Methodology:
        - **K-Means Clustering**: Unsupervised learning algorithm for grouping similar customers
        - **Elbow Method**: Determines optimal number of clusters
        - **PCA/t-SNE**: Dimensionality reduction for visualization
        - **RFM Analysis**: Recency, Frequency, Monetary value features
        
        ### 📊 Dataset Information:
        """)
        
        if segmenter.data is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(segmenter.data))
            with col2:
                st.metric("Total Customers", segmenter.data['CustomerID'].nunique())
            with col3:
                st.metric("Total Products", segmenter.data['StockCode'].nunique())
            with col4:
                st.metric("Total Countries", segmenter.data['Country'].nunique())
            
            st.subheader("Dataset Preview")
            st.dataframe(segmenter.data.head())
            
            st.subheader("Dataset Columns")
            st.write(list(segmenter.data.columns))
    
    elif app_mode == "📊 Data Preprocessing":
        st.header("📊 Data Preprocessing & Feature Engineering")
        
        if st.button("Start Data Preprocessing", type="primary"):
            with st.spinner("Preprocessing data..."):
                if segmenter.preprocess_data():
                    st.success("✅ Data preprocessing completed!")
    
    elif app_mode == "🔍 Cluster Analysis":
        st.header("🔍 Cluster Analysis & Optimal Clusters")
        
        if segmenter.customer_data is None:
            st.warning("⚠️ Please preprocess the data first in the 'Data Preprocessing' section.")
        else:
            # Prepare features
            X_scaled, features = segmenter.prepare_features()
            
            # Find optimal clusters
            optimal_clusters = segmenter.find_optimal_clusters(X_scaled)
            
            # Store for next steps
            st.session_state.X_scaled = X_scaled
            st.session_state.features = features
            st.session_state.optimal_clusters = optimal_clusters
    
    elif app_mode == "🎯 Clustering":
        st.header("🎯 Apply K-Means Clustering")
        
        if 'X_scaled' not in st.session_state:
            st.warning("⚠️ Please complete cluster analysis first in the 'Cluster Analysis' section.")
        else:
            if st.button("Apply K-Means Clustering", type="primary"):
                with st.spinner("Applying K-Means clustering..."):
                    cluster_labels = segmenter.apply_kmeans(
                        st.session_state.X_scaled, 
                        st.session_state.optimal_clusters
                    )
                    st.session_state.cluster_labels = cluster_labels
    
    elif app_mode == "📈 Visualization":
        st.header("📈 Cluster Visualization & Analysis")
        
        if 'cluster_labels' not in st.session_state:
            st.warning("⚠️ Please apply K-Means clustering first in the 'Clustering' section.")
        else:
            # Visualize clusters
            segmenter.visualize_clusters(st.session_state.X_scaled, st.session_state.features)
            
            # Analyze clusters
            segmenter.analyze_clusters()
            
            # Show customer data with clusters
            st.subheader("📋 Customer Data with Cluster Labels")
            st.dataframe(segmenter.customer_data.head(10))
    
    elif app_mode == "🚀 Deployment":
        st.header("🚀 Deployment & Business Recommendations")
        
        if segmenter.customer_data is None or 'Cluster' not in segmenter.customer_data.columns:
            st.warning("⚠️ Please complete all previous steps first.")
        else:
            segmenter.deployment_recommendations()
            
            # Export options
            st.subheader("📤 Export Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Download Cluster Data"):
                    csv = segmenter.customer_data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="customer_segments.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("Generate Cluster Report"):
                    st.info("📊 Cluster report generation feature would be implemented here")
            
            # Model persistence (conceptual)
            st.subheader("💾 Model Persistence")
            st.write("""
            For production deployment, consider:
            - Saving the trained K-Means model using joblib/pickle
            - Creating API endpoints for real-time clustering
            - Integrating with your CRM system
            - Setting up automated retraining pipelines
            """)

if __name__ == "__main__":
    main()