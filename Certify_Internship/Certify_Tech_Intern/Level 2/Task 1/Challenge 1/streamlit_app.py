import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Insurance Charges Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
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

class InsurancePredictor:
    def __init__(self):
        self.data = None
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.results = {}
        
    def load_data(self):
        """Load the insurance dataset"""
        try:
            self.data = pd.read_csv('insurance.csv')
            return True
        except FileNotFoundError:
            st.error("❌ Dataset 'insurance.csv' not found. Please make sure the file exists in the same directory.")
            return False
    
    def preprocess_data(self):
        """Preprocess the data for modeling"""
        # Create a copy
        data = self.data.copy()
        
        # Encode categorical variables
        categorical_columns = ['sex', 'smoker', 'region']
        for col in categorical_columns:
            self.label_encoders[col] = LabelEncoder()
            data[col] = self.label_encoders[col].fit_transform(data[col])
        
        # Prepare features and target
        X = data.drop('charges', axis=1)
        y = data['charges']
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale numerical features
        numerical_columns = ['age', 'bmi', 'children']
        self.X_train[numerical_columns] = self.scaler.fit_transform(self.X_train[numerical_columns])
        self.X_test[numerical_columns] = self.scaler.transform(self.X_test[numerical_columns])
        
        return X, y
    
    def train_models(self):
        """Train multiple regression models"""
        # Initialize models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror')
        }
        
        for name, model in models.items():
            # Train model
            model.fit(self.X_train, self.y_train)
            self.models[name] = model
            
            # Make predictions
            y_pred = model.predict(self.X_test)
            
            # Calculate metrics
            mse = mean_squared_error(self.y_test, y_pred)
            r2 = r2_score(self.y_test, y_pred)
            
            self.results[name] = {
                'model': model,
                'mse': mse,
                'rmse': np.sqrt(mse),
                'r2': r2,
                'predictions': y_pred
            }
        
        return self.results
    
    def predict_charges(self, input_features):
        """Predict insurance charges for new input"""
        try:
            # Create input array with exact same structure as training data
            input_data = pd.DataFrame(np.zeros((1, len(self.X_train.columns))), 
                                    columns=self.X_train.columns)
            
            # Fill in the values
            input_data['age'] = input_features['age']
            input_data['bmi'] = input_features['bmi']
            input_data['children'] = input_features['children']
            
            # Encode categorical variables
            input_data['sex'] = self.label_encoders['sex'].transform([input_features['sex']])[0]
            input_data['smoker'] = self.label_encoders['smoker'].transform([input_features['smoker']])[0]
            input_data['region'] = self.label_encoders['region'].transform([input_features['region']])[0]
            
            # Scale numerical features
            numerical_cols = ['age', 'bmi', 'children']
            input_data[numerical_cols] = self.scaler.transform(input_data[numerical_cols])
            
            # Make predictions with all models
            predictions = {}
            for name, model in self.models.items():
                predictions[name] = model.predict(input_data)[0]
            
            return predictions
            
        except Exception as e:
            st.error(f"Prediction error: {e}")
            return None

