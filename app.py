import streamlit as st
from irsyadsholat import IrsyadSholat
from function import *

st.title("Kanzul Falak")
st.write("versi : 0.1")
st.write(" ")

st.write("#### Hisab Waktu Sholat Irsyadul Murid")

time = st.date_input("Tanggal : ", "today", format = "DD/MM/YYYY")

st.write("Lintang : ")

col1, col2, col3 = st.columns(3)

with col1:
    lt_dr = st.number_input("derajat", 7)

with col2:
    lt_mnt = st.number_input("menit", 26)

with col3:
    lt_dtk = st.number_input("detik", 0.0)

rd_lt = st.radio("Selatan/Utara", ["Selatan", "Utara"], index = 0, horizontal = True)

st.write("Bujur : ")

col4, col5, col6 = st.columns(3)
with col4:
    long_dr = st.number_input("drj", 111)

with col5:
    long_mnt = st.number_input("mnt", 26)

with col6:
    long_dtk = st.number_input("dtk", 0.0)

rd_long = st.radio("Timur/Barat", ["Timur", "Barat"], index = 0, horizontal = True)

st.write(" ")
col7, col8, col9 = st.columns(3)
with col7:
    elev = st.number_input("Tinggi Tempat", 150)

with col8:
    timeZ = st.number_input("Zona Waktu", 7)

with col9:
    ihti = st.number_input("Ihthiyat (menit)", 2)


st.write(" ")
btn = st.button("Proses")

rd_latitude = False
rd_longitude = False

if btn == True:

    if rd_lt == "Selatan":
        rd_latitude = False
    else:
        rd_latitude = True
    
    if rd_long == "Timur":
        rd_longitude = True
    else:
        rd_longitude = False

    lat = toDecimal(lt_dr, lt_mnt, lt_dtk, rd_latitude)
    long = toDecimal(long_dr, long_mnt, long_dtk, rd_longitude)

    st.empty()

    ir = IrsyadSholat(
        time.day,
        time.month,
        time.year,
        lat,
        long,
        timeZ,
        elev,
        ihti
    )
    with st.container():
        st.write(" ")
        st.write(f"""###### Waktu Sholat Irsyadul Murid\n
        Tanggal         : {time.day} {time.month} {time.year}
    Lintang         : {toDegree2(lat)}
    Bujur           : {toDegree2(long)}
    Ketinggian      : {elev}
    Zona Waktu      : {timeZ}
    Ihthiyat        : {ihti} menit
    \n
    Deklinasi       : {toDegree2(ir.Dek)}
    Eq of time      : {toTime2(ir.equation())}
    Semidiameter    : {toDegree2(ir.semidiameter())}
    \n
    Imsak           : {toTime2(ir.imsakWd())} UTC {timeZ}
    Shubuh          : {toTime2(ir.shubuhWd())} UTC {timeZ}
    Terbit          : {toTime2(ir.thuluWd())} UTC {timeZ}
    Dluha           : {toTime2(ir.dluhaWd())} UTC {timeZ}
    Dzuhur          : {toTime2(ir.dzuhurWd())} UTC {timeZ}
    Ashar           : {toTime2(ir.asharWd())} UTC {timeZ}
    Maghrib         : {toTime2(ir.maghribWd())} UTC {timeZ}
    Isya'           : {toTime2(ir.isyaWd())} UTC {timeZ}
    T. malam        : {toTime2(ir.nisfulLail())} UTC {timeZ}
    \n
    Rashdu Q. 1     : {toTime2(ir.rashdu1Wd())} UTC {timeZ}
    Rashdu Q. 2     : {toTime2(ir.rashdu2Wd())} UTC {timeZ}
    Arah Qiblat     : {toDegree2(ir.azUTSB())} UTSB
    Markaz - Ka'bah : {ir.markazKabah()} Km
    Selisih jam     : {toCounter2(ir.selisihWaktu())}
    """)
        st.write(" ")
        st.empty()
        st.write(f"""
                 \tOleh :\n
                 Andi Hasan A\n
                 *LF PCNU Ngawi*\n
                 \n
                 Kode sumber : 
""")
        st.link_button("Github : kanzulfalak-st", "https://github.com/hasanelfalakiy/kanzulfalak-st")