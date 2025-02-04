# Dashboard Dasturi

Ushbu dastur Streamlit asosida IMDb Top 250 TV seriallari reytinglarini tahlil qilish uchun mo'ljallangan. Dastur berilgan ma'lumotlarni tozalash va tahlil qilish bilan shug'ullanadi hamda natijalarni turli grafikalar yordamida vizuallashtiradi.

## Kirish

Bu dastur IMDb Top 250 TV seriallari reytinglarini tahlil qilish uchun ishlab chiqilgan. Dastur ma'lumotlarni tozalash, tahlil qilish va vizualizatsiya qilish imkoniyatlarini taqdim etadi.

## Xususiyatlari

- Ma'lumotlarni Tozalash: Keraksiz ustunlarni olib tashlash va ma'lumotlarni tozalash.
- Ma'lumotlarni Tahlil qilish: Tozalangan ma'lumotlarni tahlil qilish va natijalarni scatterplot, issiqlik xaritasi va pairplot kabi grafikalar yordamida ko'rsatish.

## Talablar

- Python 3.7 yoki undan yuqori versiyasi
- Pandas
- Matplotlib
- Seaborn
- Streamlit

## O'rnatish

1. Repozitoriyani klonlash yoki skriptni yuklab olish.
2. Zarur ma'lumotlar to'plamlarini (`data.csv`, `view.csv`, `imdb_top_250_series_episode_ratings.csv`, `imdb_top_250_series_global_ratings.csv`) skript bilan bir xil papkada joylashganligini tekshiring.
3. Kerakli Python kutubxonalarini o'rnating:

```sh
pip install pandas matplotlib seaborn streamlit
