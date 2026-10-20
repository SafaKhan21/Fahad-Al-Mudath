# فهد المدعث للكهرباء · Fahad Al Medath Electrical — Store demo

Interactive demo of an online store for electrical supplies in Saudi Arabia, plus its admin panel.
It is a design and requirements prototype for the real build in Oracle APEX. No real payments are made and nothing is sent anywhere.

- Arabic (RTL) and English, light and dark mode
- Storefront: categories, search, filters, product pages, wishlist, compare, cart, contractor quote form
- Checkout with simulated mada, Visa/Mastercard, Apple Pay, stc pay, Tabby, Tamara, cash on delivery, bank transfer and SADAD
- ZATCA simplified tax invoice with a Phase 2 TLV QR code
- Admin panel: orders, products, customers, coupons, payment gateways and keys, shipping, VAT/ZATCA, notifications, store settings, users, integrations, API and webhooks, security, compliance checklist, backup

Admin settings are saved in the visitor's browser (localStorage) only.

## Files

| File | Purpose |
|---|---|
| `src.html` | The page source. Edit this. |
| `photos.js` | Product photos as embedded images, plus their credits. Generated. |
| `build.py` | Combines `src.html` and `photos.js` into the deployable pages. |
| `site/index.html` | The finished standalone site. Deploy this folder. |
| `index.html` | Same page in the format used by the Claude artifact. |
| `build_photos.py` | Rebuilds `photos.js` from the images in `photos/`. |
| `fetch_openverse.py` | Downloads Creative Commons product photos from Openverse into `photos/`. |
| `serve.py` | Serves `site/` on the company network with UTF-8 headers. |

## Build

```
python build.py
```

## Run on the company network

```
python serve.py 192.168.15.185 8085
```

The PC runs this automatically at startup through the Windows scheduled task `FahadAlMedathDemoWeb`.

## Deploy to Vercel

Import the repository in Vercel and set the output directory to `site`, with no build command.

## Photo credits

The product photos are Creative Commons licensed (CC BY, CC BY-SA, CC0). The licences require attribution,
which the site shows on its "Photo credits" page in the footer. Keep that page when the site is public, and
replace the photos with the store's own images before launch.
