import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Crime Rate Prediction System",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 10px 0px;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0px;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0px;
    }
</style>
""", unsafe_allow_html=True)

class CrimePredictor:
    def __init__(self):
        self.data = None
        self.classification_models = {}
        self.regression_models = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='median')
        self.X_train_clf = None
        self.X_test_clf = None
        self.y_train_clf = None
        self.y_test_clf = None
        self.X_train_reg = None
        self.X_test_reg = None
        self.y_train_reg = None
        self.y_test_reg = None
        
    def load_data(self):
        """Load the crime dataset"""
        try:
            # Load the dataset
            self.data = pd.read_csv('crime.csv')
            st.success(f"✅ Dataset loaded successfully with {len(self.data)} records and {len(self.data.columns)} features")
            
            # Display column information
            st.write("**Dataset Columns:**", list(self.data.columns))
            
            # Check if we have the required columns for analysis
            if 'crime_category' not in self.data.columns:
                # Try to create crime_category if we have crime rate data
                crime_rate_cols = [col for col in self.data.columns if 'crime' in col.lower() or 'rate' in col.lower()]
                if crime_rate_cols:
                    st.info(f"📊 Using '{crime_rate_cols[0]}' for crime categorization")
                    # Create crime category based on the first crime rate column found
                    crime_data = self.data[crime_rate_cols[0]]
                    bins = [0, crime_data.quantile(0.33), crime_data.quantile(0.66), crime_data.max()]
                    self.data['crime_category'] = pd.cut(crime_data, bins=bins, labels=['Low', 'Medium', 'High'])
                else:
                    st.warning("⚠️ No crime rate column found. Please ensure your dataset has crime-related data.")
            
            return True
        except FileNotFoundError:
            st.error("❌ 'crime.csv' not found. Please make sure the file exists in the same directory.")
            return False
        except Exception as e:
            st.error(f"❌ Error loading dataset: {e}")
            return False
    
    def analyze_missing_data(self):
        """Analyze and visualize missing data"""
        st.subheader("🔍 Missing Data Analysis")
        
        # Calculate missing values
        missing_data = self.data.isnull().sum()
        missing_percent = (missing_data / len(self.data)) * 100
        
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percentage': missing_percent.values
        }).sort_values('Missing_Percentage', ascending=False)
        
        missing_df = missing_df[missing_df['Missing_Count'] > 0]
        
        if len(missing_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Missing Values Summary:**")
                st.dataframe(missing_df.style.format({'Missing_Percentage': '{:.2f}%'}))
            
            with col2:
                # Visualization of missing data
                fig, ax = plt.subplots(figsize=(10, 6))
                missing_df.plot(x='Column', y='Missing_Percentage', kind='bar', ax=ax, color='coral')
                ax.set_title('Percentage of Missing Values by Column')
                ax.set_ylabel('Missing Percentage (%)')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
            
            # Show impact of missing data
            st.subheader("📉 Impact of Missing Data")
            
            # Create a copy of data with and without missing values for comparison
            complete_cases = self.data.dropna()
            incomplete_cases = self.data[self.data.isnull().any(axis=1)]
            
            if len(complete_cases) > 0 and len(incomplete_cases) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Complete Cases", len(complete_cases))
                    # Show average of first numerical column for comparison
                    numerical_cols = self.data.select_dtypes(include=[np.number]).columns
                    if len(numerical_cols) > 0:
                        avg_value = complete_cases[numerical_cols[0]].mean()
                        st.metric(f"Avg {numerical_cols[0]} (Complete)", f"{avg_value:.2f}")
                
                with col2:
                    st.metric("Incomplete Cases", len(incomplete_cases))
                    if len(numerical_cols) > 0:
                        avg_value = incomplete_cases[numerical_cols[0]].mean()
                        st.metric(f"Avg {numerical_cols[0]} (Incomplete)", f"{avg_value:.2f}")
        else:
            st.success("✅ No missing values found in the dataset!")
    
    def preprocess_data(self):
        """Preprocess the data for modeling"""
        st.subheader("🛠️ Data Preprocessing")
        
        # Create a copy of the data
        data_processed = self.data.copy()
        
        # Display original data info
        st.write("**Original Data Info:**")
        st.write(f"Shape: {data_processed.shape}")
        
        # Handle missing values
        numerical_cols = data_processed.select_dtypes(include=[np.number]).columns
        categorical_cols = data_processed.select_dtypes(include=['object']).columns
        
        # Impute numerical missing values
        if data_processed[numerical_cols].isnull().sum().sum() > 0:
            data_processed[numerical_cols] = self.imputer.fit_transform(data_processed[numerical_cols])
            st.success(f"✅ Imputed missing values in numerical columns")
        
        # Encode categorical variables
        for col in categorical_cols:
            if col != 'crime_category':  # We'll handle target separately
                self.label_encoders[col] = LabelEncoder()
                data_processed[col] = self.label_encoders[col].fit_transform(data_processed[col].astype(str))
                st.write(f"✅ Encoded categorical variable: {col}")
        
        # Prepare features for classification (predict crime category)
        classification_features = [col for col in data_processed.columns 
                                 if col != 'crime_category' and data_processed[col].dtype != 'category']
        
        # Remove any non-numeric columns that might have been missed
        classification_features = [col for col in classification_features if data_processed[col].dtype != 'object']
        
        X_clf = data_processed[classification_features]
        y_clf = data_processed['crime_category']
        
        # Prepare features for regression - use the same features as classification
        # For regression target, use the first crime-related numerical column
        crime_related_cols = [col for col in data_processed.columns 
                            if ('crime' in col.lower() or 'rate' in col.lower()) 
                            and col != 'crime_category'
                            and data_processed[col].dtype in [np.number]]
        
        if crime_related_cols:
            regression_target = crime_related_cols[0]
            X_reg = data_processed[classification_features]
            y_reg = data_processed[regression_target]
            st.info(f"📈 Using '{regression_target}' as regression target")
        else:
            # If no crime rate column, use the first numerical column
            numerical_cols = data_processed.select_dtypes(include=[np.number]).columns
            if len(numerical_cols) > 0:
                regression_target = numerical_cols[0]
                X_reg = data_processed[classification_features]
                y_reg = data_processed[regression_target]
                st.warning(f"⚠️ Using '{regression_target}' as regression target (no crime rate column found)")
            else:
                st.error("❌ No numerical columns found for regression")
                return None
        
        # Split data for classification
        self.X_train_clf, self.X_test_clf, self.y_train_clf, self.y_test_clf = train_test_split(
            X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
        )
        
        # Split data for regression
        self.X_train_reg, self.X_test_reg, self.y_train_reg, self.y_test_reg = train_test_split(
            X_reg, y_reg, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.X_train_clf_scaled = self.scaler.fit_transform(self.X_train_clf)
        self.X_test_clf_scaled = self.scaler.transform(self.X_test_clf)
        self.X_train_reg_scaled = self.scaler.fit_transform(self.X_train_reg)
        self.X_test_reg_scaled = self.scaler.transform(self.X_test_reg)
        
        st.success("✅ Data preprocessing completed!")
        st.write(f"**Classification:** Training: {self.X_train_clf.shape[0]} samples, Testing: {self.X_test_clf.shape[0]} samples")
        st.write(f"**Regression:** Training: {self.X_train_reg.shape[0]} samples, Testing: {self.X_test_reg.shape[0]} samples")
        st.write(f"**Features used:** {list(X_clf.columns)}")
        
        return data_processed
    
    def train_classification_models(self):
        """Train classification models for crime-prone areas"""
        st.subheader("🎯 Training Classification Models")
        
        # Initialize models
        models = {
            'SVM': SVC(kernel='rbf', random_state=42, probability=True),
            'Random Forest Classifier': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        classification_results = {}
        
        for name, model in models.items():
            with st.spinner(f"Training {name}..."):
                if name == 'SVM':
                    model.fit(self.X_train_clf_scaled, self.y_train_clf)
                    y_pred = model.predict(self.X_test_clf_scaled)
                    y_pred_proba = model.predict_proba(self.X_test_clf_scaled)
                else:
                    model.fit(self.X_train_clf, self.y_train_clf)
                    y_pred = model.predict(self.X_test_clf)
                    y_pred_proba = model.predict_proba(self.X_test_clf)
                
                accuracy = accuracy_score(self.y_test_clf, y_pred)
                
                classification_results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba
                }
                
                self.classification_models[name] = model
        
        # Display results
        st.subheader("📊 Classification Model Performance")
        
        results_data = []
        for name, result in classification_results.items():
            results_data.append({
                'Model': name,
                'Accuracy': result['accuracy']
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df.style.format({'Accuracy': '{:.4f}'})
                    .highlight_max(subset=['Accuracy'], color='lightgreen'))
        
        # Confusion Matrix for SVM
        if 'SVM' in classification_results:
            st.subheader("📈 SVM Confusion Matrix")
            cm = confusion_matrix(self.y_test_clf, classification_results['SVM']['predictions'])
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                       xticklabels=self.y_test_clf.unique(),
                       yticklabels=self.y_test_clf.unique())
            ax.set_xlabel('Predicted')
            ax.set_ylabel('Actual')
            ax.set_title('SVM Confusion Matrix')
            st.pyplot(fig)
        
        return classification_results
    
    def train_regression_models(self):
        """Train regression models for crime rate forecasting"""
        st.subheader("📈 Training Regression Models")
        
        # Initialize models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        regression_results = {}
        
        for name, model in models.items():
            with st.spinner(f"Training {name}..."):
                if name == 'Linear Regression':
                    model.fit(self.X_train_reg_scaled, self.y_train_reg)
                    y_pred = model.predict(self.X_test_reg_scaled)
                else:
                    model.fit(self.X_train_reg, self.y_train_reg)
                    y_pred = model.predict(self.X_test_reg)
                
                mse = mean_squared_error(self.y_test_reg, y_pred)
                rmse = np.sqrt(mse)
                r2 = r2_score(self.y_test_reg, y_pred)
                
                regression_results[name] = {
                    'model': model,
                    'mse': mse,
                    'rmse': rmse,
                    'r2': r2,
                    'predictions': y_pred
                }
                
                self.regression_models[name] = model
        
        # Display results
        st.subheader("📊 Regression Model Performance")
        
        results_data = []
        for name, result in regression_results.items():
            results_data.append({
                'Model': name,
                'MSE': result['mse'],
                'RMSE': result['rmse'],
                'R² Score': result['r2']
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df.style.format({
            'MSE': '{:.2f}',
            'RMSE': '{:.2f}',
            'R² Score': '{:.4f}'
        }).highlight_max(subset=['R² Score'], color='lightgreen'))
        
        # Actual vs Predicted plot
        st.subheader("📊 Actual vs Predicted Values")
        
        best_reg_model = max(regression_results.keys(), 
                           key=lambda x: regression_results[x]['r2'])
        y_pred_best = regression_results[best_reg_model]['predictions']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(self.y_test_reg, y_pred_best, alpha=0.6)
        ax.plot([self.y_test_reg.min(), self.y_test_reg.max()], 
                [self.y_test_reg.min(), self.y_test_reg.max()], 'r--', lw=2)
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title(f'{best_reg_model} - Actual vs Predicted\nR² = {regression_results[best_reg_model]["r2"]:.4f}')
        st.pyplot(fig)
        
        return regression_results
    
    def predict_crime(self, input_features):
        """Predict crime category and rate for new input"""
        try:
            # Prepare input data
            input_df = pd.DataFrame([input_features])
            
            # Encode categorical variables
            for col in input_df.select_dtypes(include=['object']).columns:
                if col in self.label_encoders:
                    input_df[col] = self.label_encoders[col].transform([input_df[col].iloc[0]])[0]
            
            # Ensure correct column order and fill missing columns with 0
            input_df = input_df.reindex(columns=self.X_train_clf.columns, fill_value=0)
            
            # Scale features
            input_scaled = self.scaler.transform(input_df)
            
            # Make predictions
            classification_pred = {}
            regression_pred = {}
            
            # Classification predictions
            for name, model in self.classification_models.items():
                if name == 'SVM':
                    pred_class = model.predict(input_scaled)[0]
                    pred_proba = model.predict_proba(input_scaled)[0]
                    classification_pred[name] = {
                        'class': pred_class,
                        'probability': max(pred_proba)
                    }
                else:
                    pred_class = model.predict(input_df)[0]
                    pred_proba = model.predict_proba(input_df)[0]
                    classification_pred[name] = {
                        'class': pred_class,
                        'probability': max(pred_proba)
                    }
            
            # Regression predictions
            regression_input_df = input_df.reindex(columns=self.X_train_reg.columns, fill_value=0)
            regression_input_scaled = self.scaler.transform(regression_input_df)
            
            for name, model in self.regression_models.items():
                if name == 'Linear Regression':
                    pred_value = model.predict(regression_input_scaled)[0]
                else:
                    pred_value = model.predict(regression_input_df)[0]
                regression_pred[name] = pred_value
            
            return classification_pred, regression_pred
            
        except Exception as e:
            st.error(f"Prediction error: {e}")
            return None, None

def main():
    st.markdown('<h1 class="main-header">🚔 Crime Rate Prediction System</h1>', unsafe_allow_html=True)
    
    # Initialize predictor
    predictor = CrimePredictor()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio(
        "Choose Section",
        ["🏠 Home", "📊 Data Analysis", "🛠️ Preprocessing", "🎯 Classification", "📈 Regression", "🔮 Predict"]
    )
    
    # Load data
    if not predictor.load_data():
        st.stop()
    
    if app_mode == "🏠 Home":
        st.markdown("""
        ## Welcome to Crime Rate Prediction System
        
        This application uses machine learning to predict crime rates and classify crime-prone areas 
        based on historical data and socio-economic factors.
        
        ### 📋 Features:
        - **Missing Data Analysis**: Visualize and understand the impact of missing data
        - **Data Preprocessing**: Handle missing values and encode categorical variables
        - **Crime Classification**: SVM and Random Forest to classify areas as Low/Medium/High crime
        - **Crime Forecasting**: Linear Regression and Random Forest to predict crime rates
        - **Interactive Predictions**: Make predictions for new areas
        
        ### 🎯 Models Used:
        - **Classification**: SVM, Random Forest Classifier
        - **Regression**: Linear Regression, Random Forest Regressor
        """)
        
        # Display dataset info
        if predictor.data is not None:
            st.subheader("📋 Dataset Information")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(predictor.data))
            with col2:
                st.metric("Total Features", len(predictor.data.columns))
            with col3:
                numerical_cols = len(predictor.data.select_dtypes(include=[np.number]).columns)
                st.metric("Numerical Features", numerical_cols)
            with col4:
                categorical_cols = len(predictor.data.select_dtypes(include=['object']).columns)
                st.metric("Categorical Features", categorical_cols)
            
            st.subheader("Dataset Preview")
            st.dataframe(predictor.data.head())
            
            st.subheader("Dataset Columns")
            st.write(list(predictor.data.columns))
    
    elif app_mode == "📊 Data Analysis":
        st.header("📊 Data Analysis & Missing Data Impact")
        
        # Dataset overview
        st.subheader("📋 Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", len(predictor.data))
        with col2:
            st.metric("Numerical Features", len(predictor.data.select_dtypes(include=[np.number]).columns))
        with col3:
            st.metric("Categorical Features", len(predictor.data.select_dtypes(include=['object']).columns))
        with col4:
            missing_total = predictor.data.isnull().sum().sum()
            st.metric("Total Missing Values", missing_total)
        
        # Missing data analysis
        predictor.analyze_missing_data()
        
        # Basic statistics
        st.subheader("📈 Basic Statistics")
        numerical_data = predictor.data.select_dtypes(include=[np.number])
        if not numerical_data.empty:
            st.dataframe(numerical_data.describe())
        
        # Crime distribution
        if 'crime_category' in predictor.data.columns:
            st.subheader("📊 Crime Category Distribution")
            fig, ax = plt.subplots(figsize=(8, 6))
            predictor.data['crime_category'].value_counts().plot(kind='bar', ax=ax, color=['green', 'orange', 'red'])
            ax.set_title('Distribution of Crime Categories')
            ax.set_xlabel('Crime Category')
            ax.set_ylabel('Count')
            st.pyplot(fig)
        
        # Correlation heatmap
        st.subheader("🔥 Correlation Heatmap")
        numerical_data = predictor.data.select_dtypes(include=[np.number])
        if len(numerical_data.columns) > 1:
            fig, ax = plt.subplots(figsize=(12, 8))
            correlation_matrix = numerical_data.corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax, fmt='.2f')
            ax.set_title('Feature Correlation Heatmap')
            st.pyplot(fig)
    
    elif app_mode == "🛠️ Preprocessing":
        st.header("🛠️ Data Preprocessing")
        
        if st.button("Start Data Preprocessing", type="primary"):
            with st.spinner("Preprocessing data..."):
                processed_data = predictor.preprocess_data()
                if processed_data is not None:
                    st.success("✅ Data preprocessing completed!")
                    
                    # Show preprocessing details
                    st.subheader("Preprocessing Steps Applied:")
                    st.write("1. ✅ Missing value imputation (Median for numerical features)")
                    st.write("2. ✅ Categorical variable encoding (Label Encoding)")
                    st.write("3. ✅ Feature scaling (StandardScaler)")
                    st.write("4. ✅ Train-test split (80-20 ratio)")
                    
                    # Show processed data sample
                    st.subheader("Processed Data Sample")
                    st.dataframe(processed_data.head())
    
    elif app_mode == "🎯 Classification":
        st.header("🎯 Crime Classification Models")
        
        if predictor.X_train_clf is None:
            st.warning("⚠️ Please preprocess the data first in the 'Preprocessing' section.")
        else:
            if st.button("Train Classification Models", type="primary"):
                classification_results = predictor.train_classification_models()
                
                # Feature importance for Random Forest
                if 'Random Forest Classifier' in classification_results:
                    st.subheader("🔍 Feature Importance (Random Forest)")
                    rf_model = classification_results['Random Forest Classifier']['model']
                    feature_importance = pd.DataFrame({
                        'Feature': predictor.X_train_clf.columns,
                        'Importance': rf_model.feature_importances_
                    }).sort_values('Importance', ascending=True)
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.barh(feature_importance['Feature'], feature_importance['Importance'], color='lightblue')
                    ax.set_title('Random Forest Feature Importance for Classification')
                    ax.set_xlabel('Importance')
                    st.pyplot(fig)
    
    elif app_mode == "📈 Regression":
        st.header("📈 Crime Rate Forecasting Models")
        
        if predictor.X_train_reg is None:
            st.warning("⚠️ Please preprocess the data first in the 'Preprocessing' section.")
        else:
            if st.button("Train Regression Models", type="primary"):
                regression_results = predictor.train_regression_models()
                
                # Feature importance for Random Forest
                if 'Random Forest Regressor' in regression_results:
                    st.subheader("🔍 Feature Importance (Random Forest)")
                    rf_model = regression_results['Random Forest Regressor']['model']
                    feature_importance = pd.DataFrame({
                        'Feature': predictor.X_train_reg.columns,
                        'Importance': rf_model.feature_importances_
                    }).sort_values('Importance', ascending=True)
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.barh(feature_importance['Feature'], feature_importance['Importance'], color='lightgreen')
                    ax.set_title('Random Forest Feature Importance for Regression')
                    ax.set_xlabel('Importance')
                    st.pyplot(fig)
    
    elif app_mode == "🔮 Predict":
        st.header("🔮 Predict Crime for New Area")
        
        if not predictor.classification_models or not predictor.regression_models:
            st.warning("⚠️ Please train the models first in the Classification and Regression sections.")
        else:
            st.subheader("📝 Enter Area Details")
            
            # Get available categorical values from the dataset
            available_states = []
            available_districts = []
            
            if 'state' in predictor.data.columns:
                available_states = sorted(predictor.data['state'].dropna().unique())
            if 'district' in predictor.data.columns:
                available_districts = sorted(predictor.data['district'].dropna().unique())
            
            # If no categorical data found, use defaults
            if not available_states:
                available_states = ['State_A', 'State_B', 'State_C']
            if not available_districts:
                available_districts = ['Urban', 'Rural', 'Metro']
            
            col1, col2 = st.columns(2)
            
            with col1:
                state = st.selectbox("State", options=available_states)
                district = st.selectbox("District Type", options=available_districts)
                year = st.slider("Year", min_value=2015, max_value=2025, value=2023)
                population = st.number_input("Population", min_value=10000, max_value=10000000, value=500000)
            
            with col2:
                literacy_rate = st.slider("Literacy Rate (%)", min_value=50.0, max_value=100.0, value=75.0)
                unemployment_rate = st.slider("Unemployment Rate (%)", min_value=1.0, max_value=20.0, value=8.0)
                poverty_rate = st.slider("Poverty Rate (%)", min_value=5.0, max_value=50.0, value=20.0)
                police_stations = st.number_input("Number of Police Stations", min_value=1, max_value=200, value=25)
            
            if st.button("Predict Crime", type="primary"):
                input_features = {
                    'state': state,
                    'district': district,
                    'year': year,
                    'population': population,
                    'literacy_rate': literacy_rate,
                    'unemployment_rate': unemployment_rate,
                    'poverty_rate': poverty_rate,
                    'police_stations': police_stations
                }
                
                # Add other common crime-related columns with default values
                common_columns = ['murder_cases', 'robbery_cases', 'theft_cases', 'assault_cases']
                for col in common_columns:
                    if col in predictor.data.columns:
                        input_features[col] = 0
                
                classification_pred, regression_pred = predictor.predict_crime(input_features)
                
                if classification_pred and regression_pred:
                    st.subheader("📊 Prediction Results")
                    
                    # Classification results
                    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                    st.write("**🎯 Crime Classification:**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        svm_pred = classification_pred['SVM']
                        crime_level = svm_pred['class']
                        confidence = svm_pred['probability'] * 100
                        
                        # Color code based on crime level
                        if crime_level == 'Low':
                            color = "🟢"
                        elif crime_level == 'Medium':
                            color = "🟡"
                        else:
                            color = "🔴"
                        
                        st.metric("Predicted Crime Level", f"{color} {crime_level}")
                        st.metric("Confidence", f"{confidence:.1f}%")
                    
                    with col2:
                        # Show factors affecting prediction
                        st.write("**Factors Considered:**")
                        factors = []
                        if unemployment_rate > 10:
                            factors.append("📈 High unemployment rate")
                        if poverty_rate > 25:
                            factors.append("💸 High poverty rate")
                        if literacy_rate < 70:
                            factors.append("📚 Low literacy rate")
                        if police_stations < 20:
                            factors.append("👮 Low police presence")
                        
                        if factors:
                            for factor in factors:
                                st.write(f"- {factor}")
                        else:
                            st.write("✅ Favorable conditions")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Regression results
                    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                    st.write("**📈 Crime Rate Forecast:**")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        lr_pred = regression_pred['Linear Regression']
                        st.metric("Linear Regression", f"{lr_pred:.1f}")
                    
                    with col2:
                        rf_pred = regression_pred['Random Forest Regressor']
                        st.metric("Random Forest", f"{rf_pred:.1f}")
                    
                    with col3:
                        avg_pred = (lr_pred + rf_pred) / 2
                        st.metric("Average Prediction", f"{avg_pred:.1f}")
                    
                    # Interpretation
                    st.write("**💡 Interpretation:**")
                    if avg_pred < 100:
                        st.success("Low crime rate expected - Generally safe area")
                    elif avg_pred < 250:
                        st.warning("Medium crime rate - Standard precautions advised")
                    else:
                        st.error("High crime rate - Enhanced security measures recommended")
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()