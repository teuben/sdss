

P = ./plotsp1.py

ALL = m31 n628 n1530 n3976 n4565
ARCH = m31a1 m31a2

help:
	@echo ALL=$(ALL)

all: $(ALL)

m31:
	$(P) group2/Skynet_59471_M31_group2_62068_10914.A.onoff.cal.txt 0 4 -770 -600 50 2200

n628:
	$(P) group2/Skynet_59472_ngc628_group2_62098_10938.A.onoff.cal.txt 0  8 1600 3000  100 500 800 1500

n1530:
	$(P) group2/Skynet_59472_ngc1530_group2_62102_10937.A.onoff.cal.txt 0 8 2000 2250 2650 3400 3600 5000

n3976:
	$(P) group2/Skynet_59472_ngc3976_group2_62119_10949.A.onoff.cal.txt 0 8

n4565:
	$(P) group2/Skynet_59472_ngc4565_group2_62118_10948.A.onoff.cal.txt 0 8

m31a1:
	$(P) archive/Skynet_58945_M31_10kpc_radius_44912_54515.A.onoff.cal.txt 0 8 -2100 -800 100 1000

m31a2:
	$(P) archive/Skynet_58945_M31_center_44909_54513.A.onoff.cal.txt       0 8 -2100 -600 100 1000
