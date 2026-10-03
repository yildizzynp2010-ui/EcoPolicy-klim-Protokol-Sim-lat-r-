import cv2
import mediapipe as mp
import random

# =======================================================
# ECOPOLICY: CLIMATE PROTOCOL SIMULATOR
# =======================================================

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Global Climate Simulation Metrics
global_warming_rate = 1.8   
industrial_budget = 1000     
eco_compliance_score = 45   
cooldown = 0

# Climate Policy Scenarios (Left/Right Interaction)
policy_scenarios = [
    {"text": "Implement Carbon Tax on Industries?", "yes": (-0.2, -150, 15), "no": (0.3, 200, -10)},
    {"text": "Ban Single-Use Industrial Plastics?", "yes": (-0.1, -50, 10), "no": (0.1, 100, -5)},
    {"text": "Subsidize Electric Vehicle Factories?", "yes": (-0.3, -250, 20), "no": (0.2, 150, -12)},
    {"text": "Shut Down Coal-Fired Power Plants?", "yes": (-0.4, -400, 25), "no": (0.4, 300, -20)}
]

current_scenario = random.choice(policy_scenarios)
last_decision = "Awaiting Diplomatic Decision..."

print("=====================================================")
print("  ECOPOLICY SIMULATOR STARTED                        ")
print("  Swipe RIGHT for YES / Swipe LEFT for NO            ")
print("=====================================================")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    h, w, c = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # --- SIMULATION CONTROL INTERFACE (UI) ---
    cv2.rectangle(image, (15, 15), (380, 115), (40, 40, 40), cv2.FILLED)
    cv2.putText(image, f"Global Warming Est: +{global_warming_rate:.2f} C", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    cv2.putText(image, f"Industrial Budget:  ${industrial_budget}B", (25, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 165, 255), 2)
    cv2.putText(image, f"Eco Compliance:    {eco_compliance_score}%", (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    cv2.rectangle(image, (w - 220, 15), (w - 15), (60, 60, 60), cv2.FILLED)
    cv2.putText(image, "<- LEFT: NO", (w - 200, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
    cv2.putText(image, "   RIGHT: YES ->", (w - 200, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    cv2.rectangle(image, (15, h - 70), (w - 15), (h - 15), (20, 20, 20), cv2.FILLED)
    cv2.putText(image, f"POLICY: {current_scenario['text']}", (25, h - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    cv2.putText(image, f"STATUS: {last_decision}", (25, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

    # --- REAL-TIME GESTURE PROCESSING ---
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist_x = hand_landmarks.landmark.x

            if cooldown == 0:
                if wrist_x > 0.7:  # SWIPE RIGHT
                    effects = current_scenario["yes"]
                    global_warming_rate += effects
                    industrial_budget += effects
                    eco_compliance_score += effects
                    
                    last_decision = "APPROVED! Temperature dropping, budget restricted."
                    current_scenario = random.choice(policy_scenarios)
                    cooldown = 30 
                
                elif wrist_x < 0.3:  # SWIPE LEFT
                    effects = current_scenario["no"]
                    global_warming_rate += effects
                    industrial_budget += effects
                    eco_compliance_score += effects
                    
                    last_decision = "REJECTED! Budget saved, warming rate accelerating."
                    current_scenario = random.choice(policy_scenarios)
                    cooldown = 30

            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    global_warming_rate = max(1.0, min(4.5, global_warming_rate))
    eco_compliance_score = max(0, min(100, eco_compliance_score))

    if cooldown > 0:
        cooldown -= 1

    cv2.imshow('EcoPolicy Simulator', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
