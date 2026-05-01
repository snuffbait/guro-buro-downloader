import os, re, time, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0"}

def run():
    seen = set()

    good = {
    "1girl","1_girl","2girls","3girls","multiple_girls","solo","female_focus",
    "breasts","breast","small_breasts","cleavage","thighhighs",
    "bikini","stockings","dress","skirt","camisole","maid",
    "school_uniform","boots","high_heels","pantsu","latex",
    "bodysuit","armor","torn_clothes","bloody_clothes",
    "nude","nudity","shoes","barefoot","off_shoulder","skirt_lift",
    "bandaid","toes","breastless_clothes","crotchless_clothes","cut_off_breasts",
    "ass_up","breast_busting","breastless_clothes","areolae","nipples",
    "black_hair","brown_hair","blonde_hair","blonde",
    "red_hair","purple_hair","blue_hair","green_hair",
    "blue_eyes","green_eyes","brown_eyes","glowing_eyes","missing_eye",
    "long_hair","short_hair","ponytail","twintails","hair_over_one_eye",
    "open_mouth","closed_eyes","rolling_eyes","empty_eyes","eyes_rolled_back",
    "looking_at_viewer","looking_away","looking_away","tongue","teeth","eyebrows",
    "licking_lips","fear_face","scared","wince","name_tag",
    "pussy","vagina","nipples","areolae","shaved_pussy",
    "sex","doggystyle","vaginal","cum","cum_in_pussy",
    "uncensored","censored","lesbian","anus","tentacle_sex","tentacle_rape","rape",
    "triple_penetration","necrophilia","necro","snuff","mind_control",
    "broken_rape_victim","cannibalism",
    "guro","ryona","blood","blood_on_face","corpse",
    "corpse_art","dead","death","dying","gore","rotting",
    "amputee","quadruple_amputee","missing_limbs","handless",
    "dismembered","dismemberment","disembowelment","intestines","guts","open_abdomen",
    "severed_head","severed_arm","headless","decapitation","beheading","slit_throat",
    "cut_throat","throat_cut","stabbed","impaled","knife","weapon","gun","chainsaw","sword",
    "execution","murder","killed","mass_murder","torture","bruise","bruised","bruises","injury",
    "pain","beaten","punch","punching","shooting","arrows","arrow","crushed","skinning",
    "crying","screaming","hanging","hung","asphyxiation","asphyxia","drowning","choaking",
    "choak","ishidaki","bludgeoned","eyeball","head","cut","removal","kunai","breast_busting",
    "symphony_of_destruction","defeated",
    "bondage","tied","blindfold","gag",
    "angel","wings","horns","elf","pointy_ears","cat_ears","animal_ears","samurai",
    "child","age_difference","young_girl","schoolgirl","bride","wedding","tiara",
    "princess_luna","princess_celestia","rarity","jack-o'-lantern","hell_baron",
    "animated","gif","comic","novel","visual","original","tagme","duplicate","text",
    "translation_request","hard_translated","posts","lowres","headphones","speaker",
    "chair","glasses","storage_room","toilet","grinder","waitress","bandage",
    "sparks","glowing","manly","grimdark","hair_over_one_eye","dog_tags","t-shirt",
    "bent_over","cross_stereopair","funnybizness","skyrim","love","live","cake",
    "crotchless_clothes","cut_off_breasts","breastless_clothes","ass_up","breast_busting",
    "in_the_face","off_shoulder","skirt_lift","bandaid","toes","breastless_clothes",
    "crotchless_clothes","cut_off_breasts","ass_up","breast_busting","breastless_clothes",
    "crotchless_clothes","cut_off_breasts","ass_up","breast_busting","breastless_clothes",
    "rapunzel","nepgear","asuka","hatsune","miku","vocaloid","touhou","kaguya_houraisan",
    "yakumo_yukari","samus_aran","zero_suit","metroid","nintendo","doom_(game)",
    "skullgirls","yamato_(kantai_collection)","my_little_pony","aosora_(mizore)",
    "eric806359","bcguro","neon_geniesis_evangelioj","overlord_(maruyama)","tenken_(gotannda)",
    "nameo_(judgemasterkou)","xiaoguimist","sachiko_(artist)","keisuke","keisuke_(togainu_no_chi)",
    "mayonnaise_(ringo_gakuen)","conmanwolf","mugon","kakuriyo",
    "lasers","machine","swimsuit","oil","water","fire","bow","ascot","hat",
    "ss","duplicate","hard_translated","posts","tagme"
}

    bad = {
        "boy","boys","1boy","2boys","3boys",
        "male","man","men","guy","guys","penis"
    }

    page = 0

    while True:
        pid = page * 20
        url = f"https://guro.booru.org/index.php?page=post&s=list&tags=all&pid={pid}"
        print(f"\nPage {page+1} (pid={pid})")

        try:
            soup = BeautifulSoup(
                requests.get(url, headers=HEADERS, timeout=30).text,
                "html.parser"
            )

            posts = soup.select("span.thumb a[id^=p]")

            # if no posts, skip forward instead of resetting
            if not posts:
                page += 1
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
                    requests.get(post, headers=HEADERS, timeout=30).text,
                    "html.parser"
                )

                img = psoup.find("img", id="image")
                if not img or not img.get("src"):
                    continue

                img_url = urljoin(post, img["src"])
                name = re.sub(r'[\\/*?:"<>|]', "_", img_url.split("/")[-1].split("?")[0])

                if os.path.exists(name):
                    continue

                r = requests.get(img_url, headers=HEADERS, timeout=30)

                if r.status_code == 200 and len(r.content) > 1024:
                    open(name, "wb").write(r.content)
                    print("Saved:", name)

                time.sleep(1)

            except:
                pass

        page += 1

run()
