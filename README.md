Da poženeta skripti, treba je kreirat .env fajla v obeh api datotekah, in v njih vpisat svoje podatke, ki jih dobite iz API accounta na https://developer.deyecloud.com/api , za Bluetti pa imamo že svoje podatke, lahko vam pošljem po pošti. Podatki naj zgledajo na sledeči način

APP_SECRET = tertheqADSDNZpyAq+Rc4P8UPYdtvuWVZIehTz __
TEST_DEVICE_SN = DAOo123012-3 __

Potem pa se poženeta skripti: python bluetti_commission.py         za bluetti in       python commission.py  za Deye
TO DO:
1) Kontaktirati Bluetti dokumentacijo, če so spremenili svoj API
2) Spremeniti strukturo za inverter API
3) Napisati MODBUS rešitev za Deye inverter
