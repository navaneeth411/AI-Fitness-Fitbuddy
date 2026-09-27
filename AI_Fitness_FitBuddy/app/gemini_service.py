
import os

try:
    import google.generativeai as genai
except ImportError:
    genai = None

def _model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or genai is None:
        return None
    genai.configure(api_key=api_key)
    # The project brief specifies Gemini models. This model name can be changed
    # in one place if the available Gemini model in the account changes.
    return genai.GenerativeModel("gemini-1.5-flash")

def generate_workout(name, age, weight, goal, intensity):
    model = _model()
    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.
Create a safe, practical 7-day beginner-friendly workout plan.

User:
Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Workout intensity: {intensity}

For each day provide:
1. Focus
2. Warm-up (5-10 minutes)
3. Main workout with exercises, sets/reps or duration
4. Rest guidance
5. Cool-down/recovery

Keep the answer structured and easy to read. Do not diagnose medical conditions.
If the user has a medical condition or pain, advise consulting a qualified professional.
"""
    if model is None:
        return demo_plan(name, goal, intensity)
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return demo_plan(name, goal, intensity) + f"\n\n[AI connection note: {str(e)[:160]}]"

def generate_nutrition_tip(goal):
    model = _model()
    prompt = f"""
Give one concise, practical nutrition/recovery tip for a person whose fitness goal is "{goal}".
Mention hydration and balanced meals where appropriate. Avoid medical claims.
"""
    if model is None:
        return f"Nutrition tip for {goal}: Stay hydrated and choose balanced meals with adequate protein, vegetables/fruits and whole-food carbohydrates."
    try:
        return model.generate_content(prompt).text
    except Exception:
        return f"Nutrition tip for {goal}: Stay hydrated and choose balanced, nutrient-rich meals."

def update_plan(original_plan, feedback, goal, intensity):
    model = _model()
    prompt = f"""
You are FitBuddy. Update the existing 7-day fitness plan using the user's feedback.

Goal: {goal}
Intensity: {intensity}

Existing plan:
{original_plan}

User feedback:
{feedback}

Return a revised 7-day plan. Keep it practical and structured. Clearly reflect the requested changes.
Do not provide diagnosis or unsafe medical advice.
"""
    if model is None:
        return original_plan + f"\n\nUPDATED BASED ON FEEDBACK:\n{feedback}\n\nPlease adjust exercises gradually and prioritize safe form and recovery."
    try:
        return model.generate_content(prompt).text
    except Exception:
        return original_plan + f"\n\nUPDATED BASED ON FEEDBACK:\n{feedback}"

def demo_plan(name, goal, intensity):
    return f"""FitBuddy 7-Day Plan for {name}

Goal: {goal}
Intensity: {intensity}

Day 1 – Full Body
Warm-up: 5-10 min walking and mobility
Main: Squats 3x10, wall/incline push-ups 3x8, glute bridges 3x12
Cool-down: 5 min gentle stretching

Day 2 – Cardio
Warm-up: 5 min easy walking
Main: 20-30 min brisk walking or easy cycling
Cool-down: 5 min stretching

Day 3 – Lower Body
Warm-up: 5-10 min mobility
Main: Squats 3x10, lunges 2x8 each side, calf raises 3x12
Cool-down: 5 min stretching

Day 4 – Recovery
Easy walk 15-20 min and gentle stretching.

Day 5 – Upper Body + Core
Warm-up: 5-10 min
Main: Incline push-ups 3x8, rows with safe resistance 3x10, plank 3x20 sec
Cool-down: 5 min stretching

Day 6 – Cardio + Mobility
20-30 min moderate cardio followed by 10 min mobility.

Day 7 – Rest / Active Recovery
Easy movement, hydration and adequate sleep.

Progress gradually. Stop if you experience pain or feel unwell and consult a qualified professional when needed.
"""
