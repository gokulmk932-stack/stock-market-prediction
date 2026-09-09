import streamlit as st
import base64
import yfinance as yf
import pandas as pd

from database import create_table, register_user, login_user
from model import predict_stock_price, get_prediction_graph


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Stock Market Prediction",
    page_icon="📈",
    layout="wide"
)

create_table()


# ==========================================
# LOAD CSS + BACKGROUND
# ==========================================

def load_css():

    with open("assets/background.jpg", "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    with open("assets/style.css", "r", encoding="utf-8") as f:
        css = f.read()

    css = css.replace(
        "assets/background.jpg",
        f"data:image/jpg;base64,{encoded}"
    )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


load_css()


# ==========================================
# LOGIN PAGE
# ==========================================

def login_page():

    st.markdown(
        "<h1 style='text-align:center;'>📈 Stock Market Prediction</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;color:lightgray;'>"
        "AI Powered Stock Market Prediction System"
        "</h4>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if login_user(username, password):

                st.session_state.logged_in = True

                st.success(
                    "Login Successful ✅"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password ❌"
                )


# ==========================================
# REGISTER PAGE
# ==========================================

def register_page():

    st.title("📝 Register")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        username = st.text_input(
            "Create Username",
            key="reg_user"
        )

        password = st.text_input(
            "Create Password",
            type="password",
            key="reg_pass"
        )

        if st.button(
            "Register",
            use_container_width=True
        ):

            if register_user(username, password):

                st.session_state.logged_in = True

                st.success(
                    "Account Created Successfully ✅"
                )

                st.rerun()

            else:

                st.error(
                    "Username Already Exists ❌"
                )


# ==========================================
# HOME PAGE
# ==========================================

def home_page():

    st.title("🏠 Welcome to Stock Market Prediction")

    st.write(
        "AI Powered Stock Market Prediction System"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📈\n\n"
            "**Live Stock Data**\n\n"
            "View recent stock prices and historical market data."
        )

    with col2:

        st.success(
            "🤖\n\n"
            "**AI Prediction**\n\n"
            "Predict the next day's stock price using Machine Learning."
        )

    with col3:

        st.warning(
            "📊\n\n"
            "**Market Analysis**\n\n"
            "Analyze price movements using charts and data."
        )

    st.divider()

    st.subheader("🚀 How It Works")

    st.write("""
    1. Select a company from the Stock Market page.
    2. Get the latest stock price and historical data.
    3. Run the AI prediction model.
    4. Compare actual and predicted prices.
    5. View the AI-based BUY / SELL / HOLD signal.
    """)


# ==========================================
# STOCK MARKET PAGE
# ==========================================

def stock_market_page():

    st.title("📈 Stock Market")

    st.write(
        "Select a company to view its latest market information."
    )

    stocks = pd.read_csv("stocks.csv")

    company = st.selectbox(
        "🏢 Select Company",
        stocks["Company"]
    )

    stock_name = stocks[
        stocks["Company"] == company
    ]["Symbol"].values[0]

    st.write(
        f"**Selected Stock:** {stock_name}"
    )

    st.divider()

    if st.button(
        "📈 Get Stock Data",
        key="stock_btn",
        use_container_width=True
    ):

        stock = yf.Ticker(stock_name)

        data = stock.history(
            period="1mo"
        )

        if data.empty:

            st.error(
                "❌ Stock Data Not Found"
            )

        else:

            current_price = data["Close"].iloc[-1]
            previous_price = data["Close"].iloc[-2]

            change = current_price - previous_price

            change_percent = (
                change / previous_price
            ) * 100

            st.session_state.stock_name = stock_name
            st.session_state.current_price = current_price
            st.session_state.stock_data = data

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "💰 Current Price",
                    f"₹ {current_price:.2f}"
                )

            with col2:

                st.metric(
                    "📈 Today's Change",
                    f"{change_percent:.2f}%"
                )

            with col3:

                st.metric(
                    "🏢 Company",
                    company
                )

            st.divider()

            st.subheader(
                "📋 Historical Stock Data"
            )

            st.dataframe(
                data,
                use_container_width=True
            )

            st.subheader(
                "📈 Last 1 Month Price Chart"
            )

            st.line_chart(
                data["Close"]
            )


# ==========================================
# AI PREDICTION PAGE
# ==========================================

def prediction_page():

    st.title("🤖 AI Stock Price Prediction")

    st.write(
        "Use Machine Learning to predict the next day's stock price."
    )

    st.divider()

    if "stock_name" not in st.session_state:

        st.warning(
            "⚠️ Please go to 'Stock Market' and "
            "click 'Get Stock Data' first."
        )

        return

    stock_name = st.session_state.stock_name
    current_price = st.session_state.current_price

    st.info(
        f"Selected Stock: **{stock_name}**"
    )

    if st.button(
        "🤖 Predict Tomorrow Price",
        key="predict_btn",
        use_container_width=True
    ):

        with st.spinner(
            "AI model is predicting..."
        ):

            predicted_price, accuracy, error = (
                predict_stock_price(stock_name)
            )

        if predicted_price is not None:

            st.success(
                "Prediction Completed Successfully ✅"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "🤖 Predicted Price",
                    f"₹ {predicted_price:.2f}"
                )

            with col2:

                st.metric(
                    "🎯 Model Accuracy",
                    f"{accuracy * 100:.2f}%"
                )

            with col3:

                st.metric(
                    "📉 Prediction Error",
                    f"₹ {error:.2f}"
                )

            st.divider()

            st.subheader(
                "🤖 AI Recommendation"
            )

            difference = (
                predicted_price - current_price
            )

            if difference > 0:

                st.success(
                    "🟢 BUY Signal\n\n"
                    "The predicted price is higher than "
                    "the current price."
                )

            elif difference < 0:

                st.error(
                    "🔴 SELL Signal\n\n"
                    "The predicted price is lower than "
                    "the current price."
                )

            else:

                st.warning(
                    "🟡 HOLD Signal\n\n"
                    "The predicted price is almost equal "
                    "to the current price."
                )

            st.subheader(
                "📈 Actual vs Predicted Price"
            )

            graph_data = get_prediction_graph(
                stock_name
            )

            if graph_data is not None:

                st.line_chart(
                    graph_data
                )

        else:

            st.error(
                "Prediction Failed ❌"
            )


# ==========================================
# ABOUT PAGE
# ==========================================

def about_page():

    st.title("ℹ️ About Project")

    st.subheader(
        "📈 Stock Market Prediction System"
    )

    st.write("""
    The Stock Market Prediction System is an
    AI-powered application designed to analyze
    stock market data and predict future stock prices.
    """)

    st.divider()

    st.subheader(
        "🧠 Technologies Used"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("""
        - 🐍 Python
        - 🎈 Streamlit
        - 🤖 Machine Learning
        - 📊 Pandas
        """)

    with col2:

        st.write("""
        - 📈 Yahoo Finance
        - 🔢 NumPy
        - 📉 Scikit-learn
        - 💾 SQLite Database
        """)

    st.divider()

    st.subheader(
        "🎯 Project Objective"
    )

    st.write("""
    The main objective of this project is to provide
    an easy-to-use platform for analyzing stock prices
    and generating AI-based predictions using historical
    market data.
    """)

    st.warning(
        "⚠️ This system is developed for educational "
        "and project purposes. Predictions should not "
        "be considered financial advice."
    )


# ==========================================
# LOGOUT
# ==========================================

def logout():

    st.session_state.logged_in = False

    for key in [
        "stock_name",
        "current_price",
        "stock_data"
    ]:

        if key in st.session_state:

            del st.session_state[key]

    st.rerun()


# ==========================================
# DASHBOARD
# ==========================================

def dashboard():

    st.sidebar.title("📋 Menu")

    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "Navigate",
        [
            "🏠 Home",
            "📈 Stock Market",
            "🤖 AI Prediction",
            "ℹ️ About Project"
        ]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

    if menu == "🏠 Home":

        home_page()

    elif menu == "📈 Stock Market":

        stock_market_page()

    elif menu == "🤖 AI Prediction":

        prediction_page()

    elif menu == "ℹ️ About Project":

        about_page()


# ==========================================
# APP CONTROL
# ==========================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if st.session_state.logged_in:

    dashboard()

else:

    option = st.sidebar.selectbox(
        "Choose Option",
        [
            "Login",
            "Register"
        ]
    )

    if option == "Login":

        login_page()

    else:

        register_page()


    
