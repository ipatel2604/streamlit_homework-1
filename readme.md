# Homework 2: Smart Coffee Kiosk UI - Streamlit
**Scenario:** You are upgrading the backend logic for the **"Smart Coffee Kiosk"** into a modern web dashboard. The owner needs a graphical interface to track inventory in real-time, place orders, and manage stock without writing code.

**Goal:** Build a Streamlit application that performs CRUD operations on inventory items and orders, using tabs for navigation and a JSON file for data persistence.

## Learning Goals
- Build Interactive UIs with Streamlit
- Organize content using Layout elements (Tabs, Columns, Containers, etc.)
- Implement Persistent Storage with JSON
- Handle User Input with appropriate Widgets

## Project Setup
1. **GitHub:** Create a new repository on GitHub named `misy350-homework2`.
2. **Local Folder:** Create a folder on your computer with the same name.
3. **VS Code:** Open this new folder in VS Code.
4. **Environment:**
   - Create a virtual environment (optional but recommended).
   - Install Streamlit: `pip install streamlit`.
5. **Files:** Create the following files:
   - `app.py` (Your main application code)
   - `inventory.json` (Your data storage)
   - `.gitignore` (Add `.env` and `__pycache__`)

## Requirements

### 1. Data Persistence (JSON)
- Instead of hardcoding the list every time, you must load data from `inventory.json` at the start of the app.
- Whenever data changes (New Order, Update Stock, Cancel Order), save the updated list back to `inventory.json`.

**Starter `inventory.json` Content:**
Create this file manually in your folder to start:
```json
[
    {"id": 1, "name": "Espresso", "price": 2.50, "stock": 40},
    {"id": 2, "name": "Latte", "price": 4.25, "stock": 25},
    {"id": 3, "name": "Cold Brew", "price": 3.75, "stock": 30},
    {"id": 4, "name": "Mocha", "price": 4.50, "stock": 20},
    {"id": 5, "name": "Blueberry Muffin", "price": 2.95, "stock": 18}
]
```

**Loading Data (At the top of your app):**
Use `pathlib` to check if the file exists before loading.
```python
import json
from pathlib import Path

json_file = Path("inventory.json")

if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)
else:
    # Default data if file doesn't exist
    inventory = [] 
```

**Saving Data (After any details change):**
Use this standard pattern whenever you modify the list.
```python
with open(json_file, "w") as f:
    json.dump(inventory, f, indent=4)
```

### 2. UI Structure & Navigation
- You must organize your application into four distinct sections.
- Choose a navigation structure (e.g., Tabs, Sidebar, etc.) that makes it easy for the user to switch between tasks.
  1.  **Place Order** (Create)
  2.  **View Inventory** (Read)
  3.  **Restock** (Update)
  4.  **Manage Orders** (Delete/Cancel)

---

## CRUD Sections (Implementation Guide)

### Section 1: Place Order (Create)
**Goal:** Allow the user to select an item and place an order.
1.  **Select Item:** Provide a way for the user to choose a drink from the inventory.
2.  **Quantity:** Provide an input for the user to choose how many items to order.
3.  **Customer Name:** A text input to capture the customer's name.
4.  **Action:** When the user submits the order:
    *   Check if there is enough stock.
    *   If yes:
        *   Reduce the stock in the inventory list.
        *   Calculate Total Price (`price * quantity`).
        *   Create an order dictionary `{ "order_id": "...", "customer": "...", "item": "...", "total": 8.50, "status": "Placed" }`.
        *   Append to an `orders` list (you can keep orders in `st.session_state` or a separate JSON).
        *   **Save** the updated inventory back to `inventory.json`.
        *   Show a success message.
        *   **Receipt:** Display the full order details (Order ID, Item, Customer Name, Total, Status) inside an expander.
    *   If no: Show an error message "Out of Stock".

### Section 2: View & Search Inventory (Read)
**Goal:** Display the current status of items with search functionality.
1.  **Search:** Provide a text input or search bar to filter items by name.
2.  **Metrics:** Display a summary metric (e.g., "Total Items in Stock").
3.  **Display:** Display the full (or filtered) inventory list in a clean, readable format.
    *   *Bonus:* Highlight items with low stock (e.g., stock < 10) in red or with a warning icon.

### Section 3: Restock (Update)
**Goal:** Update the stock quantity for an existing item.
1.  **Selection:** Provide a way to pick an item to restock.
2.  **New Stock Input:** Provide an input to enter the added amount (or the new total).
3.  **Action:** When the update is triggered:
    *   Update the item's stock in the list.
    *   **Save** changes to `inventory.json`.
    *   Show a success message.

### Section 4: Manage Orders (Delete/Cancel)
**Goal:** Cancel an order and return items to inventory.
1.  **View Orders:** Display the list of active orders.
2.  **Selection:** Select an order to cancel (by ID or selection).
3.  **Action:** When an order is cancelled:
    *   Change status to "Cancelled" or remove it from the list.
    *   **Important:** Find the original item and **add the quantity back** to the inventory stock.
    *   **Save** the updated inventory to `inventory.json`.
    *   Show a message "Order Cancelled and Stock Refunded".

---

## Testing Plan
Run your app with `streamlit run app.py` and perform these steps:

1.  **View Inventory:**
    *   Check that "Latte" has 25 stock.
2.  **Place Order:**
    *   Select "Latte", Quantity: 2, Name: "Alice".
    *   Place the Order.
    *   Verify "Order Placed" message.
3.  **Verify Update:**
    *   Go back to "View Inventory". Matches should now show stock of **23**.
4.  **Restock:**
    *   Go to Restock section. Select "Cold Brew". Add 10 (or set to 40).
    *   Save and verify in Inventory section.
5.  **Cancel:**
    *   Go to Manage Orders. Cancel "Alice's" order.
    *   Go to View Inventory. "Latte" stock should return to **25**.

## Deliverables
1.  **Source Code:** Submit your `app.py`
2.  **GitHub Repo:** A screenshot of your GitHub repository page showing your files.
3.  **App Screenshots:**
    *   **Place Order:** Screenshot showing the form or a success message.
    *   **View & Search:** Screenshot showing the inventory list and search bar.
    *   **Restock:** Screenshot showing the restocking interface.
    *   **Manage Orders:** Screenshot showing the order cancellation interface.# streamlit_homework-1
