"""
**Bagaimana demografi konsumen?**
- Hasil analisis menunjukkan bahwa demografi konsumen pada Ecommerce mayoritas berasal dari Negara SP dan Kota Sau Paulo

**Produk apa yang paling banyak dan paling sedikit terjual?**
- Furniture decor menjadi produk yang paling banyak terjual dan security and services menjadi produk yang paling sedikit terjual
- Health and beauty merupakan produk yang memiliki jumlah pendapatan terbanyak sedangkan yang terendah berasal dari security and service.

**Wilayah mana saja yang memiliki tingkat transaksi dan penjualan tertinggi dan terendah?**
- SP menjadi negara dengan jumlah pendapatan dan jumlah penjualan terbanyak, sedangkan jumlah pendapatan dan jumlah penjualan terendah berasal dari Negara RR
- sau paulo menjadi kota dengan jumlah pendapatan terbanyak, sedangkan polo petruqiumincu de triunfu memiliki jumlah pendapatan terendah.
**Jenis pembayaran apakah yang paling sering digunakan customers dan memiliki jumlah nilai terbesar saat pembelian?**
- Credit card menjadi jenis pembayaran yang paling diminati, diikuti dengan boleto dan voucer

**Bagaimana tingkat kepuasan konsumen apabila diukur melalui tingkat delay pengiriman dan review produk?**
- Review skor barang menunjukkan trend yang fluktuatif dengan jumlah skor terendah berada di bulan November 2016 dan Maret 2018
- Lebih dari 63% pengguna memberikan skor bintang lima berdasarkan data 30 hari terakhir..
- Sepanjang 3 tahun terakhir, pengiriman barang menunjukkan hal positif yaitu 93% tidak delay

**Bagaimana strategi yang dapat diterapkan untuk meningkatkan penjualan berdasarkan karakteristik konsumen yang ada?**
- Berdasarkan hal tersebut, pemberian promo dan diskon dapat diberikan pada konsumen di Negara SP dan Kota Sao Paulo untuk tetap meningkatkan jumlah kontribusi pembelian mereka secara konsisten.
- Mempertahankan konsistensi dari produk yang dijual dan pengiriman barang agar tidak terjadi penurunan kepuasan konsumen.
- Untuk wilayah yang memiliki pendapatan rendah perlu identifikasi lebih lanjut dari faktor eksternal nya untuk memahami tingkah laku mereka, mencakup kondisi makroekonomi, infrastruktur untuk mendukung pembelian online, dan daya beli masyarakat.

**Persiapan apa saja yang perlu dilakukan untuk melaksanakan strategi tersebut?**
- Persiapan yang dilakukan mencakup planning untuk membuat kampanye marketing dan analisis lebih mendalam pada daerah yang memiliki penjualan yang rendah

**Bagaimana performa penjualan dan revenue perusahaan dalam beberapa bulan terakhir?**
- Analisis ini menunjukkan bahwa tingkat penjualan dan pendapatan terus naik secara konsisten dari  tahun 2016 hingga 2018.
"""


# Import semua library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Membuat helper function

def create_daily_orders_df(df): # Fungsi Daily orders
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id" : "nunique",
        "price":"sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_purchase_timestamp" : "order_date",
        "order_id" : "order_count",
        "price" : "revenue"
    }, inplace=True)

    return daily_orders_df

def create_sum_order_items_df(df): # Fungsi untuk membuat Jumlah produk terbanyak atau terendah
    sum_order_items_df = df.groupby("product_category_name_english").product_photos_qty_y.sum().sort_values(ascending=False).reset_index()
    sum_order_items_df.rename(columns={
        "product_category_name_english": "product_name",
        "product_photos_qty_y": "quantity",
    }, inplace=True)
    return sum_order_items_df

def create_sum_revenue_items_df(df): # Fungsi untuk membuat pendapatan produk terbanyak atau terendah
    sum_revenue_items_df = df.groupby("product_category_name_english").price.sum().sort_values(ascending=False).reset_index()
    sum_revenue_items_df.rename(columns={
        "product_category_name_english": "product_name",
        "price": "revenue"
    }, inplace=True)
    return sum_revenue_items_df

