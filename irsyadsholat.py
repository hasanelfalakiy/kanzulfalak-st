"""
 * This file is part of kanzulfalak-st.
 *
 * kanzulfalak-st is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * kanzulfalak-st is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with kanzulfalak-st.  If not, see <https://www.gnu.org/licenses/>.
 *
"""

import math
from operator import mod

class IrsyadSholat:
	
	def __init__(
		self,
		tanggal,
		bulan,
		tahun,
		Lintang,
		Bujur,
		timeZ,
		elev,
		ihthiyat
	):
		self.tanggal = tanggal
		self.bulan = bulan
		self.tahun = tahun
		self.Lintang = Lintang
		self.Bujur = Bujur
		self.timeZ = timeZ
		self.elev = elev
		self.ihthiyat = ihthiyat
		
		iht = (self.ihthiyat/ 60)
		
		if bulan < 3:
			G = bulan + 12
		else:
			G = bulan
		if bulan < 3:
			KT = tahun - 1
		else :
			KT = tahun
		# koreksi gregorius
		krg = 2 - int(tahun / 100) + int(int(tahun / 100) / 4)

		# julian day
		JD = round(int(365.25 * (KT + 4716)) + int(30.6001 * (G + 1)) + tanggal + ((10 + 23 / 60) / 24) + krg - 1524.5,3)
		#JD = int(365.25*(2004+4716))+int(30.6001*(10+1))+14+((10+23/60)/24)+ -13 -1524.5

		# juz asal miladiyah
		JAM = (JD - 2451545) / 36525

		# data matahari wasathus syams
		S = 280.46645 + 36000.76983 * JAM
		FrS = (S / 360 - int(S / 360)) * 360

		# khooshotus syams
		m = 357.52910 + 35999.05030 * JAM
		Frm = (m / 360 - int(m / 360)) * 360

		# 'uqdatus syams
		N = 125.04 - 1934.136 * JAM
		FrN = (N / 360 - int(N / 360)) * 360

		# tahshishul awwal/ koreksi pertama
		K1 = (17.264 / 3600) * math.sin(math.radians(FrN)) + (0.206 / 3600) * math.sin(math.radians(2 * FrN))

		# tahshishus tsani/ koreksi kedua
		K2 = (-1.264 / 3600) * math.sin(math.radians(2 * FrS))

		# tahshishus tsaalist/ koreksi ketiga
		R = (9.23 / 3600) * math.cos(math.radians(FrN)) - (0.090 / 3600) * math.cos(math.radians(2 * FrN))

		# tahshishur roobi'/ koreksi keempat
		R1 = (0.548 / 3600) * math.cos(math.radians(2 * FrS))

		# mail kulli
		Q = 23.43929111 + R + R1 - (46.8150 / 3600) * JAM

		# ta'diilus syams
		E = (6898.06 / 3600) * math.sin(math.radians(Frm)) + (72.095 / 3600) * math.sin(math.radians(2 * Frm)) + (0.966 / 3600) * math.sin(math.radians(3 * Frm))

		# thuulus syams
		S1 = FrS + E + K1 + K2 - (20.47 / 3600)

		# mail syams/ deklinasi matahari
		self.Dek = math.degrees(math.asin(math.sin(math.radians(S1)) * math.sin(math.radians(Q))))

		# ta'diluz zaman/ equation of time
		self.e = (-1.915 * math.sin(math.radians(Frm)) + (-0.02) * math.sin(math.radians(2 * Frm)) + 2.466 * math.sin(math.radians(2 * S1)) + (-0.053) * math.sin(math.radians(4 * S1))) / 15

		# semidiameter
		self.SD = 0.267 / (1 - 0.017 * math.cos(math.radians(Frm)))

		# dzuhur WIS
		self.DZwis = 12 + self.e - ((timeZ * 15) - Bujur) / 15 + iht
		
		# dzuhur WD
		self.DZ = 12 - self.e + ((timeZ * 15) - Bujur) / 15 + iht

		# ashar
		H = math.degrees(math.atan(1 / (math.tan(math.radians(abs(Lintang - self.Dek))) + 1)))
		F = -math.tan(math.radians(Lintang)) * math.tan(math.radians(self.Dek))
		Ge = math.cos(math.radians(Lintang)) * math.cos(math.radians(self.Dek))

		# ashar WIS
		self.AS = 12 + math.degrees(math.acos(F + math.sin(math.radians(H)) / Ge)) / 15 + iht

		# ashar WD
		self.ASW = self.AS - self.e - (Bujur - (timeZ * 15)) / 15

		# maghrib
		Dip = (1.76 / 60) * math.sqrt(elev)
		# ho maghrib
		HM = -(self.SD + (34.5 / 60) + Dip) - 0.0024
		# maghrib WIS
		self.TM = 12 + math.degrees(math.acos(F + math.sin(math.radians(HM)) / Ge)) / 15 + iht
		# maghrib WD
		self.MW = self.TM -self. e - (Bujur - (timeZ * 15)) / 15
		
		# h isya'
		HI = -18
		# isya' WIS
		self.IS = 12 + math.degrees(math.acos(F + math.sin(math.radians(HI)) / Ge)) / 15 + iht
		# isya' WD
		self.IW = self.IS - self.e - (Bujur - (timeZ * 15)) / 15
		
		# h shubuh
		Hs = -20
		# shubuh WIS
		self.SI = 12 - math.degrees(math.acos(F + math.sin(math.radians(Hs)) / Ge)) / 15 + iht
		# shubuh WD
		self.SW = self.SI - self.e - (Bujur - (timeZ * 15)) / 15
		
		# imsak WIS
		self.IMS = self.SI - (10 / 60)
		# imsak WD
		self.IM = self.SW - (10 / 60)
		
		# h thulu'
		hT = -(self.SD + (34.5 / 60) + Dip) - 0.0024
		# thulu' WIS
		self.TI = 12 - math.degrees(math.acos(F + math.sin(math.radians(hT)) / Ge)) / 15 - iht
		# thulu' WD
		self.TW = self.TI - self.e - (Bujur - (timeZ * 15)) / 15
		
		# dluha
		hd = 4.5
		# dluha WIS
		self.dl = 12 - math.degrees(math.acos(F + math.sin(math.radians(hd)) / Ge)) / 15 + iht
		# dluha WD
		self.hW = self.dl - self.e - (Bujur - (timeZ * 15)) / 15
		
		# nishful Lail
		self.Ns = self.MW + ((self.SW + 24 - self.MW) / 2) - iht

		# arah Qiblat
		# lintang dan bujur Ka'bah'
		LK = 21.42191389
		BK = 39.82951944

		# selisih Bujur
		A = 360 - BK + Bujur - 360
		h = math.degrees(math.asin(math.sin(math.radians(Lintang)) * math.sin(math.radians(LK)) + math.cos(math.radians(Lintang)) * math.cos(math.radians(LK)) * math.cos(math.radians(A))))

		# azimuth U-B
		self.AQ = math.degrees(math.acos((math.sin(math.radians(LK)) - math.sin(math.radians(Lintang)) * math.sin(math.radians(h))) / math.cos(math.radians(Lintang)) / math.cos(math.radians(h))))

		# azimuth B-U
		self.BU = 90 - self.AQ

		# azimuth UTSB
		self.P = 360 - self.AQ

		# roshdul Qiblat
		B = 90 - Lintang
		PR = math.degrees(math.atan(1.0 / (math.cos(math.radians(B)) * math.tan(math.radians(self.P)))))
		CA = math.degrees(math.acos(math.tan(math.radians(self.Dek)) * math.tan(math.radians(B)) * math.cos(math.radians(PR))))

		# roshdul Qiblat 1 WIS
		self.Rq1 = mod(-(PR + CA) / 15 + 12, 24.0)

		# roshdul Qiblat 1 WD
		self.Rq = mod(self.Rq1 - self.e - (Bujur - (timeZ * 15)) / 15, 24.0)

		# roshdul Qiblat 2 WIS
		self.RQ = mod(-(PR - CA) / 15 + 12, 24.0)

		# toshdul Qiblat 2 WD
		self.RW = mod(self.RQ - self.e - (Bujur - (timeZ * 15)) / 15, 24.0)

		# mengetahui jarak antara 2 tempat
		selisih = Bujur - BK

		M = math.degrees(math.acos(math.sin(math.radians(Lintang)) * math.sin(math.radians(LK)) + math.cos(math.radians(Lintang)) * math.cos(math.radians(LK)) * math.cos(math.radians(selisih))))
		self.KM = M / 360 * 6.283185307 * 6378.388

		# mengetahui selisih jam Makkah - Markaz
		self.sJ = (Bujur - BK) / 15

		# selisih deklinasi dengan Lintang Ka'bah
		self.SL = self.Dek - LK

		# selisih deklinasi dengan Lintang Tempat
		self.ST = self.Dek - Lintang
	
	# deklinasi
	def deklinasi(self):
		return self.Dek
	
	# equation of time
	def equation(self):
		return self.e
	
	# semidiameter
	def semidiameter(self):
		return self.SD
	
	# dzuhur WIS
	def dzuhurWis(self):
		return self.DZwis
	
	# dzuhur WD
	def dzuhurWd(self):
		return self.DZ
	
	# ashar WIS
	def asharWis(self):
		return self.AS
	
	# ashar WD
	def asharWd(self):
		return self.ASW
	
	# maghrib WIS
	def maghribWis(self):
		return self.TM
		
	# maghrib WD
	def maghribWd(self):
		return self.MW
		
	# isya' WIS
	def isyaWis(self):
		return self.IS
	
	# isya' WD
	def isyaWd(self):
		return self.IW
		
	# shubuh WIS
	def shubuhWis(self):
		return self.SI
		
	# shubuh WD
	def shubuhWd(self):
		return self.SW
		
	# imsak WIS
	def imsakWis(self):
		return self.IMS
		
	# imsak WD
	def imsakWd(self):
		return self.IM
		
	# thulu WIS
	def thuluWis(self):
		return self.TI
		
	# thulu WD
	def thuluWd(self):
		return self.TW
		
	# dluha WIS
	def dluhaWis(self):
		return self.dl
		
	# dluha WD
	def dluhaWd(self):
		return self.hW
		
	# tengah malam
	def nisfulLail(self):
		return self.Ns
		
	# azimuth U-B
	def azUB(self):
		return self.AQ
		
	# azimuth B-U
	def azBU(self):
		return self.BU
		
	# azimuth UTSB
	def azUTSB(self):
		return self.P
		
	# rashdul Qiblat 1 WIS
	def rashdu1Wis(self):
		return self.Rq1
		
	# rashdul Qiblat 1 WD
	def rashdu1Wd(self):
		return self.Rq
		
	# rashdul Qiblat 2 WIS 
	def rashdu2Wis(self):
		return self.RQ
		
	# rashdul Qiblat 2 WD
	def rashdu2Wd(self):
		return self.RW
		
	# selisih markaz - Ka'bah
	def markazKabah(self):
		return self.KM
		
	# selisih waktu/jam
	def selisihWaktu(self):
		return self.sJ
		
	# selisih deklinasi dengan Lintang Ka'bah
	def selisihDekLK(self):
		return self.SL

	# selisih deklinasi dengan Lintang Tempat
	def selisihDekLT(self):
		return self.ST
	