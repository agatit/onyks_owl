# Onyks OWL
System optycznej lokalizacji wagonów

## Wymagania
Do działania programu wymagane jest zainstalowanie:
- Redis (działajacy na domyślnym porcie)
- TurboJPEG (w domyślnej siceżce poszukiwań)

pakiety python:
- opencv
- redis-python
- pillow-simd
- blosc
- numpy
- scipy

## Porównanie kodeków
					kod.	zapis	dekod.	wynik (kod+2*zapis+dekod)
pillow-simd BMP:	0.009	0.005	0.0009	0.020
pillow-simd TIF:	0.01	0.005	0.008
pillow-simd PNG:	0.2 	0.002	0.025
pillow-simd JPG:	0.009	0.001	0.01	0.021
pillow-simd 100:	0.02	0.002	0.02	0.044
opencv		BMP:	0.004	0.005	0.002	0.016 !
opencv		TIF:	0.06	0.003	0.04
opencv		PNG:	0.07	0.003	0.03
opencv		JPG:	0.03	0.002	0.02
TurboJPEG	def:	0.008	0.001	0.009	0.019 !
TurboJPEG	100:	0.017	0.002	0.02	0.023
blosc   BloscLZ:	0.007	0.005	0.003	0.020
blosc		LZ4:	0.008	0.004	0.002	0.018 !
blosc	   ZSTD:	0.5		0.003	0.02
numpy/pickle   :	0.004	0.005	0.003	0.017