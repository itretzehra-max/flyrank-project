def classify_risk_tier(answers):
    """
    Classifies an AI system into an EU AI Act risk tier based on structured
    yes/no answers about how the system is used.

    answers: dict with keys:
      - prohibited_use: e.g. social scoring, manipulation, real-time biometric
        surveillance in public spaces
      - high_risk_domain: used in employment, credit, education, law enforcement,
        critical infrastructure, migration, or essential public/private services
      - limited_risk_use: system interacts directly with people (chatbot, emotion
        recognition, deepfake generation) and could deceive users about being AI
    """
    flags = []
    mitigations = []

    if answers.get("prohibited_use"):
        tier = "Unacceptable Risk (Prohibited)"
        flags.append("System falls under a banned use case (e.g. social scoring, "
                      "subliminal manipulation, real-time biometric surveillance).")
        mitigations.append("This use case cannot legally be deployed in the EU. "
                            "Redesign the system to remove the prohibited function.")

    elif answers.get("high_risk_domain"):
        tier = "High Risk"
        flags.append("System is used in a high-risk domain (employment, credit, "
                      "education, law enforcement, critical infrastructure, etc.).")
        mitigations += [
            "Conduct a conformity assessment before deployment.",
            "Maintain technical documentation and a risk management system.",
            "Ensure human oversight and the ability to override outputs.",
            "Log system activity for auditability.",
        ]

    elif answers.get("limited_risk_use"):
        tier = "Limited Risk"
        flags.append("System interacts directly with users (e.g. chatbot, deepfake, "
                      "emotion recognition) and could be mistaken for a human or "
                      "real content.")
        mitigations.append("Disclose to users that they are interacting with an AI "
                            "system, or that content is AI-generated (transparency obligation).")

    else:
        tier = "Minimal Risk"
        flags.append("No high-risk or transparency-triggering characteristics identified.")
        mitigations.append("No mandatory obligations under the Act, though voluntary "
                            "codes of conduct are encouraged.")

    return {
        "tier": tier,
        "flags": flags,
        "mitigations": mitigations,
    }


# --- Worked example: an AI hiring/resume-screening tool ---
example_system = {
    "prohibited_use": False,
    "high_risk_domain": True,   # used to screen job applicants (employment domain)
    "limited_risk_use": False,
}

result = classify_risk_tier(example_system)

print("=" * 55)
print("AI RISK REGISTER — CLASSIFICATION RESULT")
print("=" * 55)
print(f"\nSystem: AI-powered resume screening tool")
print(f"Risk Tier: {result['tier']}\n")
print("Flags:")
for f in result["flags"]:
    print(f"  - {f}")
print("\nRequired mitigations:")
for m in result["mitigations"]:
    print(f"  - {m}")