def create_customer_by_state_df(df): # Fungsi identifikasi demografi customer bedasarkan negara
    customer_by_state_df = df.groupby(by="customer_state").size().sort_values(ascending=False).reset_index(name="customer_count").head(5)
    return customer_by_state_df

def create_customer_by_city_df(df): # Fungsi identifikasi demografi customer berdasarkan kota
    customer_by_city_df = df.groupby(by="customer_city").size().sort_values(ascending=False).reset_index(name="customer_count").head(5)
    return customer_by_city_df

def create_sales_revenue_by_states_df(df): # Fungsi identifikasi jumlah pendapatan berdasrkan negara
    sales_revenue_by_states_df = df.groupby("customer_state").price.sum().sort_values(ascending=False).reset_index()
    sales_revenue_by_states_df.rename(columns={
        "price" : "revenue",
    },inplace=True)
    return sales_revenue_by_states_df

def create_number_of_sales_by_states_df(df): # Fungsi identifikasi jumlah transaksi penjualan berdasarkan negara
    number_of_sales_by_states_df = df.groupby("customer_state").order_id.count().sort_values(ascending=False).reset_index()
    number_of_sales_by_states_df.rename(columns={
        "order_id" : "number_of_sales"
    },inplace=True)
    return number_of_sales_by_states_df

def create_sales_revenue_by_cities_df(df): # Fungsi identifikasi pendapatan penjualan berdasarkan kota
    sales_revenue_by_cities_df = df.groupby("customer_city").price.sum().sort_values(ascending=False).reset_index()
    sales_revenue_by_cities_df.rename(columns={
        "price" : "revenue",
    },inplace=True)
    return sales_revenue_by_cities_df

def create_number_of_sales_by_cities_df(df): # Fungsi identifikasi transaksi penjualan berdasarkan kota
    number_of_sales_by_cities_df = df.groupby("customer_city").order_id.count().sort_values(ascending=False).reset_index()
    number_of_sales_by_cities_df.rename(columns={
        "order_id" : "number_of_sales"
    },inplace=True)
    return number_of_sales_by_cities_df

def create_popular_type_of_payment_df(df): # Identifikasi jenis pembayaran yang paling banyak digunakan
    popular_type_of_payment_df = df.groupby(by = "payment_type")["order_id"].count().sort_values(ascending=False).reset_index()
    popular_type_of_payment_df.rename(columns={
        "order_id" : "payment_count"
    }, inplace = True)
    return popular_type_of_payment_df

def create_value_type_of_payment_df(df): # Identifikasi nilai pembayaran terbesar berdasarkan jenis pembayaran
    value_type_of_payment_df = df.groupby("payment_type")["payment_value"].sum().sort_values(ascending=False).reset_index()
    return value_type_of_payment_df

def create_monthly_reviews_df(df): # Identifikasi nilai rata-rata review skor per beberapa bulan terakhir
    monthly_reviews_df = df.resample(rule='ME', on='review_creation_date').agg({
    "review_score":"mean",
    })
    monthly_reviews_df.index = monthly_reviews_df.index.strftime('%Y-%m')
    monthly_reviews_df= monthly_reviews_df.reset_index()
    monthly_reviews_df.rename(columns={
    "review_creation_date":"review_date",
    }, inplace=True)
    return monthly_reviews_df

def create_review_score_distribution_df(df): # Identifikasi jumlah review score selama 30 hari terakhir
    last_date = df['review_creation_date'].max()
    start_date_last_30_days = last_date - pd.Timedelta(days=29)
    last_30_days_reviews_df = df[
        df['review_creation_date'] >= start_date_last_30_days
    ]

    # Group by review_score and count the number of reviews for each score
    review_score_distribution_df = last_30_days_reviews_df.groupby("review_score").size().reset_index(name="review_count")
    return review_score_distribution_df

def create_delay_percentage_df (df): # Identifikasi distribusi order yang mengalami delay pengiriman
    delay_percentage_df = df.groupby("is_delayed").order_id.count().reset_index()
    delay_percentage_df.rename(columns={
        "order_id":"total"
    }, inplace=True)
    return delay_percentage_df

