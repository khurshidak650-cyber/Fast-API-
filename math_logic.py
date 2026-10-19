# math_logic.py
# SkAi Advanced Math Engine: Covers basic arithmetic, algebra, geometry formulas, 
# rational numbers, and step-by-step problem-solving solvers.

import math
import re

def solve_math_problem(query: str):
    q_lower = query.lower()
    
    # 1. Rational Numbers / Parimey Sankhya (fractions, addition, subtraction, multiplication)
    if "parimey" in q_lower or "rational" in q_lower or "fraction" in q_lower or "bhinn" in q_lower:
        return {
            "topic": "Rational Numbers (परिमेय संख्याएँ)",
            "definition": "A rational number is a number that can be expressed in the form p/q where p and q are integers and q != 0.",
            "rules_hindi": [
                "1. दो परिमेय संख्याओं को जोड़ने या घटाने के लिए हर (Denominator) समान होना चाहिए। यदि समान नहीं है, तो L.C.M. (लघुत्तम समापवर्त्य) लें।",
                "2. गुणा करते समय अंश (Numerator) का अंश से और हर का हर से गुणा किया जाता है (a/b * c/d = ac / bd)।",
                "3. भाग करते समय दूसरी संख्या का व्युत्क्रम (Reciprocal) करके गुणा करते हैं।"
            ],
            "example": "जैसे: 2/3 और 7/8 का अंतर (Subtraction): (16 - 21) / 24 = -5 / 24."
        }

    # 2. Area & Volume Formulas (Geometry / Mensuration)
    elif "area" in q_lower or "volume" in q_lower or "kshetrafal" in q_lower or "ayatan" in q_lower:
        return {
            "topic": "Geometry & Mensuration Formulas (क्षेत्रफल और आयतन)",
            "formulas": {
                "ayat (Rectangle)": "Area = length * breadth, Perimeter = 2 * (length + breadth)",
                "varg (Square)": "Area = side * side, Perimeter = 4 * side",
                "vrit (Circle)": "Area = pi * r^2, Circumference = 2 * pi * r",
                "belan (Cylinder)": "Volume = pi * r^2 * h, Curved Surface Area = 2 * pi * r * h",
                "shanku (Cone)": "Volume = (1/3) * pi * r^2 * h",
                "gola (Sphere)": "Volume = (4/3) * pi * r^3, Surface Area = 4 * pi * r^2"
            },
            "tip_hindi": "सवालों को हल करते समय हमेशा यूनिट (Unit) जैसे सेमी या मीटर का ध्यान रखें और क्षेत्रफल में वर्ग (Square) तथा आयतन में घन (Cube) लगाएं।"
        }

    # 3. Basic Algebra & Equations
    elif "algebra" in q_lower or "equation" in q_lower or "समीकरण" in q_lower or "bijganit" in q_lower:
        return {
            "topic": "Algebra & Identities (बीजगणित सर्वसमिकाएँ)",
            "identities": [
                "(a + b)^2 = a^2 + 2ab + b^2",
                "(a - b)^2 = a^2 - 2ab + b^2",
                "a^2 - b^2 = (a - b)(a + b)",
                "(x + a)(x + b) = x^2 + (a + b)x + ab"
            ],
            "step_by_step_solver": "रैखिक समीकरण (Linear Equations) को हल करने के लिए चर (Variables) को एक तरफ और अचर (Constants) को दूसरी तरफ पक्षांतर (Transpose) करें।"
        }

    # 4. General Math Help & Basic Arithmetic Rules
    else:
        return {
            "topic": "General Mathematics Guide (गणित सामान्य ज्ञान)",
            "basic_rules": [
                "BODMAS Rule: Brackets -> Orders (Powers/Roots) -> Division -> Multiplication -> Addition -> Subtraction.",
                "Integers Rule: (+) * (+) = +, (-) * (-) = +, (+) * (-) = -.",
                "LCM & HCF: L.C.M. smallest common multiple hota hai aur H.C.F. highest common factor."
            ],
            "instructions": "Aap koi specific formula, jaise fraction (परिमेय संख्या), area (क्षेत्रफल), volume (आयतन), ya equation pooch sakte hain!"
        }
