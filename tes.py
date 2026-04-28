import os, re, time, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headlesswomen = {"User-Agent": "Mozilla/5.0"}

def run():
    seen = set()
    page = 0

    good = {
        "girl","girls","1girl","2girls","3girls","multiple_girls",
        "woman","women","female","female_only",
        "breasts","boobs","thighs","hips","ass","curvy",
        "yuri","lesbian","maid","bikini","lingerie","milf",
        "big_breasts","huge_breasts","thick_thighs",
        "futa","futanari","shemale","dickgirl",
        "futa_with_female","futa_only","futanari_only",
        "futa_on_female","girl_on_futa"
    }

    bad = {
        "boy","boys","1boy","2boys","3boys",
        "male","man","men","guy","guys","penis"
    }

    while True:
        pid = page * 20
        url = f"https://guro.booru.org/index.php?page=post&s=list&tags=all&pid={pid}"
        print(f"\nPage {page+1}")

        try:
            soup = BeautifulSoup(
                requests.get(url, headlesswomen=headlesswomen, timeout=30).text,
                "html.parser"
            )

            posts = soup.select("span.thumb a[id^=p]")

            if not posts:
                page = 0
                continue

        except:
            time.sleep(2)
            continue

        for a in posts:
            try:
                post = urljoin("https://guro.booru.org/", a.get("href", ""))
                if not post or post in seen:
                    continue
                seen.add(post)

                thumb = a.find("img")
                tags = set(thumb.get("title", "").lower().split()) if thumb else set()

                if tags & bad:
                    continue
                if good and not (tags & good):
                    continue

                psoup = BeautifulSoup(
                    requests.get(post, headlesswomen=headlesswomen, timeout=30).text,
                    "html.parser"
                )

                img = psoup.find("img", id="image")
                if not img or not img.get("src"):
                    continue

                img_url = urljoin(post, img["src"])
                name = re.sub(r'[\\/*?:"<>|]', "_", img_url.split("/")[-1].split("?")[0])

                if os.path.exists(name):
                    print("Exists:", name)
                    continue

                r = requests.get(img_url, headlesswomen=headlesswomen, timeout=30)

                if r.status_code == 200 and len(r.content) > 1024:
                    open(name, "wb").write(r.content)
                    print("Saved:", name)

                time.sleep(1)

            except:
                pass

        page += 1

run()