def create_rfm_df (df):
    rfm_df = df.groupby(by="customer_id", as_index = False).agg({
        "order_purchase_timestamp" : "max",
        "order_id":"nunique",
        "price":"sum"
    })

    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    # Menghitung kapan pelanggan melakukan transaksi (hari)
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = all_df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x : (recent_date - x).days)

    rfm_df.drop("max_order_timestamp", axis = 1, inplace=True)

    rfm_df["dummy_customer_id"] = [f"{i:03}" for i in range(1, len(rfm_df) + 1)]

    return rfm_df

# load berkas yang dibutuhkan
all_df = pd.read_csv("dashboard/all_df.csv")

# Memastikan data dalam bentuk tipe data datetime
datetime_columns = ["order_purchase_timestamp", "review_creation_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace= True)
all_df.reset_index(inplace=True)
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column], format="ISO8601")

# Membuat Komponen Filter
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.markdown("<h1 style='text-align: center; color: White;'>Vinland E-Commerce</h1>", unsafe_allow_html=True)
    st.image("dashboard/Vinland Logo2.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & (all_df["order_purchase_timestamp"] <= str(end_date))]

# Untuk Memanggil Helper Function
daily_orders_df = create_daily_orders_df(main_df)
sum_orders_item_df = create_sum_order_items_df(main_df)
sum_revenue_items_df = create_sum_revenue_items_df(main_df)
customer_by_state_df = create_customer_by_state_df(main_df)
customer_by_city_df = create_customer_by_city_df(main_df)
sales_revenue_by_state_df = create_sales_revenue_by_states_df(main_df)
number_of_sales_by_states_df = create_number_of_sales_by_states_df(main_df)
sales_revenue_by_cities_df =create_sales_revenue_by_cities_df(main_df)
number_of_sales_by_cities_df = create_number_of_sales_by_cities_df(main_df)
popular_type_of_payment_df = create_popular_type_of_payment_df(main_df)
value_type_of_payment_df = create_value_type_of_payment_df(main_df)
monthly_reviews_df = create_monthly_reviews_df(main_df)
review_score_distribution_df = create_review_score_distribution_df(main_df)
delay_percentage_df = create_delay_percentage_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header("Vinland E-Commerce Dashboard :sparkles:")

# Membuat bagian Daily Orders dan Total Revenue
st.subheader('Daily Orders')
col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale ='pt_BR')
    st.metric("Total Revenue", value = total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_date"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Membuat Best & Worst Performing Products
st.subheader("Best & Worst Performing Products")

# By Number of Sales
st.markdown("#### Best & Worst Perfoming Products by Number of Sales")
fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(35, 12)) # Membuat dua kanvas grafik untuk perbandingan

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="quantity", y="product_name", data=sum_orders_item_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Products", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x="quantity", y="product_name", data=sum_orders_item_df.sort_values(by="quantity", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Worst Performing Products", loc="center",fontsize=40)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=20)

plt.subplots_adjust(wspace=0.5,) # Increase the space between subplots

plt.suptitle("Best and Worst Performing Product by number of Sales", fontsize=50) # Judul Main plot
st.pyplot(fig)


# By Revenue
st.markdown("#### Best & Worst Perfoming Products by Revenues")
fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(35, 12)) # Membuat dua kanvas grafik untuk perbandingan

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="revenue", y="product_name", data=sum_revenue_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel("Million BRL", fontsize=30, fontweight="bold")
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Products", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x="revenue", y="product_name", data=sum_revenue_items_df.sort_values(by="revenue", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel("BRL", fontsize=30, fontweight ="bold")
ax[1].set_xlabel(None)
ax[1].set_title("Worst Performing Products", loc="center",fontsize=40)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=20)

plt.subplots_adjust(wspace=0.5,) # Increase the space between subplots
plt.suptitle("Best and Worst Performing Product by Revenue", fontsize=50) # Judul Main plot

st.pyplot(fig)

# Best and Worst Performing Sales By States and Cities

