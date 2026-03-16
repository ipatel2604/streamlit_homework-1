import streamlit as st
import json
import time
import uuid
from pathlib import Path

st.set_page_config(page_title="Smart Coffee Kiosk Application")
st.title("Smart Coffee Kiosk Application")

# --- Session State ---
if "inventory" not in st.session_state:
    st.session_state["inventory"] = []

if "orders" not in st.session_state:
    st.session_state["orders"] = []

if "order_counter" not in st.session_state:
    st.session_state["order_counter"] = 1

# --- Load Inventory ---
json_file = Path("inventory.json")

inventory = [
    {"id": 1, "name": "Espresso",         "price": 2.50, "stock": 40},
    {"id": 2, "name": "Latte",            "price": 4.25, "stock": 25},
    {"id": 3, "name": "Cold Brew",        "price": 3.75, "stock": 30},
    {"id": 4, "name": "Mocha",            "price": 4.50, "stock": 20},
    {"id": 5, "name": "Blueberry Muffin", "price": 2.95, "stock": 18},
]

if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)

st.session_state["inventory"] = inventory

# --- Load Orders ---
orders_file = Path("orders.json")

if orders_file.exists():
    with open(orders_file, "r") as f:
        st.session_state["orders"] = json.load(f)

st.session_state["order_counter"] = len(st.session_state["orders"]) + 1

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Place Order", "View Inventory", "Restock", "Manage Orders"])


# TAB 1 - PLACE ORDER

with tab1:
    st.markdown("## Place an Order")

    customer_name = st.text_input("Customer Name", placeholder="e.g. Alice",
                                  help="Enter the name of the customer placing the order.",
                                  key="order_customer")

    selected_item = st.selectbox("Select Item",
                                 options=st.session_state["inventory"],
                                 format_func=lambda x: f"{x['name']} (${x['price']:.2f})",
                                 key="order_item")

    quantity = st.number_input("Quantity", min_value=1, max_value=50, value=1, key="order_quantity")

    btn_place = st.button("Place Order", key="btn_place_order", use_container_width=True, type="primary")

    if btn_place:
        if not customer_name:
            st.warning("Customer name needs to be provided!")
        elif selected_item["stock"] < quantity:
            st.error("Out of Stock")
        else:
            with st.spinner("Recording your order..."):
                time.sleep(2)

                for item in st.session_state["inventory"]:
                    if item["id"] == selected_item["id"]:
                        item["stock"] -= quantity
                        break

                with open(json_file, "w") as f:
                    json.dump(st.session_state["inventory"], f, indent=4)

                order_id = f"ORD{st.session_state['order_counter']:03d}"
                st.session_state["order_counter"] += 1
                total = round(selected_item["price"] * quantity, 2)

                order = {
                    "order_id": order_id,
                    "customer": customer_name,
                    "item": selected_item["name"],
                    "quantity": quantity,
                    "total": total,
                    "status": "Placed"
                }

                st.session_state["orders"].append(order)

                with open(orders_file, "w") as f:
                    json.dump(st.session_state["orders"], f, indent=4)

            st.success("Order Placed!")
            st.info(f"Order ID: {order['order_id']}")

            with st.expander("View Receipt"):
                st.markdown(f"**Order ID:** {order['order_id']}")
                st.markdown(f"**Customer:** {order['customer']}")
                st.markdown(f"**Item:** {order['item']}")
                st.markdown(f"**Quantity:** {order['quantity']}")
                st.markdown(f"**Total:** ${order['total']:.2f}")
                st.markdown(f"**Status:** {order['status']}")

            time.sleep(4)
            st.rerun()

# TAB 2 - VIEW INVENTORY


