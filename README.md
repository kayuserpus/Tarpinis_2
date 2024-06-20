# Tarpinis_2
Antrasis tarpinis atsiskaitymas (grupinis) - internetinės parduotuvės apsipirkimo sistema

Sukurkite internetinės parduotuvės apsipirkimo sistemą, su flask  ir sqlAlchemy kuroje būtų:
1. Prisijungimas
2. Registracija (neteisingai mėginant prisijungti 3 ar daugiau kartų turėtų būti užblokuotas prisijungimas
3. Galimybę peržiūrėti savo turimą balansą
4. Galimybę papildyti savo balansą
5. Peržiūrėti sistemoje esančias prekes
6. Įsidėti sistemoje esančias prekes į krepšelį ir jį išsaugoti
7. Nusipirkti krepšelyje esančias prekes
8. Atsijungti

Administratoriaus galimybės:
1. Pridėti naują prekę 
2. Papildyti esamų prekių kiekį
3. Išimti prekę iš prekybos 
4. Peržiūrėti sistemos naudotojų sąrašą.
5. Ištrinti sistemos naudotojus
6. Sugalvokite patys for bonus points (būkite išradingi)

Papildomi reikalavimai:
1. Visur naudokite Try, except (visos klaidos turi būti pagautos ir išvesti logiški klaidos pranešimai).
2. Duomenys turi išlikti tarp programos paleidimų, tam naudokite duomenų bazę.
3. Sistema privalo turėti aiškią ir tvarkingą struktūra (static, templates, crud operations (atskiriems modeliams atskiri crud failai). Nepamirškite šių failų sudėti į aplankus.
4. Visur turi būti patikrinimai (pvz naudotojas negalėtų nusipirkti prekės kurios nėra), arba negali nusipirkti jeigu neturi tam lėšų.
5. Privalote naudoti Github bent su tokiomis šakomis (Master, Development ir task šakos (pvz AddingLoginFunctionality šaka). Turės būti, bent 10 commitų, per komandą. Negali būti tiesioginių commitų į Master šaką (apsauga yra mokama, dėl to apsimeskite, kad ji yra). Sukurkite, bent kelis pull requestus
6. Privalote panaudoti migracijas

Bonus points:
1. Padarykite prisijungimo blokavimą ant laikmačio. T.Y neteisingai įvedus 3 kartus neleidžiama mėginti 5 minutes, neteisingai įvedus 4 kartą, 1 valandą ir t.t.
2. Nuolaidos lojaliems klientams (lojalus, pirkęs daugiau, nei 3 kartus, arba išleidęs daugiau nei 500€)
3. Administratoriams galimybę nustatyti ir keisti nuolaidas.
4. Slaptažodis turi turėti reikalavimus (panaudokite Regex) (import re).
5. Slaptažodis turėtų būti šifruotas (naudokite google)