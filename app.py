import streamlit as st
import base64
import yfinance as yf
import pandas as pd

from database import create_table, register_user, login_user
from model import predict_stock_price, get_prediction_graph


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Stock Market Prediction",
    page_icon="📈",
    layout="wide"
)

create_table()


# -----------------------------------
# Load CSS + Background
# -----------------------------------

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


# -----------------------------------
# Login Page
# -----------------------------------

def login_page():

    st.markdown(
        "<h1 style='text-align:center;'>📈 Stock Market Prediction</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;color:lightgray;'>AI Powered Stock Market Prediction System</h4>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login", use_container_width=True):

            if login_user(username, password):

                st.session_state.logged_in = True

                st.success("Login Successful ✅")

                st.rerun()

            else:

                st.error("Invalid Username or Password ❌")


# -----------------------------------
# Register Page
# -----------------------------------

def register_page():

    st.title("📝 Register")

    col1, col2, col3 = st.columns([1,2,1])

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

                st.success(
                    "Account Created Successfully ✅"
                )

            else:

                st.error(
                    "Username Already Exists ❌"
                )
                
# -----------------------------------
# Dashboard
# -----------------------------------

def dashboard():

    st.title("📊 Stock Market Dashboard")

    st.write("Welcome to AI Powered Stock Market Prediction System")

    st.sidebar.title("📋 Menu")

    # Load Stock List
    stocks = pd.read_csv("stocks.csv")

    company = st.selectbox(
        "🏢 Select Company",
        stocks["Company"]
    )

    stock_name = stocks[
        stocks["Company"] == company
    ]["Symbol"].values[0]

    st.write(f"**Selected Stock:** {stock_name}")

    # -----------------------------
    # Get Stock Data
    # -----------------------------

    if st.button("📈 Get Stock Data", key="stock_btn"):

        stock = yf.Ticker(stock_name)

        data = stock.history(period="1mo")

        if data.empty:

            st.error("❌ Stock Data Not Found")

        else:

            current_price = data["Close"].iloc[-1]
            previous_price = data["Close"].iloc[-2]

            change = current_price - previous_price
            change_percent = (change / previous_price) * 100

            col1, col2 = st.columns(2)

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

            st.subheader("📋 Historical Stock Data")

            st.dataframe(
                data,
                use_container_width=True
            )

            st.subheader("📈 Last 1 Month Price Chart")

            st.line_chart(data["Close"])

            # Save for prediction
            st.session_state.stock_name = stock_name
            st.session_state.current_price = current_price
                # -----------------------------
    # AI Prediction
    # -----------------------------

    st.divider()

    st.subheader("🤖 AI Stock Price Prediction")

    if st.button("Predict Tomorrow Price", key="predict_btn"):

        if "stock_name" not in st.session_state:

            st.warning("⚠️ Please click 'Get Stock Data' first.")

        else:

            stock_name = st.session_state.stock_name
            current_price = st.session_state.current_price

            predicted_price, accuracy, error = predict_stock_price(stock_name)

            if predicted_price is not None:

                st.success("Prediction Completed Successfully ✅")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "🤖 Predicted Price",
                        f"₹ {predicted_price:.2f}"
                    )

                with col2:
                    st.metric(
                        "🎯 Model Accuracy",
                        f"{accuracy*100:.2f}%"
                    )

                with col3:
                    st.metric(
                        "📉 Prediction Error",
                        f"₹ {error:.2f}"
                    )

                st.subheader("🤖 AI Recommendation")

                difference = predicted_price - current_price

                if difference > 0:
                    st.success("🟢 BUY Signal")

                elif difference < 0:
                    st.error("🔴 SELL Signal")

                else:
                    st.warning("🟡 HOLD Signal")

                st.subheader("📈 Actual vs Predicted Price")

                graph_data = get_prediction_graph(stock_name)

                if graph_data is not None:
                    st.line_chart(graph_data)

            else:

                st.error("Prediction Failed ❌")
                    # -----------------------------
    # Logout
    # -----------------------------

    st.divider()

    if st.button("🚪 Logout", key="logout_btn"):

        st.session_state.logged_in = False
        st.rerun()


# -----------------------------------
# App Control
# -----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if st.session_state.logged_in:

    dashboard()

else:

    option = st.sidebar.selectbox(
        "Choose Option",
        ["Login", "Register"]
    )

    if option == "Login":

        login_page()

    else:

        register_page()