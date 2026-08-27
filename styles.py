"""
styles.py
Elite Luxury Dark Mode Styling for Smart Recipe Assistant.
"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');

    /* Global Theme & Background */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d0f12 !important;
        color: #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Elite Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.08) 0%, rgba(18, 22, 28, 0.8) 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        backdrop-filter: blur(12px);
        padding: 2.5rem 2.2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFF 30%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.05rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Section Headers - High Contrast Fix */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 1.45rem;
        color: #f8fafc !important; /* Pure crisp white for high contrast */
        margin: 1.8rem 0 1rem 0;
        border-left: 3px solid #D4AF37;
        padding-left: 0.8rem;
        letter-spacing: 0.01em;
    }

    /* Recipe & Feature Cards */
    .recipe-card {
        background: rgba(22, 27, 34, 0.7);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .recipe-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 0 12px 32px rgba(212, 175, 55, 0.1);
    }
    .recipe-title {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 1.35rem;
        color: #ffffff;
        margin-bottom: 0.4rem;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .badge-time { background: rgba(212, 175, 55, 0.12); color: #f3d368; border: 1px solid rgba(212, 175, 55, 0.3); }
    .badge-diff-easy { background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-diff-medium { background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-diff-hard { background: rgba(239, 68, 68, 0.12); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-match { background: rgba(59, 130, 246, 0.12); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-cuisine { background: rgba(168, 85, 247, 0.12); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }

    /* Progress Match Bar */
    .match-bar-bg {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        height: 6px;
        width: 100%;
        margin-top: 0.6rem;
        overflow: hidden;
    }
    .match-bar-fill {
        background: linear-gradient(90deg, #D4AF37, #f3d368);
        height: 100%;
        border-radius: 999px;
    }

    /* Nutrition Tiles */
    .nutrition-tile {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .nutrition-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #f3d368;
    }
    .nutrition-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
    }

    /* Shopping List & Tips */
    .shop-item {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        padding: 0.8rem 1.1rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #D4AF37;
        color: #e2e8f0;
    }
    .healthy-tip {
        background: rgba(16, 185, 129, 0.05);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        border-left: 4px solid #10b981;
        color: #e2e8f0;
    }
    .ingredient-chip {
        display: inline-block;
        background: rgba(212, 175, 55, 0.1);
        color: #f3d368;
        border: 1px solid rgba(212, 175, 55, 0.25);
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        margin: 0.25rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Streamlit UI Button Overrides */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid rgba(212, 175, 55, 0.4);
        background: linear-gradient(135deg, #1e232a 0%, #121519 100%);
        color: #f3d368 !important;
        padding: 0.55rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%);
        color: #0d0f12 !important;
        border-color: #D4AF37;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.3);
    }
</style>
"""