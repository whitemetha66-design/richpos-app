import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------- CONFIG & MATCHA-COCOA THEME -----------------
st.set_page_config(
    page_title="RichPOS - Matcha Cocoa Edition",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def apply_custom_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap');

        /* Background: Creamy Warm Background */
        html, body, [class*="css"] {
            font-family: 'Kanit', sans-serif !important;
            background-color: #FAF6F0 !important;
            color: #2D2424 !important;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }

        /* Top Header Area: Dark Cocoa Tone */
        .brand-header {
            background: linear-gradient(135deg, #3C2A21 0%, #1A120B 100%);
            padding: 18px 25px;
            border-radius: 16px;
            box-shadow: 0 10px 20px rgba(60, 42, 33, 0.15);
            margin-bottom: 20px;
        }

        /* Product Card Design: Warm Card with Matcha Hover */
        .product-card {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 14px;
            border: 1px solid #E5D9B6;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
            transition: all 0.25s ease-in-out;
            margin-bottom: 15px;
        }
        .product-card:hover {
            transform: translateY(-4px);
            border-color: #5F7161;
            box-shadow: 0 10px 20px rgba(95, 113, 97, 0.2);
        }

        div[data-testid="stImage"] img {
            height: 150px !important;
            object-fit: cover !important;
            border-radius: 12px !important;
        }

        /* Custom Buttons */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }

        /* Primary Button: Deep Matcha Green */
        button[data-testid="stBaseButton-primary"], div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4E6C50 0%, #395135 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(78, 108, 80, 0.3) !important;
        }
        button[data-testid="stBaseButton-primary"]:hover, div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #395135 0%, #2A3C27 100%) !important;
            box-shadow: 0 6px 15px rgba(78, 108, 80, 0.4) !important;
        }

        /* Secondary Action Buttons: Cocoa Milk Tone */
        div.stButton > button:not([kind="primary"]) {
            background-color: #EFEAD8 !important;
            color: #3C2A21 !important;
            border: 1px solid #D0C9B6 !important;
        }
        div.stButton > button:not([kind="primary"]):hover {
            background-color: #D0C9B6 !important;
            color: #1A120B !important;
        }

        /* Cart Sidebar Box: Warm Creamy Box */
        .cart-box {
            background: #FFFFFF;
            border: 1px solid #E5D9B6;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 10px 25px rgba(60, 42, 33, 0.08);
        }

        /* Input & Select Box styling */
        .stTextInput input, .stSelectbox select, div[data-baseweb="select"] {
            background-color: #FFFFFF !important;
            color: #3C2A21 !important;
            border-radius: 10px !important;
            border: 1px solid #D0C9B6 !important;
        }

        /* Price Tag: Cocoa Rich Brown */
        .price-tag {
            color: #6D4C41;
            font-size: 1.3rem;
            font-weight: 700;
        }

        /* Responsive Mobile tweaks */
        @media (max-width: 768px) {
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_theme()

def get_db():
    conn = sqlite3.connect("richpos.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- DATABASE AUTO MIGRATION & SEED DATA -----------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'ทั่วไป',
            stock REAL DEFAULT 0,
            unit TEXT NOT NULL,
            cost_per_unit REAL DEFAULT 0,
            min_stock REAL DEFAULT 0,
            supplier TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            img_url TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_id INTEGER,
            inventory_id INTEGER,
            qty_used REAL,
            FOREIGN KEY (menu_id) REFERENCES menus (id),
            FOREIGN KEY (inventory_id) REFERENCES inventory (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            name TEXT,
            points INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE,
            table_no TEXT,
            member_phone TEXT,
            subtotal REAL,
            vat REAL,
            grand_total REAL,
            status TEXT DEFAULT 'กำลังทำ',
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            menu_id INTEGER,
            qty INTEGER,
            price_per_unit REAL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (menu_id) REFERENCES menus (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inventory_id INTEGER,
            change_qty REAL,
            balance_qty REAL,
            type TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # --- AUTO SEED INITIAL DATA IF EMPTY ---
    cursor.execute("SELECT COUNT(*) FROM menus")
    if cursor.fetchone()[0] == 0:
        sample_menus = [
            ('มัจฉะลาเต้เย็น', 'ชา', 65.0, 'https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500'),
            ('ดาร์กโกโก้เย็น', 'นม/โกโก้', 60.0, 'https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?w=500'),
            ('เอสเพรสโซเย็น', 'กาแฟ', 55.0, 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500'),
            ('ชาไทยเย็น', 'ชา', 50.0, 'https://images.unsplash.com/photo-1558857563-b371033873b8?w=500'),
            ('อูจิมัจฉะพรีเมียม', 'ชา', 85.0, 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500')
        ]
        cursor.executemany("INSERT INTO menus (name, category, price, img_url) VALUES (?, ?, ?, ?)", sample_menus)

    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        sample_inv = [
            ('ผงมัจฉะเกรดพิธีการ', 'เมล็ดกาแฟ/ผงชา', 1000.0, 'g', 0.8, 100.0, 'Import Japan'),
            ('ผงโกโก้พรีเมียม', 'เมล็ดกาแฟ/ผงชา', 5000.0, 'g', 0.3, 500.0, 'Makro'),
            ('นมสดเมจิ', 'นม/ผลิตภัณฑ์นม', 10000.0, 'ml', 0.05, 2000.0, 'CP'),
            ('เมล็ดกาแฟ House Blend', 'เมล็ดกาแฟ/ผงชา', 2000.0, 'g', 0.45, 300.0, 'Local Roaster')
        ]
        cursor.executemany("INSERT INTO inventory (name, category, stock, unit, cost_per_unit, min_stock, supplier) VALUES (?, ?, ?, ?, ?, ?, ?)", sample_inv)

    conn.commit()
    conn.close()

init_db()

# ----------------- SESSION STATES -----------------
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "current_member" not in st.session_state:
    st.session_state.current_member = None

# ----------------- TOP NAVBAR NAVIGATION -----------------
st.markdown("""
    <div class="brand-header">
        <h1 style="margin:0; font-size: 1.8rem; color: #E5D9B6;">🍵 RichPOS <span style="font-size: 1rem; color: #A594F9;">| Matcha & Cocoa Cafe</span></h1>
    </div>
""", unsafe_allow_html=True)

page = st.selectbox("📌 เลือกหน้าจอการทำงาน", [
    "🛒 1. หน้าขาย (POS)", 
    "💳 2. ชำระเงิน (Checkout)", 
    "👤 3. ระบบสมาชิก (Members)",
    "🍳 4. จัดการครัว (KDS)", 
    "📊 5. สต็อก & แดชบอร์ด",
    "⚙️ 6. หลังบ้าน & จัดการข้อมูล (Admin)"
])

st.write("")

# ==========================================
# PAGE 1: POS MAIN SCREEN
# ==========================================
if page == "🛒 1. หน้าขาย (POS)":
    conn = get_db()
    menus = conn.execute("SELECT * FROM menus").fetchall()
    
    col_main, col_cart = st.columns([1.8, 1.2])

    with col_main:
        st.subheader("🍹 เมนูเครื่องดื่ม & อาหาร")
        
        search_query = st.text_input("🔍 ค้นหาเมนู...", placeholder="พิมพ์ชื่อเมนู เช่น มัจฉะลาเต้, โกโก้เย็น")
        
        categories = ["ทั้งหมด"] + list(set([m["category"] for m in menus])) if menus else ["ทั้งหมด"]
        selected_cat = st.radio("หมวดหมู่:", categories, horizontal=True)
        
        filtered_menus = menus
        if selected_cat != "ทั้งหมด":
            filtered_menus = [m for m in filtered_menus if m["category"] == selected_cat]
        if search_query:
            filtered_menus = [m for m in filtered_menus if search_query.lower() in m["name"].lower()]
        
        if not filtered_menus:
            st.info("ไม่พบรายการสินค้าที่ค้นหา")
        else:
            grid_cols = st.columns(2)
            for idx, item in enumerate(filtered_menus):
                with grid_cols[idx % 2]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(item["img_url"] if item["img_url"] else "https://via.placeholder.com/200", use_container_width=True)
                    st.markdown(f"### {item['name']}")
                    st.markdown(f'<div class="price-tag">฿{item["price"]:.2f}</div>', unsafe_allow_html=True)
                    
                    sweet_level = st.selectbox("หวาน", ["หวานปกติ (100%)", "หวานน้อย (50%)", "หวาน 25%", "ไม่หวาน (0%)", "หวานมาก (125%)"], key=f"sweet_{item['id']}")
                    
                    if st.button(f"🛒 เพิ่มลงตะกร้า", key=f"menu_add_{item['id']}", use_container_width=True, type="primary"):
                        cart_key = f"{item['id']}_{sweet_level}"
                        if cart_key in st.session_state.cart:
                            st.session_state.cart[cart_key]['qty'] += 1
                        else:
                            st.session_state.cart[cart_key] = {
                                'menu_id': item['id'],
                                'name': item['name'],
                                'price': item['price'],
                                'qty': 1,
                                'sweet': sweet_level
                            }
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    with col_cart:
        st.markdown('<div class="cart-box">', unsafe_allow_html=True)
        st.subheader("🛒 รายการสั่งซื้อ")
        
        c_table, c_cname = st.columns([1, 1])
        with c_table:
            table_no = st.selectbox("เลือกโต๊ะ / บริการ", ["โต๊ะ A1", "โต๊ะ A2", "โต๊ะ B1", "โต๊ะ B2", "กลับบ้าน (Takeaway)"])
        with c_cname:
            customer_name = st.text_input("ชื่อลูกค้า / คิว", placeholder="เช่น คุณเมธา")
            
        st.divider()
        st.markdown("**👤 สมาชิก (สะสมแต้ม)**")
        search_phone = st.text_input("เบอร์โทรศัพท์", placeholder="เช่น 0812345678", label_visibility="collapsed")
        
        c_search, c_clear = st.columns(2)
        if c_search.button("ค้นหา", key="btn_pos_search_mem", use_container_width=True):
            mem = conn.execute("SELECT * FROM members WHERE phone = ?", (search_phone,)).fetchone()
            if mem:
                st.session_state.current_member = dict(mem)
                st.success(f"พบคุณ {mem['name']}")
            else:
                st.error("ไม่พบสมาชิก")
        if c_clear.button("ยกเลิก", key="btn_pos_clear_mem", use_container_width=True):
            st.session_state.current_member = None
            st.rerun()

        if st.session_state.current_member:
            st.info(f"👤 **{st.session_state.current_member['name']}** ({st.session_state.current_member['points']} แต้ม)")

        st.divider()
        
        subtotal = 0.0
        if not st.session_state.cart:
            st.warning("ยังไม่มีรายการในตะกร้า")
        else:
            for cart_key, item_data in list(st.session_state.cart.items()):
                item_total = item_data["price"] * item_data["qty"]
                subtotal += item_total
                
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.write(f"**{item_data['name']}**\n({item_data['sweet']})\n฿{item_data['price']} x {item_data['qty']}")
                if c2.button("➖", key=f"cart_minus_{cart_key}"):
                    st.session_state.cart[cart_key]['qty'] -= 1
                    if st.session_state.cart[cart_key]['qty'] <= 0:
                        del st.session_state.cart[cart_key]
                    st.rerun()
                if c3.button("➕", key=f"cart_plus_{cart_key}"):
                    st.session_state.cart[cart_key]['qty'] += 1
                    st.rerun()
                st.divider()

        vat = subtotal * 0.07
        grand_total = subtotal + vat
        
        st.write(f"ราคารวม: **฿{subtotal:.2f}**")
        st.write(f"VAT (7%): **฿{vat:.2f}**")
        st.markdown(f"<h2 style='color:#4E6C50; margin-top:0;'>สุทธิ: ฿{grand_total:.2f}</h2>", unsafe_allow_html=True)
        
        if st.button("🚀 ส่งเข้าครัว / ออกบิล ➔", key="btn_submit_order", use_container_width=True, type="primary", disabled=(subtotal == 0)):
            order_no = f"ORD-{int(datetime.now().timestamp())}"
            mem_phone = st.session_state.current_member["phone"] if st.session_state.current_member else None
            final_table_info = f"{table_no} ({customer_name})" if customer_name else table_no
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO orders (order_no, table_no, member_phone, subtotal, vat, grand_total, status)
                VALUES (?, ?, ?, ?, ?, ?, 'กำลังทำ')
            """, (order_no, final_table_info, mem_phone, subtotal, vat, grand_total))
            
            order_id = cursor.lastrowid
            
            for cart_key, item_data in st.session_state.cart.items():
                menu_id = item_data['menu_id']
                qty = item_data['qty']
                price = item_data['price']
                
                cursor.execute("INSERT INTO order_items (order_id, menu_id, qty, price_per_unit) VALUES (?, ?, ?, ?)",
                               (order_id, menu_id, qty, price))
                
                recipes = conn.execute("SELECT * FROM recipes WHERE menu_id = ?", (menu_id,)).fetchall()
                for r in recipes:
                    used_qty = r["qty_used"] * qty
                    cursor.execute("UPDATE inventory SET stock = stock - ? WHERE id = ?", (used_qty, r["inventory_id"]))
                    
                    new_inv = conn.execute("SELECT stock FROM inventory WHERE id = ?", (r["inventory_id"],)).fetchone()
                    cursor.execute("INSERT INTO stock_logs (inventory_id, change_qty, balance_qty, type, note) VALUES (?, ?, ?, ?, ?)",
                                   (r["inventory_id"], -used_qty, new_inv["stock"], 'SALE', f"ตัดขาย ออเดอร์ {order_no} ({item_data['sweet']})"))
            
            conn.commit()
            st.session_state.cart = {}
            st.session_state.current_member = None
            st.success(f"บันทึกออเดอร์ {order_no} เรียบร้อย!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    conn.close()

# ==========================================
# PAGE 2: CHECKOUT & PAYMENT
# ==========================================
elif page == "💳 2. ชำระเงิน (Checkout)":
    st.subheader("💳 หน้าชำระเงิน & ออกใบเสร็จ")
    conn = get_db()
    pending_orders = conn.execute("SELECT * FROM orders WHERE status != 'ชำระเงินแล้ว' ORDER BY id DESC").fetchall()
    
    if not pending_orders:
        st.info("ไม่มีออเดอร์ค้างชำระ")
    else:
        col_list, col_pay = st.columns([1.5, 1])
        
        with col_list:
            st.markdown("**รายการออเดอร์ที่รอชำระ**")
            order_options = {f"{o['order_no']} ({o['table_no']}) - ฿{o['grand_total']:.2f}": o["id"] for o in pending_orders}
            selected_label = st.selectbox("เลือกรหัสออเดอร์", list(order_options.keys()))
            selected_id = order_options[selected_label]
            
            ord_data = conn.execute("SELECT * FROM orders WHERE id = ?", (selected_id,)).fetchone()
            items = conn.execute("""
                SELECT m.name, i.qty, i.price_per_unit 
                FROM order_items i JOIN menus m ON i.menu_id = m.id 
                WHERE i.order_id = ?
            """, (selected_id,)).fetchall()
            
            st.markdown(f"**โต๊ะ/บริการ:** {ord_data['table_no']} | **สมาชิก:** {ord_data['member_phone'] or 'ไม่ได้ระบุ'}")
            st.divider()
            for it in items:
                st.write(f"- {it['name']} x{it['qty']} = ฿{it['qty']*it['price_per_unit']:.2f}")
            st.divider()
            st.markdown(f"<h2 style='color:#4E6C50;'>ยอดชำระสุทธิ: ฿{ord_data['grand_total']:.2f}</h2>", unsafe_allow_html=True)

        with col_pay:
            st.markdown("**ดำเนินการชำระเงิน**")
            pay_method = st.radio("ช่องทางชำระเงิน", ["เงินสด (Cash)", "PromptPay QR Code"])
            
            if pay_method == "เงินสด (Cash)":
                cash_received = st.number_input("จำนวนเงินที่รับมา", min_value=float(ord_data['grand_total']), step=20.0)
                change = cash_received - ord_data['grand_total']
                st.markdown(f"<h3 style='color:#395135;'>เงินทอน: ฿{change:.2f}</h3>", unsafe_allow_html=True)
            else:
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=PromptPay_{ord_data['grand_total']}", caption="สแกนเพื่อชำระเงิน")

            if st.button("✅ ยืนยันชำระเงิน & สะสมแต้ม", key="btn_confirm_pay", type="primary", use_container_width=True):
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status = 'ชำระเงินแล้ว', payment_method = ? WHERE id = ?", (pay_method, selected_id))
                
                if ord_data['member_phone']:
                    earned_points = int(ord_data['grand_total'] // 50)
                    cursor.execute("UPDATE members SET points = points + ? WHERE phone = ?", (earned_points, ord_data['member_phone']))
                    st.toast(f"สะสมแต้มให้สมาชิกเพิ่ม +{earned_points} แต้มเรียบร้อย!")
                
                conn.commit()
                st.balloons()
                st.success("ชำระเงินสำเร็จ!")
                st.rerun()
    conn.close()

# ==========================================
# PAGE 3: MEMBER MANAGEMENT
# ==========================================
elif page == "👤 3. ระบบสมาชิก (Members)":
    st.subheader("👤 ระบบจัดการสมาชิก (CRM)")
    conn = get_db()
    
    tab1, tab2 = st.tabs(["📋 รายชื่อสมาชิกทั้งหมด", "➕ สมัครสมาชิกใหม่"])
    
    with tab1:
        members = conn.execute("SELECT phone as เบอร์โทร, name as ชื่อลูกค้า, points as แต้มสะสม, created_at as วันที่สมัคร FROM members").fetchall()
        if members:
            df_mem = pd.DataFrame([dict(row) for row in members])
            st.dataframe(df_mem, use_container_width=True)
        else:
            st.info("ยังไม่มีข้อมูลสมาชิก")

    with tab2:
        with st.form("add_member_form"):
            new_phone = st.text_input("เบอร์โทรศัพท์ (10 หลัก)")
            new_name = st.text_input("ชื่อ-นามสกุล ลูกค้า")
            submit = st.form_submit_button("บันทึกสมาชิกใหม่", type="primary")
            
            if submit:
                if len(new_phone) >= 9 and new_name:
                    try:
                        conn.execute("INSERT INTO members (phone, name, points) VALUES (?, ?, 0)", (new_phone, new_name))
                        conn.commit()
                        st.success(f"เพิ่ม คุณ{new_name} เข้าสู่ระบบสมาชิกสำเร็จ!")
                        st.rerun()
                    except:
                        st.error("เบอร์โทรนี้มีในระบบแล้ว")
                else:
                    st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
    conn.close()

# ==========================================
# PAGE 4: KITCHEN DISPLAY SYSTEM (KDS)
# ==========================================
elif page == "🍳 4. จัดการครัว (KDS)":
    st.subheader("🍳 Kitchen Display System (คิวอาหารในครัว)")
    conn = get_db()
    kds_orders = conn.execute("SELECT * FROM orders WHERE status != 'ชำระเงินแล้ว' ORDER BY id ASC").fetchall()
    
    if not kds_orders:
        st.success("🎉 เคลียร์คิวหมดแล้ว ไม่มีรายการอาหารค้าง")
    else:
        kds_cols = st.columns(2)
        for idx, ord_item in enumerate(kds_orders):
            with kds_cols[idx % 2]:
                st.markdown(f"### 📌 {ord_item['order_no']} - {ord_item['table_no']}")
                items = conn.execute("""
                    SELECT m.name, i.qty FROM order_items i 
                    JOIN menus m ON i.menu_id = m.id WHERE i.order_id = ?
                """, (ord_item['id'],)).fetchall()
                
                for item in items:
                    st.write(f"- {item['name']} x{item['qty']}")
                
                st.write(f"สถานะ: **{ord_item['status']}**")
                if ord_item['status'] == "กำลังทำ":
                    if st.button("✅ ทำเสร็จแล้ว", key=f"kds_done_{ord_item['id']}", type="primary"):
                        conn.execute("UPDATE orders SET status = 'เสร็จแล้ว' WHERE id = ?", (ord_item['id'],))
                        conn.commit()
                        st.rerun()
                elif ord_item['status'] == "เสร็จแล้ว":
                    st.success("พร้อมเสิร์ฟ 🚀")
    conn.close()

# ==========================================
# PAGE 5: INVENTORY & DASHBOARD
# ==========================================
elif page == "📊 5. สต็อก & แดชบอร์ด":
    st.subheader("📊 สรุปยอดขาย & จัดการสต็อกวัตถุดิบ")
    conn = get_db()
    
    total_sales = conn.execute("SELECT SUM(grand_total) FROM orders WHERE status = 'ชำระเงินแล้ว'").fetchone()[0] or 0.0
    total_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'ชำระเงินแล้ว'").fetchone()[0]
    total_members = conn.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    
    m1, m2, m3 = st.columns(3)
    m1.metric("ยอดขายรวม (ชำระแล้ว)", f"฿{total_sales:,.2f}")
    m2.metric("จำนวนออเดอร์", f"{total_orders} บิล")
    m3.metric("จำนวนสมาชิก", f"{total_members} คน")
    
    st.divider()
    
    tab_dash1, tab_dash2 = st.tabs(["📦 สต็อก & ขายดี", "📜 ประวัติการเคลื่อนไหวสต็อก (Stock Logs)"])
    
    with tab_dash1:
        col_inv, col_top = st.columns([1.3, 1])
        with col_inv:
            st.markdown("**📦 สต็อกวัตถุดิบคงเหลือ (Real-time)**")
            inv_items = conn.execute("SELECT * FROM inventory").fetchall()
            
            all_cats = ["ทั้งหมด"] + list(set([item["category"] if item["category"] else "ทั่วไป" for item in inv_items]))
            selected_filter_cat = st.selectbox("📁 กรองตามหมวดหมู่:", all_cats)
            
            display_items = inv_items
            if selected_filter_cat != "ทั้งหมด":
                display_items = [item for item in display_items if (item["category"] or "ทั่วไป") == selected_filter_cat]
                
            if display_items:
                table_data = []
                for i in display_items:
                    status = "🔴 ต่ำกว่ากำหนด" if i["stock"] <= i["min_stock"] else "🟢 ปกติ"
                    table_data.append({
                        "ชื่อวัตถุดิบ": i["name"],
                        "หมวดหมู่": i["category"] if i["category"] else "ทั่วไป",
                        "คงเหลือ": f"{i['stock']:.2f}",
                        "หน่วย": i["unit"],
                        "ต้นทุน/หน่วย": f"฿{i['cost_per_unit']:.4f}",
                        "จุดเตือน": f"{i['min_stock']:.2f}",
                        "สถานะ": status
                    })
                st.dataframe(pd.DataFrame(table_data), use_container_width=True)
            else:
                st.info("ไม่มีข้อมูลวัตถุดิบ")
            
        with col_top:
            st.markdown("**🏆 รายการสินค้าขายดี**")
            top_sales = conn.execute("""
                SELECT m.name AS menu_name, SUM(i.qty) AS total_qty 
                FROM order_items i 
                JOIN menus m ON i.menu_id = m.id 
                GROUP BY m.name ORDER BY total_qty DESC LIMIT 5
            """).fetchall()
            
            if top_sales:
                df_top = pd.DataFrame([dict(row) for row in top_sales])
                st.bar_chart(df_top, x="menu_name", y="total_qty")
            else:
                st.info("ยังไม่มีข้อมูลยอดขาย")

    with tab_dash2:
        st.markdown("**📜 ประวัติการปรับเปลี่ยนสต็อกย้อนหลัง**")
        logs = conn.execute("""
            SELECT l.created_at as วันเวลา, i.name as วัตถุดิบ, l.change_qty as จำนวนที่เปลี่ยน, 
                   l.balance_qty as ยอดคงเหลือ, l.type as ประเภท, l.note as หมายเหตุ
            FROM stock_logs l JOIN inventory i ON l.inventory_id = i.id 
            ORDER BY l.id DESC LIMIT 50
        """).fetchall()
        if logs:
            st.dataframe(pd.DataFrame([dict(row) for row in logs]), use_container_width=True)
        else:
            st.info("ยังไม่มีประวัติการเคลื่อนไหวสต็อก")

    conn.close()

# ==========================================
# PAGE 6: ADVANCED ADMIN PANEL (ADD / EDIT / DELETE)
# ==========================================
elif page == "⚙️ 6. หลังบ้าน & จัดการข้อมูล (Admin)":
    st.subheader("⚙️ ระบบหลังบ้าน & จัดการข้อมูลร้าน (Admin Panel)")
    conn = get_db()
    
    tab_menu, tab_stock, tab_recipe, tab_mem_edit = st.tabs([
        "🍰 จัดการเมนู", 
        "📦 จัดการสต็อก & เติม/ตัดของเสีย", 
        "🧪 จัดการสูตรอาหาร", 
        "👤 จัดการสมาชิก"
    ])
    
    with tab_menu:
        st.markdown("**➕ เพิ่มเมนูใหม่**")
        with st.form("form_add_menu"):
            m_name = st.text_input("ชื่อเมนู")
            m_cat = st.selectbox("หมวดหมู่", ["กาแฟ", "ชา", "นม/โกโก้", "โซดา/ผลไม้", "ขนม/เบเกอรี่"])
            m_price = st.number_input("ราคาขาย (บาท)", min_value=0.0, step=5.0)
            m_img = st.text_input("ลิงก์ URL รูปภาพ", value="https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=500")
            if st.form_submit_button("บันทึกเมนูใหม่", type="primary"):
                if m_name and m_price > 0:
                    conn.execute("INSERT INTO menus (name, category, price, img_url) VALUES (?, ?, ?, ?)",
                                 (m_name, m_cat, m_price, m_img))
                    conn.commit()
                    st.success(f"เพิ่มเมนู '{m_name}' สำเร็จ!")
                    st.rerun()

        st.divider()
        st.markdown("**✏️ แก้ไข / 🗑️ ลบเมนู**")
        menus = conn.execute("SELECT * FROM menus").fetchall()
        if menus:
            m_dict = {f"{m['name']} (฿{m['price']})": m for m in menus}
            selected_m_label = st.selectbox("เลือกเมนูที่ต้องการจัดการ", list(m_dict.keys()), key="select_m_manage")
            target_menu = m_dict[selected_m_label]
            
            with st.form("form_edit_menu"):
                edit_m_name = st.text_input("แก้ไขชื่อเมนู", value=target_menu["name"])
                
                cat_options = ["กาแฟ", "ชา", "นม/โกโก้", "โซดา/ผลไม้", "ขนม/เบเกอรี่"]
                default_cat_idx = cat_options.index(target_menu["category"]) if target_menu["category"] in cat_options else 0
                edit_m_cat = st.selectbox("แก้ไขหมวดหมู่", cat_options, index=default_cat_idx)
                
                edit_m_price = st.number_input("แก้ไขราคา (บาท)", value=float(target_menu["price"]), step=5.0)
                edit_m_img = st.text_input("แก้ไข URL รูปภาพ", value=target_menu["img_url"])
                
                if st.form_submit_button("💾 บันทึกการแก้ไขเมนู", type="primary"):
                    conn.execute("UPDATE menus SET name=?, category=?, price=?, img_url=? WHERE id=?",
                                 (edit_m_name, edit_m_cat, edit_m_price, edit_m_img, target_menu["id"]))
                    conn.commit()
                    st.success("อัปเดตข้อมูลเมนูสำเร็จ!")
                    st.rerun()

            if st.button("❌ ลบเมนูนี้ออกจากระบบ", key="btn_del_menu"):
                conn.execute("DELETE FROM menus WHERE id = ?", (target_menu["id"],))
                conn.execute("DELETE FROM recipes WHERE menu_id = ?", (target_menu["id"],))
                conn.commit()
                st.success("ลบเมนูเรียบร้อย!")
                st.rerun()

    with tab_stock:
        st.markdown("**➕ เพิ่มวัตถุดิบใหม่ (แบบรายละเอียด)**")
        with st.form("form_add_inv_advanced"):
            col_i1, col_i2, col_i3 = st.columns([2, 1.5, 1.5])
            inv_name = col_i1.text_input("ชื่อวัตถุดิบ (เช่น ผงมัจฉะ 100g, นมสดเมจิ 2 ลิตร)")
            inv_cat = col_i2.selectbox("หมวดหมู่วัตถุดิบ", ["นม/ผลิตภัณฑ์นม", "เมล็ดกาแฟ/ผงชา", "ไซรัป/ซอส", "ท็อปปิ้ง/วัตถุดิบสด", "บรรจุภัณฑ์ (แก้ว/ฝา/หลอด)", "ของใช้/ทำความสะอาด"])
            supplier = col_i3.text_input("ซัพพลายเออร์ / ร้านที่ซื้อ", placeholder="เช่น Makro / ร้านชา A")

            st.markdown("**📐 การแปลงหน่วย (ซื้อเป็นถุง/ขวด แต่ใช้เป็น g/ml)**")
            col_u1, col_u2, col_u3, col_u4 = st.columns(4)
            buy_unit = col_u1.text_input("หน่วยที่ซื้อ", value="ถุง")
            buy_price = col_u2.number_input("ราคาต่อหน่วยซื้อ (บาท)", min_value=0.0, value=350.0)
            base_unit = col_u3.text_input("หน่วยที่ใช้ชง", value="g")
            conversion_ratio = col_u4.number_input(f"1 {buy_unit} = กี่ {base_unit}?", min_value=1.0, value=500.0)

            cost_per_base_unit = buy_price / conversion_ratio if conversion_ratio > 0 else 0
            st.info(f"💡 ต้นทุนตกอยู่ที่: **฿{cost_per_base_unit:.4f}** ต่อ 1 {base_unit}")

            col_s1, col_s2 = st.columns(2)
            init_stock_base = col_s1.number_input(f"จำนวนสต็อกเริ่มต้น ({base_unit})", min_value=0.0, value=500.0)
            min_stock_alert = col_s2.number_input(f"แจ้งเตือนเมื่อสต็อกต่ำกว่า ({base_unit})", min_value=0.0, value=100.0)

            if st.form_submit_button("💾 บันทึกวัตถุดิบใหม่", type="primary"):
                if inv_name and base_unit:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO inventory (name, category, stock, unit, cost_per_unit, min_stock, supplier) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (inv_name, inv_cat, init_stock_base, base_unit, cost_per_base_unit, min_stock_alert, supplier))
                    
                    new_id = cursor.lastrowid
                    cursor.execute("INSERT INTO stock_logs (inventory_id, change_qty, balance_qty, type, note) VALUES (?, ?, ?, ?, ?)",
                                   (new_id, init_stock_base, init_stock_base, 'REFILL', f"เพิ่มวัตถุดิบใหม่ ({buy_price} บาท/{buy_unit})"))
                    conn.commit()
                    st.success(f"เพิ่ม '{inv_name}' เข้าระบบเรียบร้อยแล้ว!")
                    st.rerun()

        st.divider()
        st.markdown("**🚚 เติมสต็อก (Refill) / 🗑️ ปรับลดของเสีย (Waste)**")
        invs = conn.execute("SELECT * FROM inventory").fetchall()
        if invs:
            inv_dict = {f"{i['name']} (คงเหลือ: {i['stock']} {i['unit']})": i for i in invs}
            selected_inv_label = st.selectbox("เลือกวัตถุดิบที่ต้องการปรับสต็อก", list(inv_dict.keys()), key="select_inv_stock_op")
            target_inv = inv_dict[selected_inv_label]
            
            c_op1, c_op2, c_op3 = st.columns([1, 1, 1.5])
            op_type = c_op1.selectbox("ประเภทการทำรายการ", ["🚚 เติมสต็อก (Refill)", "🗑️ ของเสีย/หมดอายุ (Waste)"])
            change_qty = c_op2.number_input("จำนวน", min_value=0.01, step=1.0)
            op_note = c_op3.text_input("หมายเหตุ", placeholder="เช่น ซื้อผงมัจฉะเพิ่ม หรือ นมหมดอายุ")
            
            if st.button("⚙️ บันทึกการปรับสต็อก", type="primary", key="btn_apply_stock_op"):
                actual_change = change_qty if "เติมสต็อก" in op_type else -change_qty
                log_type = 'REFILL' if "เติมสต็อก" in op_type else 'WASTE'
                
                cursor = conn.cursor()
                cursor.execute("UPDATE inventory SET stock = stock + ? WHERE id = ?", (actual_change, target_inv["id"]))
                new_stock = target_inv["stock"] + actual_change
                
                cursor.execute("INSERT INTO stock_logs (inventory_id, change_qty, balance_qty, type, note) VALUES (?, ?, ?, ?, ?)",
                               (target_inv["id"], actual_change, new_stock, log_type, op_note))
                conn.commit()
                st.success("ปรับปรุงสต็อกและบันทึก Log เรียบร้อย!")
                st.rerun()

        st.divider()
        st.markdown("**✏️ แก้ไขข้อมูลวัตถุดิบ / ❌ ลบออกจากระบบ**")
        if invs:
            with st.form("form_edit_inv"):
                edit_i_name = st.text_input("แก้ไขชื่อวัตถุดิบ", value=target_inv["name"])
                
                inv_cat_options = ["นม/ผลิตภัณฑ์นม", "เมล็ดกาแฟ/ผงชา", "ไซรัป/ซอส", "ท็อปปิ้ง/วัตถุดิบสด", "บรรจุภัณฑ์ (แก้ว/ฝา/หลอด)", "ของใช้/ทำความสะอาด", "ทั่วไป"]
                cur_cat = target_inv["category"] if target_inv["category"] in inv_cat_options else "ทั่วไป"
                default_inv_cat_idx = inv_cat_options.index(cur_cat)
                
                edit_i_cat = st.selectbox("แก้ไขหมวดหมู่", inv_cat_options, index=default_inv_cat_idx)
                edit_i_unit = st.text_input("แก้ไขหน่วยนับ", value=target_inv["unit"])
                edit_i_cost = st.number_input("แก้ไขต้นทุนต่อหน่วย", value=float(target_inv["cost_per_unit"] or 0.0))
                edit_i_min = st.number_input("แก้ไขจุดเตือนสต็อกต่ำ", value=float(target_inv["min_stock"]))
                edit_i_supp = st.text_input("แก้ไขซัพพลายเออร์", value=target_inv["supplier"] or "")
                
                if st.form_submit_button("💾 บันทึกการแก้ไขวัตถุดิบ", type="primary"):
                    conn.execute("UPDATE inventory SET name=?, category=?, unit=?, cost_per_unit=?, min_stock=?, supplier=? WHERE id=?",
                                 (edit_i_name, edit_i_cat, edit_i_unit, edit_i_cost, edit_i_min, edit_i_supp, target_inv["id"]))
                    conn.commit()
                    st.success("อัปเดตข้อมูลวัตถุดิบสำเร็จ!")
                    st.rerun()
            
            if st.button("❌ ลบวัตถุดิบนี้ออกจากระบบถาวร", key="btn_del_inv_perm"):
                conn.execute("DELETE FROM inventory WHERE id = ?", (target_inv["id"],))
                conn.execute("DELETE FROM recipes WHERE inventory_id = ?", (target_inv["id"],))
                conn.commit()
                st.success("ลบวัตถุดิบเรียบร้อย!")
                st.rerun()

    with tab_recipe:
        st.markdown("**🧪 ผูกสูตรอาหารใหม่ (ตัดสต็อกอัตโนมัติ)**")
        menus = conn.execute("SELECT * FROM menus").fetchall()
        invs = conn.execute("SELECT * FROM inventory").fetchall()
        
        if menus and invs:
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                rec_m_id = st.selectbox("เลือกเมนู", [m["name"] for m in menus], key="rec_m")
                selected_m_id = [m["id"] for m in menus if m["name"] == rec_m_id][0]
                
            with col_r2:
                rec_i_id = st.selectbox("เลือกวัตถุดิบที่ใช้", [i["name"] for i in invs], key="rec_i")
                selected_i_id = [i["id"] for i in invs if i["name"] == rec_i_id][0]
                selected_unit = [i["unit"] for i in invs if i["name"] == rec_i_id][0]
                
            qty_used = st.number_input(f"ปริมาณที่ใช้ต่อ 1 แก้ว/จาน ({selected_unit})", min_value=0.001, format="%.3f")
            
            if st.button("🔗 บันทึกสูตรอาหาร", type="primary"):
                conn.execute("INSERT INTO recipes (menu_id, inventory_id, qty_used) VALUES (?, ?, ?)",
                             (selected_m_id, selected_i_id, qty_used))
                conn.commit()
                st.success("ผูกสูตรตัดสต็อกสำเร็จ!")
                st.rerun()

        st.divider()
        st.markdown("**✏️ แก้ไขปริมาณ / 🗑️ ถอดสูตรอาหารออก**")
        recipes_list = conn.execute("""
            SELECT r.id, m.name as menu_name, i.name as inv_name, r.qty_used, i.unit 
            FROM recipes r 
            JOIN menus m ON r.menu_id = m.id 
            JOIN inventory i ON r.inventory_id = i.id
        """).fetchall()
        
        if recipes_list:
            rec_dict = {f"{r['menu_name']} ➔ ใช้ {r['inv_name']} ({r['qty_used']} {r['unit']})": r for r in recipes_list}
            selected_rec_label = st.selectbox("เลือกสูตรที่ต้องการจัดการ", list(rec_dict.keys()), key="select_rec_manage")
            target_rec = rec_dict[selected_rec_label]
            
            new_recipe_qty = st.number_input("แก้ไขปริมาณที่ใช้ต่อ 1 แก้ว/จาน", value=float(target_rec["qty_used"]), format="%.3f", key="edit_rec_qty")
            
            c_rec_edit, c_rec_del = st.columns(2)
            if c_rec_edit.button("💾 บันทึกการแก้ไขปริมาณสูตร", type="primary"):
                conn.execute("UPDATE recipes SET qty_used = ? WHERE id = ?", (new_recipe_qty, target_rec["id"]))
                conn.commit()
                st.success("แก้ไขปริมาณสูตรอาหารสำเร็จ!")
                st.rerun()
                
            if c_rec_del.button("❌ ลบสูตรนี้ออก", key="btn_del_rec_single"):
                conn.execute("DELETE FROM recipes WHERE id = ?", (target_rec["id"],))
                conn.commit()
                st.success("ลบสูตรอาหารเรียบร้อย!")
                st.rerun()

    with tab_mem_edit:
        st.markdown("**✏️ แก้ไขข้อมูลสมาชิก / ปรับแต้มสะสม**")
        mems = conn.execute("SELECT * FROM members").fetchall()
        if mems:
            mem_dict = {f"{m['name']} ({m['phone']}) - {m['points']} แต้ม": m for m in mems}
            selected_mem_label = st.selectbox("เลือกสมาชิกที่ต้องการจัดการ", list(mem_dict.keys()), key="edit_mem_select")
            target_mem = mem_dict[selected_mem_label]
            
            with st.form("form_edit_member"):
                edit_mem_name = st.text_input("แก้ไขชื่อ-นามสกุล", value=target_mem["name"])
                edit_mem_phone = st.text_input("แก้ไขเบอร์โทรศัพท์", value=target_mem["phone"])
                add_pts = st.number_input("ปรับแต้มสะสม (ใส่ค่า + เพื่อเพิ่ม, - เพื่อลด)", value=0, step=10)
                
                if st.form_submit_button("💾 บันทึกการแก้ไขข้อมูลสมาชิก", type="primary"):
                    conn.execute("UPDATE members SET name = ?, phone = ?, points = points + ? WHERE phone = ?",
                                 (edit_mem_name, edit_mem_phone, add_pts, target_mem["phone"]))
                    conn.commit()
                    st.success("อัปเดตข้อมูลสมาชิกสำเร็จ!")
                    st.rerun()

            st.divider()
            st.markdown("**🗑️ ลบรายชื่อสมาชิก**")
            if st.button("❌ ลบสมาชิกรายนี้ออกจากระบบถาวร", key="btn_del_mem_perm"):
                conn.execute("DELETE FROM members WHERE phone = ?", (target_mem["phone"],))
                conn.commit()
                st.success("ลบรายชื่อสมาชิกเรียบร้อย!")
                st.rerun()

    conn.close()
