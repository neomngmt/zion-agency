"""URL map and English SEO metadata for every route."""

PATHS = {
    "home": "/",
    "about": "/about/",
    "services": "/services/",
    "marketing": "/services/marketing/",
    "chatting": "/services/chatting/",
    "photoshooting": "/services/photoshooting/",
    "success-stories": "/success-stories/",
    "academy": "/academy/",
    "blog": "/blog/",
    "blog-month-one": "/blog/month-one/",
    "blog-chatting-replies": "/blog/chatting-replies/",
    "blog-platform-mix": "/blog/platform-mix/",
    "blog-pricing": "/blog/pricing-mistake/",
    "blog-leaks": "/blog/content-leaked/",
    "blog-anonymous": "/blog/start-anonymously/",
    "referral": "/referral/",
    "refer-a-creator": "/refer-a-creator/",
    "apply": "/apply/",
    "contact": "/contact/",
    "privacy": "/privacy/",
    "terms": "/terms/",
}

META = {
    "home": {
        "title": "ZION | OnlyFans Management Agency for US & Czech Creators",
        "desc": "ZION is an OnlyFans management agency for creators in the US and Czech Republic. Marketing, chatting and content production, with full discretion and tracked results.",
        "h1": "ZION",
    },
    "about": {
        "title": "About ZION | A Creator-First OnlyFans Agency",
        "desc": "Meet the team behind ZION, a creator-first OnlyFans management agency built to handle the business side so creators can focus on content.",
        "h1": "About",
    },
    "services": {
        "title": "OnlyFans Management Services | ZION",
        "desc": "Marketing, chatting and content production under one roof. See how ZION's OnlyFans management services work and what is included.",
        "h1": "Services",
    },
    "marketing": {
        "title": "OnlyFans Marketing & Promotion for Creators | ZION",
        "desc": "Niche positioning and promotion across 15+ platforms to bring the right audience to your OnlyFans page. See how ZION's marketing service works.",
        "h1": "Marketing",
    },
    "chatting": {
        "title": "OnlyFans Chatting Agency & Chatter Team | ZION",
        "desc": "A dedicated CZ/US chatting team trained on your voice, built to turn subscribers into loyal, spending fans without losing authenticity.",
        "h1": "Chatting",
    },
    "photoshooting": {
        "title": "OnlyFans Content Production & Photoshoots | ZION",
        "desc": "Content planning, filming support and leak protection so creators never have to carry content production alone. Behind the scenes of a ZION shoot.",
        "h1": "Photoshooting",
    },
    "success-stories": {
        "title": "OnlyFans Agency Results & Case Studies | ZION",
        "desc": "Real case studies and creator transformations from the ZION roster: traffic, subscribers and earnings before and after, with screenshots.",
        "h1": "Success Stories",
    },
    "academy": {
        "title": "OnlyFans Creator Academy: Growth & Safety Guides | ZION",
        "desc": "Practical guides on growth, safety and monetization for OnlyFans creators, written by the ZION team.",
        "h1": "Academy",
    },
    "blog": {
        "title": "OnlyFans Growth Blog for Creators | ZION",
        "desc": "Notes on growth, chatting, marketing and safety from the ZION team. Short, practical reads for OnlyFans creators.",
        "h1": "Blog",
    },
    "blog-month-one": {
        "title": "What Actually Moves the Needle in Month One | ZION Blog",
        "desc": "The handful of decisions that shape how fast a new OnlyFans page finds its footing in its first month.",
        "h1": "What actually moves the needle in month one",
    },
    "blog-chatting-replies": {
        "title": "Why Generic Replies Cost You Renewals | ZION Blog",
        "desc": "The difference between a chatter who replies and one who builds a relationship that keeps paying off on OnlyFans.",
        "h1": "Why generic replies cost you renewals",
    },
    "blog-platform-mix": {
        "title": "Picking the Right Platform Mix for Your Niche | ZION Blog",
        "desc": "How to decide where an OnlyFans creator's marketing effort actually pays off, and which platforms to skip.",
        "h1": "Picking the right platform mix for your niche",
    },
    "blog-pricing": {
        "title": "The OnlyFans Pricing Mistake That Caps Your Income | ZION Blog",
        "desc": "How bundling and tiered pricing change the math on OnlyFans, and the pricing mistake that quietly caps income.",
        "h1": "The pricing mistake that quietly caps your income",
    },
    "blog-leaks": {
        "title": "What to Do the Day Your Content Gets Leaked | ZION Blog",
        "desc": "The steps that actually help when your OnlyFans content leaks, in the order that matters most.",
        "h1": "What to do the day your content gets leaked",
    },
    "blog-anonymous": {
        "title": "Starting on OnlyFans Anonymously, Without Losing Momentum | ZION Blog",
        "desc": "How creators build a page and an audience on OnlyFans without ever showing their face.",
        "h1": "Starting anonymously, without losing momentum",
    },
    "referral": {
        "title": "OnlyFans Referral Program: Earn Commission | ZION",
        "desc": "Refer a creator to ZION and earn a recurring commission on their growth, for as long as they stay with us.",
        "h1": "Referral program",
    },
    "refer-a-creator": {
        "title": "Refer a Creator to ZION | Recurring Commission",
        "desc": "Tell us who you have in mind and we will take it from there. Introduce a creator and get paid.",
        "h1": "Refer a creator",
    },
    "apply": {
        "title": "Apply to ZION | Join an OnlyFans Management Agency",
        "desc": "Become a ZION creator. No upfront fees and a free first consultation. Tell us a bit about yourself, no pressure and no obligation. We reply within 2 hours.",
        "h1": "Apply",
    },
    "contact": {
        "title": "Contact ZION | OnlyFans Management Agency",
        "desc": "Get in touch with ZION. Write to us about management, marketing or chatting. We usually respond within 2 hours.",
        "h1": "Contact",
    },
    "privacy": {
        "title": "Privacy Policy | ZION",
        "desc": "How ZION collects, uses and protects your information.",
        "h1": "Privacy Policy",
    },
    "terms": {
        "title": "Terms & Conditions | ZION",
        "desc": "The rules for using this website and working with ZION.",
        "h1": "Terms & Conditions",
    },
}

CRUMBS = {
    "marketing": [("home", None), ("services", "Services")],
    "chatting": [("home", None), ("services", "Services")],
    "photoshooting": [("home", None), ("services", "Services")],
    "blog-month-one": [("home", None), ("blog", "Blog")],
    "blog-chatting-replies": [("home", None), ("blog", "Blog")],
    "blog-platform-mix": [("home", None), ("blog", "Blog")],
    "blog-pricing": [("home", None), ("blog", "Blog")],
    "blog-leaks": [("home", None), ("blog", "Blog")],
    "blog-anonymous": [("home", None), ("blog", "Blog")],
    "refer-a-creator": [("home", None), ("referral", "Referral")],
}

SERVICE_SCHEMA = {
    "marketing": "OnlyFans marketing and promotion",
    "chatting": "OnlyFans chatting management",
    "photoshooting": "Content production and photoshoots for creators",
}
