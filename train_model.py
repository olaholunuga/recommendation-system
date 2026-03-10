from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy
import os
import joblib

def train_movie_model():
    # 1. Load the built-in MovieLens 100k dataset
    # Surprise handles the download and caching automatically [3], 
    data = Dataset.load_builtin('ml-100k')

    # 2. Split data into training (80%) and testing (20%) sets [1]
    trainset, testset = train_test_split(data, test_size=0.20)

    # 3. Initialize the SVD algorithm
    # SVD uses matrix factorization to estimate user-item ratings 
    # Formula: r_hat = mu + bu + bi + (qi^T * pu) 
    model = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)

    # 4. Train the model on the training set [1]
    print("Training the SVD model...")
    model.fit(trainset)

    # 5. Evaluate the model performance
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)
    
    print(f"Model Training Complete. RMSE: {rmse:.4f}, MAE: {mae:.4f}")

    # 6. Save the model for the Flask API
    os.makedirs('models', exist_ok=True)
    model_path = 'models/svd_model.joblib'
    joblib.dump(model, model_path)
    print(f"Model successfully saved to {model_path}")
    
    return model

if __name__ == "__main__":
    train_movie_model()