Da poženete skripti, treba je vnesti svoje podatke v .env.example fajla in nato jih shraniti kot .env fajla v obeh api datotekah. Podatke lahko dobite iz accounta https://developer.deyecloud.com/api , za Bluetti pa imamo že svoje podatke. Podatki nas zgledajo sledece:

APP_SECRET = tertheqADSDNZpyAq+Rc4P8UPYdtvuWVZIehTz __
TEST_DEVICE_SN = DAOo123012-3 __

Potem pa se poženeta skripti: python bluetti_commission.py         za bluetti in       python commission.py  za Deye
TO DO:
1) Spremeniti Ukaze za Deye Cloud
2) Izboljsati kodo