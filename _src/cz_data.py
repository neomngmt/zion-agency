"""Czech translation layer. translate() swaps exact English text nodes for Czech ones."""
import json, re
from pathlib import Path

CZ_PAGES = ["home", "services", "marketing", "chatting", "photoshooting", "about", "contact"]

CZ_META = {
    "home": {"title": "ZION | Agentura pro správu OnlyFans (Česko a USA)",
             "desc": "ZION je agentura pro správu OnlyFans profilů pro tvůrkyně z Česka a USA. Marketing, chatting a tvorba obsahu s plnou diskrétností a měřitelnými výsledky.",
             "h1": "ZION"},
    "services": {"title": "Služby OnlyFans agentury | ZION",
                 "desc": "Marketing, chatting a tvorba obsahu pod jednou střechou. Podívejte se, jak fungují služby agentury ZION pro správu OnlyFans a co je v nich zahrnuto.",
                 "h1": "Služby"},
    "marketing": {"title": "Marketing a propagace OnlyFans | ZION",
                  "desc": "Hledání niky a propagace na více než 15 platformách, které přivedou na váš OnlyFans správné publikum. Podívejte se, jak funguje marketing agentury ZION.",
                  "h1": "Marketing"},
    "chatting": {"title": "Chatting pro OnlyFans: tým chatterů | ZION",
                 "desc": "Tým chatterů z Česka a USA vyškolený na váš styl komunikace, který mění odběratele v loajální a platící fanoušky, a to autenticky.",
                 "h1": "Chatting"},
    "photoshooting": {"title": "Tvorba obsahu a focení pro OnlyFans | ZION",
                      "desc": "Plánování obsahu, podpora při focení a ochrana proti únikům, aby tvůrkyně nemusely tvorbu obsahu zvládat samy. Podívejte se, jak vypadá natáčení se ZION.",
                      "h1": "Focení a obsah"},
    "about": {"title": "O agentuře ZION | OnlyFans agentura pro tvůrkyně",
              "desc": "Poznejte tým za agenturou ZION. Agentura postavená pro tvůrkyně, která zvládne byznysovou stránku OnlyFans, abyste se mohly soustředit na obsah.",
              "h1": "O nás"},
    "contact": {"title": "Kontakt | ZION, agentura pro OnlyFans",
                "desc": "Napište nám ohledně správy profilu, marketingu nebo chattingu. Obvykle odpovídáme do 2 hodin.",
                "h1": "Kontakt"},
}

CZ_ATTRS = {
    "Menu": "Menu",
    "Let's talk": "Pojďme si promluvit",
    "Behind the scenes clip 1": "Záběry z natáčení 1",
    "Behind the scenes clip 3": "Záběry z natáčení 2",
    "Behind the scenes clip 4": "Záběry z natáčení 3",
    "Behind the scenes clip 5": "Záběry z natáčení 4",
    "Behind the scenes clip 6": "Záběry z natáčení 5",
    "Zion-managed creator enjoying free time": "Tvůrkyně spravovaná agenturou ZION si užívá volný čas",
    "Infloww earnings dashboard showing $1,602,343.50 tracked over the past 12 months, up 166.10%": "Přehled výdělků v Infloww: 1 602 343,50 USD za posledních 12 měsíců, meziroční nárůst 166,10 %",
    "Infloww leaderboard: ranked #1 in Czech Republic, February": "Žebříček Infloww: 1. místo v Česku, únor",
    "Infloww leaderboard: ranked #1 in Czech Republic, March": "Žebříček Infloww: 1. místo v Česku, březen",
    "Infloww leaderboard: ranked #1 in Czech Republic, April": "Žebříček Infloww: 1. místo v Česku, duben",
    "Infloww leaderboard: ranked #1 in Czech Republic, May": "Žebříček Infloww: 1. místo v Česku, květen",
    "Infloww leaderboard: ranked #1 in Czech Republic, June": "Žebříček Infloww: 1. místo v Česku, červen",
    "Infloww leaderboard: ranked #1 in Czech Republic, July": "Žebříček Infloww: 1. místo v Česku, červenec",
    "Partner brand logo 1": "Logo partnera 1",
    "Partner brand logo 2": "Logo partnera 2",
    "Partner brand logo 3": "Logo partnera 3",
    "Partner brand logo 4": "Logo partnera 4",
    "Zion chat team messaging with fans": "Chatterský tým ZION komunikuje s fanoušky",
    "Content planning and photoshoot session": "Plánování obsahu a focení",
    "DMCA content protection illustration": "Ilustrace ochrany obsahu pomocí DMCA",
}

_EN = json.loads((Path(__file__).parent / "cz_strings_en.json").read_text())
_CZ = json.loads((Path(__file__).parent / "cz_strings_cs.json").read_text())
assert len(_EN) == len(_CZ), (len(_EN), len(_CZ))
CZ_STRINGS = dict(zip(_EN, _CZ))
CZ_SHELL = {}


def translate(h):
    def node(m):
        raw = m.group(1)
        key = " ".join(raw.split())
        if key in CZ_STRINGS and CZ_STRINGS[key]:
            lead = raw[:len(raw) - len(raw.lstrip())]
            trail = raw[len(raw.rstrip()):]
            return ">" + lead + CZ_STRINGS[key] + trail + "<"
        return m.group(0)
    # keep scripts and styles untouched
    parts = re.split(r"(<script.*?</script>|<style.*?</style>)", h, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r">([^<>]+)<", node, parts[i])
        parts[i] = re.sub(r'\s(aria-label|alt)="([^"]+)"',
                          lambda m: f' {m.group(1)}="{CZ_ATTRS.get(m.group(2), m.group(2))}"', parts[i])
    return "".join(parts)
