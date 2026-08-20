import yfinance as yf
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error


def predict_stock_price(stock_symbol):

    data = yf.download(
        stock_symbol,
        period="1y",
        auto_adjust=True
    )


    if data.empty:
        return None, None, None



    close_price = data["Close"]


    if isinstance(close_price, pd.DataFrame):

        close_price = close_price.iloc[:, 0]


    df = pd.DataFrame()

    df["Close"] = close_price


    df["Prediction"] = df["Close"].shift(-1)


    df.dropna(
        inplace=True
    )


    X = df[["Close"]]

    y = df["Prediction"]



    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    model = LinearRegression()


    model.fit(
        X_train,
        y_train
    )


    # Accuracy

    test_prediction = model.predict(
        X_test
    )


    accuracy = r2_score(
        y_test,
        test_prediction
    )


    error = mean_absolute_error(
        y_test,
        test_prediction
    )



    current_price = float(
        df["Close"].iloc[-1]
    )


    predicted_price = model.predict(
        [[current_price]]
    )


    return (
        float(predicted_price[0]),
        accuracy,
        error
    )
def get_prediction_graph(stock_symbol):

    data = yf.download(
        stock_symbol,
        period="1y",
        auto_adjust=True
    )


    if data.empty:
        return None


    close_price = data["Close"]


    if isinstance(close_price, pd.DataFrame):
        close_price = close_price.iloc[:,0]


    df = pd.DataFrame()

    df["Actual"] = close_price


    df["Predicted"] = df["Actual"].shift(1)


    df.dropna(inplace=True)


    return df