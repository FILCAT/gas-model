import pandas as pd
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error, median_absolute_error
from sklearn.model_selection import train_test_split

def perform_regression(csv_file):
    df = pd.read_csv(csv_file)
    X = df[['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']]
    Y = df['TotalGas']

    # Split the dataset into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Perform multiple linear regression
    lm = LinearRegression()
    lm.fit(X_train, Y_train)

    # Predict on the test set
    Y_pred = lm.predict(X_test)

    # Print the coefficients
    print('Intercept: \n', lm.intercept_)
    print('Coefficients: \n', lm.coef_)

    # Print R^2 and MSE
    print('R^2: \n', r2_score(Y_test, Y_pred))
    print('MSE: \n', mean_squared_error(Y_test, Y_pred))
    print('Explained Var: \n', explained_variance_score(Y_test, Y_pred))
    print('Mean Absolute Error: \n', mean_absolute_error(Y_test, Y_pred))

    # For outliers, let's consider points with a large difference between actual and predicted as potential outliers
    df_test = pd.DataFrame({'Actual': Y_test, 'Predicted': Y_pred})
    df_test['Residuals'] = abs(df_test['Actual'] - df_test['Predicted'])

    # Assume that any point with a residual in the top 1% of residuals is an outlier
    threshold = df_test['Residuals'].quantile(0.999)
    outliers = df_test[df_test['Residuals'] > threshold]
    print('Potential Outliers: \n', outliers)

    Ref = df[['Address', 'Height']]
    print('Outlier References: \n', Ref.iloc[outliers.index])
    

# Usage
if len(sys.argv) < 2:
        print("Expect path to vector data")
else:
        perform_regression(sys.argv[1])
