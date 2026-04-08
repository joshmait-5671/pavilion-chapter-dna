#!/usr/bin/env python3
"""
Lloyd Weather Corpus Engine — CLI entry point.
Usage:
    python run.py                    # Run full pipeline
    python run.py ingest             # Run ingest stage only
    python run.py ingest gmail       # Run Gmail ingest only
    python run.py normalize          # Run normalize stage only
    python run.py analyze            # Run analyze stage only
    python run.py synthesize         # Run synthesize stage only
    python run.py validate           # Run validate stage only
"""
import sys
from config import RAW_DIR, CORPUS_DIR, ANALYSIS_DIR, OUTPUT_DIR


def run_ingest(source=None):
    """Stage 1: Extract raw data from sources."""
    if source is None or source == "gmail":
        from ingest.gmail import ingest_gmail
        print("📧 Ingesting Gmail...")
        count = ingest_gmail()
        print(f"   ✅ {count} emails ingested")

    if source is None or source == "whatsapp":
        from ingest.whatsapp import ingest_whatsapp
        print("💬 Ingesting WhatsApp...")
        count = ingest_whatsapp()
        print(f"   ✅ {count} messages ingested")

    if source is None or source == "twitter":
        from ingest.twitter import ingest_twitter
        print("🐦 Ingesting Twitter...")
        count = ingest_twitter()
        print(f"   ✅ {count} tweets ingested")


def run_normalize():
    """Stage 2: Normalize into unified corpus."""
    from normalize.normalizer import normalize_corpus
    print("🔄 Normalizing corpus...")
    stats = normalize_corpus()
    print(f"   ✅ {stats['total']} records in corpus")
    print(f"   📊 Sources: {stats['by_source']}")


def run_analyze():
    """Stage 3: Extract voice features and forecasting patterns."""
    from analyze.voice_extractor import extract_voice_features
    from analyze.forecast_extractor import extract_forecast_dimensions
    print("🧠 Extracting voice features...")
    extract_voice_features()
    print("   ✅ Voice features saved")
    print("📐 Extracting forecast dimensions...")
    extract_forecast_dimensions()
    print("   ✅ Forecast dimensions saved")


def run_synthesize():
    """Stage 4: Build voice profile and forecast profile."""
    from synthesize.voice_profile import build_voice_profile
    from synthesize.forecast_profile import build_forecast_profile
    print("✍️  Building voice profile...")
    build_voice_profile()
    print("   ✅ Voice profile saved to output/voice_profile.md")
    print("   ✅ Example bank saved to output/example_bank.jsonl")
    print("📊 Building forecast profile...")
    build_forecast_profile()
    print("   ✅ Forecast profile saved to output/")


def run_validate():
    """Stage 5: Test the voice profile."""
    from validate.voice_test import run_validation
    print("🧪 Running voice validation...")
    run_validation()
    print("   ✅ Validation report saved to output/validation_report.md")


STAGES = {
    "ingest": run_ingest,
    "normalize": run_normalize,
    "analyze": run_analyze,
    "synthesize": run_synthesize,
    "validate": run_validate,
}

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        for name, fn in STAGES.items():
            fn()
        print("\n🎉 Pipeline complete!")
    elif args[0] in STAGES:
        if args[0] == "ingest" and len(args) > 1:
            run_ingest(source=args[1])
        else:
            STAGES[args[0]]()
    else:
        print(f"Unknown stage: {args[0]}")
        print(f"Available: {', '.join(STAGES.keys())}")
        sys.exit(1)