with tab2:
    st.markdown("## View Inventory")

    tab_option = st.radio("View/Search", ["View", "Search"], horizontal=True, key="view_search_radio")

    if tab_option == "View":
        total_stock = sum(i["stock"] for i in st.session_state["inventory"])
        st.metric("Total Units in Stock", total_stock)
        st.divider()
        st.dataframe(st.session_state["inventory"])

    else:
        titles = []
        for item in st.session_state["inventory"]:
            titles.append(item["name"])

        selected_title = st.selectbox("Select an item", titles, key="search_select_title")

        selected_inventory_item = {}
        for item in st.session_state["inventory"]:
            if item["name"] == selected_title:
                selected_inventory_item = item
                break

        st.divider()

        selected_inventory_item = st.selectbox("Select Item",
                                               options=st.session_state["inventory"],
                                               format_func=lambda x: f"{x['name']} (${x['price']:.2f})",
                                               key="search_select_item")

        if selected_inventory_item:
            with st.expander("Item Details", expanded=True):
                st.markdown(f"### {selected_inventory_item['name']}")
                st.markdown(f"**Price:** ${selected_inventory_item['price']:.2f}")
                st.markdown(f"**Stock:** {selected_inventory_item['stock']}")

# TAB 3 - RESTOCK

with tab3:
    st.markdown("## Restock an Item")

    titles = []
    for item in st.session_state["inventory"]:
        titles.append(item["name"])

    selected_restock = st.selectbox("Select Item to Restock", titles, key="restock_select_title")

    restock_item = {}
    for item in st.session_state["inventory"]:
        if item["name"] == selected_restock:
            restock_item = item
            break

    if restock_item:
        add_amount = st.number_input("Units to Add", min_value=1, max_value=500, value=10,
                                     help="Enter how many units you want to add to the current stock.",
                                     key=f"restock_amount_{restock_item['id']}")

    btn_restock = st.button("Update Stock", key="btn_restock", use_container_width=True, type="primary")

    if btn_restock:
        with st.spinner("Updating stock..."):
            time.sleep(2)

            for item in st.session_state["inventory"]:
                if item["name"] == selected_restock:
                    item["stock"] += add_amount
                    new_stock = item["stock"]
                    break

            with open(json_file, "w") as f:
                json.dump(st.session_state["inventory"], f, indent=4)

        st.success(f"{selected_restock} restocked! New stock: {new_stock} units.")
        time.sleep(4)
        st.rerun()

# TAB 4 - MANAGE ORDERS


with tab4:
    st.markdown("## Manage Orders")

    orders = st.session_state["orders"]

    active_orders = []
    for o in orders:
        if o["status"] == "Placed":
            active_orders.append(o)

    st.markdown("### Active Orders")

    if not active_orders:
        st.info("No active orders to manage.")
    else:
        st.dataframe(active_orders)

        st.divider()

        cancel_order = st.selectbox("Select Order to Cancel",
                                    options=active_orders,
                                    format_func=lambda x: f"{x['order_id']} - {x['customer']} ({x['item']})",
                                    key="cancel_select")

        btn_cancel = st.button("Cancel Order", key="btn_cancel", use_container_width=True, type="secondary")

        if btn_cancel:
            with st.spinner("Cancelling order and refunding stock..."):
                time.sleep(2)

                for o in st.session_state["orders"]:
                    if o["order_id"] == cancel_order["order_id"]:
                        o["status"] = "Cancelled"
                        break

                for item in st.session_state["inventory"]:
                    if item["name"] == cancel_order["item"]:
                        item["stock"] += cancel_order["quantity"]
                        break

                with open(orders_file, "w") as f:
                    json.dump(st.session_state["orders"], f, indent=4)

                with open(json_file, "w") as f:
                    json.dump(st.session_state["inventory"], f, indent=4)

            st.success("Order Cancelled and Stock Refunded.")
            time.sleep(4)
            st.rerun()

    st.divider()
    st.markdown("### All Orders History")

    if not orders:
        st.info("No orders have been placed yet.")
    else:
        st.dataframe(orders)

# --- Sidebar ---
with st.sidebar:
    st.markdown("Smart Coffee Kiosk")
    if st.session_state["inventory"]:
        st.markdown(f"Total Items: {len(st.session_state['inventory'])}")