st.subheader("Best and Worst Performing Sales Revenue By States and Cities")
# By States
st.markdown("#### Best & Worst Perfoming Sales Revenue by State")
fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(25, 8))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="revenue", y="customer_state", data=sales_revenue_by_state_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Million Brazil Real")
ax[0].set_title("Best Performing Sales Revenue by States", loc="center", fontsize=20)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="revenue", y="customer_state", data=sales_revenue_by_state_df.sort_values(by="revenue", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Brazil Real")
ax[1].set_title("Worst Performing Sales Revenue by States", loc="center",fontsize=20)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle("Best and Worst Performing Sales Revenue by State", fontsize=25) # Judul Main plot
st.pyplot(fig)

# By City
st.markdown("#### Best & Worst Perfoming Sales Revenue by City")
fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(25, 8)) # Membuat dua kanvas grafik untuk perbandingan

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="revenue", y="customer_city", data=sales_revenue_by_cities_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Million Brazil Real")
ax[0].set_title("Best Performing Sales by City", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="revenue", y="customer_city", data=sales_revenue_by_cities_df.sort_values(by="revenue", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Brazil Real")
ax[1].set_title("Worst Performing Sales by City", loc="center",fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle("Best and Worst Performing Sales Revenue by City", fontsize=25) # Judul Main plot
st.pyplot(fig)

# Membuat Demografi Pelanggan
st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20,10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x= "customer_count",
        y= "customer_state",
        data= customer_by_state_df.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax = ax
    )
    ax.set_title("Number of Customer by States", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20,10))

    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]    
    sns.barplot(
        x= "customer_count",
        y= "customer_city",
        data= customer_by_city_df.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax = ax
    )
    ax.set_title("Number of Customer by Cities", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)
    st.pyplot(fig)

# The Most Popular and Revenue by Payment Types
st.subheader("The Most Popular and Greatest Revenue by Payment Types")

st.markdown("#### The Most Popular Payment Types")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    y='payment_count',
    x= 'payment_type',
    data=popular_type_of_payment_df.sort_values(by="payment_count", ascending=False),
    palette=colors,
)
ax.set_title("The Most Popular Payment Types")
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

st.markdown("#### The Greatest Revenue by Payment Types")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    y='payment_value',
    x= 'payment_type',
    data=value_type_of_payment_df.sort_values(by="payment_value", ascending=False),
    palette=colors,
)
ax.set_title(" The Greatest Revenue by Payment Types")
ax.set_ylabel("Million BRL", fontsize=15, fontweight="bold")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)


# Customer Satisfaction
st.subheader("Customer Satisfaction")

# Displays Customers Reviews and Customer Delays
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20,10))

    plt.pie(
        review_score_distribution_df['review_count'],
        labels = review_score_distribution_df['review_score'],
        autopct='%1.1f%%',
        startangle=90,
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'],
        textprops={'fontsize': 20, 'fontweight' : "bold"}, # Increase the fontsize of value and make it bold
        explode = (0,0,0,0,0.1),
        
    )
    ax.set_title("Review Score in the Last 30 Days", loc="center", fontsize = 30)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20,10))
    plt.pie(
        delay_percentage_df['total'],
        labels= delay_percentage_df['is_delayed'],
        autopct='%1.1f%%',
        startangle=90,
        colors = ['#ff9999', '#66b3ff'],
        textprops={'fontsize':20, 'fontweight' : 'bold'},
        explode =(0,0.1)
    )
    ax.set_title("Distribution of Delivery Delay", loc="center", fontsize=30)
    plt.tight_layout()
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    monthly_reviews_df["review_date"],
    monthly_reviews_df["review_score"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)

ax.set_title("Montlhy Average of Customers Reviews", loc="center", fontsize=30)
plt.yticks(fontsize=20)
plt.xticks(rotation = 45, fontsize=20)
st.pyplot(fig)



# Membuat RFM

st.subheader("Best Customer Based on RFM Parameters")

col1,col2,col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(),2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale="pt_BR")
    st.metric("Average Monetary", value=avg_monetary)

fig, ax = plt.subplots(nrows = 1, ncols=3, figsize=(35,15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="dummy_customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="frequency", x="dummy_customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="dummy_customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)
 


