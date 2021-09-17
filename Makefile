

P = ./plotsp1.py

ALL = m31 n628 n1530 n3976 n4565 n4559
ARCH = m31a1 m31a2

help:
	@echo ALL=$(ALL)

all: $(ALL)

m31:
	$(P) group2/Skynet_59471_M31_group2_62068_10914.A.onoff.cal.txt        3 0 4 -770 -600 50 2200

m31_2:
	$(P) group2/Skynet_59472_messier_31_62130_10961.A.onoff.cal.txt        3 0 8 -3000 -700 100 800

n628:
	$(P) group2/Skynet_59472_ngc628_group2_62098_10938.A.onoff.cal.txt     3 0 8 1600 3000  100 500 800 1500

n1530:
	$(P) group2/Skynet_59472_ngc1530_group2_62102_10937.A.onoff.cal.txt    3 0 8 2000 2250 2650 3400 3600 5000

n1530_2:
	$(P) group2/Skynet_59473_ngc_1530_62134_10963.A.onoff.cal.txt          3 0 8

n3976:
	$(P) group2/Skynet_59472_ngc3976_group2_62119_10949.A.onoff.cal.txt    3 0 8

n4565:
	$(P) group2/Skynet_59472_ngc4565_group2_62118_10948.A.onoff.cal.txt    3 0 8

n4559:
	$(P) group2/Skynet_59473_ngc4559_group2_62147_10970.A.onoff.cal.txt    3 0 8 -1000 -100 100 650 950 2500

# some archive examples.  Note m31a1 is on the center, the rest is.
m31a1:
	$(P) archive/Skynet_58945_M31_10kpc_radius_44912_54515.A.onoff.cal.txt 3 0 8 -2100 -800 100 1000

m31a2:
	$(P) archive/Skynet_58945_M31_center_44909_54513.A.onoff.cal.txt       3 0 8 -2100 -600 100 1000

m31a3:
	$(P) archive/Skynet_59340_ASTR344_M31_SashaLevina_59749_8627.A.onoff.cal.txt 1 0 4 -2000 -650 100 1500

m31a4:
	$(P) archive/Skynet_59202_M31_51605_573.A.onoff.cal.txt                      1 0 4 -2000 -650 100 1500