def main():
    # Main title
    st.markdown('<h1 class="main-header">🏥 Insurance Charges Prediction</h1>', unsafe_allow_html=True)
    
    # Initialize predictor
    predictor = InsurancePredictor()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio(
        "Choose Section",
        ["🏠 Home", "📊 Data Analysis", "🤖 Model Training", "🔮 Make Prediction", "📈 Results"]
    )
    
    # Load data
    if not predictor.load_data():
        return
    
    if app_mode == "🏠 Home":
        st.markdown("""
        ## Welcome to Insurance Charges Prediction System
        
        This application uses machine learning to predict insurance charges based on client attributes.
        
        ### 📋 What you can do:
        - **Data Analysis**: Explore the insurance dataset with interactive visualizations
        - **Model Training**: Train multiple machine learning models (Linear Regression, Random Forest, XGBoost)
        - **Make Predictions**: Get insurance charge predictions for new customers
        - **View Results**: Compare model performance and insights
        
        ### 🎯 Features Used for Prediction:
        - **Age**: Age of the primary beneficiary
        - **Gender**: Male or Female
        - **BMI**: Body Mass Index
        - **Children**: Number of children/dependents
        - **Smoker**: Smoking status (Yes/No)
        - **Region**: Residential area
        
        ### 🚀 Get Started:
        Use the sidebar to navigate through different sections of the application.
        """)
        
        # Quick dataset preview
        st.subheader("📋 Dataset Preview")
        st.dataframe(predictor.data.head(10))
        
    elif app_mode == "📊 Data Analysis":
        st.header("📊 Exploratory Data Analysis")
        
        # Dataset overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(predictor.data))
        with col2:
            st.metric("Average Age", f"{predictor.data['age'].mean():.1f} years")
        with col3:
            st.metric("Average BMI", f"{predictor.data['bmi'].mean():.1f}")
        with col4:
            st.metric("Average Charges", f"${predictor.data['charges'].mean():.2f}")
        
        # Visualizations
        tab1, tab2, tab3 = st.tabs(["Distribution", "Correlations", "Categorical Analysis"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(predictor.data['age'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                ax.set_title('Age Distribution')
                ax.set_xlabel('Age')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)
            
            with col2:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(predictor.data['charges'], bins=20, alpha=0.7, color='lightcoral', edgecolor='black')
                ax.set_title('Insurance Charges Distribution')
                ax.set_xlabel('Charges ($)')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)
        
        with tab2:
            # Calculate correlation matrix
            data_encoded = predictor.data.copy()
            for col in ['sex', 'smoker', 'region']:
                le = LabelEncoder()
                data_encoded[col] = le.fit_transform(data_encoded[col])
            
            fig, ax = plt.subplots(figsize=(10, 6))
            correlation_matrix = data_encoded.corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
            ax.set_title('Feature Correlation Heatmap')
            st.pyplot(fig)
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(8, 4))
                smoker_charges = predictor.data.groupby('smoker')['charges'].mean()
                ax.bar(smoker_charges.index, smoker_charges.values, color=['lightblue', 'red'])
                ax.set_title('Average Charges by Smoking Status')
                ax.set_xlabel('Smoker')
                ax.set_ylabel('Average Charges ($)')
                st.pyplot(fig)
            
            with col2:
                fig, ax = plt.subplots(figsize=(8, 4))
                region_charges = predictor.data.groupby('region')['charges'].mean()
                ax.bar(region_charges.index, region_charges.values, color=['lightgreen', 'orange', 'purple', 'yellow'])
                ax.set_title('Average Charges by Region')
                ax.set_xlabel('Region')
                ax.set_ylabel('Average Charges ($)')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
    
    elif app_mode == "🤖 Model Training":
        st.header("🤖 Model Training")
        
        if st.button("🚀 Train Models", type="primary"):
            with st.spinner("Training models... This may take a few seconds."):
                # Preprocess data
                X, y = predictor.preprocess_data()
                
                # Train models
                results = predictor.train_models()
                
                # Display results
                st.success("✅ Models trained successfully!")
                
                # Performance metrics
                st.subheader("📊 Model Performance")
                results_data = []
                for name, result in results.items():
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
                
                # Best model
                best_model_name = results_df.loc[results_df['R² Score'].idxmax(), 'Model']
                st.info(f"🎯 **Best Performing Model**: {best_model_name}")
                
                # Feature importance
                st.subheader("🔍 Feature Importance (Random Forest)")
                rf_model = predictor.models['Random Forest']
                feature_importance = pd.DataFrame({
                    'Feature': X.columns,
                    'Importance': rf_model.feature_importances_
                }).sort_values('Importance', ascending=True)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(feature_importance['Feature'], feature_importance['Importance'], color='lightgreen')
                ax.set_title('Random Forest Feature Importance')
                ax.set_xlabel('Importance')
                st.pyplot(fig)
        
        else:
            st.info("👆 Click the button above to train the machine learning models.")
    
    elif app_mode == "🔮 Make Prediction":
        st.header("🔮 Predict Insurance Charges")
        
        # Check if models are trained
        if not predictor.models:
            st.warning("⚠️ Please train the models first in the 'Model Training' section.")
            return
        
        # Input form
        st.subheader("📝 Customer Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Age", min_value=18, max_value=100, value=35)
            bmi = st.slider("BMI", min_value=15.0, max_value=50.0, value=25.0, step=0.1)
            children = st.slider("Number of Children", min_value=0, max_value=10, value=0)
        
        with col2:
            sex = st.selectbox("Gender", options=["male", "female"])
            smoker = st.selectbox("Smoker", options=["no", "yes"])
            region = st.selectbox("Region", 
                                options=["southwest", "southeast", "northwest", "northeast"])
        
        # Prediction button
        if st.button("💰 Predict Insurance Charges", type="primary"):
            with st.spinner("Calculating prediction..."):
                input_features = {
                    'age': age,
                    'sex': sex,
                    'bmi': bmi,
                    'children': children,
                    'smoker': smoker,
                    'region': region
                }
                
                predictions = predictor.predict_charges(input_features)
                
                if predictions:
                    # Display predictions
                    st.subheader("📊 Prediction Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Linear Regression",
                            f"${predictions['Linear Regression']:,.2f}"
                        )
                    
                    with col2:
                        st.metric(
                            "Random Forest",
                            f"${predictions['Random Forest']:,.2f}"
                        )
                    
                    with col3:
                        st.metric(
                            "XGBoost",
                            f"${predictions['XGBoost']:,.2f}"
                        )
                    
                    # Average prediction
                    avg_prediction = np.mean(list(predictions.values()))
                    st.success(f"🎯 **Average Predicted Charges**: ${avg_prediction:,.2f}")
                    
                    # Factors affecting premium
                    st.subheader("💡 Factors Affecting Your Premium")
                    
                    factors = []
                    if smoker == "yes":
                        factors.append("🚭 **Smoking**: Significantly increases insurance costs (typically 3-4x higher)")
                    if bmi > 30:
                        factors.append("⚖️ **High BMI**: BMI above 30 may increase your premium")
                    if age > 50:
                        factors.append("👴 **Age**: Older age typically results in higher premiums")
                    if children > 0:
                        factors.append("👪 **Children/Dependents**: More dependents can increase premium")
                    if bmi < 18.5:
                        factors.append("⚖️ **Low BMI**: Underweight may also affect premium")
                    
                    if factors:
                        for factor in factors:
                            st.write(f"- {factor}")
                    else:
                        st.write("✅ Your profile has favorable factors for insurance premiums")
    
    elif app_mode == "📈 Results":
        st.header("📈 Model Results and Insights")
        
        if not predictor.results:
            st.warning("⚠️ Please train the models first in the 'Model Training' section.")
            return
        
        # Key insights
        st.subheader("🎯 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🔍 Top Factors Affecting Insurance Charges:
            1. **Smoking Status** - Most significant factor
            2. **Age** - Older individuals pay higher premiums
            3. **BMI** - Higher BMI increases health risks
            4. **Number of Children** - More dependents increase costs
            5. **Region** - Geographic location affects pricing
            """)
        
        with col2:
            st.markdown("""
            ### 💡 Business Recommendations:
            - Focus on smoking cessation programs
            - Promote healthy BMI ranges
            - Consider regional pricing strategies
            - Use ensemble models for accurate predictions
            """)
        
        # Model comparison chart
        st.subheader("📊 Model Performance Comparison")
        
        # R² scores
        models = list(predictor.results.keys())
        r2_scores = [predictor.results[model]['r2'] for model in models]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(models, r2_scores, color=['skyblue', 'lightgreen', 'orange'])
        ax.set_title('Model Performance (R² Score)')
        ax.set_ylabel('R² Score')
        ax.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, score in zip(bars, r2_scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{score:.4f}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Actual vs Predicted for best model
        st.subheader("📈 Actual vs Predicted Charges (Best Model)")
        
        best_model_name = max(predictor.results.keys(), 
                            key=lambda x: predictor.results[x]['r2'])
        y_pred = predictor.results[best_model_name]['predictions']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(predictor.y_test, y_pred, alpha=0.6)
        ax.plot([predictor.y_test.min(), predictor.y_test.max()], 
                [predictor.y_test.min(), predictor.y_test.max()], 'r--', lw=2)
        ax.set_xlabel('Actual Charges ($)')
        ax.set_ylabel('Predicted Charges ($)')
        ax.set_title(f'{best_model_name} - Actual vs Predicted\nR² = {predictor.results[best_model_name]["r2"]:.4f}')
        st.pyplot(fig)

if __name__ == "__main__":
    main()